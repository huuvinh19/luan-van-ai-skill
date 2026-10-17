# Ví dụ kiểm thử hồ sơ

`demo-project/` là tình huống do repo tạo để minh họa, không phải luận văn thật và không chứa nguồn học thuật được bịa ra. Dữ liệu gồm 3 giá trị 10, 20, 30; trung bình 20 được tính khi tạo ví dụ.

Nhận định C001 là kết quả tính toán từ dữ liệu minh họa, không phải thông tin của một bài báo. Bảng nguồn vì vậy rỗng. Yêu cầu R001 cũng là yêu cầu giả lập cho ví dụ công cụ, không phải rubric BTEC.

Bản 1.1.0 có project_state.json với bản tóm tắt và câu xác nhận GIẢ LẬP cho unit test. Đây là dữ liệu kiểm thử rõ nhãn, không phải lời xác nhận thật của người viết hay cho phép chạy một luận văn thực tế. Khi làm dự án thật, lấy xác nhận từ cuộc trò chuyện thực tế.

```bash
python scripts/audit_project.py --project examples/demo-project
```

Báo cáo `clear` ở ví dụ chỉ nói hồ sơ minh họa không có lỗi cấu trúc được script phát hiện. Script không thực thi lại phép tính hoặc chứng nhận bài đạt yêu cầu học thuật. Khi làm bài thật, thay bằng đề, nguồn, dữ liệu và kết quả thực tế.
