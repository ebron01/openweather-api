from fastapi.testclient import TestClient
import fastapi
from weather.sql_app import crud, models, schemas
from main import weather_app

client = TestClient(weather_app)


def test_weather():
    response = client.get("api/weather/texas")
    assert response.status_code == 200

def test_weather_no_city():
    response = client.get("api/weather/")
    assert response.status_code == 404
    
def test_forecast():
    response = client.get("api/forecast/ankara?country=TR")
    assert response.status_code == 200
    
    
def test_history():
    response = client.get("/api/history/texas?start=2023-09-18&end=2023-09-20")
    assert response.status_code == 200
    
def test_history_date():
    response = client.get("/api/history/texas?start=23-09-18&end=23-09-20")
    assert response.status_code == 500