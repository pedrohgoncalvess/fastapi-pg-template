import uvicorn
from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users.router import router as users_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
