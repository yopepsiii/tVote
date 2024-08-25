from typing import Optional

from pydantic import BaseModel, EmailStr

from schemas import vote_schemas


class UserBase(BaseModel):
    firstname: str
    surname: str


class UserOut(UserBase):
    votes: list[vote_schemas.VoteUserOut]


class UserCreate(UserBase):
    email: EmailStr


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
