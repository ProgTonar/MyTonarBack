from fastapi import HTTPException, status
import httpx

class MoneyService:
    def __init__(self):                      
        self.base_url = "http://10.0.1.23/zup/hs/tested/GetMoney"
        token = "0JDQtNC80LjQvdC40YHRgtGA0LDRgtC+0YA6MTk3MTE5Njc="
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "text/html",            
            "Authorization": f"Basic {token}",
        }

    async def get_money(self, login: int):
        payload = {"tableId": login}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(    
                    method="GET",
                    url=self.base_url,
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            return {"error": "HTTP error", "status_code": e.response.status_code}
        except httpx.RequestError as e:
            return {"error": "Request failed", "message": str(e)}