# etl/db.py
import os
from sqlalchemy import create_engine

DB_URL = os.getenv('DB_URL', 'sqlite:///./data/exoplanets.db')
engine = create_engine(DB_URL, future=True)

def get_engine():
    """Return the shared SQLAlchemy Engine configured via DB_URL."""
    return engine