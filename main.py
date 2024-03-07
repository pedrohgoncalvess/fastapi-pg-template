import uvicorn
from fastapi import FastAPI, HTTPException, Query, Depends
from starlette import status
from api_models.acc_to_pay import Acc
from api_models.entity import Entity
from database.connection import dbConnection
from database.models.financial.entity import Entity as EntityModel

app = FastAPI()


@app.post("/add/entity", status_code=status.HTTP_201_CREATED)
async def add_entity(entity: Entity):
    dbConn = dbConnection
    newValidEntity = EntityModel(name=entity.name, status=entity.status)
    with dbConn as cursor:
        cursor.add(newValidEntity)
        cursor.commit()
    return "Ok"


@app.post("/add/acc")
async def add_acc(acc: Acc):
    return {"message": "Hello World"}


async def check_list_acc_params(entity: id = Query(None), type: str = Query(None), id: int = Query(None)):
    if not any([entity, type, id]):
        raise HTTPException(status_code=400, detail="At least one parameter should be passed.")
    return entity, type, id


# @app.get("/list/acc/")
# async def list_acc(params: tuple = Depends(check_list_acc_params)):
#     return {"message": f"Hello {params}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
