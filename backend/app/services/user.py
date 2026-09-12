from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories import UserRepository
from backend.app.schemas import UserCreate, UserResponse, TokenInfo
from backend.app.auth import hash_password, validate_password, encode_jwt


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repository = UserRepository(db=db)

    async def list_users(self) -> list[UserResponse]:
        users_orm = await self.user_repository.get_all()
        return [UserResponse.model_validate(user) for user in users_orm]

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        user_orm = await self.user_repository.create(name=user_create.name)
        await self.db.commit()
        await self.db.refresh(user_orm)
        return UserResponse.model_validate(user_orm)

    async def register_user(self, user_register: UserCreate) -> UserResponse:
        existing_user = await self.user_repository.get_by_email(user_register.email)
        if existing_user:
            raise HTTPException(status_code=409, detail='Пользователь уже существует')
        hashed_password = hash_password(user_register.password)
        new_user = await self.user_repository.register_user(username=user_register.name,
                                                            password=hashed_password,
                                                            email=user_register.email)
        await self.db.commit()
        return UserResponse.model_validate(new_user)

    async def get_user(self, user_id: str) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return UserResponse.model_validate(user)

    async def get_user_by_email(self,
                                email: str) -> UserResponse | None:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: str) -> None:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await self.user_repository.delete(user)
        await self.db.commit()

    async def authenticate_user(self,
                                email: str,
                                password_from_client: str) -> TokenInfo:
        user_from_db = await self.user_repository.get_by_email(email=email)

        error_message = HTTPException(status_code=401, detail='Неверный email или пароль')

        if not user_from_db:
            raise error_message

        validate_result = validate_password(password=password_from_client,
                                            hashed_password=user_from_db.password)
        if not validate_result:
            raise HTTPException(status_code=401, detail='Несвалидировал')

        jwt_payload = {
            'email': email
        }

        token = encode_jwt(jwt_payload)
        return TokenInfo(
            access_token=token,
            token_type='Bearer'
        )
