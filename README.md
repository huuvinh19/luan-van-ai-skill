# Luận Văn AI Skill

Bộ hướng dẫn tiếng Việt giúp AI hỗ trợ luận văn: hỏi rõ dự án trước khi làm, tự chuẩn hóa prompt, nghiên cứu có căn cứ, viết và sửa bài, kiểm tra trích dẫn, phản biện và tự rà công tâm. Ưu tiên Marketing; ngành, trường và yêu cầu cụ thể do người học cung cấp.

## Dùng bằng link, không cần tải hay giải nén

Gửi AI có khả năng đọc web câu lệnh sau:

```text
Đọc và áp dụng SKILL.md tại https://github.com/huuvinh19/luan-van-ai-skill cho dự án luận văn này. Trước khi viết hoặc phân tích, đọc tài liệu tao gửi, hỏi những điểm chưa rõ có ảnh hưởng đến công việc, rồi tóm tắt cách hiểu để tao xác nhận. Giữ các yêu cầu đã chốt xuyên suốt dự án; khi có thay đổi, hỏi lại đúng phần bị ảnh hưởng. Nếu không đọc được link, nói rõ và yêu cầu tao dán nội dung, đừng giả vờ đã đọc.
```

**Điểm bắt đầu cho AI: [SKILL.md](SKILL.md).** Đây là bản hướng dẫn đầy đủ trong một tệp, không cần mở ZIP, cài Python hoặc đọc toàn bộ repo để bắt đầu.

- [Đọc SKILL.md trên GitHub](https://github.com/huuvinh19/luan-van-ai-skill/blob/main/SKILL.md)
- [Đọc văn bản thuần (Raw)](https://raw.githubusercontent.com/huuvinh19/luan-van-ai-skill/main/SKILL.md)
- [Hướng dẫn cho coding agent](AGENTS.md)

AI cần thực sự truy cập được nội dung link. Nếu chatbot không có khả năng đọc URL, mở `SKILL.md` và dán nội dung vào chat. Đọc link chỉ áp dụng hướng dẫn trong ngữ cảnh đang làm; không tự cài skill vĩnh viễn hay bảo đảm mọi mô hình tuân thủ giống nhau.

## AI cần làm gì sau khi đọc?

1. Nêu ngắn phạm vi đã hiểu; hỏi tối đa 3 điểm chưa rõ quan trọng mỗi lượt. Không viết luận văn theo giả định khi còn thiếu thông tin làm thay đổi cách làm.
2. Khi đã rõ, tóm tắt dự án, công việc, đầu vào và đầu ra để người viết xác nhận; sau đó thực hiện trong phạm vi đã giao.
3. Tự làm rõ mỗi yêu cầu mới, kiểm chứng nhận định, viết có phân tích và trích dẫn Harvard theo mẫu giảng viên; chuyển đồng bộ sang APA nếu được yêu cầu.
4. Phản biện bằng căn cứ, giữ giọng học thuật trong bài nộp và tự rà trước khi giao. Báo riêng phần chưa xác minh.

Nếu dự án đã được xác nhận trong cuộc trò chuyện, dùng lại thông tin còn hiệu lực; không bắt đầu lại cuộc phỏng vấn. Không suy ra đề tài, mã môn, trường hoặc rubric từ repo.

## Thành phần

| Tệp / thư mục | Công dụng |
| --- | --- |
| [SKILL.md](SKILL.md) | Điểm vào chung, đủ quy tắc để AI dùng trực tiếp bằng link |
| [skills/academic-research-vietnamese](skills/academic-research-vietnamese/SKILL.md) | Quy trình nghiên cứu, viết và chấm sửa học thuật |
| [skills/prompt-optimizer](skills/prompt-optimizer/SKILL.md) | Tối ưu prompt theo yêu cầu, giữ ý định và biến |
| [skills/candid-academic-mentor](skills/candid-academic-mentor/SKILL.md) | Phản biện có căn cứ, giọng trao đổi phù hợp và tự rà công tâm |
| [thesis-workbench](thesis-workbench/README.md) | 15 công đoạn/chế độ, mẫu hồ sơ và công cụ Python tùy chọn |

Không cần gọi riêng ba skill để dùng quy trình chung: các quy tắc cốt lõi đã có trong `SKILL.md`. Chỉ đọc module chuyên sâu khi công việc cần.

## Kiểm tra và cập nhật

```bash
python scripts/build_skill.py --check
python thesis-workbench/scripts/verify_repo.py
python -m unittest discover -s thesis-workbench/tests -v
```

Sau khi sửa quy tắc nguồn, chạy `python scripts/build_skill.py` để cập nhật cả hai bản tổng. Công cụ kiểm tra tính nhất quán của mã và hồ sơ; chất lượng bài luận còn phụ thuộc dữ liệu, nguồn, rubric và việc AI thực hiện đúng hướng dẫn.

## Nguồn và giấy phép

Tham khảo [f/prompts.chat](https://github.com/f/prompts.chat), [linshenkx/prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) và Academic Research Skills. Attribution, snapshot và giấy phép từng thành phần được giữ tại [LICENSES.md](LICENSES.md), tài liệu provenance và các thư mục nguồn. Các mẫu nghiên cứu là dữ liệu giả lập có ghi nhãn; không phải kết quả nghiên cứu thật.
