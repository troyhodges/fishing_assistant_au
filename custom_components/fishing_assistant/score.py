import datetime
from .api import get_forecast_data, get_moon_data

def get_fish_scores():
    # Dummy implementation for now
    today = datetime.date.today()
    weather = get_forecast_data()
    moon = get_moon_data()

    return {
        "carp": 0.78,
        "trout": 0.52,
        "pike": 0.66
    }
