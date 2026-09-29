import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Copy backend/.env.example to backend/.env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
   autocommit=False,
   autoflush=False,
   bind=engine
)
Base = declarative_base()
