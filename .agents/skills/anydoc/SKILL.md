---
name: anydoc
description: Cong cu va quy trinh nap, lam sach va chuyen doi tai lieu tho (PDF, DOCX, PPTX, XLSX, CSV, TXT) thanh Clean Markdown theo kien truc Hai Dong Co (Dual-Engine Ingestion) gom batch_ingestion.py va @firecrawl/anydoc CLI. Chay cuc bo 100% tren may, 0 LLM token.
---

# anydoc: He thong Ingestion va Chuyen doi Tai lieu Cuc bo (0 LLM Token)

`anydoc` la cong cu Tang 1 (Local Ingestion & Smart Routing) trong kien truc Bien soan Giao trinh va Sach Tham khao (HDBS). Chuc nang cot loi la quet va chuyen doi tu dong toan bo tai lieu tham khao tho (`references/raw/`) cung nhu cac ban thao chuong cu (`chapters/drafts_raw/`) sang **Clean Markdown** (`clean_markdown/`, `drafts_clean/`) truc tiep tren may cuc bo, bao mat tuyet doi va **tieu ton 0 token LLM**.

Hien tai, he thong van hanh theo **Kien truc Hai Dong Co (Dual-Engine Ingestion Architecture)** ket hop giua script xu ly lo SSoT noi bo va cong cu ma nguon mo hieu nang cao `@firecrawl/anydoc`.

---

## 1. Kien truc Hai Dong Co (Dual-Engine Ingestion)

De toi uu hoa giua tinh tu dong hoa theo lo (Batch Automation) va toc do xu ly da dinh dang, quy trinh su dung 2 dong co bo tro cho nhau:

| Dac tinh | Dong co 1: Batch Pipeline SSoT (`batch_ingestion.py`) | Dong co 2: CLI Engine (`@firecrawl/anydoc`) |
|---|---|---|
| **Nguon goc** | Script Python noi bo cua project | Goi ma nguon mo Firecrawl (Rust engine) |
| **Cai dat** | Chay truc tiep qua Python (`python-docx`, `pypdf`) | `npm install -g @firecrawl/anydoc` (da cai san) |
| **Lenh thuc thi** | `python scripts/batch_ingestion.py [flags]` | `anydoc <input_file> -o <output.md>` |
| **Dinh dang manh** | `.docx`, `.pdf`, `.txt` | 14 dinh dang: `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.csv`, `.epub`, `.rtf`,... |
| **Dac diem noi bat** | Tu dong quet ca thu muc, sinh `INDEX.md`, tao YAML frontmatter chuan hoa co `chapter_title` | Toc do cuc nhanh (< 5ms), xu ly xuat sac slide PPTX, bang bieu XLSX/CSV, giu nguyen bang Markdown chuan |
| **Tinh huong dung** | Quet hang loat ca thu muc tham khao va ban thao chuong | Xu ly nhanh file don le, xu ly slide bai giang PPTX, trich xuat bang bieu XLSX, fallback khi PDF bi loi |

---

## 2. Khi nao kich hoat Skill

Kich hoat skill nay khi:
* Can nap tai lieu tham khao moi (PDF, DOCX, PPTX, XLSX, CSV) vao `references/raw/`.
* Can chuyen doi slide bai giang PPTX hoac bang so lieu XLSX vao kho tri thuc du an.
* Can chuyen doi cac ban thao chuong cu trong `chapters/drafts_raw/` sang `chapters/drafts_clean/`.
* Can lam sach tai lieu tho thanh Markdown chuan (Clean Markdown) truoc khi tien hanh Gap Analysis hoac Facts Extraction.
* Yeu cau: "Chay anydoc", "parse tai lieu raw", "lam sach chuong tho", "chuyen slide sang markdown", "chuyen Word sang markdown", "ingest chapters", "dung firecrawl anydoc".

---

## 3. Cau truc thu muc chuan hoa trong moi Project

```text
[PROJECT_ROOT]/
├── references/
│   ├── raw/                         <-- Chua tai lieu tham khao tho (PDF, DOCX, PPTX, XLSX)
│   │   ├── paper_sota_2025.pdf
│   │   └── clinical_data.xlsx
│   └── clean_markdown/              <-- anydoc xuat Markdown sach kem INDEX.md
│       ├── INDEX.md
│       ├── paper_sota_2025.md
│       └── clinical_data.md
│
└── chapters/
    ├── drafts_raw/                  <-- Chua ban thao chuong tho, slide bai giang cu
    │   ├── ch01_draft_goc.docx
    │   └── ch02_slide_bai_giang.pptx
    └── drafts_clean/                <-- anydoc xuat ban thao sach kem INDEX.md
        ├── INDEX.md
        ├── ch01_draft_goc.md
        └── ch02_slide_bai_giang.md
```

---

