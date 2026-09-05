---
name: anydoc
description: Công cụ và quy trình nạp, làm sạch và chuyển đổi hàng loạt tài liệu thô (PDF, DOCX, PPTX, TXT) thành Clean Markdown + bảng biểu và công thức LaTeX 100% cục bộ trên máy với 0 LLM token (Tầng 1 Local Ingestion Engine của HDBS). Dùng khi cần xử lý tài liệu tham khảo trong references/raw hoặc bản thảo thô trong chapters/drafts_raw, chuyển đổi sang Markdown chuẩn trước khi nạp cho Gemini/Claude.
---

# anydoc — Local Document Ingestion Engine (0 LLM Token)

`anydoc` là công cụ Tầng 1 (Local Ingestion & Smart Routing) trong kiến trúc **Hệ thống Biên soạn Giáo trình SSoT (HDBS)**. Chức năng cốt lõi là quét và chuyển đổi tự động toàn bộ tài liệu tham khảo thô cũng như các bản thảo chương cũ (.docx/.pdf) sang **Clean Markdown** trực tiếp trên máy cục bộ, không gửi ra ngoài internet và **tiêu tốn 0 token LLM**.

---

## 1. Khi nào kích hoạt Skill

Kích hoạt skill này khi:
* Cần nạp tài liệu tham khảo mới (PDF, DOCX, PPTX, TXT) vào `references/raw/`.
* Cần chuyển đổi các **bản thảo chương cũ** (Word/PDF bài giảng, tài liệu môn học cũ) trong `chapters/drafts_raw/` sang `chapters/drafts_clean/`.
* Cần làm sạch tài liệu thô thành Markdown chuẩn (Clean Markdown) trước khi tiến hành **Gap Analysis (Phân tích khoảng trống)** hoặc **Facts Extraction**.
* Cần bóc tách bảng biểu và cấu trúc tiêu đề từ tài liệu Word/PDF sang Markdown.
* Yêu cầu: "Chạy anydoc", "parse tài liệu raw", "làm sạch chương thô", "chuyển Word sang markdown", "ingest chapters".

---

## 2. Các thư mục quét tự động trong mỗi Project

```text
[PROJECT_ROOT]/
├── references/
│   ├── raw/                         <-- Chứa tài liệu tham khảo thô (PDF, DOCX)
│   │   └── paper_eeg_2024.pdf
│   └── clean_markdown/              <-- anydoc xuất Markdown tham khảo sạch kèm INDEX.md
│       ├── INDEX.md
│       └── paper_eeg_2024.md
│
└── chapters/
    ├── drafts_raw/                  <-- Chứa bản thảo chương thô ban đầu (Word/PDF bài giảng)
    │   ├── ch01_draft_goc.docx
    │   └── ch02_slide_bai_giang.pdf
    └── drafts_clean/                <-- anydoc xuất bản thảo chương sạch kèm INDEX.md
        ├── INDEX.md
        ├── ch01_draft_goc.md
        └── ch02_slide_bai_giang.md
```

---

## 3. Định dạng hỗ trợ & Quy tắc xử lý

| Định dạng | Engine xử lý cục bộ | Kết quả đầu ra |
|---|---|---|
| **DOCX** | `python-docx` | Chuẩn hóa Tiêu đề (`#`, `##`, `###`), danh sách, và bảng Markdown (`\| col1 \| col2 \|`). |
| **PDF** | `pypdf` | Bóc tách văn bản từng trang, loại bỏ header/footer rác, đánh dấu số trang `<!-- Trang X/Y -->`. |
| **TXT / MD** | Text Parser | Chuẩn hóa UTF-8, định dạng xuống dòng và gán YAML Frontmatter. |

Mọi tệp sau khi chuyển đổi đều được tự động gắn **YAML Frontmatter** chuẩn:
```markdown
---
source_file: "ch01_draft_goc.docx"
source_type: "DOCX"
parsed_by: "anydoc-v1.0"
parsed_at: "2026-09-01T08:45:00"
original_size_bytes: 1048576
---
```

---

## 4. Hướng dẫn chạy và Lệnh CLI

### Cách 1: Quét toàn bộ Project (Cả references và chapters) - Khuyên dùng
```powershell
python scripts/batch_ingestion.py
```
*(Hoặc dùng tham số rõ ràng: `python scripts/batch_ingestion.py --all`)*

### Cách 2: Chỉ quét thư mục Chapters / Drafts thô
```powershell
python scripts/batch_ingestion.py --chapters
```

### Cách 3: Chỉ quét thư mục References tài liệu tham khảo
```powershell
python scripts/batch_ingestion.py --references
```

### Cách 4: Ghi đè lại các tệp đã tồn tại
```powershell
python scripts/batch_ingestion.py --force
```

### Cách 5: Xử lý một tệp chương cụ thể
```powershell
python scripts/batch_ingestion.py -s "chapters/drafts_raw/ch01_draft.docx" -o "chapters/drafts_clean"
```

---

## 5. Tích hợp trong Chu trình 4 Tầng HDBS

```text
[references/raw/] + [chapters/drafts_raw/]
       │
       ▼ (Chạy anydoc: 0 Token, < 10 giây)
[references/clean_markdown/] + [chapters/drafts_clean/]
       │
       ▼ (Nạp cho Gemini Flash / Deep Research)
[reports/chXX_gap_report.md] + [knowledge_base/chXX_facts.json]
       │
       ▼ (Claude Sonnet / Opus biên soạn hoàn thiện 16 mục)
[chapters/chXX_ten_chuong.md]
```
