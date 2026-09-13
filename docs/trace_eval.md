# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Hoàng Trung Khải  
> **Mã Sinh Viên / Mã Học viên:** 2A202602947  
> **Chủ đề Lựa chọn:** Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent): Kiểm tra lịch phòng trống, thiết bị và tạo booking phòng họp.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | Bài toán yêu cầu nhiều bước suy luận: hiểu yêu cầu, kiểm tra phòng trống, kiểm tra thiết bị phù hợp, từ đó đưaa ra quyết định tạo booking |
| **2. Tool Interaction** | 5 / 5 | Hệ thống cần kết nối với các dịch vụ bên ngoài: lấy lịch phòng, thông tin thiết bị, thực hiện booking |
| **3. Dynamic Decision** | 4 / 5 | Tùy yêu cầu, agent có thể chỉ đặt phòng, chỉ mượn thiết bị hoặc thực hiện cả hai; đồng thời phải quyết định hành động tiếp theo dựa trên kết quả kiểm tra. |
| **4. Long Horizon Goal** | 4 / 5 | Hệ thống cần duy trì mục tiêu "đặt được một phòng phù hợp" qua các bước xử lý |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi cần tổ chức một cuộc họp 10 người từ 14:00 đến 15:00 ngày 15/09/2026 và cần một máy chiếu. Hãy tìm phương án phù hợp và đặt giúp tôi cả phòng họp lẫn thiết bị.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_room_availability",
    "arguments": {
      "capacity": 10,
      "end_time": "2026-09-15 15:00",
      "start_time": "2026-09-15 14:00"
    },
    "observation": {
      "status": "SUCCESS",
      "start_time": "2026-09-15 14:00",
      "end_time": "2026-09-15 15:00",
      "capacity": 10,
      "available_rooms": [
        {
          "room_id": "ROOM_B201",
          "name": "Phòng B201",
          "capacity": 30,
          "location": "Tòa B - Tầng 2",
          "equipment": [
            "projector",
            "microphone",
            "tv",
            "whiteboard"
          ]
        }
      ],
      "message": "Đã kiểm tra availability thành công. Chưa tạo booking."
    },
    "latency_ms": 3099.49
  },
  {
    "step": 2,
    "query": "Tôi cần tổ chức một cuộc họp 10 người từ 14:00 đến 15:00 ngày 15/09/2026 và cần một máy chiếu. Hãy tìm phương án phù hợp và đặt giúp tôi cả phòng họp lẫn thiết bị.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_equipment_availability",
    "arguments": {
      "start_time": "2026-09-15 14:00",
      "end_time": "2026-09-15 15:00",
      "quantity": 1,
      "equipment_type": "projector"
    },
    "observation": {
      "status": "SUCCESS",
      "equipment_type": "projector",
      "requested_quantity": 1,
      "available_quantity": 2,
      "start_time": "2026-09-15 14:00",
      "end_time": "2026-09-15 15:00",
      "message": "Đã kiểm tra availability thành công. Chưa tạo booking."
    },
    "latency_ms": 1597.65
  },
  {
    "step": 3,
    "query": "Tôi cần tổ chức một cuộc họp 10 người từ 14:00 đến 15:00 ngày 15/09/2026 và cần một máy chiếu. Hãy tìm phương án phù hợp và đặt giúp tôi cả phòng họp lẫn thiết bị.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_meeting_room",
    "arguments": {
      "start_time": "2026-09-15 14:00",
      "room_name": "ROOM_B201",
      "organizer": "Người dùng",
      "end_time": "2026-09-15 15:00"
    },
    "observation": {
      "status": "SUCCESS",
      "message": "Đặt phòng thành công.",
      "booking": {
        "booking_id": "RB-004",
        "room_name": "ROOM_B201",
        "start_time": "2026-09-15 14:00",
        "end_time": "2026-09-15 15:00",
        "organizer": "Người dùng"
      }
    },
    "latency_ms": 3141.39
  },
  {
    "step": 4,
    "query": "Tôi cần tổ chức một cuộc họp 10 người từ 14:00 đến 15:00 ngày 15/09/2026 và cần một máy chiếu. Hãy tìm phương án phù hợp và đặt giúp tôi cả phòng họp lẫn thiết bị.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_equipment",
    "arguments": {
      "quantity": 1,
      "end_time": "2026-09-15 15:00",
      "equipment_type": "projector",
      "start_time": "2026-09-15 14:00",
      "borrower": "Người dùng"
    },
    "observation": {
      "status": "SUCCESS",
      "message": "Đặt thiết bị thành công.",
      "booking": {
        "booking_id": "EB-003",
        "equipment_type": "projector",
        "quantity": 1,
        "start_time": "2026-09-15 14:00",
        "end_time": "2026-09-15 15:00",
        "borrower": "Người dùng"
      }
    },
    "latency_ms": 4579.46
  },
  {
    "step": 5,
    "query": "Tôi cần tổ chức một cuộc họp 10 người từ 14:00 đến 15:00 ngày 15/09/2026 và cần một máy chiếu. Hãy tìm phương án phù hợp và đặt giúp tôi cả phòng họp lẫn thiết bị.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Tôi đã hoàn tất việc đặt phòng họp và thiết bị cho bạn theo đúng yêu cầu:\n\n1. **Phòng họp**:\n   - **Tên phòng**: Phòng B201 (ROOM_B201)\n   - **Thời gian**: 14:00 - 15:00 ngày 15/09/2026\n   - **Mã đặt phòng**: `RB-004`\n   - **Người tổ chức**: Người dùng\n\n2. **Thiết bị (Máy chiếu)**:\n   - **Loại thiết bị**: Projector (Số lượng: 1)\n   - **Thời gian**: 14:00 - 15:00 ngày 15/09/2026\n   - **Mã mượn thiết bị**: `EB-003`\n   - **Người mượn**: Người dùng\n\nChúc cuộc họp của bạn diễn ra thành công tốt đẹp!",
    "latency_ms": 1478.76
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 9 / 9 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 10 lượt.
- **Kết quả đẩy Repo nộp bài:** [X] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
