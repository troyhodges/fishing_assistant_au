[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/docs/setup/custom_repositories)
[![GitHub release](https://img.shields.io/github/v/release/bairnhard/home-assistant-google-aqi?style=for-the-badge)](https://github.com/bairnhard/home-assistant-google-aqi/releases)

# 🎣 Fishing Assistant for Home Assistant

**Fishing Assistant** is a custom integration for [Home Assistant](https://www.home-assistant.io) that predicts optimal fishing times for your favorite lakes, rivers, ponds, or reservoirs — based on weather, solunar theory, and environmental factors.

> _"Is today a good day to go fishing?"_  
Let Home Assistant tell you. 🐟

---

## 📦 Features

- 🧠 Smart scoring system (0–10 scale)
- 📍 Multiple locations & fish species
- 🌅 Sunrise/sunset & twilight boost
- 🌒 Moon phase, transit & Solunar periods
- 🌦️ Live weather from Open-Meteo
- 🗺️ Location-aware (lat/lon/zone)
- 📈 7-day forecast with best fishing windows
- 🔄 Auto-refreshes 4x per day

---

## 🛠️ Installation

1. Copy the custom component folder:

   ```bash
   /custom_components/fishing_assistant/
   ```

   This folder must include:
   - `__init__.py`
   - `sensor.py`
   - `score.py`
   - `fish_profiles.py`
   - `helpers/astro.py`
   - `manifest.json`

2. Install required Python libraries:

   Add these to your `requirements` or install via pip in your HA environment:

   ```
   pandas
   aiohttp
   skyfield
   jplephem
   ```

3. Restart Home Assistant.

---

## 🧭 Configuration

You can add multiple fishing spots via the UI or YAML:

### UI (Preferred)
Go to **Settings → Devices & Services → Add Integration → Fishing Assistant**  
Enter:
- Name (e.g., “Ammersee”)
- Coordinates or Home Assistant Zone
- Fish species (comma-separated)
- Body type (lake, river, pond, reservoir)

---

## 🐟 Scoring System

Each day is given a **score from 0 to 10**, where:

| Score | Meaning |
|-------|---------|
| 0     | ❌ Stay home. Tie flies instead. |
| 3     | 😐 Meh — maybe go if you're bored. |
| 6     | 👍 Good conditions. Worth a shot. |
| 8     | 🔥 Great — pack the rods! |
| 10    | 🚨 CALL IN SICK. Risk the divorce. |

### Factors considered:

- ✅ **Air temperature** (proxy for water temp)
- 🌥 **Cloud cover**
- 💨 **Wind speed**
- 🌧 **Precipitation**
- 🧭 **Barometric pressure trend**
- 🌅 **Twilight boost** (1h around sunrise/sunset)
- 🌑 **Moon phase**
- 🌗 **Solunar periods** (transit, underfoot, rise/set)
- 🌊 **Water body type** (affects weightings)

---

## 🧠 Example Sensor Output

```yaml
sensor.ammersee_zander_fishing_score:
  state: 8
  friendly_name: Ammersee (Zander) Fishing Score
  best_window: 04:00 – 06:00
  forecast:
    2025-04-17:
      score: 8
      best_window: 04:00 – 06:00
    2025-04-18:
      score: 7
      best_window: 18:00 – 20:00
```

---

## 💡 Tips

- You can show the forecast in a Lovelace `entities` card or use `custom:weather-forecast`-like cards.
- Pair with weather and water sensors for rich dashboards.
- Tweak fish profiles and weights to better match local experience.

---

## 📚 Roadmap

- 🐠 Add bait suggestions based on conditions
- 📊 Integrate with historical catch logs
- 🛰 Use water temperature data from satellites or hydrology APIs
- 🌐 Multi-language support

---

## 🐛 Contributing

Issues and PRs welcome!  
This is built with love by anglers, for anglers.

---

## License

This project is licensed under the [MIT License](LICENSE).
