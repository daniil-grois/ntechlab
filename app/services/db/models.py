from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    x = Column(Float, default=False)
    y = Column(Float, default=False)


UserTable = User.__table__
