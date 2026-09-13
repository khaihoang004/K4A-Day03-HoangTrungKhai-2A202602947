import json
from typing import Dict, Any
from datetime import datetime


# ==============================================================================
# 1. TOOL SCHEMAS
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "check_room_availability",
        "description": (
            "CHỈ kiểm tra phòng họp còn trống. "
            "Tool này KHÔNG đặt phòng và KHÔNG tạo booking. "
            "Chỉ được gọi khi user đã cung cấp ĐẦY ĐỦ và rõ ràng: "
            "start_time, end_time và capacity. "
            "Không được tự đoán hoặc tự điền giá trị còn thiếu. "
            "Nếu thiếu bất kỳ thông tin nào, Agent phải hỏi user trước."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu sử dụng phòng, "
                        "format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc sử dụng phòng, "
                        "format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "capacity": {
                    "type": "integer",
                    "description": (
                        "Số lượng người tham dự. Phải là số nguyên > 0. "
                        "BẮT BUỘC."
                    )
                }
            },
            "required": ["start_time", "end_time", "capacity"]
        }
    },

    {
        "name": "check_equipment_availability",
        "description": (
            "CHỈ kiểm tra số lượng thiết bị còn khả dụng. "
            "Tool này KHÔNG tạo booking và KHÔNG mượn thiết bị. "
            "Chỉ được gọi khi user đã cung cấp ĐẦY ĐỦ và rõ ràng: "
            "equipment_type, quantity, start_time và end_time. "
            "Không được tự đoán hoặc tự điền giá trị còn thiếu. "
            "Nếu thiếu bất kỳ thông tin nào, Agent phải hỏi user trước."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "equipment_type": {
                    "type": "string",
                    "description": (
                        "Loại thiết bị cần mượn, ví dụ projector, "
                        "microphone, tv. BẮT BUỘC."
                    )
                },
                "quantity": {
                    "type": "integer",
                    "description": "Số lượng thiết bị cần mượn, phải > 0. BẮT BUỘC."
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu sử dụng, "
                        "format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc sử dụng, "
                        "format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
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
            "CHỈ tạo booking cho phòng họp đã được xác định cụ thể. "
            "Tool này KHÔNG tìm phòng, KHÔNG kiểm tra availability và "
            "KHÔNG tự bổ sung thông tin còn thiếu. "
            "Chỉ được gọi khi user đã cung cấp ĐẦY ĐỦ: "
            "room_name, start_time, end_time và organizer, "
            "đồng thời đã có kết quả CHECK phòng thành công "
            "cho đúng phòng và đúng khoảng thời gian. "
            "Nếu chưa đủ thông tin hoặc chưa CHECK thành công, "
            "KHÔNG được gọi tool này."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "room_name": {
                    "type": "string",
                    "description": "Tên/mã phòng đã được chọn. BẮT BUỘC."
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu, format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc, format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "organizer": {
                    "type": "string",
                    "description": "Tên người đặt phòng. BẮT BUỘC."
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
            "CHỈ tạo booking/mượn thiết bị đã được xác định cụ thể. "
            "Tool này KHÔNG kiểm tra availability và KHÔNG tự tìm thiết bị. "
            "Chỉ được gọi khi user đã cung cấp ĐẦY ĐỦ: "
            "equipment_type, quantity, start_time, end_time và borrower, "
            "đồng thời đã có kết quả CHECK thiết bị thành công "
            "cho đúng loại, số lượng và đúng khoảng thời gian. "
            "Nếu chưa đủ thông tin hoặc chưa CHECK thành công, "
            "KHÔNG được gọi tool này."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "equipment_type": {
                    "type": "string",
                    "description": "Loại thiết bị đã được chọn. BẮT BUỘC."
                },
                "quantity": {
                    "type": "integer",
                    "description": "Số lượng thiết bị cần mượn, phải > 0. BẮT BUỘC."
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Thời gian bắt đầu, format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Thời gian kết thúc, format 'YYYY-MM-DD HH:MM'. BẮT BUỘC."
                    )
                },
                "borrower": {
                    "type": "string",
                    "description": "Tên người mượn. BẮT BUỘC."
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
# 2. MOCK DATABASE
# ==============================================================================

MOCK_DATABASE = {
    "rooms": {
        "ROOM_A101": {
            "name": "Phòng A101",
            "capacity": 10,
            "location": "Tòa A - Tầng 1",
            "equipment": ["projector", "whiteboard"]
        },
        "ROOM_A102": {
            "name": "Phòng A102",
            "capacity": 20,
            "location": "Tòa A - Tầng 1",
            "equipment": ["projector", "microphone", "whiteboard"]
        },
        "ROOM_B201": {
            "name": "Phòng B201",
            "capacity": 30,
            "location": "Tòa B - Tầng 2",
            "equipment": ["projector", "microphone", "tv", "whiteboard"]
        },
        "ROOM_B202": {
            "name": "Phòng B202",
            "capacity": 8,
            "location": "Tòa B - Tầng 2",
            "equipment": ["tv", "whiteboard"]
        }
    },

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


# ==============================================================================
# 3. CHECK STATE
# ==============================================================================

# Lưu kết quả CHECK thành công để BOOK không thể chạy nếu chưa CHECK.
# Quan trọng: BOOK không tự thực hiện availability checking.
LAST_SUCCESSFUL_ROOM_CHECKS = set()
LAST_SUCCESSFUL_EQUIPMENT_CHECKS = set()


# ==============================================================================
# 4. HELPERS
# ==============================================================================

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)


def validate_time_range(start_time: str, end_time: str):
    start, end = parse_datetime(start_time), parse_datetime(end_time)

    if start >= end:
        raise ValueError("start_time phải nhỏ hơn end_time.")

    return start, end


def validate_required_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} là thông tin bắt buộc và không được để trống.")

    return value.strip()


def validate_positive_integer(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} phải là số nguyên lớn hơn 0.")

    return value


def is_time_overlap(
    existing_start: datetime,
    existing_end: datetime,
    new_start: datetime,
    new_end: datetime
) -> bool:
    return existing_start < new_end and existing_end > new_start


def room_check_key(start_time: str, end_time: str, capacity: int):
    return (start_time, end_time, capacity)


def equipment_check_key(
    equipment_type: str,
    quantity: int,
    start_time: str,
    end_time: str
):
    return (equipment_type, quantity, start_time, end_time)


# ==============================================================================
# 5. CHECK TOOLS
# ==============================================================================

def execute_check_room_availability(
    start_time: str,
    end_time: str,
    capacity: int
) -> str:
    """
    CHECK ONLY.

    Không tạo booking.
    Không chọn organizer.
    Không gọi BOOK.
    """

    try:
        start_time = validate_required_string(start_time, "start_time")
        end_time = validate_required_string(end_time, "end_time")
        capacity = validate_positive_integer(capacity, "capacity")

        new_start, new_end = validate_time_range(start_time, end_time)

    except (ValueError, TypeError) as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": str(e)
        }, ensure_ascii=False)

    available_rooms = []

    for room_id, room in MOCK_DATABASE["rooms"].items():

        if room["capacity"] < capacity:
            continue

        is_booked = False

        for booking in MOCK_DATABASE["room_bookings"]:

            if booking["room_name"] != room_id:
                continue

            existing_start = parse_datetime(booking["start_time"])
            existing_end = parse_datetime(booking["end_time"])

            if is_time_overlap(
                existing_start,
                existing_end,
                new_start,
                new_end
            ):
                is_booked = True
                break

        if not is_booked:
            available_rooms.append({
                "room_id": room_id,
                **room
            })

    if not available_rooms:
        return json.dumps({
            "status": "UNAVAILABLE",
            "start_time": start_time,
            "end_time": end_time,
            "capacity": capacity,
            "available_rooms": [],
            "message": (
                f"Không có phòng phù hợp cho {capacity} người "
                f"từ {start_time} đến {end_time}."
            )
        }, ensure_ascii=False)

    # Chỉ ghi CHECK state khi thực sự tìm được phòng.
    LAST_SUCCESSFUL_ROOM_CHECKS.add(
        room_check_key(start_time, end_time, capacity)
    )

    return json.dumps({
        "status": "SUCCESS",
        "start_time": start_time,
        "end_time": end_time,
        "capacity": capacity,
        "available_rooms": available_rooms,
        "message": (
            "Đã kiểm tra availability thành công. "
            "Chưa tạo booking."
        )
    }, ensure_ascii=False)


def execute_check_equipment_availability(
    equipment_type: str,
    quantity: int,
    start_time: str,
    end_time: str
) -> str:
    """
    CHECK ONLY.

    Không tạo booking.
    Không chọn borrower.
    """

    try:
        equipment_type = validate_required_string(
            equipment_type,
            "equipment_type"
        ).lower()

        quantity = validate_positive_integer(quantity, "quantity")

        start_time = validate_required_string(start_time, "start_time")
        end_time = validate_required_string(end_time, "end_time")

        new_start, new_end = validate_time_range(start_time, end_time)

    except (ValueError, TypeError) as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": str(e)
        }, ensure_ascii=False)

    equipment = MOCK_DATABASE["equipment"].get(equipment_type)

    if not equipment:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thiết bị '{equipment_type}'."
        }, ensure_ascii=False)

    events = []

    for booking in MOCK_DATABASE["equipment_bookings"]:

        if booking["equipment_type"] != equipment_type:
            continue

        existing_start = parse_datetime(booking["start_time"])
        existing_end = parse_datetime(booking["end_time"])

        if not is_time_overlap(
            existing_start,
            existing_end,
            new_start,
            new_end
        ):
            continue

        overlap_start = max(existing_start, new_start)
        overlap_end = min(existing_end, new_end)

        events.extend([
            (overlap_start, booking["quantity"]),
            (overlap_end, -booking["quantity"])
        ])

    events.sort(key=lambda x: (x[0], 0 if x[1] < 0 else 1))

    current_booked = 0
    max_booked = 0

    for _, delta in events:
        current_booked += delta
        max_booked = max(max_booked, current_booked)

    available_quantity = equipment["total_quantity"] - max_booked

    if available_quantity < quantity:
        return json.dumps({
            "status": "UNAVAILABLE",
            "equipment_type": equipment_type,
            "requested_quantity": quantity,
            "available_quantity": max(0, available_quantity),
            "start_time": start_time,
            "end_time": end_time,
            "message": (
                f"Không đủ {equipment['name']} "
                f"trong khoảng thời gian yêu cầu."
            )
        }, ensure_ascii=False)

    LAST_SUCCESSFUL_EQUIPMENT_CHECKS.add(
        equipment_check_key(
            equipment_type,
            quantity,
            start_time,
            end_time
        )
    )

    return json.dumps({
        "status": "SUCCESS",
        "equipment_type": equipment_type,
        "requested_quantity": quantity,
        "available_quantity": available_quantity,
        "start_time": start_time,
        "end_time": end_time,
        "message": (
            "Đã kiểm tra availability thành công. "
            "Chưa tạo booking."
        )
    }, ensure_ascii=False)


