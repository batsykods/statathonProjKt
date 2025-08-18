import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from faker import Faker
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, auth
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Privacy API")

# in main.py

# --- CORS MIDDLEWARE ---
# This regex pattern allows localhost, your main Vercel domains, 
# and ANY Vercel preview URL for your project.
allow_origin_regex = r"https?://(localhost:3000|statsone\.vercel\.app|statathonfrontend\.vercel\.app|statathonfrontend-[a-zA-Z0-9-]+\.vercel\.app)"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=allow_origin_regex, # Use the flexible regex pattern
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FAKER INSTANCE ---
fake = Faker()

# --- DATABASE DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- INITIAL USER CREATION ---
with SessionLocal() as db:
    if not db.query(models.User).filter(models.User.username == "researcher1").first():
        hashed_password = auth.get_password_hash("testpassword")
        db_user = models.User(username="researcher1", hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        print("Initial user 'researcher1' created.")

# --- API ENDPOINTS ---

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/datasets/load-school-data/")
def load_school_data(db: Session = Depends(get_db)):
    try:
        df = pd.read_csv("data/schools_data.csv")
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        
        numeric_cols = ["Primary_Schools", "Middle_Schools", "High/Senior_Secondary_Schools", "Total_in_Number"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        for _, row in df.iterrows():
            if row["District"] == "Total": continue
            if db.query(models.Dataset).filter(models.Dataset.name == row["District"]).first(): continue

            total_schools = row["Primary_Schools"] + row["Middle_Schools"] + row["High/Senior_Secondary_Schools"]
            total_colleges = row["Total_in_Number"]
            new_entry = models.Dataset(
                name=row["District"],
                source=row["State"],
                record_count=total_schools + total_colleges,
                description=f"Schools: {total_schools}, Colleges: {total_colleges}"
            )
            db.add(new_entry)
        
        db.commit()
        return {"message": f"Successfully loaded data for {len(df) - 1} districts."}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="schools_data.csv not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datasets/", response_model=list[schemas.DatasetResponse])
def read_datasets(
    source: str | None = None,
    min_records: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    MINIMUM_THRESHOLD = 3
    query = db.query(models.Dataset)
    if source:
        query = query.filter(models.Dataset.source == source)
    if min_records is not None:
        query = query.filter(models.Dataset.record_count > min_records)
    if query.count() < MINIMUM_THRESHOLD:
        raise HTTPException(status_code=403, detail="Query results in too few records.")
    return query.offset(skip).limit(limit).all()

@app.get("/")
def read_root():
    return {"status": "API is online"}