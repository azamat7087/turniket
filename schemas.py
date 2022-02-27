from pydantic import BaseModel, Field, validator, HttpUrl
from models import Parents, ChildActivities
from typing import List, Optional
from datetime import datetime, timedelta
import validators


class ParentsBase(BaseModel):
    telegram_id: str = Field(...)
    username: str = Field(...)
    child_id: int = Field(..., )

    class Config:
        orm_mode = True
        orm_model = Parents


class ParentsDBBase(ParentsBase):
    id: int = Field(None)
    date_of_add: datetime = Field(None)
    date_of_update: datetime = Field(None)

    class Config:
        orm_mode = True
        orm_model = Parents


class ChildActivitiesBase(BaseModel):
    name: str = Field(...)
    db_id: int = Field(..., )
    arrive_time: datetime = Field(..., )
    leaving_time: datetime = Field(..., )
    is_send: bool = Field(..., )

    class Config:
        orm_mode = True
        orm_model = ChildActivities


class ChildActivitiesDBBase(ParentsBase):
    id: int = Field(None)
    date_of_add: datetime = Field(None)
    date_of_update: datetime = Field(None)

    class Config:
        orm_mode = True
        orm_model = ChildActivities
