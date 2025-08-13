from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select

from app.acc import AccJson
from app.acc import check_list_acc_params
from database import DatabaseConnection
from database.models import AccPayable as AccPayableModel
from database.models import Entity as EntityModel


router = APIRouter(
    prefix="/acc",
    tags=["Account to pay", "Acc"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_acc(acc: AccJson):
    """
    Endpoint that receives an account with entity and stores.

    :param acc: JSON file that has the fields corresponding to the Acc class.
    :raises HTTPException: If an account with the same cost, operation and entity already exists
    :raises HTTPException: If an entity not exists in the database
    :return: Created string message
    """

    db_conn = DatabaseConnection()

    async with db_conn as session:
        result = await session.execute(
            select(EntityModel).where(EntityModel.id == acc.id_entity)
        )
        entity = result.scalars().first()

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Entity not exists in database."
            )

        new_acc_id = f"{acc.id_entity}-{acc.type.value}-{acc.cost:.3f}"

        result = await session.execute(
            select(AccPayableModel).where(AccPayableModel.compost_id == new_acc_id)
        )
        existing_acc = result.scalars().first()

        if existing_acc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Account already exists in database."
            )

        new_valid_acc = AccPayableModel(
            id_entity=acc.id_entity,
            type=acc.type,
            cost=acc.cost
        )

        session.add(new_valid_acc)
        await session.commit()
        await session.refresh(new_valid_acc)

        return {"id": new_valid_acc.id}


@router.get("")
async def list_acc(params: tuple = Depends(check_list_acc_params)):
    """
    An endpoint that receives multiple parameters to query acc payable.

    :param params: Entity id, type and id of acc payable as query parameter.
    :raises HTTPException: if the parameters return no acc payable.
    :return: The acc payable that correspond to the parameters.
    """

    db_conn = DatabaseConnection()

    filters = {
        'id_entity': params[0] if params[0] is not None else None,
        'type': params[1] if params[1] is not None else None,
        'id': params[2] if params[2] is not None else None
    }

    filters = {k: v for k, v in filters.items() if v is not None}

    async with db_conn as session:
        query = select(AccPayableModel)

        for key, value in filters.items():
            query = query.where(getattr(AccPayableModel, key) == value)

        result = await session.execute(query)
        valid_accs = result.scalars().all()

    if not valid_accs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found accounts payable with these parameters."
        )

    return valid_accs