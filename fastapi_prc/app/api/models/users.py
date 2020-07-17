from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from app.api.db.init_db import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), index=True)
    password_hash = Column(String(128))
    birth = Column(Date)
