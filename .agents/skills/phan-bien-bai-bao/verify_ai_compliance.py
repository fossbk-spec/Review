#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_ai_compliance.py — Doc journal_profiles/<id>.json va CHAN moi hanh dong
dua noi dung ban thao vao AI neu chinh sach tap chi khong cho phep.

Mac dinh AN TOAN: neu thieu field ai_policy hoac thieu source_url, COI NHU
CAM (fail-safe), khong mac dinh cho phep - dung nguyen tac da xac lap:
khong co tap chi nao "de tinh hon" tru khi da xac minh ro rang.

Dung:
    python scripts/verify_ai_compliance.py --journal ieee_jbhi
    python scripts/verify_ai_compliance.py --journal discover_computing --action own_prose_polish
"""
import argparse
import json
import sys
from pathlib import Path

VALID_ACTIONS = {
    "manuscript_content_to_ai": "Dua noi dung/trich xuat tu ban thao vao AI (mac dinh CAM tru khi xac minh)",
    "own_prose_polish": "Sua van phong doan danh gia REVIEWER DA TU VIET (khong dua noi dung ban thao)",
}


def find_profile(journal_id: str, base_dir: Path) -> Path | None:
    matches = list(base_dir.rglob(f"{journal_id}.json"))
    return matches[0] if matches else None


def verify(journal_id: str, action: str, profiles_dir: Path) -> int:
    profile_path = find_profile(journal_id, profiles_dir)
    if not profile_path:
        print(f"[-] KHONG TIM THAY journal_profiles/**/{journal_id}.json")
        print("[-] FAIL-SAFE: chan hanh dong nay. Tao ho so truoc (xem 02-ho-so-tham-dinh-so.md).")
        return 1

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    ai_policy = profile.get("ai_policy")

    if not ai_policy:
        print(f"[-] Ho so '{journal_id}' KHONG co truong 'ai_policy'.")
        print("[-] FAIL-SAFE: chan moi hanh dong AI cho tap chi nay cho toi khi dien du ai_policy.")
        return 1

    source_url = ai_policy.get("source_url", "")
    if not source_url or "bắt buộc điền" in source_url or "TODO" in source_url.upper():
        print(f"[-] Ho so '{journal_id}' chua co source_url that (chinh sach chua duoc xac minh).")
        print("[-] FAIL-SAFE: chan cho toi khi dien dung URL chinh sach da doc truc tiep.")
        return 1

    print(f"[+] Ho so: {profile.get('journal_name', journal_id)} ({profile.get('publisher', '?')})")
    print(f"[+] Nguon chinh sach da xac minh: {source_url}")

    if action == "manuscript_content_to_ai":
        allowed = ai_policy.get("reviewers_may_upload_manuscript_content_to_ai", False)
        if not allowed:
            print("\n[X] BI CHAN: Chinh sach tap chi nay KHONG cho phep dua noi dung ban thao")
            print("    (ke ca thong tin trich xuat: cong thuc, bang so lieu, doan code) vao AI.")
            print("    Chi duoc phep: doc thu cong + dung checklist (xem 03-tuan-thu-dao-duc-xuat-ban.md).")
            return 1
        print("\n[!] Chinh sach GHI RO cho phep - van nen uu tien Muc 1 (khong dua noi dung ban thao)")
        print("    tru khi thuc su can thiet. Xac nhan lai truoc khi tiep tuc.")
        return 0

    elif action == "own_prose_polish":
        allowed = ai_policy.get("own_prose_polish_allowed", False)
        if not allowed:
            print("\n[X] BI CHAN: Chinh sach khong xac nhan cho phep sua van phong bang AI.")
            return 1
        declare = ai_policy.get("declaration_required_for_own_prose_polish", True)
        print(f"\n[+] CHO PHEP: sua van phong doan danh gia da tu viet.")
        print(f"    Khai bao trong bao cao: {'BAT BUOC' if declare else 'khong bat buoc (nhung nen lam)'}")
        return 0

    else:
        print(f"[-] Action khong hop le: {action}. Chon trong {list(VALID_ACTIONS)}.")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiem tra ai_policy truoc khi dung AI cho phan bien.")
    parser.add_argument("--journal", required=True, help="journal_id, vi du: ieee_jbhi")
    parser.add_argument("--action", default="manuscript_content_to_ai", choices=list(VALID_ACTIONS))
    parser.add_argument("--profiles-dir", default="journal_profiles", type=Path)
    args = parser.parse_args()

    if not args.profiles_dir.exists():
        print(f"[-] Khong tim thay thu muc {args.profiles_dir}/")
        return 1

    return verify(args.journal, args.action, args.profiles_dir)


if __name__ == "__main__":
    sys.exit(main())
