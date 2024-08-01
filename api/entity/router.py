from fastapi import APIRouter, status, HTTPException

from api.entity.models.entity import Entity
from database.models.financial.entity import Entity as EntityModel
from database.connection import dbConnection


router = APIRouter(
    prefix="/entity",
    tags=["Entity"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_entity(entity: Entity):
    """
    Endpoint that receives a payment entity.

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