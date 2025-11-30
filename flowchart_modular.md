# Sơ Đồ Chương Trình Tìm Đường - Cấu Trúc Module

## Sơ đồ Kiến Trúc Module

```mermaid
flowchart TB
    subgraph "📦 Main Module"
        Main[main.py<br/>Điều phối chương trình]
    end
    
    subgraph "⚙️ Configuration"
        Config[config.py<br/>API keys, URLs, Constants]
    end
    
    subgraph "🔧 Core Modules"
        Geocoding[geocoding.py<br/>Chuyển địa chỉ → tọa độ]
        Routing[routing.py<br/>Tính toán tuyến đường]
        Weather[weather.py<br/>Lấy thông tin thời tiết]
        Mapping[mapping.py<br/>Vẽ bản đồ Folium]
        UI[ui.py<br/>Giao diện người dùng]
    end
    
    Main --> UI
    Main --> Routing
    Main --> Mapping
    
    UI --> Geocoding
    UI --> Weather
    
    Geocoding --> Config
    Routing --> Config
    Weather --> Config
    
    style Main fill:#4CAF50
    style Config fill:#2196F3
    style Geocoding fill:#FF9800
    style Routing fill:#FF9800
    style Weather fill:#FF9800
    style Mapping fill:#FF9800
    style UI fill:#FF9800
```

## Sơ đồ Tổng Quan Chương Trình Main

```mermaid
flowchart TD
    Start([🚀 BẮT ĐẦU MAIN]) --> Title[📢 In tiêu đề chương trình]
    Title --> GetLoc[🌍 get_user_locations<br/>từ ui.py]
    GetLoc --> CheckLoc{Lấy được<br/>địa chỉ?}
    CheckLoc -->|Không| Error[❌ In lỗi và kết thúc]
    CheckLoc -->|Có| Unpack[📍 Giải nén:<br/>lat1, lon1, name1<br/>lat2, lon2, name2]
    
    Unpack --> Choice[🚦 get_vehicle_choice<br/>từ ui.py]
    Choice --> Process{Xử lý<br/>theo lựa chọn}
    
    Process -->|driving| ShowCar[🚗 show_route_for_vehicle<br/>loại: driving]
    Process -->|bike| ShowBike[🏍️ show_route_for_vehicle<br/>loại: bike]
    Process -->|both| CompareBoth[🔄 compare_routes<br/>cả hai loại xe]
    
    ShowCar --> Done[✅ In HOÀN THÀNH]
    ShowBike --> Done
    CompareBoth --> Done
    Done --> End([🏁 KẾT THÚC])
    Error --> End
```

## Module: config.py

```mermaid
flowchart LR
    A[config.py] --> B[NOMINATIM_URL<br/>Geocoding API]
    A --> C[OSRM_URL<br/>Routing API]
    A --> D[OPENWEATHER_URL<br/>Weather API]
    A --> E[OPENWEATHER_API_KEY<br/>API Key]
    A --> F[USER_AGENT<br/>Request header]
    A --> G[TIMEOUT_GEOCODE<br/>15 giây]
    A --> H[TIMEOUT_ROUTING<br/>30 giây]
    
    style A fill:#2196F3,color:#fff
```

## Module: geocoding.py - Hàm geocode()

```mermaid
flowchart TD
    A([🔍 Bắt đầu geocode]) --> B[📥 Nhận địa chỉ address]
    B --> C[⏱️ time.sleep 1s<br/>tránh spam API]
    C --> D[📡 Gửi GET request<br/>đến NOMINATIM_URL]
    D --> E{📊 Có kết quả?}
    E -->|Không| F[❌ Raise ValueError<br/>Không tìm thấy địa chỉ]
    E -->|Có| G[📍 Lấy kết quả đầu tiên:<br/>lat, lon, display_name]
    G --> H([📤 Return lat, lon, name])
    F --> I([⛔ Kết thúc với lỗi])
    
    style A fill:#FF9800
    style H fill:#4CAF50
    style I fill:#F44336
```

## Module: routing.py - Hàm get_route_geometry()

