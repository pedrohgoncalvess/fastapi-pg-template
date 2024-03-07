from pydantic import BaseModel
from enum import Enum


class AccType(str, Enum):
    operation: str = "operation"
    administrative: str = "administrative"


class Acc(BaseModel):
    id_entity: int
    type: AccType
    cost: float

