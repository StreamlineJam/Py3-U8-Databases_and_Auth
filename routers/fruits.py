from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Fruits
from database import get_db
from .auth import get_current_user

router = APIRouter()


class Fruit(BaseModel):
    id: int | None = None
    fruit_type: str
    color: str
    size: int
    grown: bool
    created_on: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "fruit_type": "type of the fruit",
                "color": "color of the fruit",
                "size": 1,
                "grown": False
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_fruits(db: Session = Depends(get_db)):
    return db.query(Fruits).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_fruit(fruit: Fruit, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_fruit = Fruits(**fruit.model_dump(), planter=current_user.get("id"))
    db.add(new_fruit)
    db.commit()


@router.get("/{fruit_id}", status_code=status.HTTP_200_OK)
async def get_fruit_by_id(fruit_id: int = Path(gt=0), db: Session = Depends(get_db)):
    fruit = db.query(Fruits).filter(fruit_id == Fruit.id).first()
    if fruit is not None:
        return fruit
    raise HTTPException(status_code=404, detail=f"Fruit with id #{fruit_id} was not found")


@router.put("/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_fruit_by_id(fruit_data: Fruit, fruit_id: int = Path(gt=0), db: Session = Depends(get_db)):
    fruit = db.query(Fruits).filter(fruit_id == Fruit.id).first()

    if not fruit is None:
        raise HTTPException(status_code=404, detail=f"Fruit with id #{fruit_id} was not found")

    fruit.fruit_type = fruit_data.fruit_type
    fruit.planter = fruit_data.planter
    fruit.color = fruit_data.color
    fruit.size = fruit_data.size
    fruit.grown = fruit_data.grown

    db.add(fruit)
    db.commit()


@router.delete("/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fruit_by_id(fruit_id: int = Path(gt=0), db: Session = Depends(get_db)):
    delete_fruit = db.query(Fruits).filter(Fruits.id == fruit_id).first()

    if delete_fruit is None:
        raise HTTPException(status_code=404, detail=f"Fruit with id #{fruit_id} was not found")

    db.query(Fruits).filter(Fruits.id == fruit_id).delete()
    db.commit()