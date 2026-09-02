---
name: peer-review
description: Chạy trọn 1 chu trình phản biện 1 bài báo khoa học chuẩn quốc tế
---
1. Đặt bản thảo gốc vào `manuscripts/raw/<id>.pdf`
2. Chạy ẩn danh hóa cục bộ:
   `python scripts/anonymize_manuscript.py manuscripts/raw/<id>.pdf`
   -> Xuất ra `manuscripts/anonymized/<id>.md`
3. Kiểm tra chính sách AI của tạp chí:
   `python scripts/verify_ai_compliance.py --journal <journal_id> --action manuscript_content_to_ai`
   -> Nếu FAIL: Chỉ dùng checklist thủ công, KHÔNG nạp nội dung vào AI.
   -> Nếu PASS: Tiếp tục bước 4.
4. Macro Audit (Đối chiếu Scope & Checklist quốc tế TRIPOD-AI, CONSORT-AI).
5. Micro Technical Audit (Rà soát toán học, data split, overclaiming).
6. Kiểm tra quyền sửa văn phong:
   `python scripts/verify_ai_compliance.py --journal <journal_id> --action own_prose_polish`
7. Xuất bản `FINAL_REVIEW_REPORT.md` (Comments to Author & Confidential to Editor kèm AI Disclosure).
