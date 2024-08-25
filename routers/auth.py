from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from .. import models, utils, oauth2
from ..database import get_db
from ..schemas import auth_schemas


router = APIRouter(tags=["Аутентификация"])


@router.post("/login", response_model=auth_schemas.Token)
async def login(
        user_credentials: OAuth2PasswordRequestForm,
        db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверные данные для входа."
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверные данные для входа."
        )

    access_token = await oauth2.create_access_token(data={"user_uuid": str(user.uuid), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
