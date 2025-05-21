from fastapi import HTTPException, status
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

class MoneyService:        

    async def get_money(self, login: int):
        try:
            url = f"{os.getenv('ZUP_1C')}GetMoney"
            payload = {"tableId": f"{login}"}
            headers = {
                "authorization": f"Basic {os.getenv('ZUP_TOKEN')}",
                "content-type": "application/json",
                "accept": "application/json"
            }

            with httpx.Client() as client:
                response = client.request("GET", url, content=json.dumps(payload), headers=headers)
            
            return {"money": response.text}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail=str(e))