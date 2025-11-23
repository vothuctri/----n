#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý routing - tìm đường đi giữa 2 điểm
"""

import requests
from config import OSRM, USER_AGENT, API_TIMEOUT


def get_route_geometry(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Lấy hình học tuyến đường để vẽ bản đồ.
    
    Args:
        lon1, lat1: Tọa độ điểm bắt đầu
        lon2, lat2: Tọa độ điểm đích
        vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy)
        
    Returns:
        tuple: (geometry, distance_km, duration_hours)
    """
    r = requests.get(
        f"{OSRM}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}",
        params={"overview": "full", "geometries": "geojson"},
        headers=USER_AGENT,
        timeout=API_TIMEOUT
    )
    r.raise_for_status()
    data = r.json()
    route = data["routes"][0]
    
    return (
        route["geometry"],
        route["distance"] / 1000.0,
        route["duration"] / 3600.0
    )


def get_route_steps(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Lấy các bước chỉ dẫn chi tiết.
    
    Args:
        lon1, lat1: Tọa độ điểm bắt đầu
        lon2, lat2: Tọa độ điểm đích
        vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy)
        
    Returns:
        dict: Thông tin route với keys: distance_km, duration_min, steps
    """
    r = requests.get(
        f"{OSRM}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}",
        params={"overview": "false", "steps": "true"},
        headers=USER_AGENT,
        timeout=API_TIMEOUT
    )
    r.raise_for_status()
    data = r.json()
    route = data["routes"][0]
    
    steps = []
    for leg in route["legs"]:
        for step in leg["steps"]:
            steps.append({
                "instruction": step.get("maneuver", {}).get("instruction", "Tiếp tục đi"),
                "street_name": step.get("name", ""),
                "distance": step.get("distance", 0)
            })
    
    return {
        "distance_km": route["distance"] / 1000.0,
        "duration_min": route["duration"] / 60.0,
        "steps": steps
    }
