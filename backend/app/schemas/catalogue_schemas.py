from pydantic import BaseModel, ConfigDict


class CatalogueCreate(BaseModel):
    name: str

class CatalogueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: str
