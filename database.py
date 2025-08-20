import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get the database URL from the environment
db_url = os.getenv("DATABASE_URL")

# This is the critical fix:
# Change the protocol from 'postgres' to 'postgresql+pg8000'
# to tell SQLAlchemy to use the new, more compatible driver.
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+pg8000://", 1)

SQLALCHEMY_DATABASE_URL = db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()