# ==============================================================================
# 6. BOOK TOOLS
# ==============================================================================

def execute_book_meeting_room(
    room_name: str,
    start_time: str,
    end_time: str,
    organizer: str
) -> str:
    """
    BOOK ONLY.

    Không thực hiện availability calculation.
    Không tự tìm phòng.
    Không tự chọn phòng.
    Chỉ tạo booking sau khi:
      - đủ thông tin;
      - room đã được chọn;
      - có CHECK thành công tương ứng.
    """

    try:
        room_name = validate_required_string(room_name, "room_name")
        start_time = validate_required_string(start_time, "start_time")
        end_time = validate_required_string(end_time, "end_time")
        organizer = validate_required_string(organizer, "organizer")

        new_start, new_end = validate_time_range(start_time, end_time)

    except (ValueError, TypeError) as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": str(e)
        }, ensure_ascii=False)

    if room_name not in MOCK_DATABASE["rooms"]:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phòng '{room_name}'."
        }, ensure_ascii=False)

    room = MOCK_DATABASE["rooms"][room_name]

    # BOOK không tự check availability.
    # Nó chỉ yêu cầu Agent đã thực hiện CHECK trước đó.
    matching_check_found = False

    for start, end, capacity in LAST_SUCCESSFUL_ROOM_CHECKS:

        if start != start_time or end != end_time:
            continue

        if room["capacity"] >= capacity:
            matching_check_found = True
            break

    if not matching_check_found:
        return json.dumps({
            "status": "CHECK_REQUIRED",
            "message": (
                "Chưa có kết quả check availability thành công "
                "cho phòng và khoảng thời gian này. "
                "Hãy gọi check_room_availability trước khi booking."
            )
        }, ensure_ascii=False)

    booking_id = f"RB-{len(MOCK_DATABASE['room_bookings']) + 1:03d}"

    new_booking = {
        "booking_id": booking_id,
        "room_name": room_name,
        "start_time": start_time,
        "end_time": end_time,
        "organizer": organizer
    }

    MOCK_DATABASE["room_bookings"].append(new_booking)

    return json.dumps({
        "status": "SUCCESS",
        "message": "Đặt phòng thành công.",
        "booking": new_booking
    }, ensure_ascii=False)


