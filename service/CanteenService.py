from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import httpx
import os
from dotenv import load_dotenv
from schemas.CanteenSchema import GetReceipt, CreateMenu
from schemas.BaseSchema import RessponseMessage
from datetime import datetime
from typing import List
from models import Food, Menu, FoodCategory


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

    async def create_menu(self, foods: List[CreateMenu]):
        try:
            for food in foods:
                db_food = self.db.query(Food).filter(Food.code == food.code).first()
                
                if db_food:
                    db_food.cost = food.cost

                    food_day = Menu(food_id=db_food.id)
                    self.db.add(food_day)
                else:
                    category = self.db.query(FoodCategory).filter(FoodCategory.name == food.category).first()
                    
                    if not category:
                        raise HTTPException(status_code=404, detail=f'Категория блюда "{food.name}" не найдена')

                    food_new = Food(name=food.name, code=food.code, weight=food.weight, cost=food.cost ,category_id=category.id)
                    self.db.add(food_new)

                    self.db.flush()

                    food_day = Menu(food_id=food_new.id)
                    self.db.add(food_day)

            self.db.commit()

            return RessponseMessage(message='Меню успешно загруженно')
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail=str(e))