# Sơ đồ Chương Trình Tìm Đường Đi Ngắn Nhất

## Sơ đồ Tổng Quan Chương Trình

```mermaid
flowchart TD
    Start([🚀 BẮT ĐẦU]) --> Input[📍 Nhập địa chỉ bắt đầu và đích]
    Input --> Geocode[🔍 Tìm tọa độ địa lý<br/>geocode]
    Geocode --> Choice{🚦 Chọn loại<br/>phương tiện?}
    
    Choice -->|1. Ô tô| Car[🚗 Tìm đường cho ô tô]
    Choice -->|2. Xe máy| Bike[🏍️ Tìm đường cho xe máy]
    Choice -->|3. So sánh| Compare[🔄 So sánh cả hai]
    
    Car --> ShowCar[Hiển thị chỉ dẫn ô tô]
    ShowCar --> MapCar[🗺️ Vẽ bản đồ ô tô]
    
    Bike --> ShowBike[Hiển thị chỉ dẫn xe máy]
    ShowBike --> MapBike[🗺️ Vẽ bản đồ xe máy]
    
    Compare --> ShowBoth[Hiển thị cả 2 chỉ dẫn]
    ShowBoth --> MapCompare[🗺️ Vẽ bản đồ so sánh]
    
    MapCar --> End([✅ KẾT THÚC])
    MapBike --> End
    MapCompare --> End
```

## Sơ đồ Chi Tiết Hàm geocode()

```mermaid
flowchart TD
    A([Bắt đầu geocode]) --> B[Nhận địa chỉ q]
    B --> C[Chờ 1 giây<br/>time.sleep]
    C --> D[Gửi request đến<br/>Nominatim API]
    D --> E{Tìm thấy<br/>kết quả?}
    E -->|Không| F[❌ Raise ValueError]
    E -->|Có| G[Lấy lat, lon, name<br/>từ kết quả đầu tiên]
    G --> H([Trả về lat, lon, name])
    F --> I([Kết thúc với lỗi])
```

## Sơ đồ Chi Tiết Hàm route_steps()

```mermaid
flowchart TD
    A([Bắt đầu route_steps]) --> B[Nhận tọa độ và<br/>loại phương tiện]
    B --> C[Gửi request đến<br/>OSRM API với steps=true]
    C --> D[Nhận dữ liệu route]
    D --> E[Tính khoảng cách km<br/>và thời gian phút]
    E --> F[In tiêu đề và tổng quan]
    F --> G[Duyệt qua từng leg]
    G --> H[Duyệt qua từng step]
    H --> I[Lấy instruction,<br/>street_name, distance]
    I --> J{Có tên<br/>đường?}
    J -->|Có| K[In: instruction vào street_name]
    J -->|Không| L[In: instruction]
    K --> M{Còn step<br/>khác?}
    L --> M
    M -->|Có| H
    M -->|Không| N[In thông báo đến đích]
    N --> O([Kết thúc])
```

## Sơ đồ Chi Tiết Hàm osrm_geom()

```mermaid
flowchart TD
    A([Bắt đầu osrm_geom]) --> B[Nhận tọa độ và<br/>loại phương tiện]
    B --> C[Gửi request đến OSRM<br/>với overview=full,<br/>geometries=geojson]
    C --> D[Nhận dữ liệu routes]
    D --> E[Lấy route đầu tiên]
    E --> F[Trích xuất:<br/>- geometry hình học<br/>- distance khoảng cách<br/>- duration thời gian]
    F --> G[Chuyển đổi:<br/>distance → km<br/>duration → giờ]
    G --> H([Trả về geometry,<br/>km, giờ])
```

## Sơ đồ Vẽ Bản Đồ Đơn (draw_single_vehicle_map)

```mermaid
flowchart TD
    A([Bắt đầu vẽ bản đồ]) --> B[Nhận tọa độ, tên địa điểm,<br/>loại phương tiện]
    B --> C[Gọi osrm_geom<br/>để lấy tuyến đường]
    C --> D[Tính toán:<br/>- Điểm giữa center<br/>- Mức zoom phù hợp]
    D --> E[Tạo bản đồ Folium<br/>tại center]
    E --> F[Thêm Marker điểm đầu<br/>màu xanh, icon play]
    F --> G[Thêm Marker điểm cuối<br/>màu đỏ, icon stop]
    G --> H[Chuyển đổi<br/>coordinates thành latlon]
    H --> I[Vẽ PolyLine<br/>màu xanh/cam theo loại xe]
    I --> J{Loại xe?}
    J -->|Ô tô| K[Lưu route_driving.html]
    J -->|Xe máy| L[Lưu route_bike.html]
    K --> M([Kết thúc])
    L --> M
```

## Sơ đồ Vẽ Bản Đồ So Sánh (draw_comparison_map)

```mermaid
flowchart TD
    A([Bắt đầu so sánh]) --> B[Gọi osrm_geom<br/>cho ô tô]
    B --> C[Gọi osrm_geom<br/>cho xe máy]
    C --> D[Tạo bản đồ Folium]
    D --> E[Thêm markers<br/>điểm đầu và cuối]
    E --> F[Vẽ PolyLine ô tô<br/>màu xanh dương]
    F --> G[Vẽ PolyLine xe máy<br/>màu đỏ]
    G --> H[Thêm legend<br/>chú thích]
    H --> I[Lưu route_comparison.html]
    I --> J[So sánh khoảng cách<br/>và thời gian]
    J --> K{Xe nào<br/>ngắn hơn?}
    K -->|Ô tô| L[In: Ô tô ngắn hơn]
    K -->|Xe máy| M[In: Xe máy ngắn hơn]
    K -->|Bằng nhau| N[In: Cả hai giống nhau]
    L --> O([Kết thúc])
    M --> O
    N --> O
```

