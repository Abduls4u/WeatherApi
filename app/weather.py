from fastapi import APIRouter, HTTPException
from app.redis_cache import get_cached_weather, set_cached_weather
from app.services.visual_crossing import fetch_weather_from_api

router = APIRouter()

@router.get("/{city}")
def get_weather(city: str):
    city_key = city.lower()

    cached = get_cached_weather(city)
    if cached:
        return {"source": "cache", "data": cached}
    
    try:
        data = fetch_weather_from_api(city)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    set_cached_weather(city_key, data)
    return ({"source": "api", "data": data})
