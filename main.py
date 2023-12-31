"""Represents executable weather API."""
import asyncio
import json
import os

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from weather import SETTINGS_PATH, STATIC_FILES_PATH
from weather.api import weather
from weather.address import Address
from weather.models.location import Location
from weather.services import openweather, report
from weather.views import home

from weather.sql_app.database import engine, SessionLocal
from weather.sql_app import models, crud, schemas

weather_app = fastapi.FastAPI()
models.Base.metadata.create_all(bind=engine)
os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "1000"
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def __configure_api_keys() -> None:
    if os.environ.get('API_KEY'):
        openweather.api_key = os.environ['API_KEY']
    else:
        if not SETTINGS_PATH.exists():
            raise FileNotFoundError(
                f'"{SETTINGS_PATH}" file not found, you cannot continue!'
            )
        with SETTINGS_PATH.open() as settings_stream:
            openweather.api_key = json.load(settings_stream).get('api_key')


def __configure_routing() -> None:
    weather_app.mount(
        path='/static',
        app=StaticFiles(directory=STATIC_FILES_PATH),
        name='static',
    )
    weather_app.include_router(home.router)
    weather_app.include_router(weather.router)


def __configure_fake_data() -> None:
    """

    This was added to make it easier to test the weather event reporting
    We have /api/reports but until you submit new data each run, it's missing
    So this will give us something to start from.
    """
    asyncio.run(
        report.add_report(
            'Misty sunrise today, beautiful!',
            Location(city='Lviv', country='UA'),
        )
    )
    asyncio.run(
        report.add_report(
            'Clouds over downtown.', Location(city='Kyiv', country='UA')
        )
    )


def easyrun(address: Address) -> None:
    __configure_fake_data()
    uvicorn.run(weather_app, host=address.host, port=address.port)


__configure_routing()
__configure_api_keys()