## Sơ đồ Luồng Chính (Main Flow)

```mermaid
flowchart TD
    Start([🚀 MAIN START]) --> Title[In tiêu đề chương trình]
    Title --> GetLoc[Gọi get_user_locations]
    
    GetLoc --> InputStart[Nhập địa chỉ bắt đầu]
    InputStart --> CheckStart{Địa chỉ<br/>trống?}
    CheckStart -->|Có| DefaultStart[Dùng địa chỉ mặc định]
    CheckStart -->|Không| UseStart[Dùng địa chỉ nhập]
    
    DefaultStart --> InputEnd[Nhập địa chỉ đến]
    UseStart --> InputEnd
    
    InputEnd --> CheckEnd{Địa chỉ<br/>trống?}
    CheckEnd -->|Có| DefaultEnd[Dùng địa chỉ mặc định]
    CheckEnd -->|Không| UseEnd[Dùng địa chỉ nhập]
    
    DefaultEnd --> Geo1[geocode địa chỉ 1]
    UseEnd --> Geo1
    
    Geo1 --> Geo2[geocode địa chỉ 2]
    Geo2 --> GetChoice[Gọi get_vehicle_choice]
    
    GetChoice --> Menu[Hiển thị menu 1/2/3]
    Menu --> WaitInput[Chờ người dùng nhập]
    WaitInput --> ValidInput{Input<br/>hợp lệ?}
    ValidInput -->|Không| Error[In thông báo lỗi]
    Error --> WaitInput
    ValidInput -->|Có| Process{Xử lý<br/>theo choice}
    
    Process -->|1| Driving[show_route_for_vehicle<br/>driving]
    Process -->|2| Biking[show_route_for_vehicle<br/>bike]
    Process -->|3| Both[compare_routes]
    
    Driving --> MapD[draw_single_vehicle_map<br/>driving]
    Biking --> MapB[draw_single_vehicle_map<br/>bike]
    Both --> Steps1[route_steps ô tô]
    Steps1 --> Steps2[route_steps xe máy]
    Steps2 --> MapC[draw_comparison_map]
    
    MapD --> Done[In hoàn thành]
    MapB --> Done
    MapC --> Done
    Done --> End([✅ END])
```

## Sơ đồ Cấu Trúc Dữ Liệu

```mermaid
graph TB
    subgraph "API Response - OSRM"
        OSRM[OSRM Response]
        OSRM --> Routes[routes array]
        Routes --> Route0[routes 0]
        Route0 --> Geometry[geometry<br/>LineString GeoJSON]
        Route0 --> Distance[distance mét]
        Route0 --> Duration[duration giây]
        Route0 --> Legs[legs array]
        Legs --> Steps[steps array]
        Steps --> Maneuver[maneuver object]
        Maneuver --> Instruction[instruction string]
        Steps --> Name[name string]
        Steps --> Dist[distance number]
    end
    
    subgraph "API Response - Nominatim"
        Nom[Nominatim Response]
        Nom --> Lat[lat number]
        Nom --> Lon[lon number]
        Nom --> Display[display_name string]
    end
```

## Ghi Chú

### Các API Sử Dụng:
- **Nominatim**: `https://nominatim.openstreetmap.org` - Geocoding
- **OSRM**: `https://router.project-osrm.org` - Routing

### Các Loại Phương Tiện:
- `driving`: Ô tô (đường ô tô, cao tốc)
- `bike`: Xe máy/xe đạp (có thể đi đường hẹp)

### Các File Output:
- `route_driving.html`: Bản đồ ô tô
- `route_bike.html`: Bản đồ xe máy
- `route_comparison.html`: Bản đồ so sánh

### Các Hàm Chính:

| Hàm | Mô tả | Input | Output |
|-----|-------|-------|--------|
| `geocode(q)` | Tìm tọa độ từ địa chỉ | Địa chỉ (string) | lat, lon, name |
| `osrm_geom()` | Lấy hình học tuyến đường | Tọa độ, loại xe | geometry, km, giờ |
| `route_steps()` | Hiển thị chỉ dẫn chi tiết | Tọa độ, loại xe | None (in ra) |
| `get_vehicle_choice()` | Menu chọn xe | None | "driving"/"bike"/"both" |
| `get_user_locations()` | Nhập địa chỉ | None | lat1, lon1, name1, lat2, lon2, name2 |
| `show_route_for_vehicle()` | Hiển thị và vẽ cho 1 xe | Tọa độ, tên, loại xe | None |
| `compare_routes()` | So sánh 2 loại xe | Tọa độ, tên | None |
| `draw_single_vehicle_map()` | Vẽ bản đồ 1 xe | Tọa độ, tên, loại xe | File HTML |
| `draw_comparison_map()` | Vẽ bản đồ so sánh | Tọa độ, tên | File HTML |
