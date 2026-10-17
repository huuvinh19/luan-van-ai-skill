# Hỏi rõ và tự làm rõ yêu cầu trong cả dự án

Quy tắc của người viết, bổ sung ngày 2026-10-17: hỏi điều chưa chắc chắn về dự án cho đến khi đủ hiểu để làm đúng phạm vi đang được giao. Hỏi trước khi bắt đầu và kiểm tra lại suốt dự án. Không viết/phân tích trước rồi mới hỏi.

## Trong cuộc trò chuyện

1. Đọc tài liệu hiện có, ghi những điều đã rõ, điều thiếu và mâu thuẫn.
2. Hỏi tối đa 3 câu chính mỗi lượt, ưu tiên điểm ảnh hưởng mục tiêu, phạm vi, đầu vào, tiêu chí và đầu ra. Nhận câu trả lời rồi cập nhật và hỏi tiếp phần còn thiếu.
3. Khi đủ rõ, tóm tắt cụ thể dự án, công việc, căn cứ và đầu ra; đợi người viết xác nhận hoặc sửa. Không dùng im lặng hoặc câu “làm luôn” để tự điền câu trả lời còn thiếu.
4. Sau xác nhận, làm phạm vi đã được giao. Trước mỗi công đoạn, tự chuẩn hóa yêu cầu và so với hồ sơ. Không hỏi lại dữ kiện còn hiệu lực.
5. Khi có thay đổi/mâu thuẫn ảnh hưởng kết quả, hỏi rõ phần bị ảnh hưởng, cập nhật hồ sơ và cách hiểu. Không bắt đầu lại toàn bộ cuộc phỏng vấn nếu chỉ đổi một chi tiết.

Chỉ hỏi những điều cần cho công việc hiện tại. Ví dụ, được phép cùng bàn chọn phương pháp khi đó chính là việc người viết yêu cầu; không cần giả vờ đã chốt phương pháp trước khi thảo luận. Sửa prompt hoặc sửa repo cũng là việc riêng, không đòi đủ dữ liệu của một luận văn để thực hiện.

## Tự chuẩn hóa prompt

Sau khi nhận yêu cầu, mô hình tự lập mục tiêu, đầu vào, phạm vi, ràng buộc, đầu ra và cách kiểm tra từ ý định đã có. Giữ yêu cầu gốc để đối chiếu, không thêm nội dung nghiên cứu hoặc bịa thông tin còn thiếu. Nếu việc tối ưu cần một lựa chọn thay đổi cách làm, hỏi trước. Nếu chỉ làm rõ câu chữ trong phạm vi đã chốt, thực hiện mà không bắt người viết duyệt lại từng câu.

Trước việc lớn, báo ngắn cách hiểu và đầu ra sẽ làm. Khi được yêu cầu chỉ sửa prompt, trả prompt, không thực hiện luôn nhiệm vụ nằm trong đó. Script chỉ ghép các chỉ dẫn và kiểm tra khai báo; bước làm rõ ý nghĩa do mô hình thực hiện trong chat.

## Các trạng thái trong công cụ

| Trạng thái | Nguyên nhân | Được làm |
| --- | --- | --- |
| clarify | Thiếu thông tin liên quan hoặc có câu hỏi chặn công việc | Đọc đầu vào để làm rõ, hỏi và ghi nhận câu trả lời |
| confirm | Đủ trường cần thiết nhưng thiếu xác nhận hiện hành | Trình bày cách hiểu và đợi người viết xác nhận |
| ready | Có tóm tắt, xác nhận đúng hồ sơ và không còn câu hỏi chặn task | Thực hiện phạm vi đã được xác nhận |
| prompt_only | Chỉ yêu cầu tối ưu prompt | Sửa prompt, không thực hiện luận văn bên trong |

`project_gate.py` đọc hồ sơ khai báo, không gọi mô hình và không tự ghi xác nhận. Nó không thể chứng minh người dùng thật sự đã nói câu xác nhận hoặc mô hình đã hiểu đúng. Chỉ lưu `message` sau khi có câu trả lời thực tế, gắn với tóm tắt đã trình bày. Nếu file chứa khai báo sai, script không thay thế việc đọc và đối chiếu thực tế.

Mọi sửa đổi `project.json` hoặc bản tóm tắt `brief_summary` làm fingerprint tương ứng thay đổi; xác nhận cũ không còn mở bước triển khai. Với tài liệu ngoài thay nội dung nhưng tên không đổi, tăng `context_revision`. Với điểm chưa rõ phát sinh trong lúc làm, ghi câu hỏi chặn tương ứng trong `project_state.json`. Hash hồ sơ không tự phát hiện mọi thay đổi hoặc mâu thuẫn ngữ nghĩa của tài liệu/yêu cầu tự do; mô hình vẫn cần đối chiếu nội dung thật ở mỗi lượt.

## Ví dụ diễn biến

- Người viết yêu cầu “viết phần II” nhưng chưa rõ phần II của đề nào: hỏi đúng đề/phần, chưa viết theo dự án cũ.
- Người viết xác định đề, dữ liệu và đầu ra, nhưng chưa xác nhận tóm tắt: đưa tóm tắt, chưa triển khai.
- Đã xác nhận toàn ASM, tiếp tục mục tiếp theo không đổi phạm vi: làm tiếp, không hỏi lại doanh nghiệp và chuẩn nguồn.
- Đến bước phân tích phát hiện thiếu mã biến hoặc hai output mâu thuẫn: dừng phần phân tích liên quan, hỏi để giải quyết.
- Chỉ yêu cầu sửa câu prompt: tối ưu câu đó; không bắt đầu làm bài được nhắc trong prompt.
