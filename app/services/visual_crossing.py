import requests
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = os.getenv("VISUAL_CROSSING_BASE_URL")

def fetch_weather_from_api(city: str) -> dict:
    url = f"{BASE_URL}/{city}?unitGroup=metric&key={API_KEY}&include=current"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return (response.json())
    except requests.exceptions.HTTPError as error:
        if response.status_code == 400:
            raise ValueError(f"Invalid city name: '{city}'")
        raise ValueError(f"Weather API error ({response.status_code}): {response.text}")
    except requests.exceptions.Timeout:
        raise ValueError("Weather API timed out. Please try again later.")
    except requests.exceptions.RequestException as error:
        raise ValueError("Connection error: please try again")
    except requests.exceptions.ConnectionError:
        raise ValueError("Weather API connection failed. Please check your network.")