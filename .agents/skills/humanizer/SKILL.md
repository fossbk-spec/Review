---
name: humanizer
description: |
  Viết lại văn phong AI (AI-sounding text) thành văn phong tự nhiên của con người, giữ nguyên 100% dữ kiện, số liệu, công thức, mã code, YAML frontmatter và trích dẫn [@citekey]. Dựa trên 35 mẫu nhận diện AI của Wikipedia AI Cleanup.
license: MIT
metadata:
  version: "2.11.2"
---

# Humanizer: Tự nhiên hóa Văn phong & Loại bỏ Dấu hiệu AI

Kỹ năng này viết lại các đoạn văn bản học thuật/kỹ thuật do AI sinh ra để giọng văn tự nhiên, cô đọng, súc tích như chuyên gia con người viết — **loại bỏ mùi văn mẫu AI mà không làm thay đổi bản chất dữ kiện, thông tin hay làm sai lệch sự thật**.

---

## 1. Ba Ràng buộc An toàn Bắt buộc trong Pipeline Sách

1. **Giữ nguyên 100% dữ kiện & cấu trúc kỹ thuật:**
   - Tuyệt đối không thay đổi: Heading (`#`, `##`, `###`), trích dẫn `[@citekey]`, công thức LaTeX (`$`, `$$`), khối code (```` ``` ````), bảng biểu Markdown và YAML Frontmatter.
   - Không bịa thêm số liệu, ngày tháng, tên tác giả hay trích dẫn.
2. **Quy tắc thứ tự trong Pipeline:**
   - Chạy `Humanizer` **TRƯỚC** khi chạy `technical_qa_audit.py`.
   - Lớp QA kỹ thuật luôn là cổng gác cuối cùng để đảm bảo 100/100 điểm trước khi xuất bản.
3. **Giữ phong cách học thuật súc tích:**
   - Đối với sách chuyên khảo/tham khảo: giữ văn phong trung lập, trực diện, chuyên nghiệp; không thêm từ cảm thán hay văn phong chat.

---

## 2. Các Mẫu Dấu hiệu AI Phổ biến Cần Xử lý (35 Patterns)

### A. Nội dung & Phóng đại
- **Cắt bỏ tuyên bố tầm vóc sáo rỗng:** Bỏ các cụm *"đóng vai trò là trục xương sống"*, *"mở ra một kỷ nguyên mới"*, *"đánh dấu bước ngoặt lịch sử"*, *"là minh chứng cho"* -> thay bằng câu trần thuật trực diện.
- **Cắt bỏ phân tích nông cạn bằng từ nối liên tiếp:** Bỏ *"nhằm thúc đẩy..., tạo điều kiện..., phản ánh mối liên kết..."*.
- **Cắt bỏ văn phong quảng cáo:** Bỏ *"đột phá"*, *"vô cùng phong phú"*, *"tuyệt vời"*.
- **Loại bỏ viện dẫn mơ hồ:** Bỏ *"Nhiều chuyên gia cho rằng..."*, *"Các nhà phân tích nhận định..."* trừ khi có trích dẫn `[@citekey]` cụ thể.

### B. Từ vựng & Cấu trúc Ngữ pháp
- **Tránh từ vựng AI lạm dụng:** *"thực tế là"*, *"ngoài ra"*, *"cần nhấn mạnh rằng"*, *"bức tranh tổng thể"*, *"bản chất là"*.
- **Dùng động từ trực tiếp:** Thay vì *"đóng vai trò là..."*, dùng *"là..."*, *"gồm..."*, *"thực hiện..."*.
- **Bỏ nhóm-ba-từ gượng ép:** Tránh gom các bộ ba đồng nghĩa sáo rỗng (*"sáng tạo, đổi mới và toàn diện"*).
- **Bỏ câu phủ định lửng:** Bỏ *"Không chỉ là X, mà còn là Y"*, *"không cần suy đoán"*.

### C. Định dạng & Chatbot
- **Loại bỏ gạch ngang dài (em-dash `—`):** Thay bằng dấu chấm, phẩy hoặc ngoặc đơn phù hợp ngữ cảnh tiếng Việt.
- **Bỏ Emoji & Bolding quá mức:** Không dùng icon/emoji trong văn bản chuyên khảo.
- **Loại bỏ rác chatbot:** Bỏ các câu mở đầu/kết thúc kiểu chatbot (*"Hy vọng điều này giúp ích!"*, *"Hãy cùng đi sâu vào..."*).

---

## 3. Cách sử dụng

```text
/humanizer

Humanize phần văn xuôi thân bài của file chapters/chXX_*.md — giữ nguyên toàn bộ
heading, citekey [@...], khối code, bảng biểu, công thức LaTeX và YAML frontmatter.
```
