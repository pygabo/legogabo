from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]

    class Config:
        orm_mode = True


class UserInput(BaseModel):
    name: str
    email: str
    age: Optional[int]
