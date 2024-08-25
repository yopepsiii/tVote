import uuid

from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    candidate_id: int
    type: conint(le=1)

    class Config:
        from_attributes = True


class VoteUserOut(VoteBase):
    pass


class VoteCreate(VoteBase):
    pass
