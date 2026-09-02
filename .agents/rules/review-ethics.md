# RÀNG BUỘC ĐẠO ĐỨC PHẢN BIỆN KHOA HỌC (COPE / SPRINGER / IEEE)

1. **BẮT BUỘC KIỂM TRA CHÍNH SÁCH AI:**
   Chạy `python scripts/verify_ai_compliance.py --journal <id> --action <hanh_dong>`
   TRƯỚC KHI đưa bất kỳ nội dung nào từ bản thảo vào AI. Nếu script trả về lỗi (exit code != 0),
   TỪ CHỐI thực hiện — chỉ cung cấp checklist để reviewer con người tự đối soát.

2. **KHÔNG CÓ TẠP CHÍ NÀO "DỄ TÍNH HƠN" VỀ BẢO MẬT BẢN THẢO:**
   Mọi tạp chí mặc định nghiêm ngặt như nhau: CẤM upload bản thảo hoặc thông tin trích xuất
   vào GenAI đám mây trừ khi trường `ai_policy` có `source_url` chính thức xác nhận khác.

3. **BẢO MẬT PII & ẨN DANH HÓA CỤC BỘ:**
   Không bao giờ đọc trực tiếp file trong `manuscripts/raw/` — chỉ đọc qua bản đã ẩn danh
   trong `manuscripts/anonymized/` và reviewer vẫn phải tự kiểm tra lại bằng mắt.

4. **KHAI BÁO MINH BẠCH (DISCLOSURE):**
   Nếu có dùng AI (dù chỉ để sửa văn phong nhận xét riêng), bắt buộc khai báo trong
   `FINAL_REVIEW_REPORT.md` mục Confidential Comments to Editor theo đúng yêu cầu của tạp chí.
