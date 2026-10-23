# Quy trình một dự án

1. Đọc ngữ cảnh đã có; hỏi môn và ngành còn thiếu, không mặc định từ ví dụ. Xác định công đoạn đang cần hỗ trợ.
2. Trợ lý tự chọn module phù hợp, đọc và giữ prompt thực sự dùng cùng lý do trong active_prompt. Không bắt người viết chuẩn bị hay chọn prompt.
3. Lấy câu hỏi/đề bài, rubric nếu có và mục tiêu muốn đạt; chỉ hỏi phần còn thiếu. Tiếp tục làm rõ đầu vào/ràng buộc ảnh hưởng phạm vi hiện tại, tối đa ba câu chính mỗi lượt.
4. Bóc từng câu/mệnh đề thành yêu cầu R1… có nội dung, bắt buộc/gợi ý, vị trí căn cứ và cách kiểm tra. Không tự tạo rubric hoặc coi mục tiêu điểm là kết quả chấm.
5. Lập dàn ý theo đề; mỗi mục liên kết yêu cầu, ý phân tích và bằng chứng cần có. Kiểm tra mọi yêu cầu bắt buộc có nơi đáp ứng, mỗi mục nằm trong phạm vi; lưu project_memory.
6. Tóm tắt cách hiểu và dàn ý cho người viết xác nhận, rồi thực hiện phạm vi đã giao. Không xin phép lại từng mục đã được giao; không viết kết quả khi còn điểm cản cách làm.
7. Trước khi trả từng phần, đọc lại bộ nhớ và đối chiếu đề/rubric → yêu cầu → dàn ý → đoạn/bằng chứng thực tế. Sửa cả dàn ý nếu nó hiểu sai đề; đọc lại bản cuối sau sửa.
8. Ghi lỗi và cách tránh vào known_errors/tiến độ; cập nhật hồ sơ khi yêu cầu thay đổi. Chỉ làm rõ phần bị ảnh hưởng. Xuất prompt và tóm tắt hồ sơ hiện hành khi bàn giao sang chat khác.

Bộ nhớ gồm project.json, project_state.json và progress.md khi có file; trong chat giữ hồ sơ bằng văn bản. Không gọi đó là trí nhớ vĩnh viễn hoặc nhận đã lưu file chưa thực sự lưu. Mẫu và ví dụ công khai không chứa dữ kiện của người viết.

Quy tắc chọn prompt và bộ nhớ nằm trong prompt tổng và SKILL.md, nên AI đọc tệp cốt lõi vẫn thực hiện được mà không chạy script. Công cụ [audit](TOOLS.md) chỉ kiểm tra hồ sơ khai báo; chiều sâu, độ đúng nguồn và mức P/M/D vẫn phải đối chiếu bài thực tế. Xem [CHECKLIST](CHECKLIST.md) khi tự rà.
