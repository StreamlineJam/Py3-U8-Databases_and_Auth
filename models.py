from datetime import datetime, timezone
from sqlalchemy import Column, Float, String, Boolean, Integer, DateTime
from database import Base


class Profiles(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gpa = Column(Float)
    school = Column(String)
    gender = Column(String)
    have_pet = Column(Boolean)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    alt_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    join_on = Column(DateTime, default=datetime.now(timezone.utc))