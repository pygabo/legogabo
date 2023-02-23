import strawberry
from typing import Optional


@strawberry.type
class UserType:
    id: int
    username: str
    email: str


@strawberry.input
class CreateUserInput:
    username: str
    email: str
    password: str


@strawberry.type
class CreateUserResponse:
    user: Optional[UserType]
    error: Optional[str]
