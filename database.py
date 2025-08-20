import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get the database URL from the environment
db_url = os.getenv("DATABASE_URL")

# This is the critical fix:
# Render's PostgreSQL requires SSL. If the URL is for a Render database,
# we need to ensure it uses SSL.
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Another common issue is that the default driver doesn't work well on Render
# We will use a more compatible one if needed.
# if db_url and "onrender.com" in db_url:
#     if "?sslmode=require" not in db_url:
#         db_url += "?sslmode=require"


SQLALCHEMY_DATABASE_URL = db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()