```mermaid
flowchart TD
    A([🛣️ Bắt đầu get_route_geometry]) --> B[📥 Nhận:<br/>lon1, lat1<br/>lon2, lat2<br/>vehicle_type]
    B --> C[🔧 Xác định profile<br/>driving → driving-car<br/>bike → driving-bike]
    C --> D[📡 Gửi GET request<br/>OSRM với:<br/>overview=full<br/>geometries=geojson]
    D --> E[📊 Lấy route đầu tiên]
    E --> F[📐 Trích xuất:<br/>geometry coordinates<br/>distance mét<br/>duration giây]
    F --> G[🔄 Chuyển đổi:<br/>distance → km<br/>duration → giờ]
    G --> H([📤 Return<br/>geometry, km, hrs])
    
    style A fill:#FF9800
    style H fill:#4CAF50
```

## Module: routing.py - Hàm get_route_steps()

```mermaid
flowchart TD
    A([📍 Bắt đầu get_route_steps]) --> B[📥 Nhận tọa độ<br/>và vehicle_type]
    B --> C[🔧 Xác định profile<br/>driving/bike]
    C --> D[📡 Gửi request<br/>với steps=true]
    D --> E[📊 Nhận route data]
    E --> F[📐 Tính toán:<br/>km và phút]
    F --> G[🔢 Tạo dict result:<br/>distance_km, time_min,<br/>steps array]
    G --> H[🔄 Duyệt legs và steps]
    H --> I[📝 Lấy từng step:<br/>instruction<br/>street_name<br/>distance]
    I --> J[➕ Thêm vào steps array]
    J --> K{Còn<br/>steps?}
    K -->|Có| I
    K -->|Không| L([📤 Return result dict])
    
    style A fill:#FF9800
    style L fill:#4CAF50
```

## Module: weather.py - Hàm get_weather()

```mermaid
flowchart TD
    A([🌤️ Bắt đầu get_weather]) --> B[📥 Nhận lat, lon]
    B --> C[🔑 Kiểm tra<br/>OPENWEATHER_API_KEY]
    C --> D{API key<br/>hợp lệ?}
    D -->|Không| E[⚠️ Return None<br/>với warning message]
    D -->|Có| F[📡 Gửi request đến<br/>OpenWeatherMap API<br/>với units=metric]
    F --> G{Request<br/>thành công?}
    G -->|Không| H[❌ Return None<br/>với error message]
    G -->|Có| I[📊 Trích xuất dữ liệu:<br/>temp, feels_like<br/>humidity, description<br/>wind_speed]
    I --> J[🔄 Tạo weather dict]
    J --> K([📤 Return weather dict])
    E --> L([⛔ Kết thúc])
    H --> L
    
    style A fill:#FF9800
    style K fill:#4CAF50
    style L fill:#F44336
```

## Module: mapping.py - Hàm create_single_vehicle_map()

```mermaid
flowchart TD
    A([🗺️ Bắt đầu create_single_vehicle_map]) --> B[📥 Nhận:<br/>lat1, lon1, lat2, lon2<br/>name1, name2<br/>geometry, km, hrs<br/>vehicle_type, output_file]
    B --> C[📐 Tính điểm giữa:<br/>center_lat, center_lon]
    C --> D[🎨 Tạo bản đồ Folium<br/>tại center, zoom=11]
    D --> E[📍 Thêm Marker điểm đầu<br/>màu green, icon play]
    E --> F[📍 Thêm Marker điểm cuối<br/>màu red, icon stop]
    F --> G[🔄 Chuyển coordinates<br/>thành lat,lon format]
    G --> H{Loại xe?}
    H -->|driving| I[🎨 Màu xanh dương #0066CC]
    H -->|bike| J[🎨 Màu cam #FF6600]
    I --> K[🖊️ Vẽ PolyLine lên bản đồ]
    J --> K
    K --> L[💾 Lưu file HTML]
    L --> M([📤 Return output_file])
    
    style A fill:#FF9800
    style M fill:#4CAF50
```

