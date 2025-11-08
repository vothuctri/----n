#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
import folium
from urllib.parse import quote

# --- THÊM CÁC HẰNG SỐ BỊ THIẾU ---
NOMINATIM = "https://nominatim.openstreetmap.org"
OSRM = "https://router.project-osrm.org"
UA = {"User-Agent": "OSM-Demo-Combined/1.0 (contact: your_email@example.com)"}
# -----------------------------------

def geocode(q):
    """
    Chỉ giữ MỘT hàm geocode.
    Hàm này luôn trả về 3 giá trị (lat, lon, tên).
    """
    time.sleep(1.0)
    r = requests.get(f"{NOMINATIM}/search", params={"q": q, "format": "jsonv2", "limit": 1}, headers=UA)
    r.raise_for_status()
    j = r.json()
    if not j: raise ValueError(f"Không tìm thấy: {q}")
    return float(j[0]["lat"]), float(j[0]["lon"]), j[0].get("display_name", q)

def osrm_geom(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Hàm này lấy HÌNH HỌC (geometry) để VẼ BẢN ĐỒ.
    vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy/xe đạp)
    """
    r = requests.get(f"{OSRM}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}",
                     params={"overview":"full","geometries":"geojson"}, headers=UA, timeout=120)
    r.raise_for_status()
    data = r.json()
    route = data["routes"][0]
    return route["geometry"], route["distance"]/1000.0, route["duration"]/3600.0

def route_steps(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Hàm này lấy CHỈ DẪN (steps) để IN RA VĂN BẢN.
    vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy/xe đạp)
    """
    r = requests.get(f"{OSRM}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}",
                     params={"overview":"false","steps":"true"}, headers=UA, timeout=120)
    r.raise_for_status()
    data = r.json()
    route = data["routes"][0]
    dist_km = route["distance"]/1000.0
    dur_min = route["duration"]/60.0
    
    # Hiển thị loại phương tiện
    vehicle_name = "🚗 Ô TÔ" if vehicle_type == "driving" else "🏍️ XE MÁY"
    print(f"\n{'='*60}")
    print(f"   {vehicle_name} - CHỈ DẪN ĐƯỜNG ĐI")
    print(f"{'='*60}")
    print(f"📏 Quãng đường: {dist_km:,.1f} km")
    print(f"⏱️  Thời gian ước tính: {dur_min:,.0f} phút (~{dur_min/60:.1f} giờ)")
    print(f"{'='*60}")
    print("\n📍 CHỈ DẪN CHI TIẾT:\n")
    
    for leg in route["legs"]:
        for i, step in enumerate(leg["steps"]):
            # Sử dụng .get() để tránh KeyError
            instruction = step.get("maneuver", {}).get("instruction", "Tiếp tục đi")
            street_name = step.get("name", "")
            distance_m = step.get("distance", 0)
            if street_name:
                print(f"  {i+1}. {instruction} vào {street_name} ({distance_m:,.0f} m)")
            else:
                print(f"  {i+1}. {instruction} ({distance_m:,.0f} m)")
    
    print(f"\n{'='*60}")
    print("✅ ĐÃ ĐẾN ĐÍCH!")
    print(f"{'='*60}\n")