def execute_book_equipment(
    equipment_type: str,
    quantity: int,
    start_time: str,
    end_time: str,
    borrower: str
) -> str:
    """
    BOOK ONLY.

    Không thực hiện availability calculation.
    Không tự check số lượng.
    Chỉ tạo booking sau khi đã CHECK thành công.
    """

    try:
        equipment_type = validate_required_string(
            equipment_type,
            "equipment_type"
        ).lower()

        quantity = validate_positive_integer(quantity, "quantity")

        start_time = validate_required_string(start_time, "start_time")
        end_time = validate_required_string(end_time, "end_time")

        borrower = validate_required_string(borrower, "borrower")

        validate_time_range(start_time, end_time)

    except (ValueError, TypeError) as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": str(e)
        }, ensure_ascii=False)

    if equipment_type not in MOCK_DATABASE["equipment"]:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thiết bị '{equipment_type}'."
        }, ensure_ascii=False)

    check_key = equipment_check_key(
        equipment_type,
        quantity,
        start_time,
        end_time
    )

    if check_key not in LAST_SUCCESSFUL_EQUIPMENT_CHECKS:
        return json.dumps({
            "status": "CHECK_REQUIRED",
            "message": (
                "Chưa có kết quả check availability thành công "
                "cho thiết bị, số lượng và khoảng thời gian này. "
                "Hãy gọi check_equipment_availability trước khi booking."
            )
        }, ensure_ascii=False)

    booking_id = f"EB-{len(MOCK_DATABASE['equipment_bookings']) + 1:03d}"

    new_booking = {
        "booking_id": booking_id,
        "equipment_type": equipment_type,
        "quantity": quantity,
        "start_time": start_time,
        "end_time": end_time,
        "borrower": borrower
    }

    MOCK_DATABASE["equipment_bookings"].append(new_booking)

    return json.dumps({
        "status": "SUCCESS",
        "message": "Đặt thiết bị thành công.",
        "booking": new_booking
    }, ensure_ascii=False)


