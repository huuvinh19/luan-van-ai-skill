# Tự chuẩn hóa yêu cầu trong dự án

Tự áp dụng bước này khi nhận yêu cầu mới trong một dự án luận văn đang hoạt động. Người viết không cần gọi lại `$prompt-optimizer` ở mỗi lượt.

1. Giữ nguyên yêu cầu gốc. Xác định việc cần làm, dữ liệu/tài liệu đầu vào, phạm vi, ràng buộc, đầu ra và căn cứ để kiểm tra kết quả.
2. Đối chiếu với hồ sơ dự án đã xác nhận. Sắp xếp lại yêu cầu thành chỉ dẫn ngắn, rõ và có thể thực hiện. Giữ nguyên dữ liệu, ý định, thuật ngữ, các biến `{{...}}`/`${...}` và những chỉnh sửa đã chốt.
3. Phân biệt nội dung người viết nói, thông tin thực sự đọc được trong tài liệu và đề xuất của mày. Không tự thêm đề tài, doanh nghiệp, mẫu, phương pháp, nguồn, thang điểm hoặc mục tiêu mới để lấp chỗ thiếu.
4. Nếu việc hiểu yêu cầu cần một lựa chọn có ảnh hưởng hoặc còn mâu thuẫn, chuyển sang bước hỏi. Không tối ưu bằng cách đoán ý rồi chạy trước. Nếu đã rõ và nằm trong phạm vi được xác nhận, thực hiện yêu cầu đã làm rõ mà không xin duyệt lại một lần sửa câu chữ thuần túy.
5. Trước việc lớn, báo một câu ngắn về cách hiểu và đầu ra sẽ làm. Không cần đổ toàn bộ prompt nội bộ vào cuộc trò chuyện. Khi người viết yêu cầu xem prompt, trả bản hoàn chỉnh để copy.

Khi sửa một prompt ngắn, giữ bản sửa gọn theo phạm vi đó. Không chép lại cả bộ quy tắc luận văn, liệt kê mọi đầu vào có thể thiếu hoặc tự thêm nhiều công đoạn chưa được giao. Chỉ thêm chi tiết để giải quyết điểm mơ hồ cụ thể; giữ nguyên các biến và các ràng buộc cần thiết.

“Tự sửa prompt” ở đây là quy trình mô hình làm rõ và cấu trúc yêu cầu. Các script đi kèm ghép quy tắc, giữ yêu cầu gốc và kiểm tra hồ sơ; chúng không gọi mô hình để tự viết lại câu chữ hoặc xác nhận thay người dùng.
