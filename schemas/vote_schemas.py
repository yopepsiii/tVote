import uuid

from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    candidate_id: int
    type: conint(le=1)


class VoteUserOut(BaseModel):
    pass


class VoteCreate(VoteBase):
    pass
