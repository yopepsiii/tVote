from pydantic import BaseModel, conint


class ProfburoVoteBase(BaseModel):
    type: conint(le=2)  # 0 - против, 1 - за

    class Config:
        from_attributes = True


class ProfburoVoteUserOut(ProfburoVoteBase):
    pass


class ProfburoVoteCreate(ProfburoVoteBase):
    pass
