"""Apply RETAIN decisions: copy/convert source photos into public/photos/ with new names."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from scripts.curation.convert_to_jpeg import convert_to_jpeg


def apply(decisions_path: Path, src_dir: Path, dst_dir: Path, chevalier_hd_dir: Path | None = None) -> dict:
    """Copy/convert RETAIN photos. Returns {section: [new_names]} for Task 11 patching."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    sections: dict[str, list[str]] = {}
    skipped: list[tuple[str, str]] = []

    decisions = [json.loads(l) for l in decisions_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    for d in decisions:
        if d["decision"] != "RETAIN":
            continue
        src_name = d["filename"]
        new_name = d["new_name"]
        section = d["section"]
        if not new_name or not section:
            skipped.append((src_name, "missing_new_name_or_section"))
            continue

        # Origin determines source dir & whether conversion is needed
        origin = d["origin"]
        ext = Path(src_name).suffix.lower()

        if origin == "chevalier":
            if not chevalier_hd_dir:
                skipped.append((src_name, "chevalier_hd_dir_not_provided"))
                continue
            # Find the HD match by stem (e.g., chevalier2.webp -> chevalier2-hd.jpg or similar)
            hd_candidates = list(chevalier_hd_dir.glob(f"{Path(src_name).stem}*"))
            if not hd_candidates:
                skipped.append((src_name, "chevalier_hd_not_found"))
                continue
            src_path = hd_candidates[0]
            dst_path = dst_dir / new_name
            convert_to_jpeg(src_path, dst_path)
        elif ext in (".png", ".webp"):
            src_path = src_dir / src_name
            dst_path = dst_dir / new_name
            convert_to_jpeg(src_path, dst_path)
        else:
            # .jpg / .jpeg -> straight copy
            src_path = src_dir / src_name
            dst_path = dst_dir / new_name
            shutil.copy2(src_path, dst_path)

        sections.setdefault(section, []).append(new_name)

    return {"sections": sections, "skipped": skipped}


if __name__ == "__main__":
    decisions = Path(sys.argv[1])
    src = Path(sys.argv[2])
    dst = Path(sys.argv[3])
    hd = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    result = apply(decisions, src, dst, hd)
    print(json.dumps(result, indent=2, ensure_ascii=False))
