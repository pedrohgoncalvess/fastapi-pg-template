from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from app.entity import EntityJson
from database.models import Entity as EntityModel
from database import DatabaseConnection


router = APIRouter(
    prefix="/entity",
    tags=["Entity"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_entity(entity: EntityJson):
    """
    Endpoint that receives a payment entity.

    :param entity: JSON file that has the fields corresponding to the Entity class.
    :raises HTTPException: If an entity with the same name already exists in the database.
    :return: a JSON with the ID of the new entity.
    """

    db_conn = DatabaseConnection()

    async with db_conn as session:
        result = await session.execute(
            select(EntityModel).where(EntityModel.name == entity.name)
        )
        existing_entity = result.scalars().first()

        if existing_entity:
            raise HTTPException(
                detail="Entity already exists in database",
                status_code=status.HTTP_409_CONFLICT
            )

        new_valid_entity = EntityModel(name=entity.name, status=entity.status)

        session.add(new_valid_entity)
        await session.commit()
        await session.refresh(new_valid_entity)

        return {"id": new_valid_entity.id}