from typing import Optional

from pydantic import BaseModel


class MemberBase(BaseModel):
    firstname: str
    surname: str
    info: Optional[str] = None
    direction: Optional[str] = None
    photo: str


class MemberCreate(MemberBase):
    pass


class MemberOut(MemberBase):
    id: int


class MemberUpdate(BaseModel):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    info: Optional[str] = None
    direction: Optional[str] = None
    photo: Optional[str] = None
