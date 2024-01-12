from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers import profiles
from routers import tasks
from routers import auth
from routers import fruits

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(profiles.router, prefix="/profiles")
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(fruits.router, prefix="/fruits", tags=["Fruits"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="10.6.20.110", reload=True)
