import uuid

from pydantic import BaseModel

from app.schemas import user_schemas


class AdminOut(BaseModel):
    user: user_schemas.UserAdmin

    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    user_id: uuid.UUID
