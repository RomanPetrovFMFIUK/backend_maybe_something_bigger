from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.data_base import get_db
from backend.app.schemas import UserResponse
from backend.app.auth import decode_jwt
from backend.app.services import UserService

http_bearer = HTTPBearer()


async def get_current_auth_user(
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        decoded_token = decode_jwt(token.credentials)
    except:
        raise HTTPException(status_code=401)
    email = decoded_token['email']
    user_service = UserService(db=db)
    user = await user_service.get_user_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404,
                            detail='Пользователь не найден')
    return user
