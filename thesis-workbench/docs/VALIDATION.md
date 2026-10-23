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

## Cập nhật 1.3.0 — 2026-10-23

Luồng mới bắt buộc chọn/giữ prompt sau bối cảnh, lấy đề/tiêu chí/mục tiêu, bóc yêu cầu thành dàn ý và giữ hồ sơ đối chiếu suốt cuộc chat. Gate bổ sung select_prompt, plan và ràng buộc xác nhận với project_memory. Các kiểm tra cũ được điều chỉnh tại điểm thứ tự bước thay đổi; bổ sung 10 kiểm tra về prompt thực sự có nội dung, hỏi đúng phần thiếu, bao phủ yêu cầu bắt buộc, liên kết mã, đổi mục tiêu/dàn ý và giữ nhật ký lỗi. Tổng cộng 61 unit/integration tests đạt.

Ba hội thoại mới chỉ được giao skill và yêu cầu thực tế giả lập, không nhận đáp án hoặc chẩn đoán. Marketing chọn review rồi xin đề/bài/mục tiêu, giữ phạm vi và xuất lại được prompt, bảy yêu cầu cùng dàn ý trước xác nhận. IT chọn outline, liên kết yêu cầu với kế hoạch; khi tiền phạt trở thành bắt buộc, cập nhật yêu cầu cũ và nêu cách tính chưa được cung cấp. Ca chỉ sửa prompt vẫn giữ biến và không chạy phỏng vấn hay viết bài. Đây là kiểm thử hữu hạn trong cùng mô hình mặc định, không phải chứng nhận đa mô hình hoặc trí nhớ vĩnh viễn.

Đầu vào, phản hồi và kết quả công cụ nằm trong [nhật ký 1.3.0](project-memory-validation-2026-10-23.json). Công cụ vẫn chỉ kiểm tra khai báo; phải đọc đề/bài thật để xác nhận đầy đủ yêu cầu và chất lượng nguồn. Hồ sơ cũ thiếu trường mới cần bổ sung từ dữ kiện thực tế, không tự tạo prompt, tiêu chí hoặc xác nhận cho một dự án thật.
