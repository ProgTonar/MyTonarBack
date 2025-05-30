from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import httpx
import os
from dotenv import load_dotenv
from schemas.CanteenSchema import GetReceipt, CreateMenu, CreateScore
from schemas.BaseSchema import RessponseMessage
from datetime import datetime, time
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

    async def create_menu(self, foods: List[CreateMenu]):
        try:
            for food in foods:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')
        
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

            foods_today = []

            for item in raw_foods:
                foods_today.append({
                    'name': item.name,
                    'cost': item.cost,
                    'weight': item.weight,
                    'category': item.category.name,
                    'score': item.weight,
                    'feedback': item.weight
                })

            return foods_today
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except Exception as e:
            raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')
        
    async def create_food_score(self, score: CreateScore):
        try:
            existing_score = self.db.query(FoodScore).filter(
                FoodScore.food_id == score.food_id,
                FoodScore.user_id == score.user_id
            ).first()

            if existing_score:
                raise HTTPException(status_code=409, detail='Вы уже оценивали это блюдо')
            
            food = self.db.query(Food).filter(Food.id == score.food_id).first()
            
            if not food:
                raise HTTPException(status_code=404, detail='Блюдо не найдено')
            
            new_score = FoodScore(
                score=score.score, 
                food_id=score.food_id, 
                user_id=score.user_id
            )
            
            self.db.add(new_score)
            self.db.commit()

            return RessponseMessage(message='Оценка успешно поставлена')
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))