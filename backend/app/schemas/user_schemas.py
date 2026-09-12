from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: str

class UserCreate(BaseModel):
    name: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str