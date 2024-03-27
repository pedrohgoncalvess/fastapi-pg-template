from pydantic import BaseModel
from enum import Enum

#TODO: Make docstrings read by sphinx
class AccType(str, Enum):
    """
    An implementation to limit the options of the type field in the Acc model.
    """
    operation: str = "operation"
    administrative: str = "administrative"


class Acc(BaseModel):
    """
    A model to follow to represent the entity acc_payable in the database in the JSON of the requests.
    """
    id_entity: int
    type: AccType
    cost: float

