"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any
from datetime import datetime, timedelta

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "check_room_availability",
        "description": (
            "Kiểm tra danh sách các phòng họp phù hợp và còn trống "
            "trong khoảng thời gian yêu cầu, dựa trên sức chứa."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu sử dụng phòng, "
                        "format 'YYYY-MM-DD HH:MM', ví dụ '2026-09-15 14:00'"
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc sử dụng phòng, "
                        "format 'YYYY-MM-DD HH:MM', ví dụ '2026-09-15 16:00'"
                    )
                },
                "capacity": {
                    "type": "integer",
                    "description": "Số lượng người tham dự cuộc họp"
                }
            },
            "required": [
                "start_time",
                "end_time",
                "capacity"
            ]
        }
    },

    {
        "name": "check_equipment_availability",
        "description": (
            "Kiểm tra số lượng thiết bị còn khả dụng "
            "trong khoảng thời gian yêu cầu."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "equipment_type": {
                    "type": "string",
                    "description": (
                        "Loại thiết bị cần mượn, "
                        "ví dụ: 'projector', 'microphone', 'tv'"
                    )
                },
                "quantity": {
                    "type": "integer",
                    "description": "Số lượng thiết bị cần mượn"
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu sử dụng thiết bị, "
                        "format 'YYYY-MM-DD HH:MM', "
                        "ví dụ '2026-09-15 14:00'"
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc sử dụng thiết bị, "
                        "format 'YYYY-MM-DD HH:MM', "
                        "ví dụ '2026-09-15 16:00'"
                    )
                }
            },
            "required": [
                "equipment_type",
                "quantity",
                "start_time",
                "end_time"
            ]
        }
    },

    {
        "name": "book_meeting_room",
        "description": (
            "Tạo booking cho một phòng họp đã được xác nhận còn trống. "
            "Tool sẽ kiểm tra lại conflict trước khi tạo booking."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "room_name": {
                    "type": "string",
                    "description": "Tên hoặc mã phòng họp cần đặt"
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu cuộc họp, "
                        "format 'YYYY-MM-DD HH:MM'"
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc cuộc họp, "
                        "format 'YYYY-MM-DD HH:MM'"
                    )
                },
                "organizer": {
                    "type": "string",
                    "description": "Tên người đặt phòng"
                }
            },
            "required": [
                "room_name",
                "start_time",
                "end_time",
                "organizer"
            ]
        }
    },

    {
        "name": "book_equipment",
        "description": (
            "Tạo yêu cầu mượn hoặc đặt thiết bị đã được xác nhận còn khả dụng. "
            "Tool sẽ kiểm tra lại số lượng và conflict thời gian trước khi booking."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "equipment_type": {
                    "type": "string",
                    "description": (
                        "Loại thiết bị cần mượn, "
                        "ví dụ: 'projector', 'microphone', 'tv'"
                    )
                },
                "quantity": {
                    "type": "integer",
                    "description": "Số lượng thiết bị cần mượn"
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu sử dụng thiết bị, "
                        "format 'YYYY-MM-DD HH:MM'"
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc sử dụng thiết bị, "
                        "format 'YYYY-MM-DD HH:MM'"
                    )
                },
                "borrower": {
                    "type": "string",
                    "description": "Tên người mượn thiết bị"
                }
            },
            "required": [
                "equipment_type",
                "quantity",
                "start_time",
                "end_time",
                "borrower"
            ]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    # ==============================================================
    # ROOMS
    # ==============================================================
    "rooms": {
        "ROOM_A101": {
            "name": "Phòng A101",
            "capacity": 10,
            "location": "Tòa A - Tầng 1",
            "equipment": [
                "projector",
                "whiteboard"
            ]
        },

        "ROOM_A102": {
            "name": "Phòng A102",
            "capacity": 20,
            "location": "Tòa A - Tầng 1",
            "equipment": [
                "projector",
                "microphone",
                "whiteboard"
            ]
        },

        "ROOM_B201": {
            "name": "Phòng B201",
            "capacity": 30,
            "location": "Tòa B - Tầng 2",
            "equipment": [
                "projector",
                "microphone",
                "tv",
                "whiteboard"
            ]
        },

        "ROOM_B202": {
            "name": "Phòng B202",
            "capacity": 8,
            "location": "Tòa B - Tầng 2",
            "equipment": [
                "tv",
                "whiteboard"
            ]
        }
    },

    # ==============================================================
    # EQUIPMENT
    # ==============================================================
    "equipment": {
        "projector": {
            "name": "Máy chiếu",
            "total_quantity": 3
        },

        "microphone": {
            "name": "Micro không dây",
            "total_quantity": 5
        },

        "tv": {
            "name": "TV màn hình lớn",
            "total_quantity": 2
        },

        "whiteboard": {
            "name": "Bảng trắng",
            "total_quantity": 4
        }
    },

    # ==============================================================
    # ROOM BOOKINGS
    # ==============================================================
    "room_bookings": [
        {
            "booking_id": "RB001",
            "room_name": "ROOM_A101",
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00",
            "organizer": "Nguyễn Văn An"
        },

        {
            "booking_id": "RB002",
            "room_name": "ROOM_A102",
            "start_time": "2026-09-15 09:00",
            "end_time": "2026-09-15 11:00",
            "organizer": "Trần Thị Bình"
        }
    ],

    # ==============================================================
    # EQUIPMENT BOOKINGS
    # ==============================================================
    "equipment_bookings": [
        {
            "booking_id": "EB001",
            "equipment_type": "projector",
            "quantity": 1,
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00",
            "borrower": "Nguyễn Văn An"
        },

        {
            "booking_id": "EB002",
            "equipment_type": "microphone",
            "quantity": 2,
            "start_time": "2026-09-15 09:00",
            "end_time": "2026-09-15 11:00",
            "borrower": "Trần Thị Bình"
        }
    ]
}

