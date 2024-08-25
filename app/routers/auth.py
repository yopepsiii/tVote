from typing import Annotated

from authlib.oauth2 import OAuth2Error
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from app.oauth2 import oauth_client, create_access_token
from .. import models, utils, oauth2
from ..database import get_db
from ..schemas import auth_schemas


router = APIRouter(tags=["Аутентификация"])


@router.post("/login", response_model=auth_schemas.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    print(form_data.password)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверные данные для входа."
        )
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверные данные для входа."
        )

    access_token = await oauth2.create_access_token(data={"user_id": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("login_google_callback")
    return await oauth_client.google.authorize_redirect(request, redirect_uri)


@router.get("/login/google/callback")
async def login_google_callback(request: Request, db: Session = Depends(get_db)):
    userinfo = await get_userinfo(request)

    user = db.query(models.User).filter(models.User.email == userinfo['email']).first()  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = await create_access_token(
        data={"user_id": str(user.id),
              "email": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_userinfo(request: Request):
    try:
        token = await oauth_client.google.authorize_access_token(request)
    except OAuth2Error as e:
        raise e.error

    return token['userinfo']