## Module: mapping.py - Hàm create_comparison_map()

```mermaid
flowchart TD
    A([🔄 Bắt đầu create_comparison_map]) --> B[📥 Nhận:<br/>Tọa độ, tên địa điểm<br/>geom_car, km_car, hrs_car<br/>geom_bike, km_bike, hrs_bike]
    B --> C[📐 Tính điểm giữa]
    C --> D[🎨 Tạo bản đồ Folium]
    D --> E[📍 Thêm markers<br/>điểm đầu và cuối]
    E --> F[🚗 Vẽ PolyLine ô tô<br/>màu xanh #0066CC]
    F --> G[🏍️ Vẽ PolyLine xe máy<br/>màu đỏ #FF0000]
    G --> H[📊 Tạo HTML legend<br/>chú thích]
    H --> I[➕ Thêm legend vào bản đồ]
    I --> J[💾 Lưu route_comparison.html]
    J --> K[📊 Tính toán so sánh:<br/>diff_km, diff_min<br/>faster_vehicle]
    K --> L([📤 Return filename,<br/>comparison dict])
    
    style A fill:#FF9800
    style L fill:#4CAF50
```

## Module: ui.py - Hàm get_vehicle_choice()

```mermaid
flowchart TD
    A([🚦 Bắt đầu get_vehicle_choice]) --> B[📢 In tiêu đề MENU]
    B --> C[📋 In 3 lựa chọn:<br/>1. Ô tô<br/>2. Xe máy<br/>3. So sánh]
    C --> D[⌨️ Input từ người dùng]
    D --> E{Input<br/>hợp lệ?}
    E -->|1| F[📤 Return driving]
    E -->|2| G[📤 Return bike]
    E -->|3| H[📤 Return both]
    E -->|Không| I[⚠️ In lỗi:<br/>Lựa chọn không hợp lệ]
    I --> D
    
    style A fill:#FF9800
    style F fill:#4CAF50
    style G fill:#4CAF50
    style H fill:#4CAF50
```

## Module: ui.py - Hàm get_user_locations()

```mermaid
flowchart TD
    A([📍 Bắt đầu get_user_locations]) --> B[📢 In tiêu đề<br/>NHẬP ĐỊA CHỈ]
    B --> C[⌨️ Input địa chỉ bắt đầu]
    C --> D{Địa chỉ<br/>trống?}
    D -->|Có| E[📍 Dùng default:<br/>Hồ Chí Minh]
    D -->|Không| F[✅ Dùng địa chỉ nhập]
    E --> G[⌨️ Input địa chỉ đích]
    F --> G
    G --> H{Địa chỉ<br/>trống?}
    H -->|Có| I[📍 Dùng default:<br/>Hà Nội]
    H -->|Không| J[✅ Dùng địa chỉ nhập]
    I --> K[🔍 geocode địa chỉ 1]
    J --> K
    K --> L{Thành<br/>công?}
    L -->|Không| M[❌ Return None]
    L -->|Có| N[🔍 geocode địa chỉ 2]
    N --> O{Thành<br/>công?}
    O -->|Không| M
    O -->|Có| P[🌤️ get_weather cho địa chỉ 1]
    P --> Q[🌤️ get_weather cho địa chỉ 2]
    Q --> R[📊 display_weather cho cả 2]
    R --> S([📤 Return<br/>lat1, lon1, name1<br/>lat2, lon2, name2])
    M --> T([⛔ Kết thúc với None])
    
    style A fill:#FF9800
    style S fill:#4CAF50
    style T fill:#F44336
```

## Module: ui.py - Hàm display_weather()

```mermaid
flowchart TD
    A([🌤️ Bắt đầu display_weather]) --> B[📥 Nhận weather_data, location_name]
    B --> C{weather_data<br/>có dữ liệu?}
    C -->|Không| D[⚠️ In: Không có dữ liệu thời tiết]
    C -->|Có| E[📢 In tiêu đề với location_name]
    E --> F[🌡️ In nhiệt độ temp°C]
    F --> G[🤔 In cảm giác feels_like°C]
    G --> H[💧 In độ ẩm humidity%]
    H --> I[☁️ In mô tả description]
    I --> J[💨 In tốc độ gió wind_speed m/s]
    J --> K([✅ Kết thúc hiển thị])
    D --> K
    
    style A fill:#FF9800
    style K fill:#4CAF50
```

