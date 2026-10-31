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

## Cập nhật 1.3.1 — 2026-10-31

Đưa năm nhóm kiểm tra do người dùng yêu cầu vào quy tắc dùng chung, SKILL.md, prompt tổng, module review/citations/self-review, checklist và mẫu báo cáo. Hồ sơ academic phải ghi đủ content, source_verification, in_text_citations, reference_list và language_presentation; bỏ nhóm hoặc giấu mục chưa kiểm tra sau kết luận ready sẽ bị phát hiện. Báo cáo general cũ vẫn tương thích.

Thêm năm kiểm tra cho báo cáo đủ nhóm, nhóm thiếu, nhóm sai kiểu/tên, khai báo giới hạn khi chưa xem bố cục và exit code CLI. Tổng cộng 66/66 unit/integration tests đạt; bản sinh, snapshot, module, giấy phép, liên kết và metadata của skill đã cài đều qua kiểm tra.

Một hội thoại mới đã chọn review, xác nhận phạm vi rồi chấm/sửa theo đủ năm nhóm: sửa phép tính 12/20 thành 60%; bác suy rộng/nhân quả; nhận ra citation lệch năm, entry thiếu, nguồn lặp/không dùng; không nhận đã xác minh nguồn hoặc xem định dạng từ văn bản thuần. Đầu vào và phản hồi ở additional_runs của [nhật ký hành vi](behavior-samples.json). Đây là kiểm thử hữu hạn, không chứng nhận đa mô hình hay khả năng kiểm chứng nguồn/bố cục khi không truy cập được chúng.
