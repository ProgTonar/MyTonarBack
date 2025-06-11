from sqlalchemy.orm import Session
from schemas.AppealSchema import CreateAppeal, AddAnswer, ChangeActive, PutLike
from schemas.BaseSchema import RessponseMessage
from models.Appeal.AppealModel import Appeal
from models.Appeal.StatusAppealModel import StatusAppeal
from models.Appeal.LikeAppealModel import LikeAppeal
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

class AppealService:
    def __init__(self, db: Session):
        self.db = db

    async def create_appeal(self, data: CreateAppeal):
        try:
            appeal = Appeal(
                title = data.title,
                description = data.description,
                status_id = data.status_id,
                user_id = data.user_id,
            )

            self.db.add(appeal)
            self.db.commit()

            return RessponseMessage(message='Обращение успешно создано')
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail='Ошибка базы данных')
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail='Произошла ошибка')
        
    async def get_appeal_detail (self, appeal_id: int):
        try:
            db_appeal = self.db.get(Appeal, appeal_id)

            if not db_appeal or db_appeal.active == False:
                raise HTTPException(status_code=404, detail='Обращение не найдено')
                        
            response = {
                'titile': db_appeal.title,
                'description': db_appeal.description,
                'status': db_appeal.status.name,
                'user_id': db_appeal.user_id,
                'likes': len(db_appeal.likes)
            }

            return response
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_all_appeal (self):
        try:
            db_appeals = self.db.query(Appeal).filter(Appeal.active == True).all()

            if not db_appeals:
                raise HTTPException(status_code=404, detail='Обращений не найдено')

            all_appeals = []
            for appeal in db_appeals:
                all_appeals.append({
                    'titile': appeal.title,
                    'description': appeal.description,
                    'status': appeal.status.name,
                    'user_id': appeal.user_id,
                    'likes': len(appeal.likes)
                })

            return all_appeals
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def add_answer_appeal (self, data: AddAnswer):
        try:
            db_appeal = self.db.get(Appeal, data.id)

            if not db_appeal:
                raise HTTPException(status_code=404, detail='Обращение не найдено')

            db_appeal.answer = data.answer

            self.db.commit()

            return RessponseMessage(message='Ответ успешно записан')
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def delete_appeal (self, appeal_id: int):
        try:
            db_appeal = self.db.get(Appeal, appeal_id)

            if not db_appeal:
                raise HTTPException(status_code=404, detail='Обращение не найдено')

            self.db.delete(db_appeal)

            self.db.commit()

            return RessponseMessage(message='Обращение успешно удалено')
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_statuses_appeal (self):
        try:
            db_status = self.db.query(StatusAppeal).all()

            if not db_status:
                raise HTTPException(status_code=404, detail='Обращение не найдено')
            
            statuses = []
            for item in db_status:
                statuses.append( {
                    'id': item.id,
                    'name': item.name
                })

            return statuses
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def change_active_appeal (self, data: ChangeActive):
        try:
            db_appeal = self.db.get(Appeal, data.id)

            if not db_appeal:
                raise HTTPException(status_code=404, detail='Обращение не найдено')
            
            db_appeal.active = data.active

            self.db.commit()
            
            return RessponseMessage(message='Активность изменена')
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    async def put_like (self, data: PutLike):
        try:
            check_appeal = self.db.get(Appeal, data.appeal_id)

            if not check_appeal:
                raise HTTPException(status_code=404, detail='Обращение не найдено')

            db_like = self.db.query(LikeAppeal).filter(LikeAppeal.user_id == data.user_id).filter(LikeAppeal.appeal_id == data.appeal_id).first()

            if db_like:
                self.db.delete(db_like)
                msg = 'Лайк удален'
            else:
                like = LikeAppeal(
                    user_id = data.user_id,
                    appeal_id = data.appeal_id
                )

                msg = 'Лайк поставлен'

                self.db.add(like)
                
            self.db.commit()
            
            return RessponseMessage(message=msg)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))