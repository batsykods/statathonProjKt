from fastapi import FastAPI
from . import models
from .database import engine

# 2. Create the database tables (this is the best place for it)
models.Base.metadata.create_all(bind=engine)

# 3. Create your FastAPI app instance

app = FastAPI(
    title="Privacy-Preserving Data Platform API",
    description="API for securely querying anonymized data.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "API is running!"}