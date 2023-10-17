import http
from typing import Any, Dict, List, Optional, Union

import fastapi
from fastapi import Depends

from weather.models.location import Location
from weather.models.reports import Report, ReportSubmittal
from weather.models.validation import ValidationError
from weather.services import openweather
from weather.services.report import add_report, reports

from weather.sql_app.crud import (
    create_report,
    get_city,
    create_city,
    create_report_bulk,
)
from weather.sql_app.database import SessionLocal
import datetime
from weather.sql_app.schemas import Report, City, ReportBulk
from sqlalchemy.orm import Session


router = fastapi.APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/api/weather/{city}')
async def weather(
    location: Location = Depends(),
    units: str = 'metric',
    db: Session = Depends(get_db),
) -> Union[Optional[Dict[str, Any]], fastapi.Response]:
    """Returns a city weather route."""
    try:
        data = openweather.report(
            location.city, location.country, units, 'weather'
        )
        aw_data = await data
        city = get_city(db, location.city)
        if not city:
            city = create_city(db, City(name=location.city))
        new_data = {
            "date": datetime.datetime.now(),
            "country": location.country,
            "temp": aw_data["temp"],
            "feels_like": aw_data["feels_like"],
            "temp_min": aw_data["temp_min"],
            "temp_max": aw_data["temp_max"],
            "pressure": aw_data["pressure"],
            "humidity": aw_data["humidity"],
            "owner_city": city.id,
        }
        report = Report(**new_data)
        create_report(db=db, report=report)
        return aw_data
    except ValidationError as flaw:
        return fastapi.Response(
            content=flaw.error_message, status_code=flaw.status_code
        )
    except Exception as flaw:
        return fastapi.Response(
            content=str(flaw),
            status_code=int(http.HTTPStatus.INTERNAL_SERVER_ERROR),
        )


@router.get('/api/reports', name='reports', response_model=List[Report])
async def all_reports() -> List[Report]:
    """Returns all weather reports."""
    return await reports()


@router.post(
    '/api/reports',
    name='add_report',
    status_code=int(http.HTTPStatus.CREATED),
    response_model=Report,
)
async def post_report(report_submittal: ReportSubmittal) -> Report:
    """Add a new weather report."""
    return await add_report(
        report_submittal.description, report_submittal.location
    )


@router.get('/api/forecast/{city}')
async def forecast(
    location: Location = Depends(),
    units: str = 'metric',
    db: Session = Depends(get_db),
) -> Union[Optional[Dict[str, Any]], fastapi.Response]:
    """Returns a city weather route."""
    try:
        data = openweather.report(
            location.city, location.country, units, 'forecast'
        )
        aw_data = await data
        city = get_city(db, location.city)
        if not city:
            city = create_city(db, City(name=location.city))
        new_data = []
        for data in aw_data:
            new_data.append(
                {
                    "date": datetime.datetime.fromtimestamp(data['dt']),
                    "country": location.country,
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_min": data["main"]["temp_min"],
                    "temp_max": data["main"]["temp_max"],
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                    "owner_city": city.id,
                }
            )
        create_report_bulk(db=db, reports=new_data)
        return new_data
    except ValidationError as flaw:
        return fastapi.Response(
            content=flaw.error_message, status_code=flaw.status_code
        )
    except Exception as flaw:
        return fastapi.Response(
            content=str(flaw),
            status_code=int(http.HTTPStatus.INTERNAL_SERVER_ERROR),
        )


@router.get('/api/history/{city}')
async def history(
    start : str, 
    end : str, 
    location: Location = Depends(),
    units: str = 'metric',
    db: Session = Depends(get_db),

) -> Union[Optional[Dict[str, Any]], fastapi.Response]:
    """Returns a city weather route."""
    try:
        # startdate format 2023-10-02
        date_format = "%Y-%m-%d"
        start_ = int(datetime.datetime.strptime(start, date_format).timestamp())
        end_ = int(datetime.datetime.strptime(end, date_format).timestamp())
        
        data = openweather.report(
            location.city, location.country, units, 'history', start_, end_
        )
        aw_data = await data
        city = get_city(db, location.city)
        if not city:
            city = create_city(db, City(name=location.city))
        new_data = []
        for data in aw_data:
            new_data.append(
                {
                    "date": datetime.datetime.fromtimestamp(data['dt']),
                    "country": location.country,
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_min": data["main"]["temp_min"],
                    "temp_max": data["main"]["temp_max"],
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                    "owner_city": city.id,
                }
            )
        create_report_bulk(db=db, reports=new_data)
        return new_data
    except ValidationError as flaw:
        return fastapi.Response(
            content=flaw.error_message, status_code=flaw.status_code
        )
    except Exception as flaw:
        return fastapi.Response(
            content=str(flaw),
            status_code=int(http.HTTPStatus.INTERNAL_SERVER_ERROR),
        )



