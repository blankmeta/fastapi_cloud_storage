from datetime import datetime

from pydantic import BaseModel


class FileCreateDTO(BaseModel):
    name: str
    path: str
    user_id: int


class FileDTO(BaseModel):
    id: int
    name: str
    path: str
    user_id: int
    create_date: datetime


class FileDBDTO(BaseModel):
    id: int
    size: int
    name: str
    path: str
    create_date: datetime

    class Config:
        orm_mode = True