# =====================================
# HELPERS
# =====================================

DATETIME_FORMAT = "%Y-%m-%d %H:%M"

def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)

def validate_time_range(start_time: str, end_time: str):
    start, end = parse_datetime(start_time), parse_datetime(end_time)
    if start >= end:
        raise ValueError("start_time phải nhỏ hơn end_time.")
    return start, end

def is_time_overlap(existing_start: datetime, existing_end: datetime, new_start: datetime, new_end: datetime) -> bool:
    return existing_start < new_end and existing_end > new_start

def execute_check_room_availability(start_time: str, end_time: str, capacity: int) -> str:
    try:
        new_start, new_end = validate_time_range(start_time, end_time)
        if capacity <= 0: raise ValueError("capacity phải lớn hơn 0.")
    except ValueError as e:
        return json.dumps({"status": "INVALID_ARGUMENT", "message": str(e)}, ensure_ascii=False)

    available_rooms = []
    for room_id, room in MOCK_DATABASE["rooms"].items():
        if room["capacity"] < capacity: continue
        is_booked = False
        for booking in MOCK_DATABASE["room_bookings"]:
            if booking["room_name"] != room_id: continue
            existing_start = parse_datetime(booking["start_time"])
            existing_end = parse_datetime(booking["end_time"])
            if is_time_overlap(existing_start, existing_end, new_start, new_end):
                is_booked = True
                break
        if not is_booked: available_rooms.append({"room_id": room_id, **room})

    if not available_rooms:
        return json.dumps({"status": "UNAVAILABLE", "message": f"Không có phòng phù hợp cho {capacity} người từ {start_time} đến {end_time}."}, ensure_ascii=False)

    return json.dumps({"status": "SUCCESS", "start_time": start_time, "end_time": end_time, "capacity": capacity, "available_rooms": available_rooms}, ensure_ascii=False)

