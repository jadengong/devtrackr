# deps.py
from collections.abc import Generator  # Python 3.11+ (preferred)
# from typing import Generator  # <- use this instead on older Python
from sqlalchemy.orm import Session
from db import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
