from fastapi import APIRouter, Depends
from backend.app.schemas import (UserCreate,
                                 UserResponse,
                                 UserLogin,
                                 TokenInfo)
from backend.app.services import UserService, TelegramService
from backend.app.dependencies import get_current_auth_user
from backend.app.dependencies import get_uow
from backend.app.repositories import UnitOfWork
from backend.app.bot.bot import BOT

router = APIRouter(prefix="/users", tags=["Users"])

user_service = UserService()
telegram_service = TelegramService(bot=BOT)

@router.get("/", response_model=list[UserResponse])
async def get_users(uow: UnitOfWork = Depends(get_uow)) -> list[UserResponse]:
    return await user_service.list_users(uow=uow)


@router.get('/me', response_model=UserResponse)
def auth_user_check_self_info(
        user: UserResponse = Depends(get_current_auth_user)
):
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: str,
        uow: UnitOfWork = Depends(get_uow),
) -> UserResponse:
    return await user_service.get_user(uow=uow, user_id=user_id)


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(get_current_auth_user)])
async def delete_user(
        user_id: str,
        uow: UnitOfWork = Depends(get_uow),
        current_user: UserResponse = Depends(get_current_auth_user)
) -> None:
    return await user_service.delete_user(uow=uow, user_id=user_id, current_user=current_user)


@router.post('/register', response_model=UserResponse)
async def register_user(
        user: UserCreate,
        uow: UnitOfWork = Depends(get_uow)
) -> UserResponse:
    reg_user = await user_service.register_user(uow=uow, user_register=user)
    await telegram_service.send_message_about_new_user(
        user=reg_user
    )
    return reg_user


@router.post('/login', response_model=TokenInfo)
async def login_user(
        user: UserLogin,
        uow: UnitOfWork = Depends(get_uow)
) -> TokenInfo:
    token = await user_service.authenticate_user(uow=uow, password_from_client=user.password,
                                                 email=user.email)
    return token
