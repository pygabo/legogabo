from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase


class User(BaseModel):
    id: int
    name: str
    email: str


class UserRepository:
    def get_user(self, user_id: int) -> User:
        pass

    def create_user(self, user: User) -> User:
        pass


class Neo4jUserRepository(UserRepository):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_user(self, user_id: int) -> User:
        with self._driver.session() as session:
            result = session.run("MATCH (u:User {id: $user_id}) RETURN u.name as name, u.email as email",
                                 user_id=user_id)
            record = result.single()
            if record:
                return User(id=user_id, name=record["name"], email=record["email"])
            else:
                raise HTTPException(status_code=404, detail="User not found")

    def create_user(self, user: User) -> User:
        with self._driver.session() as session:
            session.run("CREATE (u:User {id: $id, name: $name, email: $email})", id=user.id, name=user.name,
                        email=user.email)
        return user


app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user_repo = Neo4jUserRepository(uri="bolt://neo4j:7687", user="neo4j", password="neo4j")
    user = user_repo.get_user(user_id=user_id)
    return user


@app.post("/users")
async def create_user(user: User):
    user_repo = Neo4jUserRepository(uri="bolt://neo4j:7687", user="neo4j", password="neo4j")
    created_user = user_repo.create_user(user=user)
    return created_user
