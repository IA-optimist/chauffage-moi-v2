"""Classify batch files by origin based on filename patterns.

See spec §1 (Inventaire source) for the 5 expected origins.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from enum import Enum
from pathlib import Path


class Origin(str, Enum):
    FB_CDN = "fb_cdn"
    DURLEM = "durlem"
    WHATSAPP = "whatsapp"
    CHEVALIER = "chevalier"
    TEST = "test"


_FB_CDN_RE = re.compile(r"^\d{9,}_\d{9,}_\d+_n\.jpg$", re.IGNORECASE)
_DURLEM_RE = re.compile(r"^Capture d'écran .*\.png$", re.IGNORECASE)
_WHATSAPP_RE = re.compile(r"^WhatsApp Image .*\.jpe?g$", re.IGNORECASE)
_CHEVALIER_RE = re.compile(r"^chevalier\d+\.webp$", re.IGNORECASE)
_TEST_RE = re.compile(r"^fb-(race|test)-(test|photo).*\.jpg$", re.IGNORECASE)


def classify_filename(name: str) -> Origin:
    """Return Origin or raise ValueError if no pattern matches."""
    if _TEST_RE.match(name):
        return Origin.TEST
    if _FB_CDN_RE.match(name):
        return Origin.FB_CDN
    if _DURLEM_RE.match(name):
        return Origin.DURLEM
    if _WHATSAPP_RE.match(name):
        return Origin.WHATSAPP
    if _CHEVALIER_RE.match(name):
        return Origin.CHEVALIER
    raise ValueError(f"Unknown origin for filename: {name!r}")


def inventory(folder: Path) -> dict:
    """Build inventory dict {filename: origin} + a counts summary."""
    files = {}
    unknown = []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        try:
            files[p.name] = classify_filename(p.name).value
        except ValueError:
            unknown.append(p.name)
    counts = dict(Counter(files.values()))
    return {"files": files, "counts": counts, "unknown": unknown, "total": len(files)}


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fb-photos-raw")
    result = inventory(folder)
    print(json.dumps(result, indent=2, ensure_ascii=False))
