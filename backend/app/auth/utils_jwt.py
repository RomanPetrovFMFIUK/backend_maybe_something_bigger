import jwt
import bcrypt
from datetime import datetime, timedelta, timezone

from backend.app.core import get_settings

settings = get_settings()


# кодируем наш payload на основе приватного ключа, который мы сгенерировали при помощи openssl в jwt-private.pem

def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = 15
):
    time_now = datetime.now(timezone.utc)
    to_encode = payload.copy()
    expire = time_now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire,
                     iat=time_now)
    encoded = jwt.encode(to_encode,
                         private_key,
                         algorithm=algorithm)
    return encoded


# декодируем наш токен на основе публичного ключа

def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token,
                         public_key,
                         algorithms=[algorithm])
    return decoded


def hash_password(
        password: str
) -> str:
    salt = bcrypt.gensalt()  # Это криптографическая соль = Случайная последовательность данных
    pwd_bytes: bytes = password.encode('utf-8')
    # Вычисляем хэш при помощи байтов закодированного пароля и криптографической соли
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt=salt)
    return hashed_bytes.decode('utf-8')


def validate_password(
        password: str,
        hashed_password: str | bytes
) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password.encode('utf-8'),
                          hashed_password=hashed_password)
