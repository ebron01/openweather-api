docker compose up --build


http://localhost:4444/api/weather/ankara?country=TR
http://localhost:4444/api/weather/texas?country=US&units=imperial



http://localhost:4444/api/history/texas?start=2023-09-18&end=2023-09-20
http://localhost:4444/api/history/texas&country=US?start=2023-09-10&end=2023-09-11



http://localhost:4444/api/forecast/texas&country=US
http://localhost:4444/api/forecast/ankara&country=TR?units=metric
http://localhost:4444/api/forecast/texas&country=US?units=imperial


docker exec {container-name} pytest tests/test_calls.py


