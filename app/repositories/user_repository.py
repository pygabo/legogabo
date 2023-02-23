from typing import List

from neo4j import GraphDatabase

from app.models.user import User, UserInput


class UserRepository:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_user(self, user: UserInput) -> User:
        with self.driver.session() as session:
            query = (
                "CREATE (u:User {name: $name, email: $email, age: $age})"
                "RETURN id(u) AS id, u.name AS name, u.email AS email, u.age AS age"
            )
            result = session.run(query, name=user.name, email=user.email, age=user.age)
            return User(**result.single())

    def get_user_by_id(self, user_id: int) -> User:
        with self.driver.session() as session:
            query = (
                "MATCH (u:User) WHERE id(u) = $user_id "
                "RETURN id(u) AS id, u.name AS name, u.email AS email, u.age AS age"
            )
            result = session.run(query, user_id=user_id)
            return User(**result.single())

    def get_user_by_email(self, email: str) -> User:
        with self.driver.session() as session:
            query = (
                "MATCH (u:User) WHERE u.email = $email "
                "RETURN id(u) AS id, u.name AS name, u.email AS email, u.age AS age"
            )
            result = session.run(query, email=email)
            return User(**result.single()) if result.single() else None

    def get_users(self) -> List[User]:
        with self.driver.session() as session:
            query = (
                "MATCH (u:User) "
                "RETURN id(u) AS id, u.name AS name, u.email AS email, u.age AS age"
            )
            result = session.run(query)
            return [User(**record) for record in result]

    def update_user(self, user: User) -> User:
        with self.driver.session() as session:
            query = (
                "MATCH (u:User) WHERE id(u) = $id "
                "SET u.name = $name, u.email = $email, u.age = $age "
                "RETURN id(u) AS id, u.name AS name, u.email AS email, u.age AS age"
            )
            result = session.run(query, id=user.id, name=user.name, email=user.email, age=user.age)
            return User(**result.single())

    def delete_user(self, user_id: int) -> bool:
        with self.driver.session() as session:
            query = "MATCH (u:User) WHERE id(u) = $user_id DELETE u"
            result = session.run(query, user_id=user_id)
            return bool(result.summary().counters.nodes_deleted)
