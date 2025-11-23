#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý thời tiết - lấy thông tin thời tiết từ OpenWeatherMap
"""

import requests
from config import OPENWEATHER, OPENWEATHER_API_KEY


def get_weather(lat, lon):
    """
    Lấy thông tin thời tiết cho một địa điểm.
    
    Args:
        lat, lon: Tọa độ địa điểm
        
    Returns:
        dict: Thông tin thời tiết hoặc None nếu lỗi
    """
    # Nếu chưa có API key, bỏ qua
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return None
    
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",  # Celsius
            "lang": "vi"  # Tiếng Việt
        }
        r = requests.get(OPENWEATHER, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        return {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    except (requests.exceptions.RequestException, KeyError, IndexError):
        return None
