# Quy trình luận văn

Trước khi triển khai lần đầu, đọc đầu vào, hỏi các điểm ảnh hưởng cách làm và xác nhận bản tóm tắt dự án theo [PROJECT_DIALOGUE](PROJECT_DIALOGUE.md). Sau khi chốt, đi từ công đoạn đang cần và tái sử dụng kết quả đã đủ căn cứ. Mỗi dự án có hồ sơ riêng; không kế thừa môn, rubric hoặc doanh nghiệp từ dự án khác.

| Công đoạn | Đầu vào | Kết quả để tiếp tục |
| --- | --- | --- |
| Đọc đề | Đề, rubric, hướng dẫn và tài liệu hiện hành | `project.json`, `requirements.csv`; xác định phần thiếu ảnh hưởng cách làm |
| Đề cương | Câu hỏi, phạm vi và tiêu chí thực tế | Dàn ý, lập luận dự kiến, nhu cầu bằng chứng |
| Nguồn | Câu hỏi/nhận định cần xác minh | `sources.json`, truy vấn đã thực hiện và vị trí nội dung được đọc |
| Tổng quan | Nguồn đủ truy cập | So sánh, tổng hợp và giới hạn; không chỉ tóm tắt từng bài |
| Phương pháp | Câu hỏi và dữ liệu khả dụng | Thiết kế có lý do, biến/thang đo, giới hạn; phân biệt dự kiến/đã làm |
| Phân tích | Dữ liệu thật và bằng chứng xử lý | Output, mã/lệnh nếu có, diễn giải đúng phạm vi |
| Viết | Dàn ý và bản đồ nhận định–bằng chứng | Bản thảo có trích dẫn đúng câu và danh mục tương ứng |
| Chấm sửa | Bản thảo và rubric | Bằng chứng đạt/thiếu từng tiêu chí, vị trí lỗi và bản đã sửa |
| Dịch/xuất | Bản đã rà, ngôn ngữ/định dạng được yêu cầu | Bản cuối được đối chiếu; báo rõ phần chưa kiểm tra được |

## Làm việc với hồ sơ

- `requirements.csv`: một dòng cho mỗi yêu cầu thật. Gợi ý tham khảo có `kind=suggestion`; không đổi thành bắt buộc.
- `sources.json`: metadata và trạng thái đọc. `content_checked` là khai báo của người đã đọc, không phải kết luận do script cấp.
- `claims.csv`: liên kết nhận định với nguồn hoặc bằng chứng dữ liệu. Đây là bảng nội bộ, không dùng ID như S001 thay trích dẫn Harvard trong bài nộp.
- `progress.md`: ghi đã làm gì, đầu ra hiện hành ở đâu, vướng gì và bước tiếp theo. Sau lần sửa quan trọng, cập nhật tiến độ rồi tiếp tục trong phạm vi đã được giao.
- `project_state.json`: bản tóm tắt đã xác nhận, câu trả lời/câu hỏi còn mở và dấu hồ sơ của lần xác nhận. Đổi hồ sơ làm xác nhận cũ hết hiệu lực trong công cụ.

Hỏi các điểm chưa chắc chắn ảnh hưởng đến kết quả, theo từng lượt và cập nhật câu trả lời. Chưa triển khai nội dung khi còn câu hỏi cản cách làm hoặc chưa xác nhận phạm vi lần đầu. Sau khi chốt, xử lý lựa chọn thông thường trong phạm vi được giao; không xin phép lại từng phần. Tự chuẩn hóa yêu cầu ở mỗi lượt, hỏi lại khi có mâu thuẫn hoặc thay đổi quan trọng.

## Tự rà trước khi trả

Đối chiếu kết quả thực tế với từng yêu cầu, không đánh dấu đạt chỉ vì có tên mục. Với tiêu chí M/D nếu rubric có, kiểm tra bằng chứng về phân tích/đánh giá mà tiêu chí yêu cầu. Sửa lỗi quan trọng trước, sau đó lỗi diễn đạt và hình thức. Khi bản đã đáp ứng phần kiểm tra được, giao kết quả và nêu giới hạn cụ thể, tránh lặp các lượt tự chấm không có phát hiện mới.

Danh sách kiểm tra chi tiết ở [CHECKLIST](CHECKLIST.md). Công cụ [audit](TOOLS.md) hỗ trợ phát hiện hồ sơ thiếu hoặc mâu thuẫn, không chứng nhận chất lượng luận văn.
