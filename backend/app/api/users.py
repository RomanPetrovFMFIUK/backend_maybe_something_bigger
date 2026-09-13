from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.data_base import get_db
from backend.app.schemas import (UserCreate,
                                 UserResponse,
                                 UserLogin,
                                 TokenInfo)
from backend.app.services import UserService
from backend.app.dependencies import get_current_auth_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    service = UserService(db=db)
    return await service.list_users()

@router.get('/me', response_model=UserResponse)
def auth_user_check_self_info(
        user: UserResponse = Depends(get_current_auth_user)
):
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: str,
        db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = UserService(db=db)
    return await service.get_user(user_id=user_id)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
        user_id: str,
        db: AsyncSession = Depends(get_db),
) -> None:
    service = UserService(db=db)
    await service.delete_user(user_id=user_id)

@router.post('/register')
async def register_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = UserService(db=db)
    reg_user = await service.register_user(user_register=user)
    return reg_user

@router.post('/login', response_model=TokenInfo)
async def login_user(
        user: UserLogin,
        db: AsyncSession = Depends(get_db)
) -> TokenInfo:
    service = UserService(db=db)
    token = await service.authenticate_user(password_from_client=user.password,
                                      email=user.email)
    return token