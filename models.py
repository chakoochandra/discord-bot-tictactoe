from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import INTEGER, TEXT
from sqlalchemy.types import PickleType, Boolean  # noqa

Base = declarative_base()


class Tic(Base):
    __tablename__ = "tic"
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    avatar = Column(TEXT)
    history = Column(PickleType, default=[])
