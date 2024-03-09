import uvicorn
from fastapi import FastAPI, HTTPException, Query
from starlette import status
from api_models.acc_to_pay import Acc
from api_models.entity import Entity
from database.connection import dbConnection
from database.models.financial.entity import Entity as EntityModel
from database.models.financial.acc_payable import AccPayable as AccPayableModel

app = FastAPI()


@app.post("/add/entity", status_code=status.HTTP_201_CREATED)
async def add_entity(entity: Entity):
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
            raise HTTPException(detail="Document already exists in database", status_code=status.HTTP_409_CONFLICT)


@app.post("/add/acc", status_code=status.HTTP_201_CREATED)
async def add_acc(acc: Acc):
    dbConn = dbConnection
    newValidAcc = AccPayableModel(id_entity=acc.id_entity, type=acc.type, cost=acc.cost)
    with dbConn as cursor:
        allAccs = cursor.query(AccPayableModel).all()
        accsIds = [acc.compost_id for acc in allAccs]
        allEntitys = cursor.query(EntityModel).all()
        entitysId = [entity.id for entity in allEntitys]
        newAccId = f"{acc.id_entity}-{acc.type}-{str(acc.cost).replace(',','.')}"
        if acc.id_entity not in entitysId:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Entity not exists in database.")
        if newAccId not in accsIds:
            cursor.add(newValidAcc)
            cursor.commit()
            return "Created"
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists in database.")


async def check_list_acc_params(entity: id = Query(None), type: str = Query(None), id: int = Query(None)):
    if not any([entity, type, id]):
        raise HTTPException(status_code=400, detail="At least one parameter should be passed.")
    return entity, type, id


# @app.get("/list/acc/")
# async def list_acc(params: tuple = Depends(check_list_acc_params)):
#     return {"message": f"Hello {params}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
