import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from starlette import status

from app import utils, models, oauth2
from app.database import get_db
from app.oauth2 import is_current_user_admin, get_current_user
from app.schemas import user_schemas
from app.utils import validate

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/me', response_model=user_schemas.UserOut)
@cache(namespace='users/me')
async def get_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    return await validate(value=user, class_type=user_schemas.UserOut)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(new_data: user_schemas.UserCreate,
                      db: Session = Depends(get_db)):
    new_data.password = utils.hash(new_data.password)
    new_user = models.User(**new_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = await oauth2.create_access_token(data={"user_id": str(new_user.id), "email": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch('/{id}', response_model=user_schemas.UserOut)
async def update_user(id: uuid.UUID, updated_data: user_schemas.UserUpdate,
                      current_user_admin=Depends(is_current_user_admin), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с ID {id} не найден.")
    if updated_data['password']:
        updated_data.password = utils.hash(updated_data.password)

    update_data = updated_data.dict(exclude_unset=True)

    # Обновить пользователя только с этими полями
    if update_data:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)

        await FastAPICache.clear(namespace='users/me')

    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: uuid.UUID, current_user_admin=Depends(is_current_user_admin),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с ID {id} не найден.")
    db.delete(user)
    db.commit()

    await FastAPICache.clear()

    return {'message': 'Пользователь успешно удален.'}
