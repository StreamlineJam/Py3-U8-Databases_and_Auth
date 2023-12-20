from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Users
from database import get_db

router = APIRouter()


class User(BaseModel):
    id: int | None = None
    name: str
    alt_name: str
    email: str
    password: str
    is_active: bool
    role: str
    created_on: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jack",
                "alt_name": "郑天健",
                "email": "260021@bjsmicschool.com",
                "password": "963.52",
                "is_active": True,
                "role": ""
            }
        }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    new_user = Users(**user.model_dump())

    db.add(new_user)
    db.commit()