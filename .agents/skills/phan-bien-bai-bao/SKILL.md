---
name: phan-bien-bai-bao
description: Quy trình phản biện bài báo khoa học đa tạp chí trên Google Antigravity — chuyển hướng dẫn phản biện (Reviewer Guidelines) của từng tạp chí thành Hồ sơ Thẩm định Số (journal_profiles/*.json), chạy pipeline 4 tầng an toàn để tạo báo cáo phản biện chuẩn quốc tế. ĐẶC BIỆT QUAN TRỌNG: Khung tuân thủ đạo đức xuất bản (COPE/Springer Nature/Elsevier/IEEE) được đặt lên đầu vì hầu hết tạp chí cấm tuyệt đối việc nạp bản thảo hoặc thông tin trích xuất của người khác vào AI. Dùng khi người dùng nhận lời phản biện (peer review) cho một tạp chí cụ thể — KHÔNG dùng cho việc viết bài của chính mình (dùng skill `viet-bai-bao-khoa-hoc`).
---

# Phản biện Bài báo Khoa học Đa Tạp chí (Journal Peer Review)

> [!CAUTION]
> ### ⚠️ RÀNG BUỘC ĐẠO ĐỨC XUẤT BẢN & BẢO MẬT BẢN THẢO (ĐỌC ĐẦU TIÊN)
> **Bản thảo khoa học gửi phản biện là tài liệu MẬT (Confidential Document).**  
> Theo điều lệ chính thức của các nhà xuất bản hàng đầu thế giới (**Springer Nature, Elsevier, Nature Portfolio, IEEE, COPE**):
> 1. **CẤM TUYỆT ĐỐI** việc tải toàn văn bản thảo, hoặc **BẤT KỲ THÔNG TIN TRÍCH XUẤT NÀO** (công thức toán học, trích đoạn văn bản, bảng số liệu thực nghiệm, đoạn mã nguồn) vào bất kỳ công cụ AI tạo sinh nào (*GenAI/LLMs*). Việc nạp dữ liệu của người khác lên đám mây công cộng bị coi là hành vi vi phạm nghiêm trọng thỏa thuận bảo mật học thuật (*Breach of Confidentiality*).
> 2. **BẮT BUỘC KHAI BÁO:** Nếu có sử dụng bất kỳ công cụ hỗ trợ nào (ví dụ: công cụ kiểm tra chính tả cục bộ hoặc phần mềm phân tích mã nguồn), reviewer **bắt buộc phải khai báo minh bạch** trong phần *Ý kiến kín gửi riêng Tổng biên tập (Confidential Comments to the Editor)*.
> 3. **TRÁCH NHIỆM CUỐI CÙNG:** Reviewer chịu trách nhiệm 100% về tính xác thực, công tâm và khoa học của bản nhận xét. AI không bao giờ được phép thay thế phán đoán chuyên môn của con người.
> 
> 👉 **Quy tắc thực thi:** Trước khi thực hiện bất kỳ thao tác nào, bắt buộc phải kiểm tra trường `ai_policy` trong tệp `journal_profiles/<id>.json` của tạp chí đó.

---

## 1. Khi Nào Kích Hoạt Skill Này

* Khi nhận lời mời phản biện (*Peer Review*) từ Ban biên tập một tạp chí khoa học quốc tế.
* Cần chuyển đổi hướng dẫn phản biện (*Reviewer Guidelines / Rubrics*) của tạp chí thành hồ sơ thẩm định chuẩn hóa để đánh giá bài báo một cách khách quan, hệ thống.
* Cần xử lý phản biện cho nhiều tạp chí có triết lý bình duyệt khác nhau (ví dụ: *IEEE JBHI* đòi hỏi tính đột phá giải thuật, trong khi *Discover Computing* của Springer Nature tuyên bố rõ *"không đánh giá tính mới/tầm quan trọng mà chỉ thẩm định tính đúng đắn phương pháp"*).

> [!IMPORTANT]
> **PHÂN BIỆT RÕ VAI TRÒ:**  
> * Dùng skill **`phan-bien-bai-bao`**: Khi bạn đóng vai trò là **Người phản biện (Reviewer)** thẩm định bài của người khác.
> * Dùng skill **`viet-bai-bao-khoa-hoc`**: Khi bạn là **Tác giả (Author)** viết bài báo của chính mình để nộp đăng.

---

## 2. Trường `ai_policy` Bắt Buộc trong Schema `journal_profiles/*.json`

Để ngăn chặn việc áp dụng nhầm chính sách đạo đức giữa các tạp chí khác nhau, mọi tệp hồ sơ tạp chí trong `journal_profiles/<id>.json` **bắt buộc phải khai báo trường `ai_policy`** ở cấp độ cao nhất:

```json
{
  "$schema": "https://hdbs.academic/schemas/journal_profile_v2.json",
  "journal_id": "discover_computing",
  "journal_name": "Discover Computing",
  "publisher": "Springer Nature",
  "issn": "2948-3107",
  
  "ai_policy": {
    "reviewer_ai_usage": "strictly_prohibited",
    "manuscript_upload_policy": "prohibited_entire_and_extracted",
    "rationale": "Springer Nature cấm tuyệt đối việc đưa bản thảo hoặc bất kỳ thông tin trích xuất nào (công thức, code, data) vào GenAI để bảo vệ quyền tác giả và bí mật học thuật.",
    "disclosure_required": true,
    "disclosure_target": "Confidential Comments to the Editor",
    "publisher_policy_url": "https://www.springernature.com/gp/reviewers/peer-review-policy"
  },

  "review_philosophy": {
    "evaluate_novelty": false,
    "evaluate_methodological_soundness": true,
    "evaluate_data_integrity": true
  },
  
  "rubric_weights": {
    "methodology_rigor": 0.40,
    "data_code_transparency": 0.30,
    "reporting_limitations": 0.20,
    "presentation_clarity": 0.10
  }
}
```

### Các giá trị chuẩn của `reviewer_ai_usage`:
* `"strictly_prohibited"`: Cấm hoàn toàn mọi hình thức sử dụng AI cho bản thảo (Springer Nature, Nature Portfolio, Elsevier).
* `"conditional_with_disclosure"`: Cho phép hỗ trợ dịch thuật/văn phong với điều kiện ẩn danh hóa 100% và phải gửi báo cáo giải trình kèm theo cho Editor (IEEE).
* `"open_pilot"`: Các tạp chí thử nghiệm quy trình AI-assisted review có sự cấp phép rõ ràng trong thư mời review.

---

## 3. Pipeline 4 Tầng Thực thi An Toàn (Ethics-Compliant Pipeline)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: INGESTION CỤC BỘ & ẨN DANH HÓA TUYỆT ĐỐI (Local Only)         │
│ - Dùng `batch_ingestion.py` bóc tách văn bản trên máy local            │
│ - Tước bỏ 100% metadata: tên tác giả, đơn vị công tác, mã định danh    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 2: MACRO AUDIT THEO RUBRIC TẠP CHÍ & CHECKLIST QUỐC TẾ            │
│ - Đối chiếu Scope của `journal_profiles/<id>.json`                     │
│ - Quét danh mục chuẩn báo cáo: TRIPOD-AI, CONSORT-AI, PRISMA 2020      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 3: MICRO TECHNICAL AUDIT (Thẩm định Kỹ thuật Sâu)                 │
│ - Thẩm định Toán học, Data Leakage, Data Split, Overclaiming           │
│ - Chỉ xử lý các logic toán/kỹ thuật tổng quát đã tách khỏi dữ liệu nhạy cảm│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 4: CHUẨN HÓA VĂN PHONG PHẢN BIỆN CHUYÊN NGHIỆP (Tone Polish)      │
│ - Văn phong xây dựng, lịch lãm, chuẩn mực học thuật quốc tế            │
│ - Tách bạch: Comments to Authors vs. Confidential Comments to Editor   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Cấu trúc Mẫu Báo cáo Phản biện Chuẩn Quốc tế (Peer Review Report)

Mọi báo cáo phản biện do hệ thống xuất ra bắt buộc phải có cấu trúc 2 phần độc lập:

### PHẦN 1: Comments to the Author(s) (Gửi Tác giả)
1. **Summary of the Paper:** Tóm tắt khách quan đóng góp chính của bài báo (3–4 câu).
2. **General Evaluation:** Nhận xét tổng quan theo đúng tiêu chí của tạp chí.
3. **Major Comments (Vấn đề cốt lõi bắt buộc sửa):** Các lỗi về phương pháp luận, rò rỉ dữ liệu (Data Leakage), suy diễn kết luận quá mức (Overclaiming), thiếu sót trong đối chứng thực nghiệm.
4. **Minor Comments (Chi tiết kỹ thuật & Trình bày):** Lỗi chính tả, lỗi chú thích hình ảnh/bảng biểu, ký hiệu toán học chưa thống nhất.

### PHẦN 2: Confidential Comments to the Editor (Gửi riêng Tổng biên tập)
1. **Recommendation:** *Accept / Minor Revision / Major Revision / Reject*.
2. **Frank Assessment:** Đánh giá thẳng thắn về mức độ đóng góp thực chất của bài báo.
3. **AI Disclosure Statement (Bắt buộc):** Khai báo minh bạch việc sử dụng công cụ hỗ trợ theo đúng quy định tại trường `ai_policy` của tạp chí.

---

## 5. Danh mục File Tham chiếu Nâng cao

| Tệp tham chiếu | Nội dung & Vai trò |
| :--- | :--- |
| [`references/01-quy-trinh-4-tang.md`](references/01-quy-trinh-4-tang.md) | Chi tiết kỹ thuật quy trình 4 tầng thẩm định, đã chuẩn hóa lệnh Ingestion. |
| [`references/02-ho-so-tham-dinh-so.md`](references/02-ho-so-tham-dinh-so.md) | Hướng dẫn tạo và cấu hình `journal_profiles/*.json` cho từng tạp chí. |
| [`references/03-tuan-thu-dao-duc-xuat-ban.md`](references/03-tuan-thu-dao-duc-xuat-ban.md) | Tổng hợp điều lệ bảo mật bản thảo của Springer Nature, Elsevier, IEEE, COPE. |
| [`references/04-mau-bao-cao-phan-bien.md`](references/04-mau-bao-cao-phan-bien.md) | Template báo cáo chuẩn định dạng Markdown xuất PDF/Word gửi Ban biên tập. |
| [`checklist-humanize-review-report.md`](checklist-humanize-review-report.md) | **Checklist tự Humanize bằng tay** — Khử văn phong AI cho báo cáo mà không cần nạp text lên mạng. |
