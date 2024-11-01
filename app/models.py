from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    guest_count = Column(Integer, nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    table_number = Column(String, nullable=False)


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String)
    seats = Column(Integer)
