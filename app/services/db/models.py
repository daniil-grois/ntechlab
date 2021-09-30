from sqlalchemy import Column, Float, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    x = Column(DECIMAL, default=False)
    y = Column(DECIMAL, default=False)


UserTable = User.__table__
