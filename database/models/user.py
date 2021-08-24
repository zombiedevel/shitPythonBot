from sqlalchemy import Column, String, Integer, Boolean

from database import Base, session
from database.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegramId = Column(Integer, unique=True)
    username = Column(String(32))
    firstName = Column(String(64))
    lastName = Column(String(64))
    status = Column(Boolean)


def GetActiveCount() -> int:
    result = session.query(User)
    result.status = True
    return result.count()


def GetActiveUsers():
    result = session.query(User)
    result.status = True
    return result.all()