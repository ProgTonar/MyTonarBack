from pydantic import BaseModel, Field
from typing import Optional

class RessponseMessage(BaseModel):
    message: Optional[str] = Field(..., max_length=100)
