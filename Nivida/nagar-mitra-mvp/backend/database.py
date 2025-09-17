from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# For MVP, we'll use SQLite instead of PostgreSQL for easier setup
# In production, switch to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nagar_mitra.db")

# For PostgreSQL, use:
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/nagar_mitra_db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()