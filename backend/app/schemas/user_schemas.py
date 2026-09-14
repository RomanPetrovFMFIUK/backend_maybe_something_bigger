from typing import Any, Self

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, computed_field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    full_name: str
    id: str
    age: int

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str
    email: EmailStr
    age: int
    @field_validator('age')
    def validate(cls, value: Any) -> Self:
        if value < 12:
            raise ValueError('Возраст должен быть больше 12')
        return value
    @computed_field
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'

class UserLogin(BaseModel):
    email: str
    password: str