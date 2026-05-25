"""Perceptual-hash deduplication: compare candidates against a reference set.

Spec §7 rule 2 (REJECT doublon vs 23 already-integrated photos) and rule 6
(internal redundancy). Threshold = hamming distance <= 5 on imagehash.phash.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import imagehash
from PIL import Image, UnidentifiedImageError

DEDUP_THRESHOLD = 5  # hamming distance — spec §7.2 / §7.6
_SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def hash_file(path: Path) -> imagehash.ImageHash:
    """Compute pHash 64-bit. Raises on unreadable files."""
    with Image.open(path) as img:
        # imagehash needs RGB; some PNG/WebP have palette/alpha modes
        return imagehash.phash(img.convert("RGB"))


def _is_image(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in _SUPPORTED


def find_duplicates(candidates: Path, reference: Path) -> dict:
    """For each candidate, find the closest reference within DEDUP_THRESHOLD.

    Returns: {candidate_name: {"match": ref_name, "distance": int}}
    """
    ref_hashes: list[tuple[str, imagehash.ImageHash]] = []
    for r in sorted(reference.iterdir()):
        if not _is_image(r):
            continue
        try:
            ref_hashes.append((r.name, hash_file(r)))
        except (UnidentifiedImageError, OSError) as exc:
            print(f"WARN: cannot hash reference {r.name}: {exc}", file=sys.stderr)

    out: dict = {}
    for c in sorted(candidates.iterdir()):
        if not _is_image(c):
            continue
        try:
            ch = hash_file(c)
        except (UnidentifiedImageError, OSError) as exc:
            print(f"WARN: cannot hash candidate {c.name}: {exc}", file=sys.stderr)
            continue
        best: Optional[tuple[str, int]] = None
        for rname, rh in ref_hashes:
            d = ch - rh
            if best is None or d < best[1]:
                best = (rname, d)
        if best and best[1] <= DEDUP_THRESHOLD:
            out[c.name] = {"match": best[0], "distance": int(best[1])}
    return out


def find_internal_clusters(folder: Path) -> list[list[str]]:
    """Group candidates by pHash similarity (spec §7.6 internal redundancy).

    Returns clusters of >=2 filenames where all pairs are within DEDUP_THRESHOLD.
    """
    items: list[tuple[str, imagehash.ImageHash]] = []
    for p in sorted(folder.iterdir()):
        if not _is_image(p):
            continue
        try:
            items.append((p.name, hash_file(p)))
        except (UnidentifiedImageError, OSError):
            continue

    clusters: list[list[str]] = []
    used: set[str] = set()
    for i, (name_i, h_i) in enumerate(items):
        if name_i in used:
            continue
        group = [name_i]
        for name_j, h_j in items[i + 1 :]:
            if name_j in used:
                continue
            if (h_i - h_j) <= DEDUP_THRESHOLD:
                group.append(name_j)
                used.add(name_j)
        if len(group) > 1:
            used.add(name_i)
            clusters.append(group)
    return clusters


if __name__ == "__main__":
    candidates = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fb-photos-raw")
    reference = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("public/photos")
    dups = find_duplicates(candidates, reference)
    clusters = find_internal_clusters(candidates)
    print(json.dumps(
        {"vs_reference": dups, "internal_clusters": clusters},
        indent=2, ensure_ascii=False,
    ))
