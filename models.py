from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
