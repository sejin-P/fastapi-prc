from app.api.db.init_db import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()