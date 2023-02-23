from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
