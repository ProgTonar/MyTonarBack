from sqlalchemy.orm import Session 
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import httpx
import os
from dotenv import load_dotenv
from schemas.CanteenSchema import GetReceipt, CreateMenu, CreateScore
from schemas.BaseSchema import RessponseMessage
from datetime import datetime
from typing import List
from models import Food, Menu, FoodCategory, FoodScore


load_dotenv()

class CanteenService:

    def __init__(self, db: Session):
        self.db = db

    async def get_receipt_date(self, data: GetReceipt):
        try:
            url = f"{os.getenv('CANTEEN_1C')}GetFoodOrders"

            raw_date_begin = datetime.strptime(data.date_begin, '%d.%m.%Y')
            formated_date_begin = raw_date_begin.strftime('%Y%m%d')

            raw_date_end = datetime.strptime(data.date_end, '%d.%m.%Y')
            formated_date_end = raw_date_end.strftime('%Y%m%d')

            payload = {
                "tabel_id": data.login,
                "date_begin": formated_date_begin,
                "date_end": formated_date_end,
            }

            headers = {
                "authorization": f"Basic {os.getenv('CANTEEN_TOKEN')}",
                "content-type": "application/json",
                "accept": "application/json"
            }

            response = httpx.post(url, json=payload, headers=headers)
            
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')
        
    async def get_receipt_now(self, login: int):
        try:
            url = f"{os.getenv('CANTEEN_1C')}GetFoodOrders"

            today = datetime.today()
            formated_date = today.strftime('%Y%m%d')

            payload = {
                "tabel_id": str(login),
                "date_begin": formated_date,
                "date_end": formated_date,
            }

            headers = {
                "authorization": f"Basic {os.getenv('CANTEEN_TOKEN')}",
                "content-type": "application/json",
                "accept": "application/json"
            }

            response = httpx.post(url, json=payload, headers=headers)
            
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

    async def create_menu(self, data: List[CreateMenu]):
        try:
            for food in data:
                db_food = self.db.query(Food).filter(Food.code == food.code).first()
                
                if db_food:
                    db_food.cost = food.cost

                    food_day = Menu(food_id=db_food.id, date=food.date)
                    self.db.add(food_day)
                else:
                    category = self.db.query(FoodCategory).filter(FoodCategory.name == food.category).first()
                    
                    if not category:
                        raise HTTPException(status_code=404, detail=f'Категория блюда "{food.name}" не найдена')

                    food_new = Food(name=food.name, code=food.code, weight=food.weight, cost=food.cost ,category_id=category.id)
                    self.db.add(food_new)

                    self.db.flush()

                    food_day = Menu(food_id=food_new.id, date=food.date)
                    self.db.add(food_day)

            self.db.commit()

            return RessponseMessage(message='Меню успешно загруженно')
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except HTTPException as e:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_menu_today(self):
        try:
            today = datetime.today().date()

            filter_menu = (
                self.db.query(
                    func.max(Menu.id)
                )
                .filter(Menu.date == today)
                .group_by(Menu.food_id)
                .subquery()
            )

            raw_foods = (
                self.db.query(Food)
                .join(Menu, and_(
                    Menu.food_id == Food.id,
                    Menu.id.in_(filter_menu)
                ))
                .all()
            )

            if not raw_foods:
                raise HTTPException(status_code=404, detail='Меню на сегодня не найдено')

            foods_today = []

            for item in raw_foods:
                avg_score = self.db.query(
                    func.avg(FoodScore.score)
                ).filter(FoodScore.food_id == item.id).scalar()

                avg_score = round(avg_score, 2) if avg_score is not None else 0

                foods_today.append({
                    'id': item.id,
                    'name': item.name,
                    'cost': item.cost,
                    'weight': item.weight,
                    'category': item.category.name,
                    'score': avg_score,
                    'feedback': len(item.score)
                })

            return foods_today
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except HTTPException as e:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def create_food_score(self, data: CreateScore):
        try:
            existing_score = self.db.query(FoodScore).filter(
                FoodScore.food_id == data.food_id,
                FoodScore.user_id == data.user_id
            ).first()

            if existing_score:
                raise HTTPException(status_code=409, detail='Вы уже оценивали это блюдо')
            
            food = self.db.query(Food).filter(Food.id == data.food_id).first()
            
            if not food:
                raise HTTPException(status_code=404, detail='Блюдо не найдено')
            
            new_score = FoodScore(
                score=data.score,
                food_id=data.food_id, 
                user_id=data.user_id
            )

            if data.feedback:
                new_score.feedback = data.feedback

            
            self.db.add(new_score)
            self.db.commit()

            return RessponseMessage(message='Оценка успешно поставлена')
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except HTTPException as e:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_detail_food(self, food_id: int):
        try:
            raw_scores = self.db.query(FoodScore).filter(FoodScore.food_id == food_id).all()
            
            scores = []

            total = 0
            count = 0
            
            for item in raw_scores:
                scores.append({
                    "user_id": item.user_id,
                    "score": item.score,
                    "feedback": item.feedback,
                    "date": {
                        "date": item.created_at.strftime("%d.%m.%Y"),
                        "time": item.created_at.strftime("%H:%M"),
                    }
                })

                total+=item.score
                count+=1
            
            avg_score = round(total / count if count > 0 else 0, 2)
            

            food = self.db.query(Food).filter(Food.id == food_id).first()

            if not food:
                raise HTTPException(status_code=404, detail='Такого блюда не найдено')

            response = {
                "name": food.name,
                "weight": food.weight,
                "avg_score": avg_score,
                "count_score": len(raw_scores),
                "feedback": scores,
            }

            return response
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except HTTPException as e:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))