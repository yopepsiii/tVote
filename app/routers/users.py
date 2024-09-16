import uuid
from copy import deepcopy
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from app import utils, models
from config import settings
from app.database import get_db
from app.oauth2 import is_current_user_admin, get_current_user
from app.schemas import user_schemas
from app.utils import validate, validate_list

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=user_schemas.UserOut)
@cache(namespace="users/me")
async def get_user(
        current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    return await validate(value=user, class_type=user_schemas.UserOut)


@router.get('/', response_model=List[user_schemas.UserOut])
@cache(namespace='users')
async def get_users(current_user_admin=Depends(is_current_user_admin), db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return await validate_list(values=users, class_type=user_schemas.UserOut)


@router.get("/search", response_model=List[user_schemas.UserAdminSearch])
async def search_users(
        query: Optional[str],
        current_user_admin=Depends(is_current_user_admin),
        db: Session = Depends(get_db),
):
    users = (
        db.query(models.User)
        .filter(
            func.lower(
                models.User.firstname + models.User.surname + models.User.email
            ).contains(query.lower())
        )
        .limit(5)
        .all()
    )
    return users


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(new_data: user_schemas.UserCreate,
                      db: Session = Depends(get_db), current_user_admin=Depends(is_current_user_admin)):
    new_data.password = utils.hash(new_data.password)
    new_user = models.User(**new_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await FastAPICache.clear(namespace="users")

    return new_user


@router.patch('/{id}')
async def update_user(id: uuid.UUID, updated_data: user_schemas.UserUpdate,
                      current_user_admin=Depends(is_current_user_admin), db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.user_id == id).first()

    if admin and admin.user_id != current_user_admin.id and current_user_admin.email != settings.owner_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не можете изменять данные других '
                                                                          'администраторов.')

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    unhashed_new_password = deepcopy(updated_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {id} не найден.",
        )
    if (
            user.email == settings.owner_email
            and current_user_admin.email != settings.owner_email
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Че брат, думал все так просто?",
        )
    if updated_data.password is not None:
        updated_data.password = utils.hash(updated_data.password)

    update_data = updated_data.dict(exclude_unset=True)

    # Обновить пользователя только с этими полями
    if update_data:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)

        if unhashed_new_password is not None:
            user.password = unhashed_new_password

        await FastAPICache.clear(namespace='users')
        await FastAPICache.clear(namespace='users/me')

    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: uuid.UUID, current_user_admin=Depends(is_current_user_admin),
                      db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.user_id == id).first()

    if admin and current_user_admin.email != settings.owner_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не можете удалять других '
                                                                          'администраторов.')
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {id} не найден.",
        )
    if (
            user.email == settings.owner_email
            and current_user_admin.email != settings.owner_email
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Че брат, думал все так просто?",
        )
    db.delete(user)
    db.commit()

    await FastAPICache.clear()

    return {"message": "Пользователь успешно удален."}
