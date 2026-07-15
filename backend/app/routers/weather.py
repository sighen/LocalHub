import os

import httpx
from fastapi import APIRouter, HTTPException

from app.schemas import WeatherCurrent

router = APIRouter()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SEOUL_LAT = 37.5665
SEOUL_LON = 126.9780


def _describe(weather_id: int) -> tuple[str, str]:
    if weather_id == 800:
        return "☀️", "여행 최적 (맑음)"
    if 801 <= weather_id <= 804:
        return "⛅", "야외 투어 적합 (구름 조금)"
    if 200 <= weather_id <= 232:
        return "⛈️", "경보 대비 요망 (천둥번개)"
    if 300 <= weather_id <= 531:
        return "🌦️", "실내 박물관 투어 권장 (비 조금)"
    if 600 <= weather_id <= 622:
        return "🌨️", "방한 대비 필요 (눈)"
    if 701 <= weather_id <= 781:
        return "🌫️", "시야 확보 주의 (안개)"
    return "☀️", "여행 최적 (맑음)"


@router.get("/current", response_model=WeatherCurrent)
def get_current_weather():
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=503, detail="OPENWEATHER_API_KEY가 설정되지 않았습니다.")

    response = httpx.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": SEOUL_LAT,
            "lon": SEOUL_LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "kr",
        },
        timeout=5.0,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="날씨 정보를 가져오지 못했습니다.")

    data = response.json()
    icon, status = _describe(data["weather"][0]["id"])

    return WeatherCurrent(temp=round(data["main"]["temp"], 1), icon=icon, status=status)
