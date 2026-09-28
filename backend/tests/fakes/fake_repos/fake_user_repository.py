import uuid

from backend.app.models import User

class FakeUserRepository:
    def __init__(self, initial_users: list[User] | None = None) -> None:
        self._storage: dict[str, User] = {}

        if initial_users:
            for user in initial_users:
                if not user.id:
                    user.id = str(uuid.uuid4())
                self._storage[str(user.id)] = user

    async def get_all(self) -> list[User]:
        return list(self._storage.values())

    async def get_by_id(self, user_id: str) -> User | None:
        return self._storage.get(user_id)

    async def delete(self, user: User) -> None:
        self._storage.pop(user.id)

    async def get_by_email(self, email: str) -> User | None:
        for user in self._storage.values():
            if user.email == email:
                return user
        return None

    async def register_user(self,
                            name: str,
                            surname: str,
                            password: str,
                            email: str,
                            age: int,
                            full_name: str) -> User:
        reg_user = User(name=name,
                        surname=surname,
                        password=password,
                        email=email,
                        age=age,
                        full_name=full_name)
        if getattr(reg_user, "id", None) is None:
            reg_user.id = str(uuid.uuid4())

        self._storage[str(reg_user.id)] = reg_user
        return reg_user