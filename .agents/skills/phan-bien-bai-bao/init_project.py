#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_project.py — Khoi tao du an PHAN BIEN BAI BAO chuan trong 5 giay.
Bao mat 2 tang: manuscripts/raw/ (goc) + manuscripts/anonymized/ (da an danh),
ca hai deu bi loai khoi Git. Khong tao pedagogy.md/CLAUDE.md sai loai.
"""
from pathlib import Path

FOLDERS = [
    "manuscripts/raw", "manuscripts/anonymized",
    "journal_profiles/springer_nature", "journal_profiles/ieee_acm",
    "journal_profiles/biomedical_clinical", "journal_profiles/other",
    "checklists", "reviews", "templates", "scripts",
    ".agents/rules", ".agents/workflows", ".agents/skills",
]

AGENTIGNORE = """manuscripts/raw/
guidelines_raw/
*.pdf
*.docx
*.pptx
.venv/
.git/
__pycache__/
"""

GITATTRIBUTES = """* text=auto eol=lf
*.pdf binary
*.docx binary
"""

GITIGNORE = """manuscripts/raw/
manuscripts/anonymized/
reviews/**/anonymized_extract.md
.venv/
.env
__pycache__/
"""

CLAUDE_MD = """# AGENT DIRECTIVES

Xem .agents/rules/review-ethics.md de biet day du rang buoc dao duc phan bien -
BAT BUOC chay scripts/verify_ai_compliance.py truoc khi dua bat ky noi dung
ban thao nao vao AI.
"""

REVIEW_ETHICS_MD = """# Rang buoc Dao duc Phan bien

1. BAT BUOC chay `python scripts/verify_ai_compliance.py --journal <id> --action <hanh_dong>`
   TRUOC khi dua bat ky noi dung tu ban thao vao AI. Neu script tra ve loi (exit code != 0),
   TU CHOI thuc hien - chi cung cap checklist de reviewer con nguoi tu doi soat.
2. KHONG co "nhom tap chi de tinh hon" - moi tap chi mac dinh nghiem ngat nhu nhau
   tru khi ai_policy cua dung tap chi do da xac nhan khac (co source_url that).
3. Khong bao gio doc truc tiep file trong manuscripts/raw/ - chi qua ban da an danh
   trong manuscripts/anonymized/, va van phai tu kiem tra bang mat truoc khi tin.
4. Neu co dung AI (du chi muc duoc phep), phai khai bao trong FINAL_REVIEW_REPORT.md
   theo dung yeu cau declaration_required_for_own_prose_polish cua tap chi.
"""

WORKFLOW_MD = """---
name: peer-review
description: Chay tron 1 chu trinh phan bien 1 bai bao, tuan thu ai_policy tung tap chi
---
1. Dat ban thao vao manuscripts/raw/<id>.pdf
2. Chay python scripts/anonymize_manuscript.py <id> -> manuscripts/anonymized/<id>.md
3. Chay python scripts/verify_ai_compliance.py --journal <journal_id> --action manuscript_content_to_ai
   -> Neu FAIL: chi dung checklist thu cong, KHONG dua noi dung vao AI.
   -> Neu PASS: tiep tuc buoc 4.
4. Macro Audit (doi chieu journal_profiles/<nhom>/<journal_id>.json) -> audit_macro.md
5. Micro Technical Audit -> audit_micro.md
6. Chay verify_ai_compliance.py --action own_prose_polish truoc khi dung Humanizer chuan hoa van phong
7. Xuat FINAL_REVIEW_REPORT.md theo templates/, kem khai bao AI neu can
"""

FILES = {
    ".agentignore": AGENTIGNORE,
    ".gitattributes": GITATTRIBUTES,
    ".gitignore": GITIGNORE,
    "CLAUDE.md": CLAUDE_MD,
    ".agents/rules/review-ethics.md": REVIEW_ETHICS_MD,
    ".agents/workflows/peer-review.md": WORKFLOW_MD,
}


def bootstrap():
    print("Dang khoi tao du an phan bien bai bao chuan...")
    for f in FOLDERS:
        Path(f).mkdir(parents=True, exist_ok=True)
    for path_str, content in FILES.items():
        path = Path(path_str)
        if path.exists():
            print(f"  [o] Bo qua (da ton tai): {path_str}")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"  [+] Da tao: {path_str}")
    print("Hoan tat. Copy scripts/verify_ai_compliance.py va anonymize_manuscript.py")
    print("tu skill phan-bien-bai-bao vao day. Nho tai checklists/ (TRIPOD-AI, CONSORT-AI...)")
    print("tu nguon chinh thuc truoc khi dung.")


if __name__ == "__main__":
    bootstrap()
