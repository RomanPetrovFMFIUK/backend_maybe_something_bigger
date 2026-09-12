from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: int
    amount: int
    user_id: str

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    price: int
    amount: int
    user_id: str