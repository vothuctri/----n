#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File cấu hình - chứa các hằng số và API keys
"""

# API Endpoints
NOMINATIM = "https://nominatim.openstreetmap.org"
OSRM = "https://router.project-osrm.org"
OPENWEATHER = "https://api.openweathermap.org/data/2.5/weather"

# API Keys
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"  # Thay bằng API key từ https://openweathermap.org/api

# Headers
USER_AGENT = {"User-Agent": "OSM-Demo-Combined/1.0 (contact: your_email@example.com)"}

# Timeouts
GEOCODE_DELAY = 1.0  # Giây
API_TIMEOUT = 120    # Giây
