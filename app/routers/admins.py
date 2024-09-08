import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.oauth2 import is_current_user_admin, is_current_user_owner
from app.schemas import admin_schemas

router = APIRouter(prefix="/admins", tags=["Администраторы"])


@router.get('/', response_model=List[admin_schemas.AdminOut])
async def get_admins(db: Session = Depends(get_db), current_user_admin=Depends(is_current_user_admin)):
    admins = db.query(models.Admin).all()
    return admins


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_admin(new_admin_data: admin_schemas.AdminCreate, db: Session = Depends(get_db),
                       current_user_owner=Depends(is_current_user_owner)):
    existing_user = db.query(models.User).filter(models.User.id == new_admin_data.user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пользователь с ID {new_admin_data.user_id} не найден.")
    new_admin = models.Admin(**new_admin_data.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(user_id: uuid.UUID, db: Session = Depends(get_db),
                       current_user_owner=Depends(is_current_user_owner)):
    admin = db.query(models.Admin).filter(models.Admin.user_id == user_id).first()
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Админ с ID {user_id} не найден.")
    db.delete(admin)
    db.commit()
    return