## Module: ui.py - Hàm display_route_steps()

```mermaid
flowchart TD
    A([📍 Bắt đầu display_route_steps]) --> B[📥 Nhận route_data, vehicle_type]
    B --> C[📊 Lấy distance_km, time_min]
    C --> D[📢 In tổng quan:<br/>khoảng cách, thời gian]
    D --> E[📝 In tiêu đề CHỈ DẪN]
    E --> F[🔢 step_num = 1]
    F --> G[🔄 Duyệt qua steps array]
    G --> H[📍 Lấy instruction, street, dist]
    H --> I{Có tên<br/>đường?}
    I -->|Có| J[📢 In: step_num. instruction<br/>vào street dist m]
    I -->|Không| K[📢 In: step_num. instruction<br/>dist m]
    J --> L[➕ step_num++]
    K --> L
    L --> M{Còn<br/>steps?}
    M -->|Có| G
    M -->|Không| N[🏁 In: Đã đến đích]
    N --> O([✅ Kết thúc])
    
    style A fill:#FF9800
    style O fill:#4CAF50
```

## Module: ui.py - Hàm display_comparison_result()

```mermaid
flowchart TD
    A([📊 Bắt đầu display_comparison_result]) --> B[📥 Nhận comparison dict]
    B --> C[📢 In tiêu đề<br/>KẾT QUẢ SO SÁNH]
    C --> D[📏 In chênh lệch km]
    D --> E[⏱️ In chênh lệch phút]
    E --> F{Ai nhanh<br/>hơn?}
    F -->|car| G[🚗 In: Ô tô nhanh hơn]
    F -->|bike| H[🏍️ In: Xe máy nhanh hơn]
    F -->|equal| I[⚖️ In: Cả hai giống nhau]
    G --> J([✅ Kết thúc])
    H --> J
    I --> J
    
    style A fill:#FF9800
    style J fill:#4CAF50
```

## Hàm show_route_for_vehicle() trong main.py

```mermaid
flowchart TD
    A([🚗 Bắt đầu show_route_for_vehicle]) --> B[📥 Nhận tọa độ, tên,<br/>vehicle_type]
    B --> C[📢 In tiêu đề loại xe]
    C --> D[📍 get_route_steps<br/>từ routing.py]
    D --> E[📊 display_route_steps<br/>từ ui.py]
    E --> F[📢 In tiêu đề VẼ BẢN ĐỒ]
    F --> G[🛣️ get_route_geometry<br/>từ routing.py]
    G --> H[📊 In thông tin km, phút]
    H --> I[🗺️ create_single_vehicle_map<br/>từ mapping.py]
    I --> J[✅ In đã lưu bản đồ]
    J --> K([🏁 Kết thúc])
    
    style A fill:#4CAF50
    style K fill:#4CAF50
```

## Hàm compare_routes() trong main.py

```mermaid
flowchart TD
    A([🔄 Bắt đầu compare_routes]) --> B[📥 Nhận tọa độ, tên]
    B --> C[📢 In tiêu đề SO SÁNH]
    C --> D[📍 get_route_steps cho ô tô]
    D --> E[📊 display_route_steps ô tô]
    E --> F[📍 get_route_steps cho xe máy]
    F --> G[📊 display_route_steps xe máy]
    G --> H[📢 In tiêu đề VẼ BẢN ĐỒ]
    H --> I[🛣️ get_route_geometry ô tô]
    I --> J[📊 In thông tin ô tô]
    J --> K[🛣️ get_route_geometry xe máy]
    K --> L[📊 In thông tin xe máy]
    L --> M[🗺️ create_comparison_map<br/>từ mapping.py]
    M --> N[✅ In đã lưu bản đồ]
    N --> O[📊 display_comparison_result<br/>từ ui.py]
    O --> P([🏁 Kết thúc])
    
    style A fill:#4CAF50
    style P fill:#4CAF50
```

