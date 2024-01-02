from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers import profiles
from routers import tasks
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(profiles.router, prefix="/profiles")
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth.router, prefix="", tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
