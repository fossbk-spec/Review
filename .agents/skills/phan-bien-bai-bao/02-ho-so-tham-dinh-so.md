# Hồ sơ Thẩm định Số — `journal_profiles/<id>.json`

## Vì sao cần cấu hình riêng từng tạp chí

Mỗi tạp chí có triết lý bình duyệt khác hẳn nhau — áp dụng sai rubric là lỗi phản biện thực chất, không chỉ lỗi hình thức. Ví dụ đối lập trực tiếp:
- **IEEE JBHI** (kỹ thuật): đặt nặng tính mới giải thuật, bắt buộc Ablation Study.
- **Discover Computing** (Springer Nature): tuyên bố rõ trong hướng dẫn *"We do not ask reviewers to assess the significance of the research"* — **không được** chê bài báo "thiếu tính đột phá".

Dùng nhầm rubric IEEE cho một bài Discover Computing sẽ tạo ra phản hồi sai yêu cầu của tạp chí.

## Schema chuẩn

```json
{
  "journal_id": "ieee_jbhi",
  "journal_name": "IEEE Journal of Biomedical and Health Informatics",
  "publisher": "IEEE",
  "aims_and_scope": "...",
  "review_dimensions": [
    {
      "dimension_id": "DIM_01",
      "name": "Technical Novelty & Mathematical Soundness",
      "weight": "Critical (30%)",
      "criteria": ["...", "..."]
    }
  ],
  "decision_thresholds": {
    "accept": "...", "minor_revision": "...", "major_revision": "...", "reject": "..."
  },
  "ai_policy": {
    "reviewers_may_upload_manuscript_content_to_ai": false,
    "own_prose_polish_allowed": true,
    "declaration_required_for_own_prose_polish": true,
    "source_url": "URL trang chính sách chính thức đã đọc — bắt buộc điền, không để trống"
  }
}
```

### ⚠️ Đã sửa: bỏ hệ thống "nhóm tạp chí dễ tính / khó tính" — mặc định nghiêm ngặt cho MỌI tạp chí

Một thiết kế trước đó phân tạp chí thành nhiều nhóm với mức độ cho phép AI khác nhau (ví dụ coi nhóm IEEE/ACM/Elsevier là "cho phép có điều kiện, chỉ cần khai báo"). **Đã tra cứu trực tiếp và xác minh điều này sai** — nhiều nguồn chính thức (IEEE RAS, IEEE CASS/AESS, Elsevier qua CASRAI) đều dùng ngôn ngữ nghiêm ngặt gần như tuyệt đối:

> IEEE: *"Using AI is NOT allowed"* cho việc review. Ngoại lệ duy nhất, phạm vi rất hẹp: sửa ngữ pháp/văn phong **của chính đoạn đánh giá reviewer đã tự viết xong** — và với đúng phạm vi hẹp này, IEEE ghi rõ *"Disclosure... is recommended but not required"*.
>
> Elsevier: *"Reviewers must not upload a manuscript, or any part of it, to a generative AI tool."* Cùng phạm vi hẹp: chỉ cho phép *"improving the language of a reviewer's own report"*.

Một nguồn tổng hợp chính sách nhiều nhà xuất bản kết luận: *"Nearly universal prohibition on uploading manuscripts to AI tools due to confidentiality concerns"* — tức **hầu hết nhà xuất bản lớn hội tụ về cùng một chuẩn nghiêm ngặt**, khác biệt thực tế duy nhất là **có bắt buộc khai báo hay không** cho đúng phạm vi hẹp "sửa văn phong đoạn đánh giá đã tự viết" — không phải khác biệt về việc bản thảo có được đưa vào AI hay không.

**Nguyên tắc thiết kế mới:** mọi hồ sơ `journal_profiles/*.json` mặc định `reviewers_may_upload_manuscript_content_to_ai: false` — **không có tạp chí nào được coi là "dễ tính hơn"** trừ khi đã đọc trực tiếp chính sách của đúng tạp chí đó và xác nhận khác. Trường `declaration_required_for_own_prose_polish` mới là điểm khác biệt thực sự giữa các tạp chí (Springer Nature yêu cầu khai báo cả cho việc sửa văn phong riêng của reviewer; IEEE thì không bắt buộc — nhưng cả hai đều **cấm đưa nội dung bản thảo vào AI**).

**Trường `ai_policy` bắt buộc điền trước khi dùng hồ sơ này, không suy đoán từ tạp chí khác dù cùng publisher.** Xem `03-tuan-thu-dao-duc-xuat-ban.md`.

## Ví dụ: Discover Computing — mô hình "Sound Science", khác hẳn tạp chí kỹ thuật

```json
{
  "journal_id": "discover_computing",
  "journal_name": "Discover Computing",
  "publisher": "Springer Nature",
  "editorial_model": "Sound Science / Technical Validity",
  "evaluation_rules": {
    "assess_significance": false,
    "assess_novelty": false,
    "max_revision_workload_days": 10,
    "allow_major_experimental_requests": false
  },
  "core_checkpoints": [
    {"checkpoint_id": "CHK_01_OVERCLAIMING", "focus": "Rewrite overstated conclusions"},
    {"checkpoint_id": "CHK_02_LIMITATIONS", "focus": "Explain the limitations of the work"},
    {"checkpoint_id": "CHK_03_DATA_ACCURACY", "focus": "Text matches what data actually show"},
    {"checkpoint_id": "CHK_04_FUNDAMENTAL_FLAWS", "focus": "Soundness check (reject criteria)"}
  ],
  "decision_framework": {
    "reject_if": "Fundamentally flawed methodology, invalid data interpretation, unfixable errors.",
    "revise_if": "Sound but needs essential revisions doable within 10 days."
  },
  "ai_policy": {
    "reviewers_may_upload_manuscript_content_to_ai": false,
    "own_prose_polish_allowed": true,
    "declaration_required_for_own_prose_polish": true,
    "source_url": "https://link.springer.com/brands/discover/policies"
  }
}
```

## Ví dụ: IEEE — cùng mức nghiêm ngặt, khác ở yêu cầu khai báo

```json
{
  "journal_id": "ieee_jbhi",
  "journal_name": "IEEE Journal of Biomedical and Health Informatics",
  "publisher": "IEEE",
  "ai_policy": {
    "reviewers_may_upload_manuscript_content_to_ai": false,
    "own_prose_polish_allowed": true,
    "declaration_required_for_own_prose_polish": false,
    "source_url": "https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/#ai-generated-text"
  }
}
```
Khác biệt duy nhất so với Discover Computing: IEEE **không bắt buộc** khai báo cho việc sửa văn phong đoạn đánh giá reviewer tự viết (`declaration_required_for_own_prose_polish: false`) — nhưng cấm đưa nội dung bản thảo vào AI **giống hệt nhau**.

## Quy trình tạo hồ sơ mới cho một tạp chí chưa có

1. Tải Guidelines chính thức từ trang tạp chí (không dùng bản tổng hợp thứ cấp).
2. Đọc trực tiếp — không chỉ để AI tóm tắt — ít nhất phần "Aims & Scope" và phần chính sách AI/đạo đức.
3. Điền schema trên, đặc biệt `ai_policy.source_url` phải trỏ đúng trang đã đọc.
4. Lưu vào `journal_profiles/<id>.json`, không tái sử dụng hồ sơ tạp chí khác làm mẫu nếu chưa xác nhận cùng chính sách.
