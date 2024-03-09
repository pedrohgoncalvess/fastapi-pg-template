from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str = Field(..., max_length=50)
    status: bool
