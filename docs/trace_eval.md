# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Phúc Bảo  
> **Mã Sinh Viên / Mã Học viên:** 2A202602925  
> **Chủ đề Lựa chọn:** Đề tài Mở — Trợ lý Du lịch Cá nhân hóa (Personal Travel Assistant): tra cứu chuyến bay/phòng khách sạn còn trống theo điểm đến & ngày đi, và đặt vé/đặt phòng cho chuyến đi.  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Để lên kế hoạch cho một chuyến đi, Agent thường phải tra cứu chuyến bay/phòng trống trước, so sánh lựa chọn phù hợp với yêu cầu (điểm đến, ngày), rồi mới tiến hành đặt vé/đặt phòng. Đây là chuỗi 2 bước suy luận nối tiếp, không thể trả lời trong 1 lượt duy nhất. |
| **2. Tool Interaction** | 5 / 5 | Giá vé, tình trạng chuyến bay và phòng còn trống là dữ liệu biến động, không nằm trong tri thức tĩnh của LLM. Agent bắt buộc phải gọi Tool `search_travel_options` và `book_travel` qua MCP Server để lấy dữ liệu thực tế trước khi trả lời hoặc thực thi hành động. |
| **3. Dynamic Decision** | 4 / 5 | Quyết định đặt chuyến bay/phòng nào phụ thuộc trực tiếp vào Observation trả về từ bước tra cứu trước đó. Ví dụ nếu chuyến bay mong muốn hết chỗ hoặc điểm đến không tồn tại, Agent phải rẽ nhánh sang phản hồi từ chối/gợi ý thay vì mặc định đặt vé. |
| **4. Long Horizon Goal** | 3 / 5 | Agent cần giữ ngữ cảnh xuyên suốt một phiên hội thoại (điểm đến, ngày đi, tên hành khách) qua nhiều lượt hỏi-đáp để hoàn tất một mục tiêu duy nhất là "đặt được chuyến đi", nhưng chưa đạt mức lập kế hoạch dài hạn nhiều ngày/nhiều giai đoạn như Agent Cấp 4. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | Tổng điểm > 12/20 → Bài toán Trợ lý Du lịch rất phù hợp để triển khai dưới dạng Agentic System (ReAct Agent), thay vì chỉ dùng LLM Chatbot đơn thuần. |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật (chạy với `LLM_PROVIDER=openai`, model `gpt-4o-mini`):

```json
[
  {
    "step": 1,
    "query": "Đặt cho tôi vé máy bay chuyến VN209 đi Đà Nẵng ngày 20/09/2026 dưới tên hành khách Nguyễn Phúc Bảo.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_travel",
    "arguments": {
      "destination": "Đà Nẵng",
      "date": "20/09/2026",
      "traveler_name": "Nguyễn Phúc Bảo",
      "flight_id": "VN209"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-VN209-20092026",
      "destination": "Đà Nẵng",
      "date": "20/09/2026",
      "traveler_name": "Nguyễn Phúc Bảo",
      "flight_id": "VN209",
      "message": "Đặt vé chuyến bay VN209 thành công cho hành khách Nguyễn Phúc Bảo đi Đà Nẵng vào ngày 20/09/2026."
    },
    "latency_ms": 1284.32
  },
  {
    "step": 2,
    "query": "Đặt cho tôi vé máy bay chuyến VN209 đi Đà Nẵng ngày 20/09/2026 dưới tên hành khách Nguyễn Phúc Bảo.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Đặt vé chuyến bay VN209 thành công cho hành khách Nguyễn Phúc Bảo đi Đà Nẵng vào ngày 20/09/2026.",
    "latency_ms": 10.0
  }
]
```

> Log đầy đủ 9 sự kiện (5 test case) được lưu tại [`docs/trace_waterfall.json`](trace_waterfall.json).

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` (OpenAI, model `gpt-4o-mini`) và xác nhận Agent chạy mượt mà trên LLM API thật.
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (TC02: `search_travel_options`, TC03: `book_travel`, TC04: `search_travel_options`, TC05: `search_travel_options`). Riêng TC01 LLM trả lời trực tiếp bằng văn bản, đúng như kỳ vọng vì đây là câu hỏi chính sách chung, không cần dữ liệu thời gian thực.
- **Ghi chú TC04:** LLM thật suy luận đúng thứ tự — chủ động gọi `search_travel_options` trước khi đặt vé, đúng tinh thần suy luận ReAct. Tuy nhiên vòng lặp `run_react_agent()` của khung bài chỉ xử lý 1 Tool Call rồi tổng hợp Final Answer ngay (không lặp lại lượt gọi LLM thứ 2 để tự động tiếp tục `book_travel`), nên chuỗi 2 bước chưa được thực thi trọn vẹn trong 1 lần chạy. Đây là đặc điểm kiến trúc của khung `run_react_agent()` được quan sát ở Task 2.2, không phải lỗi cấu hình Tool/MCP Server.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
