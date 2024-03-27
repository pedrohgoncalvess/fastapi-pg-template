from pydantic import BaseModel, Field


#TODO: Make docstrings read by sphinx
class Entity(BaseModel):
    """
    A model to follow to represent the entity table in the database in the JSON of the requests
    """
    name: str = Field(..., max_length=50)
    status: bool
