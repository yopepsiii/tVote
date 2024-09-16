import uuid

from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    candidate_id: int
    type: conint(le=2)  # 0 - против, 1 - за, 2 - воздержался

    class Config:
        from_attributes = True


class VoteUserOut(VoteBase):
    pass


class VoteCreate(VoteBase):
    pass
