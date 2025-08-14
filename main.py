from fastapi import FastAPI

app = FastAPI(
    title="Privacy-Preserving Data Platform API",
    description="API for securely querying anonymized data.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "API is running!"}