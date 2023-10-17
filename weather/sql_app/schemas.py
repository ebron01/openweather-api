from typing import List, Union, Optional
from pydantic import BaseModel
import datetime


class Report(BaseModel):
    # description: str
    date: datetime.datetime
    temp: float
    country: str
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    owner_city: int


class City(BaseModel):
    name: str
    # reports : Union[List[Report], None] = None
    reports: List[Report] = []


class ReportBulk(BaseModel):
    reports: List[Report] = []
