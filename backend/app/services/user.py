from fastapi import HTTPException
from backend.app.schemas import UserCreate, UserResponse, TokenInfo
from backend.app.auth import hash_password, validate_password, encode_jwt
from backend.app.repositories import UnitOfWork


class UserService:
    async def list_users(self, uow: UnitOfWork) -> list[UserResponse]:
        async with uow:
            users_orm = await uow.users.get_all()
            return [UserResponse.model_validate(user) for user in users_orm]

    async def register_user(self, uow: UnitOfWork, user_register: UserCreate) -> UserResponse:
        async with uow:
            existing_user = await uow.users.get_by_email(user_register.email)
            if existing_user:
                raise HTTPException(status_code=409, detail='Пользователь уже существует')
            hashed_password = hash_password(user_register.password)
            new_user = await uow.users.register_user(username=user_register.name,
                                                     password=hashed_password,
                                                     email=user_register.email)
            return UserResponse.model_validate(new_user)

    async def get_user(self, uow: UnitOfWork, user_id: str) -> UserResponse:
        async with uow:
            user = await uow.users.get_by_id(user_id=user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return UserResponse.model_validate(user)

    async def get_user_by_email(self, uow: UnitOfWork, email: str) -> UserResponse | None:
        async with uow:
            user = await uow.users.get_by_email(email=email)
            if not user:
                raise HTTPException(status_code=404, detail='Пользователь не найден')
            return UserResponse.model_validate(user)

    async def delete_user(self,uow: UnitOfWork, user_id: str) -> None:
        async with uow:
            user = await uow.users.get_by_id(user_id=user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            await uow.users.delete(user)

    async def authenticate_user(self,
                                uow: UnitOfWork,
                                email: str,
                                password_from_client: str) -> TokenInfo:
        async with uow:
            user_from_db = await uow.users.get_by_email(email=email)

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
