import pytest

from fastapi import HTTPException

from backend.app.schemas import (UserCreate,
                                 UserResponse)


async def test_list_user_empty(uow, user_service):
    result = await user_service.list_users(uow=uow)

    assert result == []


async def test_register_user_success(uow, user_service):
    fake_user = UserCreate(name='Иван',
                           surname='Иванов',
                           password='secret',
                           email='ivan@test.com',
                           age=25)
    result = await user_service.register_user(uow=uow, user_register=fake_user)
    assert result.full_name == 'Иван Иванов'
    assert result.age == 25
    assert result.id is not None


async def test_register_user_duplicate_email(uow, user_service):
    fake_user1 = UserCreate(name='Иван',
                            surname='Иванов',
                            password='secret',
                            email='ivan@test.com',
                            age=25)

    fake_user2 = UserCreate(name='Роман',
                            surname='Алексеев',
                            password='supersecret',
                            email='ivan@test.com',
                            age=18)

    with pytest.raises(HTTPException) as http_exc:
        await user_service.register_user(uow=uow, user_register=fake_user1)
        await user_service.register_user(uow=uow, user_register=fake_user2)

    assert http_exc.value.status_code == 409


async def test_get_user(uow, user_service):
    new_user_schema = UserCreate(name='Александр',
                                 surname='Македонский',
                                 password='supersecret',
                                 email='alex@mac.com',
                                 age=18)
    new_user = await user_service.register_user(uow, new_user_schema)

    get_user = await user_service.get_user(uow=uow, user_id=new_user.id)

    assert new_user == get_user


async def test_get_user_not_found(uow, user_service):
    with pytest.raises(HTTPException) as http_exc:
        await user_service.get_user(uow=uow, user_id='')
    assert http_exc.value.status_code == 404


async def test_delete_user_success(uow, user_service):
    user_admin_schema = UserCreate(name='Админ',
                                   surname='Админский',
                                   password='supersecret',
                                   email='admin@admin.com',
                                   age=66,
                                   admin=True)

    default_user_schema = UserCreate(name='Обычный',
                                     surname='Пользователь',
                                     password='supersecret',
                                     email='default@user.com',
                                     age=21)

    user_admin = await user_service.register_user(uow,
                                                  user_admin_schema)
    default_user = await user_service.register_user(uow,
                                                    default_user_schema)

    admin_response = UserResponse(id=user_admin.id,
                                  full_name='Admin',
                                  age=30,
                                  admin=True)
    await user_service.delete_user(uow,
                                   default_user.id,
                                   admin_response)

    res = await uow.users.get_by_id(default_user.id)

    assert res is None


async def test_delete_user_not_admin(uow, user_service):
    default_user_schema1 = UserCreate(name='Обычный',
                                      surname='Пользователь1',
                                      password='supersecret',
                                      email='default1@user.com',
                                      age=21)

    default_user_schema2 = UserCreate(name='Обычный',
                                      surname='Пользователь2',
                                      password='supersecret',
                                      email='default2@user.com',
                                      age=21)

    default_user1 = await user_service.register_user(uow,
                                                     default_user_schema1)

    default_user2 = await user_service.register_user(uow,
                                                     default_user_schema2)

    with pytest.raises(HTTPException) as http_exc:
        await user_service.delete_user(uow, default_user1.id, default_user2)

    assert http_exc.value.status_code == 403


async def test_delete_user_self(uow, user_service):
    default_user_schema = UserCreate(name='Обычный',
                                     surname='Пользователь1',
                                     password='supersecret',
                                     email='default1@user.com',
                                     age=21)
    default_user = await user_service.register_user(uow,
                                                    default_user_schema)

    with pytest.raises(HTTPException) as http_exc:
        await user_service.delete_user(uow, default_user.id, default_user)

    assert http_exc.value.status_code == 403


async def test_authenticate_user_success(uow, user_service):
    raw_password = 'secret123'
    default_user_schema = UserCreate(
        name='Обычный',
        surname='Пользователь1',
        password=raw_password,
        email='default1@user.com',
        age=21,
    )

    await user_service.register_user(uow, default_user_schema)

    token_info = await user_service.authenticate_user(
        uow,
        'default1@user.com',
        raw_password,
    )

    assert token_info.token_type == 'Bearer'
    assert token_info.access_token is not None


async def test_authenticate_user_wrong_email(uow, user_service):
    raw_password = 'secret123'
    default_user_schema = UserCreate(
        name='Обычный',
        surname='Пользователь1',
        password=raw_password,
        email='default1@user.com',
        age=21,
    )

    await user_service.register_user(uow, default_user_schema)

    with pytest.raises(HTTPException) as http_exc:
        await user_service.authenticate_user(
            uow,
            'notdefault1@user.com',
            raw_password,
        )

    assert http_exc.value.status_code == 401

async def test_authenticate_user_wrong_password(uow, user_service):
    default_user_schema = UserCreate(
        name='Обычный',
        surname='Пользователь1',
        password='correct',
        email='default1@user.com',
        age=21,
    )

    await user_service.register_user(uow, default_user_schema)

    with pytest.raises(HTTPException) as http_exc:
        await user_service.authenticate_user(
            uow,
            'default1@user.com',
            'wrong',
        )

    assert http_exc.value.status_code == 401