## Sơ đồ Luồng Dữ Liệu

```mermaid
flowchart LR
    subgraph "Input"
        A[👤 Người dùng<br/>nhập địa chỉ]
    end
    
    subgraph "Processing"
        B[🔍 Geocoding<br/>địa chỉ → tọa độ]
        C[🛣️ Routing<br/>tính toán đường đi]
        D[🌤️ Weather<br/>lấy thời tiết]
        E[🗺️ Mapping<br/>vẽ bản đồ]
    end
    
    subgraph "Output"
        F[📊 Hiển thị<br/>chỉ dẫn]
        G[💾 File HTML<br/>bản đồ]
    end
    
    A --> B
    B --> C
    B --> D
    C --> E
    C --> F
    E --> G
    D --> F
    
    style A fill:#2196F3
    style B fill:#FF9800
    style C fill:#FF9800
    style D fill:#FF9800
    style E fill:#FF9800
    style F fill:#4CAF50
    style G fill:#4CAF50
```

## Bảng Chức Năng Modules

| Module | File | Chức năng chính | Dependencies |
|--------|------|-----------------|--------------|
| **Config** | `config.py` | Cấu hình API URLs, keys, timeouts | Không |
| **Geocoding** | `geocoding.py` | `geocode(address)` → lat, lon, name | config.py, requests |
| **Routing** | `routing.py` | `get_route_geometry()`, `get_route_steps()` | config.py, requests |
| **Weather** | `weather.py` | `get_weather(lat, lon)` → weather dict | config.py, requests |
| **Mapping** | `mapping.py` | `create_single_vehicle_map()`, `create_comparison_map()` | folium |
| **UI** | `ui.py` | `get_vehicle_choice()`, `get_user_locations()`, `display_*()` | geocoding.py, weather.py |
| **Main** | `main.py` | `main()`, `show_route_for_vehicle()`, `compare_routes()` | ui.py, routing.py, mapping.py |

## Bảng API Endpoints

| API | URL | Mục đích | Module sử dụng |
|-----|-----|----------|----------------|
| **Nominatim** | `https://nominatim.openstreetmap.org/search` | Geocoding (địa chỉ → tọa độ) | geocoding.py |
| **OSRM** | `https://router.project-osrm.org/route/v1/` | Routing (tính đường đi) | routing.py |
| **OpenWeather** | `https://api.openweathermap.org/data/2.5/weather` | Weather (thông tin thời tiết) | weather.py |

## Cấu Trúc File Output

```mermaid
graph LR
    A[Program] --> B[route_driving.html<br/>🚗 Bản đồ ô tô]
    A --> C[route_bike.html<br/>🏍️ Bản đồ xe máy]
    A --> D[route_comparison.html<br/>🔄 Bản đồ so sánh]
    
    style B fill:#0066CC,color:#fff
    style C fill:#FF6600,color:#fff
    style D fill:#9C27B0,color:#fff
```

## Ghi Chú Kỹ Thuật

### Ưu điểm của Cấu trúc Module:
1. **Separation of Concerns**: Mỗi module có trách nhiệm riêng
2. **Reusability**: Có thể tái sử dụng các hàm dễ dàng
3. **Maintainability**: Dễ bảo trì và sửa lỗi
4. **Testability**: Dễ viết unit test cho từng module
5. **Scalability**: Dễ mở rộng thêm tính năng mới

### Quy tắc Import:
- `main.py` import từ `ui`, `routing`, `mapping`
- `ui.py` import từ `geocoding`, `weather`
- `geocoding`, `routing`, `weather` import từ `config`
- Không có circular imports

### Error Handling:
- `geocode()`: Raise ValueError nếu không tìm thấy
- `get_weather()`: Return None nếu lỗi
- `get_user_locations()`: Return None nếu lỗi geocoding
- `main()`: Kiểm tra None trước khi xử lý
