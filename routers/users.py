import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
import utils
from database import get_db
from oauth2 import is_current_user_admin, get_current_user
from schemas import user_schemas

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/me', response_model=user_schemas.UserOut)
async def get_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uuid == current_user.uuid).first()
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserOut)
async def create_user(new_data: user_schemas.UserCreate, current_user_admin=Depends(is_current_user_admin),
                      db: Session = Depends(get_db)):
    new_user = models.User(**new_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.patch('/{uuid}', response_model=user_schemas.UserOut)
async def update_user(uuid: uuid.UUID, updated_data: user_schemas.UserUpdate,
                      current_user_admin=Depends(is_current_user_admin), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.uuid == uuid)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с UUID {uuid} не найден.")
    if updated_data['password']:
        updated_data.password = utils.hash(updated_data.password)

    update_data = updated_data.dict(exclude_unset=True)

    # Обновить пользователя только с этими полями
    if update_data:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)

    return user


@router.delete('/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uuid: uuid.UUID, current_user_admin=Depends(is_current_user_admin),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uuid == uuid).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с UUID {uuid} не найден.")
    db.delete(user)
    db.commit()
    return {'message': 'Пользователь успешно удален.'}