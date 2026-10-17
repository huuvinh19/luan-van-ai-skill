# Kết quả kiểm tra bản 1.2.0

Ngày kiểm tra: 2026-10-17.

- Snapshot, prompt tổng, module và link nội bộ: đạt.
- 40 unit/integration tests: đạt; gồm bước hỏi/xác nhận cũ và kiểm tra hồ sơ tự chấm mới.
- Audit hồ sơ mẫu đầy đủ và gate mẫu: exit 0; mẫu chưa điền: exit 1 đúng dự kiến.
- Audit báo cáo tự rà repo: exit 0 về tính nhất quán cấu trúc.
- Hai tình huống từ hai ngữ cảnh agent tách biệt: sửa 12/20 thành 60%, không suy rộng cho cả nước; không xác nhận đạt D khi thiếu bài và rubric. Xem behavior-samples.json.
- Tự rà repo theo yêu cầu người viết ở reviews/repo-v1.2.0.json; không tự cho điểm số hoặc mức D.

Đánh giá trong phạm vi triển khai: đủ để dùng thử có theo dõi. Hai tình huống không chứng minh hành vi ổn định trên mọi mô hình hoặc loại bỏ hoàn toàn xu hướng chiều người dùng. Unit tests chỉ kiểm tra công cụ và cấu trúc, không chấm chất lượng luận văn. Tự rà repo là cùng trợ lý ở một lượt riêng; hai agent trả lời tình huống không phải reviewer độc lập chấm bản repo.

Log lệnh ở validation-results.json. Các giới hạn này phải được giữ khi giới thiệu kết quả, không đổi thành cam kết mô hình luôn phản biện đúng.
