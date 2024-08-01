from pydantic import BaseModel, Field


class Entity(BaseModel):
    """
    A model to follow to represent the entity table in the database in the JSON of the requests
    """
    name: str = Field(..., max_length=50)
    status: bool
