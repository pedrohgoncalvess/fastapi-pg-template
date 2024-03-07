from pydantic import BaseModel


class Entity(BaseModel):
    name: str
    status: bool
