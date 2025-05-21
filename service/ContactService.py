from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.contacts import Contacts
from schemas.ContactSchema import Contacts as ContactsSchema, UpdateContacts, CreateContacts

class ContactService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_contacts(db: AsyncSession, skip: int = 0, limit: int = 100_000):
        result = await db.execute(select(Contacts).offset(skip).limit(limit))
        contacts_list = result.scalars().all()
        
        validated_contacts = []
        for contact in contacts_list:
            # Преобразование пустых email в None
            contact_dict = {
                "id": contact.id,
                "name": contact.name,
                "job_title": contact.job_title,
                "v_phonenumber": contact.v_phonenumber,
                "short_phonenumber": contact.short_phonenumber,
                "mobile_phone": contact.mobile_phone,
                "email": contact.email if contact.email and contact.email.strip() else None,
                "created_at": contact.created_at,
                "updated_at": contact.updated_at,
            }
            validated_contacts.append(ContactsSchema.model_validate(contact_dict))
        
        return validated_contacts

    async def get_contact_by_id(db: AsyncSession, contact_id: int):
        result = await db.execute(select(Contacts).filter(Contacts.id == contact_id))
        contact = result.scalar_one_or_none()
        
        if not contact:
            raise HTTPException(status_code=404, detail="Контакт не найден")
        
        contact_dict = {
            "id": contact.id,
            "name": contact.name,
            "job_title": contact.job_title,
            "v_phonenumber": contact.v_phonenumber,
            "short_phonenumber": contact.short_phonenumber,
            "mobile_phone": contact.mobile_phone,
            "email": contact.email if contact.email and contact.email.strip() else None,
            "created_at": contact.created_at,
            "updated_at": contact.updated_at,
        }
        
        return ContactsSchema.model_validate(contact_dict)

    async def update_contact(db: AsyncSession, contact_id: int, contact_update: UpdateContacts):
        result = await db.execute(select(Contacts).filter(Contacts.id == contact_id))
        existing_contact = result.scalar_one_or_none()
        
        if not existing_contact:
            raise HTTPException(status_code=404, detail="Контакт не найден")
        
        update_data = contact_update.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            return await get_contact_by_id(db, contact_id)
        
        await db.execute(
            update(Contacts)
            .where(Contacts.id == contact_id)
            .values(**update_data)
        )
        await db.commit()
        
        return await get_contact_by_id(db, contact_id)

    async def delete_contact(db: AsyncSession, contact_id: int):
        result = await db.execute(select(Contacts).filter(Contacts.id == contact_id))
        existing_contact = result.scalar_one_or_none()
        
        if not existing_contact:
            raise HTTPException(status_code=404, detail="Контакт не найден")
        
        await db.execute(delete(Contacts).where(Contacts.id == contact_id))
        await db.commit()
        
        return {"message": f"Контакт с ID {contact_id} успешно удален"}

    async def create_contact(db: AsyncSession, contact_data: CreateContacts):
        db_contact = Contacts(
            name=contact_data.name,
            job_title=contact_data.job_title,
            v_phonenumber=contact_data.v_phonenumber,
            short_phonenumber=contact_data.short_phonenumber,
            mobile_phone=contact_data.mobile_phone,
            email=contact_data.email,
        )
        

        db.add(db_contact)
        
        try:
            await db.commit()
            await db.refresh(db_contact)
            return ContactsSchema.model_validate(db_contact, from_attributes=True)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))