def execute_check_equipment_availability(equipment_type: str, quantity: int, start_time: str, end_time: str) -> str:
    equipment_type = equipment_type.strip().lower()
    try:
        new_start, new_end = validate_time_range(start_time, end_time)
        if quantity <= 0: raise ValueError("quantity phải lớn hơn 0.")
    except ValueError as e:
        return json.dumps({"status": "INVALID_ARGUMENT", "message": str(e)}, ensure_ascii=False)

    equipment = MOCK_DATABASE["equipment"].get(equipment_type)
    if not equipment:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy thiết bị '{equipment_type}'."}, ensure_ascii=False)

    events = []
    for booking in MOCK_DATABASE["equipment_bookings"]:
        if booking["equipment_type"] != equipment_type: continue
        existing_start = parse_datetime(booking["start_time"])
        existing_end = parse_datetime(booking["end_time"])
        if not is_time_overlap(existing_start, existing_end, new_start, new_end): continue
        overlap_start, overlap_end = max(existing_start, new_start), min(existing_end, new_end)
        events.extend([(overlap_start, booking["quantity"]), (overlap_end, -booking["quantity"])])

    events.sort(key=lambda x: (x[0], 0 if x[1] < 0 else 1))
    current_booked, max_booked = 0, 0
    for _, delta in events:
        current_booked += delta
        max_booked = max(max_booked, current_booked)

    available_quantity = equipment["total_quantity"] - max_booked
    if available_quantity < quantity:
        return json.dumps({"status": "UNAVAILABLE", "equipment_type": equipment_type, "requested_quantity": quantity, "available_quantity": max(0, available_quantity), "start_time": start_time, "end_time": end_time, "message": f"Không đủ {equipment['name']} trong khoảng thời gian yêu cầu."}, ensure_ascii=False)

    return json.dumps({"status": "SUCCESS", "equipment_type": equipment_type, "requested_quantity": quantity, "available_quantity": available_quantity, "start_time": start_time, "end_time": end_time}, ensure_ascii=False)

def execute_book_meeting_room(room_name: str, start_time: str, end_time: str, organizer: str) -> str:
    try:
        new_start, new_end = validate_time_range(start_time, end_time)
    except ValueError as e:
        return json.dumps({"status": "INVALID_ARGUMENT", "message": str(e)}, ensure_ascii=False)

    if room_name not in MOCK_DATABASE["rooms"]:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy phòng '{room_name}'."}, ensure_ascii=False)

    for booking in MOCK_DATABASE["room_bookings"]:
        if booking["room_name"] != room_name: continue
        existing_start = parse_datetime(booking["start_time"])
        existing_end = parse_datetime(booking["end_time"])
        if is_time_overlap(existing_start, existing_end, new_start, new_end):
            return json.dumps({"status": "CONFLICT", "message": f"Phòng {room_name} đã được đặt trong khoảng thời gian này.", "conflict_booking": booking}, ensure_ascii=False)

    booking_id = f"RB-{len(MOCK_DATABASE['room_bookings']) + 1:03d}"
    new_booking = {"booking_id": booking_id, "room_name": room_name, "start_time": start_time, "end_time": end_time, "organizer": organizer}
    MOCK_DATABASE["room_bookings"].append(new_booking)

    return json.dumps({"status": "SUCCESS", "message": "Đặt phòng thành công.", "booking": new_booking}, ensure_ascii=False)

