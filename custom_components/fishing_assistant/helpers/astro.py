from datetime import datetime, timedelta, timezone
from typing import Dict
from skyfield.api import load, wgs84
from skyfield import almanac
import os
from homeassistant.core import HomeAssistant
import logging


async def calculate_astronomy_forecast(hass: HomeAssistant, lat: float, lon: float, days: int = 7) -> Dict[str, dict]:
    ts = load.timescale()
    
    # Check if ephemeris file exists, if not create the directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    eph_path = os.path.join(data_dir, "de421.bsp")
    
    # Download if not exists
    if not os.path.exists(eph_path):
        _LOGGER = logging.getLogger(__name__)
        _LOGGER.info("Downloading skyfield ephemeris data...")
        # Use executor to download without blocking
        def download_eph():
            import urllib.request
            url = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de421.bsp"
            urllib.request.urlretrieve(url, eph_path)
            return load(eph_path)
            
        eph = await hass.async_add_executor_job(download_eph)
    else:
        # Load existing file
        eph = await hass.async_add_executor_job(lambda: load(eph_path))
    location = wgs84.latlon(lat, lon)

    start_date = datetime.now(timezone.utc).date()
    end_date = start_date + timedelta(days=days)

    t0 = ts.utc(start_date.year, start_date.month, start_date.day)
    t1 = ts.utc(end_date.year, end_date.month, end_date.day)

    # Astronomy events
    moon_phases = almanac.moon_phases(eph)
    moon_rise_set = almanac.risings_and_settings(eph, eph['Moon'], location)
    moon_transits = almanac.meridian_transits(eph, eph['Moon'], location)
    sun_rise_set = almanac.sunrise_sunset(eph, location)

    # Init empty containers
    events = {
        "moon_phase": {},
        "moonrise": {},
        "moonset": {},
        "moon_transit": {},
        "moon_underfoot": {},
        "sunrise": {},
        "sunset": {}
    }

    # Moon phase per day
    times, phases = almanac.find_discrete(t0, t1, moon_phases)
    for t, p in zip(times, phases):
        date_str = str(t.utc_datetime().date())
        events["moon_phase"][date_str] = float(round(p % 1, 3))

    # Moonrise / moonset
    times, events_raw = almanac.find_discrete(t0, t1, moon_rise_set)
    for t, ev in zip(times, events_raw):
        date_str = str(t.utc_datetime().date())
        key = "moonrise" if ev == 1 else "moonset"
        events[key][date_str] = t.utc_strftime("%H:%M")

    # Transit / underfoot
    times, events_raw = almanac.find_discrete(t0, t1, moon_transits)
    for t, ev in zip(times, events_raw):
        date_str = str(t.utc_datetime().date())
        key = "moon_transit" if ev == 1 else "moon_underfoot"
        if key not in events:
            events[key] = {}
        events[key][date_str] = t.utc_strftime("%H:%M")

    # Sunrise / sunset
    times, events_raw = almanac.find_discrete(t0, t1, sun_rise_set)
    for t, ev in zip(times, events_raw):
        date_str = str(t.utc_datetime().date())
        key = "sunrise" if ev == 1 else "sunset"
        events[key][date_str] = t.utc_strftime("%H:%M")

    # Final forecast
    forecast = {}
    for i in range(days):
        d = start_date + timedelta(days=i)
        ds = str(d)
        forecast[ds] = {
            "moon_phase": events["moon_phase"].get(ds),
            "moonrise": events["moonrise"].get(ds),
            "moonset": events["moonset"].get(ds),
            "moon_transit": events["moon_transit"].get(ds),
            "moon_underfoot": events["moon_underfoot"].get(ds),
            "sunrise": events["sunrise"].get(ds),
            "sunset": events["sunset"].get(ds),
        }

    return forecast
