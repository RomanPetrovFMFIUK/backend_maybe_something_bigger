from pydantic import BaseModel, ConfigDict

from schemas import ProductResponse


class CatalogueCreate(BaseModel):
    name: str

class CatalogueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: str
    products: list[ProductResponse] = []
