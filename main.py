import uvicorn
from fastapi import FastAPI

from api.acc.router import router as acc_router
from api.entity.router import router as entity_router


app = FastAPI()

app.include_router(acc_router)
app.include_router(entity_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info", reload=True)
