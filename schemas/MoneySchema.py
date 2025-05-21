from pydantic import BaseModel, Field
from typing import Optional

class MoneySchema(BaseModel):
    money: str