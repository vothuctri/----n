#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module giao diện người dùng - xử lý input/output và hiển thị
"""

from geocoding import geocode
from weather import get_weather


def get_vehicle_choice():
    """
    Hỏi người dùng chọn loại phương tiện.
    
    Returns:
        str: "driving", "bike", hoặc "both"
    """
    print("\n" + "="*70)
    print("   🚦 CHỌN LOẠI PHƯƠNG TIỆN")
    print("="*70)
    print("1. 🚗 Ô tô")
    print("2. 🏍️ Xe máy")
    print("3. 🔄 So sánh cả hai")
    print("="*70)
    
    while True:
        choice = input("\nNhập lựa chọn của bạn (1/2/3): ").strip()
        if choice == "1":
            return "driving"
        elif choice == "2":
            return "bike"
        elif choice == "3":
            return "both"
        else:
            print("❌ Lựa chọn không hợp lệ! Vui lòng chọn 1, 2 hoặc 3.")


def get_user_locations():
    """
    Hỏi người dùng nhập địa chỉ bắt đầu và đích.
    
    Returns:
        tuple: (lat1, lon1, name1, lat2, lon2, name2) hoặc None nếu lỗi
    """
    print("\n" + "="*70)
    print("   📍 NHẬP ĐỊA CHỈ")
    print("="*70)
    
    # Nhập địa chỉ
    start_address = input("Địa chỉ bắt đầu: ").strip()
    if not start_address:
        start_address = "Dinh Thống Nhất, TPHCM, Việt Nam"
        print(f"  → Sử dụng mặc định: {start_address}")
    
    end_address = input("Địa chỉ đến: ").strip()
    if not end_address:
        end_address = "Sân bay Tân Sơn Nhất, TPHCM, Việt Nam"
        print(f"  → Sử dụng mặc định: {end_address}")
    
    # Lấy tọa độ
    print("\n🔍 Đang tìm kiếm địa chỉ...")
    try:
        lat1, lon1, name1 = geocode(start_address)
        print(f"  ✓ Điểm đầu: {name1}")
        display_weather(lat1, lon1, "điểm đầu")
        
        lat2, lon2, name2 = geocode(end_address)
        print(f"  ✓ Điểm đến: {name2}")
        display_weather(lat2, lon2, "điểm đến")
        
        return lat1, lon1, name1, lat2, lon2, name2
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None


def display_weather(lat, lon, location_label):
    """
    Hiển thị thông tin thời tiết.
    
    Args:
        lat, lon: Tọa độ
        location_label: Nhãn địa điểm (ví dụ: "điểm đầu")
    """
    weather = get_weather(lat, lon)
    
    if weather is None:
        print("  ⚠️  Chưa cấu hình API key thời tiết (xem WEATHER_SETUP.md)")
        return
    
    print(f"\n  🌤️  Thời tiết tại {location_label}:")
    print(f"     🌡️  Nhiệt độ: {weather['temp']:.1f}°C (cảm giác như {weather['feels_like']:.1f}°C)")
    print(f"     ☁️  Tình trạng: {weather['description'].capitalize()}")
    print(f"     💧 Độ ẩm: {weather['humidity']}%")
    print(f"     💨 Gió: {weather['wind_speed']:.1f} m/s")


def display_route_steps(route_data, vehicle_type):
    """
    Hiển thị chỉ dẫn đường đi chi tiết.
    
    Args:
        route_data: Dict từ get_route_steps()
        vehicle_type: "driving" hoặc "bike"
    """
    vehicle_name = "🚗 Ô TÔ" if vehicle_type == "driving" else "🏍️ XE MÁY"
    
    print(f"\n{'='*60}")
    print(f"   {vehicle_name} - CHỈ DẪN ĐƯỜNG ĐI")
    print(f"{'='*60}")
    print(f"📏 Quãng đường: {route_data['distance_km']:,.1f} km")
    print(f"⏱️  Thời gian ước tính: {route_data['duration_min']:,.0f} phút (~{route_data['duration_min']/60:.1f} giờ)")
    print(f"{'='*60}")
    print("\n📍 CHỈ DẪN CHI TIẾT:\n")
    
    for i, step in enumerate(route_data['steps'], 1):
        instruction = step['instruction']
        street_name = step['street_name']
        distance_m = step['distance']
        
        if street_name:
            print(f"  {i}. {instruction} vào {street_name} ({distance_m:,.0f} m)")
        else:
            print(f"  {i}. {instruction} ({distance_m:,.0f} m)")
    
    print(f"\n{'='*60}")
    print("✅ ĐÃ ĐẾN ĐÍCH!")
    print(f"{'='*60}\n")


def display_comparison_result(comparison):
    """
    Hiển thị kết quả so sánh giữa ô tô và xe máy.
    
    Args:
        comparison: Dict từ create_comparison_map()
    """
    print("\n" + "="*70)
    print("   📊 KẾT QUẢ SO SÁNH")
    print("="*70)
    print(f"🚗 Ô tô:    {comparison['car_km']:>8.1f} km  |  {comparison['car_min']:>6.0f} phút")
    print(f"🏍️ Xe máy:  {comparison['bike_km']:>8.1f} km  |  {comparison['bike_min']:>6.0f} phút")
    print(f"{'─'*70}")
    
    if comparison['shorter'] == 'car':
        print(f"✅ Ô tô ngắn hơn: {comparison['diff_km']:.1f} km ({comparison['diff_min']:.0f} phút)")
    elif comparison['shorter'] == 'bike':
        print(f"✅ Xe máy ngắn hơn: {comparison['diff_km']:.1f} km ({comparison['diff_min']:.0f} phút)")
    else:
        print(f"✅ Cả hai đi cùng đường!")
    print("="*70)
