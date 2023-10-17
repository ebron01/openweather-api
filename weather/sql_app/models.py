from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship
import datetime
from .database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    reports = relationship("Report", back_populates="city", lazy="dynamic")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    # description = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)

    country = Column(String)
    owner_city = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="reports")


class ReportBulk(Base):
    __tablename__ = "reports_bulk"

    id = Column(Integer, primary_key=True, index=True)
    # description = Column(String, index=True)
    date = Column(DateTime)
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)

    country = Column(String)
    owner_city = Column(Integer, ForeignKey("cities.id"))

    # city = relationship("City", back_populates="reports")
