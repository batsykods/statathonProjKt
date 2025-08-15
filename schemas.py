# in schemas.py
from pydantic import BaseModel

class DatasetBase(BaseModel):
    name: str
    description: str | None = None
    source: str

class DatasetCreate(DatasetBase):
    pass

class DatasetResponse(DatasetBase):
    id: int

    class Config:
        from_attributes = True