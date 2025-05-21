from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.ContactSchema import Contacts as ContactsSchema, ContactsListResponse, UpdateContacts, CreateContacts
from database import get_db
from typing import Dict, Any
from services.ContactService import get_all_contacts, get_contact_by_id, update_contact, delete_contact, create_contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/", 
    response_model=ContactsListResponse,
    summary="Получение списка контактов",
    description="Возвращает список всех контактов с возможностью пагинации"
)
async def get_contacts(
    skip: int = Query(0, description="Количество записей, которые нужно пропустить"), 
    limit: int = Query(default=1000, gt=0, le=10000, description="Максимальное количество записей для возврата"), 
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
):
    cache_key = f"contacts:all:{skip}:{limit}"
    
    if cached := await cache.get(cache_key):
        return ContactsListResponse(**cached)
    
    contacts = await get_all_contacts(db, skip, limit)
    response_data = {
        "items": [contact.model_dump() for contact in contacts],
        "total": len(contacts),
        "page": skip // limit + 1 if limit > 0 else 1,
        "size": limit
    }
    
    await cache.set(cache_key, response_data, ttl=1800) 
    return ContactsListResponse(**response_data)


@router.get(
    "/{contact_id}", 
    response_model=ContactsSchema,
    summary="Получение контакта по ID",
    description="Возвращает детальную информацию о контакте по его ID"
)
async def get_contact(
    contact_id: int = Path(..., title="ID контакта", description="Уникальный идентификатор контакта", ge=1),
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
):
    cache_key = f"contacts:id:{contact_id}"
    
    if cached := await cache.get(cache_key):
        return ContactsSchema(**cached)
    
    contact = await get_contact_by_id(db, contact_id)
    if contact:
        await cache.set(cache_key, contact.model_dump(), ttl=1800)  
    return contact


@router.patch(
    "/{contact_id}", 
    response_model=ContactsSchema,
    summary="Обновление контакта",
    description="Обновляет информацию о контакте по его ID"
)
async def update_contact_endpoint(
    contact_update: UpdateContacts,
    contact_id: int = Path(..., title="ID контакта", description="Уникальный идентификатор контакта для обновления", ge=1),
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
):
    updated_contact = await update_contact(db, contact_id, contact_update)

    await cache.delete(f"contacts:id:{contact_id}")
    await cache.invalidate_pattern("contacts:all:*")
    return updated_contact


@router.delete(
    "/{contact_id}", 
    response_model=Dict[str, Any],
    summary="Удаление контакта",
    description="Удаляет контакт по его ID"
)
async def delete_contact_endpoint(
    contact_id: int = Path(..., title="ID контакта", description="Уникальный идентификатор контакта для удаления", ge=1),
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
):
    result = await delete_contact(db, contact_id)

    await cache.delete(f"contacts:id:{contact_id}")
    await cache.invalidate_pattern("contacts:all:*")
    return result

@router.post(
    "/", 
    response_model=ContactsSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового контакта",
    description="Создает новый контакт в базе данных"
)
async def create_contact_endpoint(
    contact_data: CreateContacts,
    db: AsyncSession = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
):
    new_contact = await create_contact(db, contact_data)
    await cache.invalidate_pattern("contacts:all:*")
    return new_contact