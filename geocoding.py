#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý geocoding - tìm tọa độ từ địa chỉ
"""

import time
import requests
from config import NOMINATIM, USER_AGENT, GEOCODE_DELAY


def geocode(address):
    """
    Tìm tọa độ địa lý từ địa chỉ.
    
    Args:
        address (str): Địa chỉ cần tìm
        
    Returns:
        tuple: (lat, lon, name) - Tọa độ và tên đầy đủ
        
    Raises:
        ValueError: Nếu không tìm thấy địa chỉ
    """
    time.sleep(GEOCODE_DELAY)
    r = requests.get(
        f"{NOMINATIM}/search",
        params={"q": address, "format": "jsonv2", "limit": 1},
        headers=USER_AGENT
    )
    r.raise_for_status()
    j = r.json()
    
    if not j:
        raise ValueError(f"Không tìm thấy: {address}")
    
    return float(j[0]["lat"]), float(j[0]["lon"]), j[0].get("display_name", address)
