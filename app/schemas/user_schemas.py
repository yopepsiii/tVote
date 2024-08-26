import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas import vote_schemas


class UserBase(BaseModel):
    firstname: str
    surname: str


class UserOut(UserBase):
    id: uuid.UUID
    email: EmailStr
    votes: list[vote_schemas.VoteUserOut]

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserAdmin(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class UserAdminSearch(UserBase):
    id: uuid.UUID
    email: EmailStr
