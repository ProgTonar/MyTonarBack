from pydantic import BaseModel, Field
from typing import Any, Dict


class MoneyRequest(BaseModel):
    tableId: str = Field(..., description="ID таблицы для запроса")
