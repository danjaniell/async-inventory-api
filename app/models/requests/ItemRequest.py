from pydantic import BaseModel


class AddItemRequest(BaseModel):
    id: int
    name: str
    description: str


class UpdateItemRequest(BaseModel):
    name: str
    description: str
