from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Profiles
from database import get_db

router = APIRouter()


class Profile(BaseModel):
    id: int | None = None
    name: str = Field(min_length=3)
    gpa: float = Field(lt=5.0)
    school: str = Field(min_length=3, max_length=250)
    gender: str = Field(min_length=0, max_length=7)
    have_pet: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "James",
                "gpa": "4.0",
                "school": "SMIC",
                "gender": "Male",
                "have_pet": False
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_profiles(db: Session = Depends(get_db)):
    return db.query(Profiles).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_profile(profile: Profile, db: Session = Depends(get_db)):
    new_profile = Profiles(**profile.model_dump())

    db.add(new_profile)
    db.commit()


@router.get("/{profile_id}", status_code=status.HTTP_200_OK)
async def get_profile_by_id(profile_id: int = Path(gt=0), db: Session = Depends(get_db)):
    profile = db.query(Profiles).filter(profile_id == Profiles.id).first()
    if profile is not None:
        return profile
    raise HTTPException(status_code=404, detail=f"Profile with id #{profile_id} was not found")


@router.put("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile_by_id(profile_data: Profile, profile_id: int = Path(gt=0), db: Session = Depends(get_db)):
    profile = db.query(Profiles).filter(profile_id == Profiles.id).first()

    if profile is None:
        raise HTTPException(status_code=404, detail=f"Profile with id #{profile_id} was not found")

    profile.title = profile_data.name
    profile.author = profile_data.gpa
    profile.description = profile_data.school
    profile.priority = profile_data.gender
    profile.complete = profile_data.have_pet

    db.add(profile)
    db.commit()


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_by_id(profile_id: int = Path(gt=0), db: Session = Depends(get_db)):
    delete_profile = db.query(Profiles).filter(Profiles.id == profile_id).first()

    if delete_profile is None:
        raise HTTPException(status_code=404, detail=f"Profile with id #{profile_id} was not found")

    db.query(Profiles).filter(Profiles.id == profile_id).delete()
    db.commit()
