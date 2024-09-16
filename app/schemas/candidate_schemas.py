from typing import Optional

from pydantic import BaseModel


class CandidateBase(BaseModel):
    firstname: str
    surname: str
    year_of_study: int
    group: str
    study_dirrection: str
    photo: str


class CandidateOut(CandidateBase):
    id: int
    likes_count: int
    dislikes_count: int
    abstaines_count: int

class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    year_of_study: Optional[int] = None
    group: Optional[str] = None
    faculty: Optional[str] = None
    study_dirrection: Optional[str] = None
    photo: Optional[str] = None
