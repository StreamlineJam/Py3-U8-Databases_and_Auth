from os import environ as env
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from models import Users
from database import get_db
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

JSON_SECRET = env.get("JSON_SECRET")
JSON_ALG = env.get("JSON_ALG")


class UserDBOut(BaseModel):
    name: str
    alt_name: str
    email: str


class User(BaseModel):
    id: int | None = None
    name: str
    alt_name: str
    email: str
    password: str
    is_active: bool
    role: str
    join_on: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jack",
                "alt_name": "郑天健",
                "email": "260021@bjsmicschool.com",
                "password": "123456",
                "is_active": True,
                "role": ""
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, JSON_SECRET, algorithm=JSON_ALG)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, JSON_SECRET, algorithms=JSON_ALG)
        user_email: str = payload.get("sub")
        user_id = payload.get("id")
        if user_email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")
        return {"id": user_id, "email": user_email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials")


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    new_user = Users(**user.model_dump())
    new_user.password = bcrypt_context.hash(new_user.password)

    db.add(new_user)
    db.commit()


@router.get("/users/me", response_model=UserDBOut)
async def get_user_profile(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(Users).filter(Users.id == current_user.get("id")).first()

    if user is not None:
        return UserDBOut(name=user.name,
                         alt_name=user.alt_name,
                         email=user.email)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile is not found")


@router.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can not authorize")

    token = create_access_token(user.email, user.id, timedelta(minutes=90))

    return {"access_token": token, "token_type": "bearer"}