## 4. Huong dan su dung chi tiet tung Dong co

### 4.1. Dong co 1: Batch Pipeline SSoT (`batch_ingestion.py`)

Dung khi can quet tu dong toan bo thu muc theo tieu chuan cua project.

* **Quet toan bo Project (ca references va chapters):**
  ```powershell
  python scripts/batch_ingestion.py
  ```
* **Chi quet thu muc Chapters / Drafts tho:**
  ```powershell
  python scripts/batch_ingestion.py --chapters
  ```
* **Chi quet thu muc References:**
  ```powershell
  python scripts/batch_ingestion.py --references
  ```
* **Ghi de lai cac file da ton tai:**
  ```powershell
  python scripts/batch_ingestion.py --force
  ```
* **Xu ly mot file cu the:**
  ```powershell
  python scripts/batch_ingestion.py -s "chapters/drafts_raw/ch01.docx" -o "chapters/drafts_clean"
  ```

Moi file xuat ra tu Dong co 1 duoc tu dong gan YAML Frontmatter chuan:
```markdown
---
source_file: "ch01_draft_goc.docx"
source_type: "DOCX"
chapter_title: "Chuong 1: Tong quan ve He thong Thong tin Y te"
parsed_by: "anydoc-v1.1"
parsed_at: "2026-09-04T15:30:00"
original_size_bytes: 1048576
---
```

### 4.2. Dong co 2: CLI Engine `@firecrawl/anydoc`

Dung khi can chuyen doi nhanh mot file don le, xu ly slide thuyet trinh PPTX, bang tinh XLSX, hoac xu ly cac file PDF co bo cuc 2 cot phuc tap ma parser Python kho xu ly.

* **Kiem tra cai dat:**
  ```powershell
  anydoc --version
  ```
  (He thong da cai san ban toan cuc v0.2.4).

* **Chuyen doi file PDF hoc thuat:**
  ```powershell
  anydoc references/raw/paper_2025.pdf -o references/clean_markdown/paper_2025.md
  ```

* **Chuyen doi slide bai giang PPTX sang Markdown:**
  ```powershell
  anydoc chapters/drafts_raw/ch02_slide.pptx -o chapters/drafts_clean/ch02_slide.md
  ```

* **Trich xuat bang so lieu XLSX / CSV thanh bang Markdown chuan:**
  ```powershell
  anydoc references/raw/clinical_trial_stats.xlsx -o references/clean_markdown/clinical_trial_stats.md
  ```

* **Gan Frontmatter bo sung cho file xuat tu `@firecrawl/anydoc`:**
  Sau khi xuat file `.md`, gan them khoi YAML o dau file de dam bao tuong thich cong cu audit:
  ```markdown
  ---
  source_file: "paper_2025.pdf"
  source_type: "PDF"
  parsed_by: "firecrawl/anydoc-v0.2.4"
  parsed_at: "2026-09-04T15:30:00"
  ---
  ```

---

## 5. Canh bao dac thu khi xu ly tieng Viet va Tai lieu Hoc thuat

1. **Uu tien nguon DOCX truoc PDF:** Neu ban thao co ca file `.docx` va `.pdf`, luon uu tien trich xuat tu `.docx`. Parser docx doc truc tiep XML noi bo, bao toan 100% Unicode tieng Viet va cac ky tu dac biet.
2. **Kiem tra loi Mojibake va Ligature:** PDF hoc thuat (dac biet la PDF cu hoac PDF dung font TCVN/VnTime) co the bi loi font nhung hoac loi font ligature (vi du so "10" bi tach thanh ky tu la, hoac cac dau tieng Viet bi ma hoa sai).
3. **Kiem tra sau khi Ingest:**
   * Trong project Dr May Day: Chay ngay `python scripts/audit_references.py` de phat hien trung lap va mojibake.
   * Trong project HDBS / EMR / KTPMUD: Chay `python scripts/technical_qa_audit.py` de kiem tra toan ven frontmatter va chat luong Markdown.

---

## 6. Tich hop vao Quy trinh 4 Tang Bien soan

```text
[references/raw/] + [chapters/drafts_raw/]
       │
       ▼ (anydoc Dual-Engine: batch_ingestion.py hoac @firecrawl/anydoc CLI, 0 Token)
[references/clean_markdown/] + [chapters/drafts_clean/]
       │
       ▼ (Kiem tra audit: audit_references.py hoac technical_qa_audit.py)
[Xac nhan Markdown sach, khong mojibake, khong trung lap]
       │
       ▼ (Nap cho Gemini Flash / Deep Research)
[reports/gap_report.md] + [knowledge_base/chXX_facts.json]
       │
       ▼ (Claude bien soan hoan thien theo dung khung hoc thuat cua project)
[chapters/chXX_ten_chuong.md]
```
