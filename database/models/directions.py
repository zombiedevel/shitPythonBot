from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError

from database import session
from database.models import BaseModel


class Directions(BaseModel):
    __tablename__ = "directions"
    Id = Column('id', Integer, primary_key=True)
    Direction = Column('direction', String(20), unique=True)
    Count = Column('count', Integer)


def SaveDirection(sym_from: str, sym_to: str):
    print(sym_from, sym_to)
    direction = Directions(Direction=f"{sym_from}-{sym_to}", Count=1)
    session.add(direction)
    try:
        session.commit()
    except IntegrityError:
        print("Duplicate direction")
    finally:
        session.close()
        return
