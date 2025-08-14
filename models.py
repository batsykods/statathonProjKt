# in models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from  database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())