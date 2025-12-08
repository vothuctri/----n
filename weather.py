#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý thời tiết - sử dụng wttr.in API (miễn phí, không cần API key)
"""

import requests


def get_weather(lat, lon):
    """
    Lấy thông tin thời tiết cho một địa điểm.
    
    Args:
        lat, lon: Tọa độ địa điểm
        
    Returns:
        dict: Thông tin thời tiết hoặc None nếu lỗi
    """
    try:
        url = f"https://wttr.in/{lat},{lon}?format=j1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Lấy thông tin thời tiết hiện tại
        current = data["current_condition"][0]
        
        return {
            "temp": float(current["temp_C"]),
            "feels_like": float(current["FeelsLikeC"]),
            "humidity": int(current["humidity"]),
            "description": current["weatherDesc"][0]["value"],
            "wind_speed": float(current["windspeedKmph"]) / 3.6  # Chuyển km/h sang m/s
        }
    except Exception:
        return None