def execute_book_equipment(equipment_type: str, quantity: int, start_time: str, end_time: str, borrower: str) -> str:
    equipment_type = equipment_type.strip().lower()
    try:
        new_start, new_end = validate_time_range(start_time, end_time)
        if quantity <= 0: raise ValueError("quantity phải lớn hơn 0.")
    except ValueError as e:
        return json.dumps({"status": "INVALID_ARGUMENT", "message": str(e)}, ensure_ascii=False)

    equipment = MOCK_DATABASE["equipment"].get(equipment_type)
    if not equipment:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy thiết bị '{equipment_type}'."}, ensure_ascii=False)

    events = []
    for booking in MOCK_DATABASE["equipment_bookings"]:
        if booking["equipment_type"] != equipment_type: continue
        existing_start = parse_datetime(booking["start_time"])
        existing_end = parse_datetime(booking["end_time"])
        if not is_time_overlap(existing_start, existing_end, new_start, new_end): continue
        overlap_start, overlap_end = max(existing_start, new_start), min(existing_end, new_end)
        events.extend([(overlap_start, booking["quantity"]), (overlap_end, -booking["quantity"])])

    events.sort(key=lambda x: (x[0], 0 if x[1] < 0 else 1))
    current_booked, max_booked = 0, 0
    for _, delta in events:
        current_booked += delta
        max_booked = max(max_booked, current_booked)

    available_quantity = equipment["total_quantity"] - max_booked
    if available_quantity < quantity:
        return json.dumps({"status": "CONFLICT", "message": f"Không đủ {equipment['name']} để đặt {quantity} cái.", "requested_quantity": quantity, "available_quantity": max(0, available_quantity)}, ensure_ascii=False)

    booking_id = f"EB-{len(MOCK_DATABASE['equipment_bookings']) + 1:03d}"
    new_booking = {"booking_id": booking_id, "equipment_type": equipment_type, "quantity": quantity, "start_time": start_time, "end_time": end_time, "borrower": borrower}
    MOCK_DATABASE["equipment_bookings"].append(new_booking)

    return json.dumps({"status": "SUCCESS", "message": "Đặt thiết bị thành công.", "booking": new_booking}, ensure_ascii=False)

TOOL_ROUTER = {
    "check_room_availability": execute_check_room_availability,
    "check_equipment_availability": execute_check_equipment_availability,
    "book_meeting_room": execute_book_meeting_room,
    "book_equipment": execute_book_equipment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    if tool_name not in TOOL_ROUTER:
        return json.dumps({"status": "UNKNOWN_TOOL", "message": f"Tool '{tool_name}' không tồn tại."}, ensure_ascii=False)
    try:
        return TOOL_ROUTER[tool_name](**arguments)
    except TypeError as e:
        return json.dumps({"status": "INVALID_ARGUMENT", "message": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "EXECUTION_ERROR", "message": str(e)}, ensure_ascii=False)

def main():
    print("=" * 70 + "\nFACILITIES TOOLS TEST\n" + "=" * 70)
    
    print("\n[1] CHECK ROOM")
    print(dispatch_tool_call("check_room_availability", {"start_time": "2026-09-15 14:00", "end_time": "2026-09-15 15:00", "capacity": 10}))
    
    print("\n[2] CHECK EQUIPMENT")
    print(dispatch_tool_call("check_equipment_availability", {"equipment_type": "projector", "quantity": 1, "start_time": "2026-09-15 14:00", "end_time": "2026-09-15 15:00"}))
    
    print("\n[3] BOOK ROOM")
    print(dispatch_tool_call("book_meeting_room", {"room_name": "ROOM_A102", "start_time": "2026-09-15 14:00", "end_time": "2026-09-15 15:00", "organizer": "Hoàng Trung Khải"}))
    
    print("\n[4] BOOK EQUIPMENT")
    print(dispatch_tool_call("book_equipment", {"equipment_type": "projector", "quantity": 1, "start_time": "2026-09-15 14:00", "end_time": "2026-09-15 15:00", "borrower": "Hoàng Trung Khải"}))
    
    print("\n[5] TEST ROOM CONFLICT")
    print(dispatch_tool_call("book_meeting_room", {"room_name": "ROOM_A102", "start_time": "2026-09-15 14:30", "end_time": "2026-09-15 15:30", "organizer": "Test User"}))
    
    print("\n[6] ROOM BOOKINGS\n", json.dumps(MOCK_DATABASE["room_bookings"], ensure_ascii=False, indent=2))
    print("\n[7] EQUIPMENT BOOKINGS\n", json.dumps(MOCK_DATABASE["equipment_bookings"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()