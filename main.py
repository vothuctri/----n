#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH CHÍNH - Tìm đường đi ngắn nhất
Chạy file này để khởi động chương trình
"""

from ui import get_vehicle_choice, get_user_locations, display_route_steps, display_comparison_result
from routing import get_route_geometry, get_route_steps
from mapping import create_single_vehicle_map, create_comparison_map


def show_route_for_vehicle(lon1, lat1, lon2, lat2, name1, name2, vehicle_type):
    """
    Hiển thị chỉ đường và vẽ bản đồ cho một loại phương tiện.
    """
    vehicle_name = "🚗 Ô TÔ" if vehicle_type == "driving" else "🏍️ XE MÁY"
    print("\n" + "="*70)
    print(f"   TÌM ĐƯỜNG CHO {vehicle_name}")
    print("="*70)
    
    # Lấy và hiển thị chỉ dẫn
    route_data = get_route_steps(lon1, lat1, lon2, lat2, vehicle_type)
    display_route_steps(route_data, vehicle_type)
    
    # Vẽ bản đồ
    print("\n" + "="*70)
    print(f"   🗺️ VẼ BẢN ĐỒ CHO {vehicle_name}")
    print("="*70)
    
    vehicle_text = "Ô tô" if vehicle_type == "driving" else "Xe máy"
    vehicle_icon = "🚗" if vehicle_type == "driving" else "🏍️"
    
    print(f"\n{vehicle_icon} Đang tính toán tuyến đường {vehicle_text}...")
    geometry, km, hrs = get_route_geometry(lon1, lat1, lon2, lat2, vehicle_type)
    print(f"  ✓ {vehicle_text}: {km:,.1f} km, {hrs*60:.0f} phút")
    
    print("\n🗺️ Đang vẽ bản đồ...")
    output_file = f"route_{vehicle_type}.html"
    create_single_vehicle_map(
        lat1, lon1, lat2, lon2, name1, name2,
        geometry, km, hrs, vehicle_type, output_file
    )
    print(f"  ✓ Đã lưu bản đồ: {output_file}")
    print("="*70)


def compare_routes(lon1, lat1, lon2, lat2, name1, name2):
    """
    So sánh tuyến đường giữa ô tô và xe máy.
    """
    print("\n" + "="*70)
    print("   🔄 SO SÁNH Ô TÔ VÀ XE MÁY")
    print("="*70)
    
    # Hiển thị chỉ đường cho ô tô
    print("\n" + "─"*70)
    print("   1️⃣ CHỈ ĐƯỜNG CHO Ô TÔ 🚗")
    print("─"*70)
    route_car = get_route_steps(lon1, lat1, lon2, lat2, "driving")
    display_route_steps(route_car, "driving")
    
    # Hiển thị chỉ đường cho xe máy
    print("\n" + "─"*70)
    print("   2️⃣ CHỈ ĐƯỜNG CHO XE MÁY 🏍️")
    print("─"*70)
    route_bike = get_route_steps(lon1, lat1, lon2, lat2, "bike")
    display_route_steps(route_bike, "bike")
    
    # Vẽ bản đồ so sánh
    print("\n" + "="*70)
    print("   🗺️ VẼ BẢN ĐỒ SO SÁNH")
    print("="*70)
    
    print("\n🚗 Đang tính toán tuyến đường ô tô...")
    geom_car, km_car, hrs_car = get_route_geometry(lon1, lat1, lon2, lat2, "driving")
    print(f"  ✓ Ô tô: {km_car:,.1f} km, {hrs_car*60:.0f} phút")
    
    print("\n🏍️ Đang tính toán tuyến đường xe máy...")
    geom_bike, km_bike, hrs_bike = get_route_geometry(lon1, lat1, lon2, lat2, "bike")
    print(f"  ✓ Xe máy: {km_bike:,.1f} km, {hrs_bike*60:.0f} phút")
    
    print("\n🗺️ Đang vẽ bản đồ...")
    output_file, comparison = create_comparison_map(
        lat1, lon1, lat2, lon2, name1, name2,
        geom_car, km_car, hrs_car,
        geom_bike, km_bike, hrs_bike
    )
    print(f"  ✓ Đã lưu bản đồ: {output_file}")
    
    # Hiển thị kết quả so sánh
    display_comparison_result(comparison)


def main():
    """
    Hàm chính của chương trình.
    """
    print("="*70)
    print("   🗺️  CHƯƠNG TRÌNH TÌM ĐƯỜNG ĐI NGẮN NHẤT")
    print("="*70)
    
    # Bước 1: Lấy địa chỉ từ người dùng
    locations = get_user_locations()
    if not locations:
        print("❌ Không thể lấy địa chỉ. Chương trình kết thúc.")
        return
    
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


if __name__ == "__main__":
    main()
