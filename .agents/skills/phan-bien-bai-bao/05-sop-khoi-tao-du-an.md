# SOP Khởi tạo Dự án — Phản biện Bài báo Khoa học trên Google Antigravity

> Kế thừa cấu trúc tốt từ một tài liệu kiến trúc đã review (`reviews/YYYY/REV_<ID>/`, `checklists/` riêng từng chuẩn báo cáo, ẩn danh hoá 2 tầng) — đã sửa điểm sai quan trọng nhất: bỏ hệ thống "4 nhóm tạp chí, mức AI khác nhau" (không đúng thực tế, xem `02-ho-so-tham-dinh-so.md`), thay bằng mặc định nghiêm ngặt cho mọi tạp chí + gate tự động `verify_ai_compliance.py` đã kiểm thử.

## Sơ đồ 4 bước

```text
BƯỚC 1: Cấu trúc thư mục (2 tầng bảo mật bản thảo)  →  BƯỚC 2: Hàng rào token + Rule đạo đức  →
BƯỚC 3: Môi trường + Global Skills  →  BƯỚC 4: Git + alias
```

## BƯỚC 1 — Cấu trúc thư mục

```bash
mkdir -p manuscripts/raw manuscripts/anonymized \
  journal_profiles/springer_nature journal_profiles/ieee_acm \
  journal_profiles/biomedical_clinical journal_profiles/other \
  checklists \
  reviews \
  templates \
  scripts \
  .agents/rules .agents/workflows .agents/skills
```

| Thư mục | Mục đích |
|---|---|
| `manuscripts/raw/` | Bản thảo gốc PDF/Word — **agent bị chặn đọc trực tiếp** (`.agentignore`), chỉ script `anonymize_manuscript.py` được mở |
| `manuscripts/anonymized/` | Bản đã tước tên tác giả/viện/email — vẫn **không đưa vào Git** (xem Bước 2) |
| `journal_profiles/<nhóm>/` | Phân theo nhóm publisher **chỉ để tổ chức thư mục**, KHÔNG ngụ ý nhóm nào "dễ tính hơn" về AI — mỗi file vẫn phải tự khai đầy đủ `ai_policy` |
| `checklists/` | Chuẩn báo cáo quốc tế dạng file riêng (TRIPOD-AI, CONSORT-AI, PRISMA, STARD) — tải từ nguồn chính thức, không tự viết lại nội dung chuẩn |
| `reviews/<năm>/REV_<journal>_<số>/` | Một thư mục riêng mỗi lượt review — xem cấu trúc con ở Bước 1b |
| `templates/` | Mẫu báo cáo (`report_comments_to_authors.md`, `report_confidential_editor.md`) |

### Bước 1b — Cấu trúc con của một lượt review

```
reviews/2026/REV_discover_computing_001/
├── metadata.json          # journal_id, manuscript_id, deadline, ngày nhận
├── anonymized_extract.md  # CHỈ phần cần thiết đã ẩn danh — KHÔNG toàn văn
├── audit_macro.md         # đối chiếu Scope/Checklist
├── audit_micro.md         # mổ xẻ kỹ thuật (chỉ nếu ai_policy cho phép — xem Bước 2)
└── FINAL_REVIEW_REPORT.md # báo cáo cuối, theo mẫu 04-mau-bao-cao-phan-bien.md
```

## BƯỚC 2 — Hàng rào bảo vệ & Rule đạo đức

### 1. `.agentignore`
```gitignore
manuscripts/raw/
guidelines_raw/
*.pdf
*.docx
*.pptx
.venv/
.git/
__pycache__/
```

### 2. `.gitattributes`
```gitattributes
* text=auto eol=lf
*.pdf binary
*.docx binary
```

### 3. `.gitignore` (quan trọng: loại trừ cả bản đã ẩn danh, không chỉ bản gốc)
```gitignore
manuscripts/raw/
manuscripts/anonymized/
reviews/**/anonymized_extract.md
.venv/
.env
```
Lý do loại trừ cả `anonymized_extract.md`: ẩn danh tên tác giả không đồng nghĩa xoá hết thông tin nhận diện được — vẫn có thể suy ra bản thảo nào qua nội dung kỹ thuật đặc trưng nếu bị public trên GitHub.

### 4. Rule đạo đức — `.agents/rules/review-ethics.md`

Nội dung đầy đủ đã có ở `03-tuan-thu-dao-duc-xuat-ban.md` — copy nguyên vào đây, không viết lại. Điểm cốt lõi Agent phải tuân thủ:
```markdown
# Rang buoc Dao duc Phan bien

1. BAT BUOC chay `python scripts/verify_ai_compliance.py --journal <id> --action <hanh_dong>`
   TRUOC khi dua bat ky noi dung nao tu ban thao vao AI. Neu script tra ve loi (exit code != 0),
   TU CHOI thuc hien - chi cung cap checklist de reviewer con nguoi tu doi soat.
2. Khong co "nhom tap chi de tinh hon" - moi tap chi mac dinh nghiem ngat nhu nhau tru khi
   ai_policy cua dung tap chi do da xac nhan khac.
3. Khong bao gio doc truc tiep file trong manuscripts/raw/ - chi qua ban da an danh.
```

**`CLAUDE.md` chỉ trỏ tới file trên**, không lặp lại nội dung — đúng nguyên tắc đã dùng ở các skill khác.

### 5. Workflow — `.agents/workflows/peer-review.md`

Nội dung đầy đủ ở `01-quy-trinh-4-tang.md` — copy nguyên vào đây, gọi bằng `/peer-review`.

## BƯỚC 3 — Môi trường & Global Skills

```bash
python3 -m venv .venv && source .venv/bin/activate   # macOS
python -m venv .venv; .\.venv\Scripts\Activate.ps1    # Windows
pip install pyyaml pydantic requests
```

```bash
npx skills add firecrawl/anydoc --global      # hoặc dùng hdbs-anydoc nội bộ nếu đã có
npx skills add blader/humanizer --global      # đã cài sẵn trong tài khoản Claude này
```

## BƯỚC 4 — Git & Alias

```bash
git init && git add . && git commit -m "feat: khoi tao du an phan bien bai bao voi bao mat 2 tang"
```
```bash
alias gsave='git add . && git commit -m "update: checkpoint" && git push origin main'
alias gload='git fetch origin && git merge origin/main'
```

## `init_project.py` — khởi tạo 1 lệnh

File đầy đủ: **[`scripts/init_project.py`](../scripts/init_project.py)** — đã kiểm thử chạy thật, tạo đủ thư mục + file cấu hình, không tạo `pedagogy.md`/`CLAUDE.md` sai loại (đúng bài học từ các dự án sách trước đó).
```bash
python init_project.py
```

## Script ẩn danh hoá — `scripts/anonymize_manuscript.py`

Xem file thật ở `scripts/anonymize_manuscript.py` trong skill này. **Giới hạn cần biết**: đây là công cụ hỗ trợ dựa trên regex (xoá email, dòng "Author(s):"/"Affiliation:" phổ biến, tên file gốc) — **không thay thế việc reviewer tự kiểm tra bằng mắt** trước khi coi bản thảo đã thực sự ẩn danh, vì tên tác giả có thể xuất hiện dưới nhiều dạng không đoán trước được (footer, watermark, metadata ẩn trong PDF, tên file đính kèm hình ảnh).
