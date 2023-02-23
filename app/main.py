from fastapi import FastAPI
from app.repositories.user_repository import UserRepository
from app.models.user import UserInput
from app.services.user_service import UserService

app = FastAPI()

user_repo = UserRepository(uri="bolt://neo4j:7687", user="neo4j", password="neo4j")
user_service = UserService(user_repository=user_repo)


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id=user_id)
    return user


@app.post("/users")
async def create_user(user: UserInput):
    created_user = user_service.create_user(user=user)
    return created_user
