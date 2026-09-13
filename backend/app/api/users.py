from fastapi import APIRouter, Depends
from backend.app.schemas import (UserCreate,
                                 UserResponse,
                                 UserLogin,
                                 TokenInfo)
from backend.app.services import UserService
from backend.app.dependencies import get_current_auth_user
from dependencies import get_uow
from repositories import UnitOfWork

router = APIRouter(prefix="/users", tags=["Users"])

user_service = UserService()


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


@router.delete("/{user_id}", status_code=204)
async def delete_user(
        user_id: str,
        uow: UnitOfWork = Depends(get_uow),
) -> None:
    return await user_service.delete_user(uow=uow, user_id=user_id)


@router.post('/register')
async def register_user(
        user: UserCreate,
        uow: UnitOfWork = Depends(get_uow)
) -> UserResponse:
    reg_user = await user_service.register_user(uow=uow, user_register=user)
    return reg_user


@router.post('/login', response_model=TokenInfo)
async def login_user(
        user: UserLogin,
        uow: UnitOfWork = Depends(get_uow)
) -> TokenInfo:
    token = await user_service.authenticate_user(uow=uow, password_from_client=user.password,
                                                 email=user.email)
    return token
