# 🌤️ Python Weather App

A terminal-based weather app built with Python that fetches **real live weather data** using the [OpenWeatherMap API](https://openweathermap.org/api).

## Features

- 🌡️ **Current Weather** — temperature, humidity, wind, pressure, visibility
- 📅 **5-Day Forecast** — daily high/low and conditions
- 🔄 **Unit Toggle** — switch between °Celsius and °Fahrenheit instantly
- 📋 **Search History** — saves your last 10 searched cities (stored in JSON)
- ❌ **Error Handling** — handles bad city names, no internet, invalid API key

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/python-weather-app.git
cd python-weather-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a FREE API key
1. Go to [openweathermap.org](https://openweathermap.org) and create a free account
2. Go to **API keys** in your dashboard
3. Copy your key

### 4. Add your API key
Open `weather.py` and replace line 14:
```python
API_KEY = "YOUR_API_KEY_HERE"   # ← paste your key here
```

### 5. Run it
```bash
python weather.py
```

## Usage

```
════════════════════════════════════════════════
        🌤️  PYTHON WEATHER APP
════════════════════════════════════════════════

  MENU
────────────────────────────────────────────────
  [1] Search city weather
  [2] 5-day forecast
  [3] Toggle units  (currently °C)
  [4] Search history
  [5] Quit
```

## Project Structure

```
python-weather-app/
├── weather.py           # Main application
├── requirements.txt     # Python dependencies
├── search_history.json  # Auto-created on first search
└── README.md            # This file
```

## Requirements

- Python 3.10+
- Internet connection
- Free OpenWeatherMap API key

## License

MIT License
