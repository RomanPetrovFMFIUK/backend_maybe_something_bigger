from pathlib import Path
import jwt as pyjwt

import pytest

from backend.app.auth import (hash_password,
                              validate_password,
                              encode_jwt,
                              decode_jwt)

private_key = Path("backend/jwt-private.pem").read_text()
public_key = Path("backend/jwt-public.pem").read_text()

def test_hash_password_returns_strings():
    password = hash_password('password')
    assert type(password) == str
    assert password != 'password'
    assert password is not None

def test_validate_password_correct():
    hashed = hash_password('password')
    result = validate_password('password', hashed)
    assert result

def test_validate_password_incorrect():
    hashed = hash_password('password')
    result = validate_password('wrong password', hashed)
    assert not result

def test_encode_decode_jwt_roundtrip():

    payload = {"email": 'test@test.com'}
    token = encode_jwt(payload, private_key)
    decoded = decode_jwt(token, public_key)
    assert decoded['email'] == 'test@test.com'

def test_decode_jwt_invalid_token():
    with pytest.raises(pyjwt.PyJWTError):
        decode_jwt("мусор", public_key=public_key)
