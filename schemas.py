# in schemas.py
from pydantic import BaseModel

class DatasetBase(BaseModel):
    name: str
    description: str | None = None
    source: str

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int

    class Config:
        from_attributes = True # Pydantic v2
        # orm_mode = True # Pydantic v1