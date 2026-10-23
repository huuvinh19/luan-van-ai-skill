# Chọn prompt và giữ bộ nhớ dự án

Áp dụng luồng bắt buộc: hỏi bối cảnh → chọn và giữ prompt → lấy đề, tiêu chí, mục tiêu → bóc tách yêu cầu → lập dàn ý → xác nhận cách hiểu → thực hiện và đối chiếu. Trong chat chỉ có văn bản, thực hiện cùng quy trình bằng một hồ sơ ngắn trong ngữ cảnh; không cần chạy script.

## Chọn prompt trước khi xin bộ đề

Sau khi biết môn/ngành và việc đang cần hỗ trợ, tự chọn prompt chính theo công việc thực tế. Nếu chưa biết việc cần làm, hỏi một câu về công đoạn hoặc chọn prompt tiếp nhận tạm thời; chưa tự chọn đề tài/phương pháp. Không bắt người dùng tự biết hay chọn tên prompt.

| Việc hiện tại | Prompt/module chính |
| --- | --- |
| Chưa rõ dự án, đọc đề | intake hoặc clarify |
| Bóc tách đề, lập kế hoạch | outline |
| Tìm/đọc/tổng hợp nguồn | sources hoặc literature |
| Thiết kế nghiên cứu, phân tích dữ liệu | methodology hoặc analysis |
| Viết, chấm sửa bài | draft hoặc review |
| Rà nguồn, dịch, hoàn thiện tệp | citations, translate hoặc export |
| Chỉ sửa prompt | optimize, không thực hiện bài nằm trong prompt |

Đọc module được chọn và kết hợp với quy tắc chung. Nếu chỉ có tệp này mà không mở được module, tự soạn prompt làm việc tương đương theo yêu cầu thực tế, ghi rõ là bản soạn tại chỗ; không nhận đã đọc tệp chưa truy cập được. Không dùng nguyên prompt nguồn còn chứa doanh nghiệp, dữ liệu hoặc ví dụ của dự án khác.

Giữ bản prompt thực sự dùng, công đoạn và lý do chọn trong `active_prompt`. Đây là chỉ dẫn công việc có thể đưa người dùng xem, không phải suy nghĩ nội bộ. Không chỉ lưu tên prompt hoặc câu “đã ghi nhớ”. Báo ngắn: “Tao chọn prompt … để …; tao sẽ dùng nó cùng hồ sơ yêu cầu của dự án này.” Không cần in toàn bộ prompt trừ khi được yêu cầu. Đổi công đoạn thì chọn module thích hợp, giữ yêu cầu dự án còn hiệu lực; chỉ làm rõ lại khi phạm vi/ý nghĩa thay đổi.

Sau khi chọn và giữ prompt, hỏi: “Tao cần mày cung cấp: câu hỏi/đề bài; tiêu chí chấm bài nếu có; mục tiêu muốn đạt được.” Đọc những gì đã gửi và chỉ hỏi phần còn thiếu, không đòi gửi lại. Ghi mục tiêu riêng với tiêu chí bắt buộc: mong đạt D không chứng minh đã đạt D. Nếu chưa có rubric, ghi đúng là chưa có; với việc nhỏ tự xác định, ghi phạm vi và tiêu chí người dùng thực sự chọn, không bịa yêu cầu giảng viên.

## Bóc từng yêu cầu thành dàn ý có căn cứ

Khi đủ thông tin ảnh hưởng bước hiện tại, đọc từng câu/mệnh đề và tách thành các yêu cầu nguyên tử có mã R1, R2…: động từ phải thực hiện, nội dung/đối tượng, phạm vi, mức phân tích, bằng chứng, giới hạn và cách kiểm tra. Giữ vị trí/câu gốc làm căn cứ, phân biệt bắt buộc với gợi ý. Giữ cả điều kiện nhỏ như “hai biến”, “so sánh”, “giải thích hạn chế”, số từ, hình/bảng và nguồn. Không tự tách một câu thành yêu cầu ngoài ý đề.

Lập dàn ý theo từng mục của đề. Mỗi mục ghi mã yêu cầu đáp ứng, ý phân tích cần có và bằng chứng cần dùng/chưa có. Kiểm tra cả hai chiều: mọi yêu cầu bắt buộc có mục đáp ứng; mỗi mục có lý do thuộc phạm vi. Không lập dàn ý chung chung trước rồi ép đề vào. Với nhiệm vụ chỉ một đoạn, dàn ý có thể là vài ý ngắn; không ép thành cả chương. Nếu đang sửa bài có sẵn, lập bản đồ cấu trúc bài hiện tại với đề trước khi sửa, giữ phần đúng và sửa phần thiếu.

Lưu bảng yêu cầu và dàn ý vào `project_memory`, rồi tóm tắt cách hiểu và lấy xác nhận trước lần viết/phân tích đầu tiên. Được bóc tách đề và lập dàn ý chuẩn bị trước bước xác nhận; chưa viết kết quả nghiên cứu. Mọi yêu cầu bắt buộc chưa được ánh xạ hoặc còn mâu thuẫn phải được xử lý trước phần viết bị ảnh hưởng.

## Bộ nhớ dùng xuyên suốt cuộc chat

Hồ sơ hiện hành gồm: môn/ngành; mục tiêu và phạm vi; prompt được chọn; đề/rubric và vị trí căn cứ; yêu cầu R1…; dàn ý liên kết yêu cầu; quyết định đã xác nhận; dữ liệu/nguồn và trạng thái kiểm chứng; câu hỏi mở; lỗi đã gặp cùng cách tránh. Dùng `project.json`, `project_state.json` và `progress.md` khi có thao tác tệp. Nếu dùng `requirements.csv`, giữ cùng mã yêu cầu với hồ sơ hiện hành. Không ghi dữ liệu dự án riêng vào repo/skill công khai.

Trước mỗi lần viết, sửa, dịch hoặc trả kết quả, đọc lại phần hồ sơ liên quan và đối chiếu: yêu cầu gốc → mục dàn ý → đoạn/bằng chứng thực tế. Dàn ý là công cụ đối chiếu; đề và rubric vẫn là căn cứ quyết định. Sửa dàn ý khi phát hiện nó bỏ sót hoặc hiểu sai đề. Kiểm tra lại các lỗi từng mắc, nhất là số liệu, trích dẫn, phạm vi và điều đã bị giảng viên nhắc; cập nhật lỗi/cách sửa vào `known_errors` hoặc tiến độ. Không báo “đã đạt” chỉ vì bảng tự ghi covered.

Khi có yêu cầu mới, cập nhật hồ sơ, yêu cầu và dàn ý bị ảnh hưởng; đánh dấu bản cũ không còn áp dụng thay vì giữ hai chỉ dẫn mâu thuẫn. Không hỏi lại điều đã chốt còn hiệu lực. Khi đổi chat, xuất bản bàn giao gồm prompt và hồ sơ hiện hành để mang sang; đọc lại trước khi tiếp tục. Chỉ nhận đã lưu tệp khi thật sự lưu được. “Bộ nhớ” là hồ sơ trong ngữ cảnh/tệp của dự án, không phải sửa trọng số mô hình hoặc bảo đảm nhớ vĩnh viễn qua mọi chat.
