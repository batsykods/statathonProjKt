# in main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Absolute imports will now work correctly
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/datasets/", response_model=schemas.DatasetResponse)
def create_dataset(dataset: schemas.DatasetCreate, db: Session = Depends(get_db)):
    db_dataset = db.query(models.Dataset).filter(models.Dataset.name == dataset.name).first()
    if db_dataset:
        raise HTTPException(status_code=400, detail="Dataset name already registered")

    new_dataset = models.Dataset(**dataset.model_dump())
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset

@app.get("/")
def read_root():
    return {"status": "API is running!"}