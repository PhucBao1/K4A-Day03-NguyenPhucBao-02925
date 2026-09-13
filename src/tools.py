"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Trợ lý Du lịch Cá nhân hóa (Personal Travel Assistant).
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "search_travel_options",
        "description": "Tra cứu các chuyến bay và phòng khách sạn còn trống theo điểm đến và ngày đi.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Điểm đến cần tra cứu (ví dụ: 'Đà Nẵng')"
                },
                "date": {
                    "type": "string",
                    "description": "Ngày đi cần tra cứu, định dạng dd/mm/yyyy (ví dụ: '20/09/2026')"
                }
            },
            "required": ["destination", "date"]
        }
    },

    # --------------------------------------------------------------------------
    # HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'book_travel'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt vé máy bay / đặt phòng khách sạn cho chuyến đi.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - destination (string): Điểm đến của chuyến đi (ví dụ: 'Đà Nẵng')
    #    - date (string): Ngày đi, định dạng dd/mm/yyyy (ví dụ: '20/09/2026')
    #    - traveler_name (string): Tên hành khách cần đặt vé/phòng
    #    - flight_id (string, không bắt buộc): Mã chuyến bay muốn đặt (ví dụ: 'VN209')
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "book_travel",
        "description": "Đặt vé máy bay hoặc đặt phòng khách sạn cho một chuyến đi.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Điểm đến của chuyến đi (ví dụ: 'Đà Nẵng')"
                },
                "date": {
                    "type": "string",
                    "description": "Ngày đi, định dạng dd/mm/yyyy (ví dụ: '20/09/2026')"
                },
                "traveler_name": {
                    "type": "string",
                    "description": "Tên hành khách cần đặt vé/phòng"
                },
                "flight_id": {
                    "type": "string",
                    "description": "Mã chuyến bay muốn đặt, nếu người dùng chỉ định cụ thể (ví dụ: 'VN209')"
                }
            },
            "required": ["destination", "date", "traveler_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "Đà Nẵng": {
        "20/09/2026": {
            "flights": [
                {"flight_id": "VN209", "airline": "Vietnam Airlines", "departure_time": "08:00", "price_vnd": 1850000, "seats_available": 12}
            ],
            "hotels": [
                {"hotel_id": "DN-HL01", "name": "Danang Beach Resort", "price_per_night_vnd": 1200000, "rooms_available": 5}
            ]
        }
    },
    "Phú Quốc": {
        "25/09/2026": {
            "flights": [
                {"flight_id": "VJ501", "airline": "Vietjet Air", "departure_time": "10:30", "price_vnd": 2100000, "seats_available": 8}
            ],
            "hotels": [
                {"hotel_id": "PQ-HL02", "name": "Phu Quoc Ocean Villas", "price_per_night_vnd": 2500000, "rooms_available": 3}
            ]
        }
    }
}


def execute_search_travel_options(destination: str, date: str) -> str:
    """Thực thi tra cứu chuyến bay/khách sạn theo điểm đến và ngày đi"""
    options = MOCK_DATABASE.get(destination.strip(), {}).get(date.strip())
    if options:
        return json.dumps({
            "status": "SUCCESS",
            "destination": destination,
            "date": date,
            "data": options
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy chuyến bay/phòng khách sạn nào đi '{destination}' vào ngày '{date}'."
        }, ensure_ascii=False)


def execute_book_travel(destination: str, date: str, traveler_name: str, flight_id: str = None) -> str:
    """Thực thi đặt vé máy bay / đặt phòng khách sạn"""
    booking_ref = flight_id or destination[:2].upper()
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{booking_ref}-{date.replace('/', '')}",
        "destination": destination,
        "date": date,
        "traveler_name": traveler_name,
        "flight_id": flight_id,
        "message": (
            f"Đặt {'vé chuyến bay ' + flight_id if flight_id else 'vé/phòng'} thành công cho "
            f"hành khách {traveler_name} đi {destination} vào ngày {date}."
        )
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "search_travel_options": execute_search_travel_options,
    "book_travel": execute_book_travel
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
