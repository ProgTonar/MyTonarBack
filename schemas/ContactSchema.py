from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Any


# class ContactsBase(BaseModel):
#     name: str = Field(description="ФИО сотрудника")
#     job_title: str = Field(description="Должность")
#     v_phonenumber: str = Field(description="Внутренний телефонный номер")
#     short_phonenumber: str = Field(description="Короткий телефонный номер")
#     mobile_phone: str = Field(description="Мобильный телефон")
#     email: Optional[EmailStr] = Field(None, description="Электронная почта")

#     @field_validator('email', mode='before')
#     @classmethod
#     def empty_str_to_none(cls, v):
#         if v == '' or v is None:
#             return None
#         return v

# class CreateContacts(ContactsBase):
#     pass

# class UpdateContacts(BaseModel):
#     name: Optional[str] = Field(None, description="ФИО сотрудника")
#     job_title: Optional[str] = Field(None, description="Должность")
#     v_phonenumber: Optional[str] = Field(None, description="Внутренний телефонный номер")
#     short_phonenumber: Optional[str] = Field(None, description="Короткий телефонный номер")
#     mobile_phone: Optional[str] = Field(None, description="Мобильный телефон")
#     email: Optional[EmailStr] = Field(None, description="Электронная почта")

#     @field_validator('email', mode='before')
#     @classmethod
#     def empty_str_to_none(cls, v):
#         if v == '' or v is None:
#             return None
#         return v

# class Contacts(ContactsBase):
#     id: int = Field(description="Уникальный идентификатор контакта")
#     created_at: datetime = Field(description="Дата и время создания")
#     updated_at: Optional[datetime] = Field(None, description="Дата и время последнего обновления")

#     class Config:
#         from_attributes = True 
#         arbitrary_types_allowed = True

# class ContactsListResponse(BaseModel):
#     items: List[Contacts] = Field(description="Список контактов")
#     total: int = Field(description="Общее количество контактов")
#     page: int = Field(description="Текущая страница")
#     size: int = Field(description="Размер страницы")