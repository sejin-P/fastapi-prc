from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    price: float
    description: str


class ItemResponse(BaseModel):
    title: str
    price: float
