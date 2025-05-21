import httpx
from fastapi import HTTPException, status


class MoneyService:
    def __init__(self):                      
        self.base_url = "http://10.0.1.23/zup/hs/tested/GetMoney"
        token = "0JDQtNC80LjQvdC40YHRgtGA0LDRgtC+0YA6MTk3MTE5Njc="
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "text/html",            
            "Authorization": f"Basic {token}",
        }

    async def get_money(self, table_id: str):
        payload = {"tableId": table_id}

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

        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Внешний сервис вернул ошибку: {exc}",
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Не удалось подключиться к сервису: {exc}",
            )