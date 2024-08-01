from fastapi import APIRouter, status, HTTPException, Depends

from api.acc.models.acc import Acc
from api.acc.service import check_list_acc_params
from database.connection import dbConnection
from database.models.financial.acc_payable import AccPayable as AccPayableModel
from database.models.financial.entity import Entity as EntityModel


router = APIRouter(
    prefix="/acc",
    tags=["Account to pay", "Acc"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_acc(acc: Acc):
    """
    Endpoint that receives an account with entity and stores.

    :param acc: JSON file that has the fields corresponding to the Acc class.
    :raises HTTPException: If an account with the same cost, operation and entity already exists :HTTPException: If an entity not exists in the database:
    :return: Created string message
    """

    dbConn = dbConnection
    newValidAcc = AccPayableModel(
        id_entity=acc.id_entity,
        type=acc.type,
        cost=acc.cost
    )

    with dbConn as cursor:
        allAccs = cursor.query(AccPayableModel).all()
        accsIds = [acc.compost_id for acc in allAccs]
        allEntitys = cursor.query(EntityModel).all()
        entitysId = [entity.id for entity in allEntitys]
        newAccId = f"{acc.id_entity}-{acc.type}-{str(acc.cost).replace(',', '.')}"

        if acc.id_entity not in entitysId:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Entity not exists in database."
            )

        if newAccId not in accsIds:
            cursor.add(newValidAcc)
            cursor.commit()
            return "Created"
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Account already exists in database."
            )


@router.get("")
async def list_acc(params: tuple = Depends(check_list_acc_params)):
    """
    An endpoint that receives multiple parameters to query acc payable.

    :param params: Entity id, type and id of acc payable as query parameter.
    :raises HTTPException: if the parameters return no acc payable.
    :return: The acc payable that correspond to the parameters.
    """

    dbConn = dbConnection
    with dbConn as cursor:
        filters = {
            'id_entity': params[0] if params[0] is not None else None,
            'type': params[1] if params[1] is not None else None,
            'id': params[2] if params[2] is not None else None
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        validyAccs = cursor.query(AccPayableModel).filter_by(**filters).all()

    if not validyAccs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found accounts payable with these parameters."
        )
    return validyAccs