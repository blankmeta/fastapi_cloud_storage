from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserRequestDTO(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserInDB(UserRequestDTO):
    hashed_password: str
