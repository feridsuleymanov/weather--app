"""
============================================
  Weather App — Python
  Uses OpenWeatherMap API (free tier)
  Features: current weather, 5-day forecast,
  search history, unit toggle (C / F)
============================================
"""

import requests
import json
import os
from datetime import datetime

# ── Config ────────────────────────────────
API_KEY   = "YOUR_API_KEY_HERE"   # <-- replace with your key
BASE_URL  = "https://api.openweathermap.org/data/2.5"
HISTORY_FILE = "search_history.json"


# ── Helpers ───────────────────────────────

def celsius_to_fahrenheit(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)


def kelvin_to_celsius(k: float) -> float:
    return round(k - 273.15, 1)


def format_temp(celsius: float, unit: str) -> str:
    if unit == "C":
        return f"{celsius}°C"
    return f"{celsius_to_fahrenheit(celsius)}°F"


def wind_direction(degrees: int) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(degrees / 45) % 8]


def print_banner():
    print("\n" + "═" * 48)
    print("        🌤️  PYTHON WEATHER APP")
    print("═" * 48)


def print_separator():
    print("─" * 48)


# ── History ───────────────────────────────

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def add_to_history(city: str, history: list) -> list:
    city = city.title()
    if city in history:
        history.remove(city)
    history.insert(0, city)          # most recent first
    return history[:10]              # keep last 10


def show_history(history: list):
    if not history:
        print("\n  No search history yet.")
        return
    print("\n  📋 Recent Searches:")
    for i, city in enumerate(history, 1):
        print(f"     {i}. {city}")


# ── API Calls ─────────────────────────────

def get_current_weather(city: str) -> dict | None:
    url    = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 401:
            print("\n  ❌ Invalid API key. Check your key in weather.py")
            return None
        if response.status_code == 404:
            print(f"\n  ❌ City '{city}' not found. Try another name.")
            return None
        if response.status_code != 200:
            print(f"\n  ❌ API error: {response.status_code}")
            return None

        return response.json()

    except requests.exceptions.ConnectionError:
        print("\n  ❌ No internet connection. Check your network.")
        return None
    except requests.exceptions.Timeout:
        print("\n  ❌ Request timed out. Try again.")
        return None


def get_forecast(city: str) -> dict | None:
    url    = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException:
        return None


# ── Display ───────────────────────────────

def display_current(data: dict, unit: str):
    city       = data["name"]
    country    = data["sys"]["country"]
    temp_c     = kelvin_to_celsius(data["main"]["temp"])
    feels_c    = kelvin_to_celsius(data["main"]["feels_like"])
    temp_min_c = kelvin_to_celsius(data["main"]["temp_min"])
    temp_max_c = kelvin_to_celsius(data["main"]["temp_max"])
    humidity   = data["main"]["humidity"]
    desc       = data["weather"][0]["description"].title()
    wind_spd   = round(data["wind"]["speed"] * 3.6, 1)   # m/s → km/h
    wind_deg   = data["wind"].get("deg", 0)
    visibility = data.get("visibility", 0) // 1000        # m → km
    pressure   = data["main"]["pressure"]

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset  = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
    updated = datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M")

    print(f"\n  📍 {city}, {country}")
    print(f"  🕐 Last updated: {updated}")
    print_separator()
    print(f"  🌡️  Temperature : {format_temp(temp_c, unit)}")
    print(f"  🤔 Feels Like  : {format_temp(feels_c, unit)}")
    print(f"  ⬆️  High        : {format_temp(temp_max_c, unit)}")
    print(f"  ⬇️  Low         : {format_temp(temp_min_c, unit)}")
    print_separator()
    print(f"  ⛅ Condition   : {desc}")
    print(f"  💧 Humidity    : {humidity}%")
    print(f"  💨 Wind        : {wind_spd} km/h {wind_direction(wind_deg)}")
    print(f"  👁️  Visibility  : {visibility} km")
    print(f"  🔵 Pressure    : {pressure} hPa")
    print_separator()
    print(f"  🌅 Sunrise     : {sunrise}")
    print(f"  🌇 Sunset      : {sunset}")


def display_forecast(data: dict, unit: str):
    print(f"\n  📅 5-DAY FORECAST")
    print_separator()

    # Group by day (API returns every 3 hours)
    days: dict[str, list] = {}
    for entry in data["list"]:
        day = datetime.fromtimestamp(entry["dt"]).strftime("%A, %b %d")
        days.setdefault(day, []).append(entry)

    shown = 0
    for day, entries in days.items():
        if shown >= 5:
            break
        temps_c = [kelvin_to_celsius(e["main"]["temp"]) for e in entries]
        desc    = entries[len(entries)//2]["weather"][0]["description"].title()
        high    = format_temp(max(temps_c), unit)
        low     = format_temp(min(temps_c), unit)
        print(f"  {day:<20} ⬆️{high:>7}  ⬇️{low:>7}  {desc}")
        shown += 1


# ── Main Menu ─────────────────────────────

def main():
    history = load_history()
    unit    = "C"   # default Celsius

    print_banner()
    print("  Free weather data via OpenWeatherMap API")

    while True:
        print("\n  MENU")
        print_separator()
        print("  [1] Search city weather")
        print("  [2] 5-day forecast")
        print(f"  [3] Toggle units  (currently °{unit})")
        print("  [4] Search history")
        print("  [5] Quit")
        print_separator()

        choice = input("  Choice: ").strip()

        if choice == "1":
            city = input("\n  Enter city name: ").strip()
            if not city:
                print("  Please enter a city name.")
                continue
            data = get_current_weather(city)
            if data:
                display_current(data, unit)
                history = add_to_history(city, history)
                save_history(history)

        elif choice == "2":
            city = input("\n  Enter city name: ").strip()
            if not city:
                print("  Please enter a city name.")
                continue
            data = get_forecast(city)
            if data:
                display_forecast(data, unit)
                history = add_to_history(city, history)
                save_history(history)
            else:
                print("  ❌ Could not fetch forecast.")

        elif choice == "3":
            unit = "F" if unit == "C" else "C"
            print(f"\n  ✅ Units switched to °{unit}")

        elif choice == "4":
            show_history(history)

        elif choice == "5":
            print("\n  👋 Goodbye!\n")
            break

        else:
            print("  Invalid choice. Enter 1–5.")


if __name__ == "__main__":
    main()
