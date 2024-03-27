import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.params import Depends
from starlette import status
from api_models.acc_to_pay import Acc
from api_models.entity import Entity
from database.connection import dbConnection
from database.models.financial.entity import Entity as EntityModel
from database.models.financial.acc_payable import AccPayable as AccPayableModel

app = FastAPI()


@app.post("/add/entity", status_code=status.HTTP_201_CREATED)
async def add_entity(entity: Entity):
    """
    Endpoint that receives a payment entity and stores.

    :param entity: JSON file that has the fields corresponding to the Entity class.
    :raises HTTPException: If an entity with the same name already exists in the database.
    :return: a JSON with the ID of the new entity.
    """

    dbConn = dbConnection
    newValidEntity = EntityModel(name=entity.name, status=entity.status)

    with dbConn as cursor:
        allEntitys = cursor.query(EntityModel).all()
        entitysName = [entity.name for entity in allEntitys]

        if entity.name not in entitysName:
            cursor.add(newValidEntity)
            cursor.commit()
            newEntity = cursor.query(EntityModel).filter(EntityModel.name == entity.name).first()
            return {"id": newEntity.id}

        else:
            raise HTTPException(
                detail="Document already exists in database",
                status_code=status.HTTP_409_CONFLICT
            )


@app.post("/add/acc", status_code=status.HTTP_201_CREATED)
async def add_acc(acc: Acc):
    """
    Endpoint that receives an account with entity and stores.

    :param acc: JSON file that has the fields corresponding to the Acc class.
    :raises HTTPException: If an account with the same name already: HTTPException: If an entity not exists in the database:
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


async def check_list_acc_params(entity: int = Query(None), type: str = Query(None), id: int = Query(None)):
    """
    Is a parameter validation function on an endpoint.

    :param entity: id of Entity in the database.
    :param type: type of Acc [operation, administrative].
    :param id: id of Acc in the database.
    :raises HTTPException: if none of the 3 parameters are passed.
    :return: Value of 3 parameters.
    """

    if not any([entity, type, id]):
        raise HTTPException(status_code=400, detail="At least one parameter should be passed.")
    return entity, type, id


@app.get("/list/acc/")
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
