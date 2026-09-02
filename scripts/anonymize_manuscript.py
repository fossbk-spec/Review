#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anonymize_manuscript.py — Cong cu HO TRO an danh hoa ban thao truoc khi trich
xuat noi dung (KHONG thay the viec tu kiem tra bang mat).

Xu ly: doc file .docx/.pdf/.txt/.md, chuyen sang text/markdown (qua pandoc
neu co, hoac doc truc tiep .txt/.md), roi xoa/che cac mau hinh hay lo danh
tinh: email, dong "Author(s):"/"Affiliation:"/"Corresponding author",
ten file goc (thuong chua ten tac gia).

GIOI HAN QUAN TRONG (doc truoc khi dung that):
- Chi bat duoc mau hinh PHO BIEN bang regex - khong bat duoc moi truong hop
  (vi du ten tac gia xuat hien tu nhien trong cau van, watermark trong PDF,
  metadata an trong file .docx/.pdf nhu "Author" property).
- Anh/hinh ve co the chua watermark/logo vien nghien cuu - script nay
  KHONG xu ly anh.
- BAT BUOC tu doc lai file da an danh truoc khi tin tuong no da sach.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

EMAIL_RE = re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b')

IDENTIFYING_LINE_PATTERNS = [
    re.compile(r'(?im)^.*\bauthor\s*\(?s?\)?\s*:.*$'),
    re.compile(r'(?im)^.*\btác giả\s*:.*$'),
    re.compile(r'(?im)^.*\b(affiliation|đơn vị|viện nghiên cứu)s?\s*:.*$'),
    re.compile(r'(?im)^.*\bcorresponding author\b.*$'),
    re.compile(r'(?im)^.*\b(grant|funding)\s*(no\.?|number)?\s*:.*$'),
]

METADATA_STRIP_FIELDS = ["author", "title", "creator", "producer", "lastmodifiedby"]


def convert_to_markdown(src: Path, tmp_dir: Path) -> str:
    """Chuyen doi sang markdown. Uu tien pandoc (giu bang/cong thuc tot hon)."""
    if src.suffix.lower() in (".md", ".txt"):
        return src.read_text(encoding="utf-8", errors="replace")

    if shutil.which("pandoc"):
        out = tmp_dir / (src.stem + ".md")
        result = subprocess.run(
            ["pandoc", str(src), "-t", "markdown", "-o", str(out)],
            capture_output=True, text=True)
        if result.returncode == 0 and out.exists():
            return out.read_text(encoding="utf-8", errors="replace")
        print(f"  [!] pandoc loi ({result.stderr.strip()[:200]}) - thu cach khac.")

    raise RuntimeError(
        f"Khong the chuyen doi {src.name} - can cai pandoc, hoac tu chuyen "
        f"sang .md/.txt truoc khi chay script nay."
    )


def anonymize_text(text: str) -> tuple[str, dict]:
    stats = {"emails_removed": 0, "identifying_lines_removed": 0}

    def _count_and_replace(pattern, replacement, s, key):
        matches = pattern.findall(s)
        stats[key] += len(matches)
        return pattern.sub(replacement, s)

    text = _count_and_replace(EMAIL_RE, "[EMAIL ĐÃ ẨN]", text, "emails_removed")
    for pat in IDENTIFYING_LINE_PATTERNS:
        text = _count_and_replace(pat, "[DÒNG NHẬN DIỆN ĐÃ ẨN]", text, "identifying_lines_removed")

    return text, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Ho tro an danh hoa ban thao truoc khi dua vao AI.")
    parser.add_argument("input", type=Path, help="File trong manuscripts/raw/")
    parser.add_argument("-o", "--output", type=Path, default=None,
                         help="Mac dinh: manuscripts/anonymized/<ten>.md")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"[-] Khong tim thay file: {args.input}")
        return 1

    output = args.output or Path("manuscripts/anonymized") / (args.input.stem + ".md")
    output.parent.mkdir(parents=True, exist_ok=True)

    tmp_dir = Path("manuscripts/anonymized/.tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        raw_text = convert_to_markdown(args.input, tmp_dir)
    except RuntimeError as e:
        print(f"[-] {e}")
        return 1
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    clean_text, stats = anonymize_text(raw_text)
    output.write_text(clean_text, encoding="utf-8")

    print(f"[+] Da ghi: {output}")
    print(f"[+] Da an: {stats['emails_removed']} email, "
          f"{stats['identifying_lines_removed']} dong nhan dien (Author/Affiliation/...).")
    print("\n[!] BAT BUOC: mo lai file va tu doc kiem tra bang mat truoc khi tin da sach.")
    print("[!] Script nay KHONG xu ly: ten tac gia xuat hien tu nhien trong cau van,")
    print("    watermark/logo trong anh, metadata an trong file goc (Author property).")
    print("    Neu file goc la PDF/DOCX, kiem tra rieng thuoc tinh 'Author' cua file")
    print("    (vi du: exiftool, hoac File > Properties trong Word/Adobe).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
