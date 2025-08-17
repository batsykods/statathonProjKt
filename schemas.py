from pydantic import BaseModel

class DatasetBase(BaseModel):
    name: str
    source: str
    record_count: int
    description: str | None = None

class DatasetResponse(DatasetBase):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str