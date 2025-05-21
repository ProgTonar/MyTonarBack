import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class MoneyService:
    def __init__(self):                      
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/html',            
            'Authorization': f'Basic {os.getenv('ZUP_TOKEN')}',
        }

    async def get_money(self, login: int):
        payload = {"tableId": login}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(    
                    method = "GET",
                    url = os.getenv('ZUP_1C') + 'GetMoney',
                    headers = self.headers,
                    json = payload,
                )
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            return {"error": "HTTP error", "status_code": e.response.status_code}
        except httpx.RequestError as e:
            return {"error": "Request failed", "message": str(e)}