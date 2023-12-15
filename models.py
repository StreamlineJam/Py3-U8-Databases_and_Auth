from datetime import datetime
from sqlalchemy import Column, Float, String, Boolean, Integer
from database import Base


class Profiles(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gpa = Column(Float)
    school = Column(String)
    gender = Column(String)
    have_pet = Column(Boolean)
