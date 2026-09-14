from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import User



class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.db.get(User, user_id)

    async def delete(self, user: User) -> None:
        await self.db.delete(user)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


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
        self.db.add(reg_user)
        return reg_user