# ==============================================================================
# 7. TOOL ROUTER
# ==============================================================================

TOOL_ROUTER = {
    "check_room_availability": execute_check_room_availability,
    "check_equipment_availability": execute_check_equipment_availability,
    "book_meeting_room": execute_book_meeting_room,
    "book_equipment": execute_book_equipment
}


def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:

    if tool_name not in TOOL_ROUTER:
        return json.dumps({
            "status": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' không tồn tại."
        }, ensure_ascii=False)

    try:
        return TOOL_ROUTER[tool_name](**arguments)

    except TypeError as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": str(e)
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "message": str(e)
        }, ensure_ascii=False)


# ==============================================================================
# 8. TESTS
# ==============================================================================

def main():
    print("=" * 70)
    print("FACILITIES TOOLS - STRICT CHECK / BOOK SEPARATION")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # TEST 1: CHECK ROOM
    # --------------------------------------------------------------------------
    print("\n[1] CHECK ROOM")

    print(dispatch_tool_call(
        "check_room_availability",
        {
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00",
            "capacity": 10
        }
    ))

    # --------------------------------------------------------------------------
    # TEST 2: BOOK ROOM SAU KHI CHECK
    # --------------------------------------------------------------------------
    print("\n[2] BOOK ROOM AFTER CHECK")

    print(dispatch_tool_call(
        "book_meeting_room",
        {
            "room_name": "ROOM_A102",
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00",
            "organizer": "Hoàng Trung Khải"
        }
    ))

    # --------------------------------------------------------------------------
    # TEST 3: CHECK EQUIPMENT
    # --------------------------------------------------------------------------
    print("\n[3] CHECK EQUIPMENT")

    print(dispatch_tool_call(
        "check_equipment_availability",
        {
            "equipment_type": "projector",
            "quantity": 1,
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00"
        }
    ))

    # --------------------------------------------------------------------------
    # TEST 4: BOOK EQUIPMENT SAU KHI CHECK
    # --------------------------------------------------------------------------
    print("\n[4] BOOK EQUIPMENT AFTER CHECK")

    print(dispatch_tool_call(
        "book_equipment",
        {
            "equipment_type": "projector",
            "quantity": 1,
            "start_time": "2026-09-15 14:00",
            "end_time": "2026-09-15 15:00",
            "borrower": "Hoàng Trung Khải"
        }
    ))

    # --------------------------------------------------------------------------
    # TEST 5: BOOK WITHOUT CHECK -> MUST FAIL
    # --------------------------------------------------------------------------
    print("\n[5] BOOK WITHOUT CHECK")

    print(dispatch_tool_call(
        "book_meeting_room",
        {
            "room_name": "ROOM_B201",
            "start_time": "2026-09-16 14:00",
            "end_time": "2026-09-16 15:00",
            "organizer": "Test User"
        }
    ))

    # --------------------------------------------------------------------------
    # TEST 6: FINAL DATABASE
    # --------------------------------------------------------------------------
    print("\n[6] ROOM BOOKINGS")
    print(json.dumps(
        MOCK_DATABASE["room_bookings"],
        ensure_ascii=False,
        indent=2
    ))

    print("\n[7] EQUIPMENT BOOKINGS")
    print(json.dumps(
        MOCK_DATABASE["equipment_bookings"],
        ensure_ascii=False,
        indent=2
    ))


if __name__ == "__main__":
    main()