def get_vehicle_choice():
    """
    Hàm cho người dùng chọn loại phương tiện.
    Trả về: "driving" hoặc "bike" hoặc "both"
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
    Hàm lấy địa chỉ từ người dùng.
    Trả về: (lat1, lon1, name1, lat2, lon2, name2)
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
        
        lat2, lon2, name2 = geocode(end_address)
        print(f"  ✓ Điểm đến: {name2}")
        
        return lat1, lon1, name1, lat2, lon2, name2
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

def show_route_for_vehicle(lon1, lat1, lon2, lat2, name1, name2, vehicle_type):
    """
    Hàm hiển thị chỉ đường cho một loại phương tiện và vẽ bản đồ.
    """
    vehicle_name = "🚗 Ô TÔ" if vehicle_type == "driving" else "🏍️ XE MÁY"
    print("\n" + "="*70)
    print(f"   TÌM ĐƯỜNG CHO {vehicle_name}")
    print("="*70)
    route_steps(lon1, lat1, lon2, lat2, vehicle_type=vehicle_type)
    
    # Vẽ bản đồ cho loại xe này
    draw_single_vehicle_map(lon1, lat1, lon2, lat2, name1, name2, vehicle_type)

def compare_routes(lon1, lat1, lon2, lat2, name1, name2):
    """
    Hàm so sánh tuyến đường giữa ô tô và xe máy, và vẽ bản đồ.
    """
    print("\n" + "="*70)
    print("   🔄 SO SÁNH Ô TÔ VÀ XE MÁY")
    print("="*70)
    
    # Hiển thị chỉ đường cho ô tô
    print("\n" + "─"*70)
    print("   1️⃣ CHỈ ĐƯỜNG CHO Ô TÔ 🚗")
    print("─"*70)
    route_steps(lon1, lat1, lon2, lat2, vehicle_type="driving")
    
    # Hiển thị chỉ đường cho xe máy
    print("\n" + "─"*70)
    print("   2️⃣ CHỈ ĐƯỜNG CHO XE MÁY 🏍️")
    print("─"*70)
    route_steps(lon1, lat1, lon2, lat2, vehicle_type="bike")
    
    # Vẽ bản đồ so sánh
    draw_comparison_map(lon1, lat1, lon2, lat2, name1, name2)

def draw_single_vehicle_map(lon1, lat1, lon2, lat2, name1, name2, vehicle_type):
    """
    Hàm vẽ bản đồ cho một loại phương tiện.
    """
    vehicle_name = "Ô tô" if vehicle_type == "driving" else "Xe máy"
    vehicle_icon = "🚗" if vehicle_type == "driving" else "🏍️"
    
    print("\n" + "="*70)
    print(f"   🗺️ VẼ BẢN ĐỒ CHO {vehicle_icon} {vehicle_name.upper()}")
    print("="*70)
    
    # Lấy tuyến đường
    print(f"\n{vehicle_icon} Đang tính toán tuyến đường {vehicle_name}...")
    geom, km, hrs = osrm_geom(lon1, lat1, lon2, lat2, vehicle_type=vehicle_type)
    print(f"  ✓ {vehicle_name}: {km:,.1f} km, {hrs*60:.0f} phút")
    
    # Vẽ bản đồ
    print("\n🗺️ Đang vẽ bản đồ...")
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    
    # Tự động điều chỉnh zoom
    if km < 10:
        zoom = 13
    elif km < 50:
        zoom = 11
    elif km < 200:
        zoom = 9
    else:
        zoom = 7
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
    
    # Marker điểm đầu và cuối
    folium.Marker(
        [lat1, lon1], 
        popup=f"<b>Điểm đầu</b><br>{name1}", 
        tooltip="Bắt đầu",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [lat2, lon2], 
        popup=f"<b>Điểm cuối</b><br>{name2}", 
        tooltip="Kết thúc",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Vẽ tuyến đường
    color = 'blue' if vehicle_type == "driving" else 'orange'
    latlon = [(lat, lon) for lon, lat in geom["coordinates"]]
    folium.PolyLine(
        latlon, 
        color=color, 
        weight=5, 
        opacity=0.7,
        popup=f"<b>{vehicle_icon} {vehicle_name}</b><br>{km:,.1f} km<br>{hrs*60:.0f} phút"
    ).add_to(m)
    
    # Lưu file
    output_file = f"route_{vehicle_type}.html"
    m.save(output_file)
    print(f"  ✓ Đã lưu bản đồ: {output_file}")
    print("="*70)

def draw_comparison_map(lon1, lat1, lon2, lat2, name1, name2):
    """
    Hàm vẽ bản đồ so sánh giữa ô tô và xe máy.
    """
    print("\n" + "="*70)
    print("   🗺️ VẼ BẢN ĐỒ SO SÁNH")
    print("="*70)
    
    # Lấy tuyến đường cho ô tô
    print("\n🚗 Đang tính toán tuyến đường ô tô...")
    geom_car, km_car, hrs_car = osrm_geom(lon1, lat1, lon2, lat2, vehicle_type="driving")
    print(f"  ✓ Ô tô: {km_car:,.1f} km, {hrs_car*60:.0f} phút")
    
    # Lấy tuyến đường cho xe máy
    print("\n🏍️ Đang tính toán tuyến đường xe máy...")
    geom_bike, km_bike, hrs_bike = osrm_geom(lon1, lat1, lon2, lat2, vehicle_type="bike")
    print(f"  ✓ Xe máy: {km_bike:,.1f} km, {hrs_bike*60:.0f} phút")
    
    # Vẽ bản đồ
    print("\n🗺️ Đang vẽ bản đồ...")
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Marker điểm đầu và cuối
    folium.Marker(
        [lat1, lon1], 
        popup=f"<b>Điểm đầu</b><br>{name1}", 
        tooltip="Bắt đầu",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [lat2, lon2], 
        popup=f"<b>Điểm cuối</b><br>{name2}", 
        tooltip="Kết thúc",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Vẽ tuyến đường ô tô (màu xanh dương)
    latlon_car = [(lat, lon) for lon, lat in geom_car["coordinates"]]
    folium.PolyLine(
        latlon_car, 
        color='blue', 
        weight=5, 
        opacity=0.7,
        popup=f"<b>🚗 Ô tô</b><br>{km_car:,.1f} km<br>{hrs_car*60:.0f} phút"
    ).add_to(m)
    
    # Vẽ tuyến đường xe máy (màu đỏ)
    latlon_bike = [(lat, lon) for lon, lat in geom_bike["coordinates"]]
    folium.PolyLine(
        latlon_bike, 
        color='red', 
        weight=5, 
        opacity=0.7,
        popup=f"<b>🏍️ Xe máy</b><br>{km_bike:,.1f} km<br>{hrs_bike*60:.0f} phút"
    ).add_to(m)
    
    # Thêm chú thích
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Chú thích:</b></p>
    <p><span style="color:blue">━━━</span> Ô tô: {:.1f} km</p>
    <p><span style="color:red">━━━</span> Xe máy: {:.1f} km</p>
    </div>
    '''.format(km_car, km_bike)
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Lưu file
    output_file = "route_comparison.html"
    m.save(output_file)
    print(f"  ✓ Đã lưu bản đồ: {output_file}")
    
    # So sánh kết quả
    print("\n" + "="*70)
    print("   📊 KẾT QUẢ SO SÁNH")
    print("="*70)
    print(f"🚗 Ô tô:    {km_car:>8.1f} km  |  {hrs_car*60:>6.0f} phút")
    print(f"🏍️ Xe máy:  {km_bike:>8.1f} km  |  {hrs_bike*60:>6.0f} phút")
    print(f"{'─'*70}")
    diff_km = abs(km_car - km_bike)
    diff_min = abs(hrs_car*60 - hrs_bike*60)
    if km_car < km_bike:
        print(f"✅ Ô tô ngắn hơn: {diff_km:.1f} km ({diff_min:.0f} phút)")
    elif km_bike < km_car:
        print(f"✅ Xe máy ngắn hơn: {diff_km:.1f} km ({diff_min:.0f} phút)")
    else:
        print(f"✅ Cả hai đi cùng đường!")
    print("="*70)

if __name__ == "__main__":
    
    print("="*70)
    print("   🗺️  CHƯƠNG TRÌNH TÌM ĐƯỜNG ĐI NGẮN NHẤT")
    print("="*70)
    
    # Bước 1: Lấy địa chỉ từ người dùng
    locations = get_user_locations()
    if not locations:
        print("❌ Không thể lấy địa chỉ. Chương trình kết thúc.")
        exit(1)
    
    lat1, lon1, name1, lat2, lon2, name2 = locations
    
    # Bước 2: Cho người dùng chọn phương tiện
    choice = get_vehicle_choice()
    
    # Bước 3: Thực hiện theo lựa chọn
    if choice == "driving":
        show_route_for_vehicle(lon1, lat1, lon2, lat2, name1, name2, "driving")
    elif choice == "bike":
        show_route_for_vehicle(lon1, lat1, lon2, lat2, name1, name2, "bike")
    elif choice == "both":
        compare_routes(lon1, lat1, lon2, lat2, name1, name2)
    
    print("\n" + "="*70)
    print("   ✅ HOÀN THÀNH!")
    print("="*70)