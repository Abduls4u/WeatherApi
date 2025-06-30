from fastapi import FastAPI
from app.weather import router as weather_router


app = FastAPI(title="Weather API with Redis cache")
app.include_router(weather_router, prefix="/weather")