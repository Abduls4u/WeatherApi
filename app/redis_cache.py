from redis import Redis
import os
import json
from dotenv import load_dotenv
from redis.exceptions import ConnectionError


load_dotenv()
try:
    r = Redis(host="localhost", port=6379, db=0, decode_responses=True)
    r.ping()  # Try connecting
except ConnectionError:
    r = None
    print("⚠️ Warning: Redis is not running. Caching will be disabled.")
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY_SECONDS", 43200)) #12 hours default

def get_cached_weather(city: str):
    if not r:
        return None
    data = r.get(city)
    if data:
        return json.loads(data)
    return None

def set_cached_weather(city: str, data: dict):
    if not r:
        return
    r.set(city, json.dumps(data), ex=CACHE_EXPIRY)