# Photos /realisations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrichir la galerie publique `/realisations` du site Astro `chauffage-mirror` avec les photos pertinentes d'un batch de 90 fichiers actuellement stockés au mauvais endroit (`Chauffage-et-moi-Site/Photos/`), tout en nettoyant ce dossier orphelin du repo AI OS.

**Architecture:** Deux repos sans couplage runtime. **(1)** Repo AI OS (`Chauffage-et-moi-Site`) reçoit uniquement un patch `.gitignore` sur une branche dédiée, puis suppression physique du dossier `Photos/`. **(2)** Repo Astro (`chauffageetmoi-v2`, branche `feat/realisations-batch-2026-05`) reçoit : archive batch dans `fb-photos-raw/` (gitignored), 3 scripts Python de curation (`scripts/curation/`), curation report markdown, photos curées dans `public/photos/`, extension de `src/pages/realisations.astro`. Déploiement automatique via Vercel sur push.

**Tech Stack:** Astro 5 + Tailwind 3 + TypeScript (Node 22) côté site · Python 3.11 + Pillow + imagehash pour curation · git/GitHub + Vercel pour déploiement.

**Spec source:** [`docs/superpowers/specs/2026-05-25-photos-realisations-design.md`](../specs/2026-05-25-photos-realisations-design.md)

---

## File Structure

### Repo `chauffageetmoi-v2` (cwd = `C:\Users\maxen\chauffageetmoi-v2`)

| Action | Path | Responsabilité |
|---|---|---|
| Create | `fb-photos-raw/` (dir) | Archive des 90 fichiers source, gitignored |
| Modify | `.gitignore` | Ajout d'une ligne `fb-photos-raw/` |
| Create | `scripts/curation/__init__.py` | Marqueur de package Python |
| Create | `scripts/curation/inventory.py` | Classifie les 90 fichiers par origine (FB/Durlem/WhatsApp/Chevalier/test) |
| Create | `scripts/curation/dedup_phash.py` | Calcule perceptual hash, détecte doublons vs `public/photos/` existants |
| Create | `scripts/curation/convert_to_jpeg.py` | PNG/WebP → JPEG q=85 avec fond blanc si alpha |
| Create | `scripts/curation/tests/test_dedup.py` | Tests phash : identité, différence |
| Create | `scripts/curation/tests/test_convert.py` | Tests conversion : alpha, dimensions, qualité |
| Create | `scripts/curation/tests/test_inventory.py` | Tests classification par filename |
| Create | `scripts/curation/requirements.txt` | `Pillow>=10.0` + `imagehash>=4.3` |
| Create | `docs/realisations-curation-2026-05-25.md` | Curation report markdown — gate utilisateur |
| Create | `public/photos/<N nouveaux>.jpg` | Photos curées avec noms sémantiques |
| Modify | `src/pages/realisations.astro` | Extend `gal*` arrays, conditionnellement créer galPAC + section, rename Adoucisseurs |

### Repo `Chauffage-et-moi-Site` (cwd = `C:\Users\maxen\Documents\Chauffage-et-moi-Site`)

| Action | Path | Responsabilité |
|---|---|---|
| Modify | `.gitignore` | Ajout d'une ligne `Photos/` |
| Delete | `Photos/` (dir) | Supprimé du disque après archive dans Astro repo |

---

## Phase A — Cleanup AI OS (Tasks 1-2)

### Task 1: Add `Photos/` to AI OS `.gitignore` on dedicated branch

**Files:**
- Modify: `C:\Users\maxen\Documents\Chauffage-et-moi-Site\.gitignore`

**Context:** Le repo AI OS est actuellement sur la branche `phase-34-editable-policy` (recovery policy en cours). Ce changement doit aller sur une branche séparée pour ne pas mélanger les deux features. Spec §11 done criteria : "Le commit `.gitignore` du repo AI OS est sur une branche autre que `phase-34-editable-policy`".

- [ ] **Step 1: Stash any uncommitted changes (defensive)**

```bash
cd "C:/Users/maxen/Documents/Chauffage-et-moi-Site"
git status --short
```

Expected: empty output, or only untracked `Photos/` and `.claude/`. If staged/modified tracked files exist, stash them: `git stash push -m "wip phase-34"` and unstash after Task 2.

- [ ] **Step 2: Create dedicated branch from master**

```bash
git fetch origin
git checkout -b chore/gitignore-photos-orphan origin/master
```

Expected: `Switched to a new branch 'chore/gitignore-photos-orphan'` based on `4915200 Add recovery readiness policy engine`.

- [ ] **Step 3: Append `Photos/` to `.gitignore`**

Edit `.gitignore` — add this block at the end:

```
# Photo batch orphelin (déplacé vers chauffageetmoi-v2/fb-photos-raw/)
Photos/
```

- [ ] **Step 4: Verify .gitignore matches Photos/ folder**

```bash
git status --ignored Photos/ 2>&1 | head -5
```

Expected: `Photos/` listed under "Ignored files" (or no output if directory empty/missing on this branch — both are fine, the rule will apply if it ever reappears).

- [ ] **Step 5: Commit and push**

```bash
git add .gitignore
git commit -m "chore: ignore Photos/ orphan folder

Le dossier Photos/ (90 photos Facebook/Durlem/WhatsApp/Chevalier) est
apparu le 23 mai sans rattachement au code AI OS. Le contenu a été
archivé dans le repo Astro chauffageetmoi-v2/fb-photos-raw/ et la
galerie /realisations enrichie en conséquence. Cette règle gitignore
prévient toute réintroduction accidentelle.

Voir spec chauffageetmoi-v2/docs/superpowers/specs/2026-05-25-photos-realisations-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
git push -u origin chore/gitignore-photos-orphan
```

Expected: 1 file changed, push succeeds, PR can be opened on GitHub.

- [ ] **Step 6: Switch back to working branch**

```bash
git checkout phase-34-editable-policy
git stash pop 2>&1 || true   # only if Step 1 stashed something
```

Expected: back on `phase-34-editable-policy`, working tree restored.

---

### Task 2: Sync 90 source photos to `chauffageetmoi-v2/fb-photos-raw/`

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\fb-photos-raw\` (dir + 90 files)
- Modify: `C:\Users\maxen\chauffageetmoi-v2\.gitignore`

**Context:** Pas de suppression du dossier source pendant cette phase — c'est la backup. La suppression est en Task 15 après confirmation prod.

- [ ] **Step 1: Verify Astro repo state**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
git branch --show-current
git status --short
```

Expected: branch `feat/realisations-batch-2026-05`, working tree clean (last commits `7b384ea` and `ee68504` = spec).

- [ ] **Step 2: Create `fb-photos-raw/` directory**

```bash
mkdir -p fb-photos-raw
```

Expected: directory created (or already exists, idempotent).

- [ ] **Step 3: Add `fb-photos-raw/` to `.gitignore`**

Edit `C:\Users\maxen\chauffageetmoi-v2\.gitignore` — append after the `.vercel` line:

```

# Source photos archive (90 files, batch 2026-05-25 — see spec)
fb-photos-raw/
```

- [ ] **Step 4: Copy 90 photos from AI OS Photos/ to fb-photos-raw/**

```bash
cp -a "/c/Users/maxen/Documents/Chauffage-et-moi-Site/Photos/." "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/"
```

Expected: no output (silent success).

- [ ] **Step 5: Verify count and integrity**

```bash
ls "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/" | wc -l
du -sh "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/"
```

Expected: `90` files, `~19M`. If count differs, abort and investigate before continuing.

- [ ] **Step 6: Verify gitignore covers it**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
git status --short fb-photos-raw/ 2>&1 | head -3
```

Expected: empty output (folder is fully ignored).

- [ ] **Step 7: Commit the .gitignore change**

```bash
git add .gitignore
git commit -m "chore: ignore fb-photos-raw/ archive

Archive locale des 90 fichiers source du batch 2026-05-25
(62 FB-CDN + 10 PNG Durlem + 11 WhatsApp + 5 chevalier WebP + 2 test).
Préservée sur disque pour traçabilité, jamais commitée.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

Expected: 1 file changed, on branch `feat/realisations-batch-2026-05`.

---

## Phase B — Curation tooling (Tasks 3-6)

### Task 3: Bootstrap curation scripts package + dependencies

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\__init__.py`
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\requirements.txt`
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\tests\__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
mkdir -p scripts/curation/tests
```

- [ ] **Step 2: Create empty package markers**

Create `scripts/curation/__init__.py` with content:

```python
"""Curation tooling for the 2026-05-25 photos batch.

See: docs/superpowers/specs/2026-05-25-photos-realisations-design.md
One-shot scripts used during the integration of the FB/Durlem/WhatsApp/Chevalier
batch into /realisations. Not used at runtime.
"""
```

Create `scripts/curation/tests/__init__.py` with content:

```python
```

(empty file, just marker)

- [ ] **Step 3: Create requirements.txt**

Create `scripts/curation/requirements.txt`:

```
Pillow>=10.0
imagehash>=4.3
```

- [ ] **Step 4: Install dependencies**

```bash
python -m pip install -r scripts/curation/requirements.txt
```

Expected: `Successfully installed Pillow-X.Y imagehash-A.B` (or "already installed"). Pillow is already present per discovery; only imagehash needs installing.

- [ ] **Step 5: Verify imports work**

```bash
python -c "import PIL, imagehash; print(f'Pillow {PIL.__version__}'); print(f'imagehash {imagehash.__version__}')"
```

Expected: both versions printed, no `ModuleNotFoundError`.

- [ ] **Step 6: Commit**

```bash
git add scripts/curation/__init__.py scripts/curation/tests/__init__.py scripts/curation/requirements.txt
git commit -m "chore(curation): bootstrap Python package + deps

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Inventory script (classifies by origin) — TDD

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\inventory.py`
- Test: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\tests\test_inventory.py`

**Why:** §1 spec lists 5 origins (FB-CDN, Durlem, WhatsApp, Chevalier, test). The downstream scripts need to know each file's origin to apply the right curation rules (e.g., test → auto-reject, Chevalier → resolution check + Google reviews retrieval).

- [ ] **Step 1: Write the failing test**

Create `scripts/curation/tests/test_inventory.py`:

```python
"""Tests for the inventory classifier."""
import pytest
from pathlib import Path

from scripts.curation.inventory import classify_filename, Origin


@pytest.mark.parametrize("filename,expected", [
    # FB CDN pattern: digits_digits_...n.jpg
    ("505715303_1367150891594005_8359931051889009865_n.jpg", Origin.FB_CDN),
    ("523360329_1402863128022781_3621832922668640343_n.jpg", Origin.FB_CDN),
    # Durlem: French screenshot naming
    ("Capture d'écran 2026-05-25 191033.png", Origin.DURLEM),
    # WhatsApp
    ("WhatsApp Image 2026-05-25 at 14.32.33.jpeg", Origin.WHATSAPP),
    ("WhatsApp Image 2026-05-25 at 14.32.34 (3).jpeg", Origin.WHATSAPP),
    # Chevalier WebP
    ("chevalier1.webp", Origin.CHEVALIER),
    ("chevalier5.webp", Origin.CHEVALIER),
    # Test artefacts
    ("fb-race-test.jpg", Origin.TEST),
    ("fb-test-photo-0.jpg", Origin.TEST),
])
def test_classify_filename(filename: str, expected: Origin):
    assert classify_filename(filename) == expected


def test_classify_filename_unknown_raises():
    with pytest.raises(ValueError, match="Unknown origin"):
        classify_filename("random-thing.jpg")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
python -m pytest scripts/curation/tests/test_inventory.py -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.curation.inventory'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/curation/inventory.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest scripts/curation/tests/test_inventory.py -v
```

Expected: all 10 parametrized cases + the unknown case = 11 PASSED.

- [ ] **Step 5: Run on real batch**

```bash
python scripts/curation/inventory.py fb-photos-raw > /tmp/inventory.json
python -c "import json; d=json.load(open('/tmp/inventory.json')); print('Counts:', d['counts']); print('Total:', d['total']); print('Unknown:', d['unknown'])"
```

Expected:
```
Counts: {'fb_cdn': 62, 'durlem': 10, 'whatsapp': 11, 'chevalier': 5, 'test': 2}
Total: 90
Unknown: []
```

If any unknown filenames appear → investigate and extend the regex before proceeding.

- [ ] **Step 6: Commit**

```bash
git add scripts/curation/inventory.py scripts/curation/tests/test_inventory.py
git commit -m "feat(curation): inventory script classifies batch by origin

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Perceptual-hash deduplication script — TDD

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\dedup_phash.py`
- Test: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\tests\test_dedup.py`

**Why:** Spec §7 rule 2 (REJECT doublon vs 23 photos déjà intégrées) et rule 6 (redondance interne du batch). Threshold = hamming distance ≤ 5 sur `imagehash.phash` 64-bit.

- [ ] **Step 1: Write the failing test**

Create `scripts/curation/tests/test_dedup.py`:

```python
"""Tests for the perceptual-hash deduplication logic."""
import shutil
from pathlib import Path

import imagehash
import pytest
from PIL import Image

from scripts.curation.dedup_phash import (
    DEDUP_THRESHOLD,
    hash_file,
    find_duplicates,
)


@pytest.fixture
def tmp_photos(tmp_path: Path) -> Path:
    """Create a tiny test photoset: two near-identical + one different."""
    folder = tmp_path / "photos"
    folder.mkdir()
    # Image A: red square
    Image.new("RGB", (200, 200), color=(220, 30, 30)).save(folder / "a.jpg")
    # Image A': same red square saved twice (identical hash, dist=0)
    Image.new("RGB", (200, 200), color=(220, 30, 30)).save(folder / "a_copy.jpg")
    # Image B: blue square (different hash, dist >> threshold)
    Image.new("RGB", (200, 200), color=(30, 30, 220)).save(folder / "b.jpg")
    return folder


def test_hash_file_deterministic(tmp_photos: Path):
    h1 = hash_file(tmp_photos / "a.jpg")
    h2 = hash_file(tmp_photos / "a.jpg")
    assert h1 == h2


def test_identical_images_have_zero_distance(tmp_photos: Path):
    h_a = hash_file(tmp_photos / "a.jpg")
    h_a_copy = hash_file(tmp_photos / "a_copy.jpg")
    assert (h_a - h_a_copy) == 0


def test_different_images_have_large_distance(tmp_photos: Path):
    h_a = hash_file(tmp_photos / "a.jpg")
    h_b = hash_file(tmp_photos / "b.jpg")
    assert (h_a - h_b) > DEDUP_THRESHOLD


def test_find_duplicates_matches_within_threshold(tmp_photos: Path, tmp_path: Path):
    # candidates folder = a_copy.jpg only; reference = a.jpg
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    shutil.copy(tmp_photos / "a_copy.jpg", candidates / "a_copy.jpg")
    shutil.copy(tmp_photos / "b.jpg", candidates / "b.jpg")
    reference = tmp_path / "reference"
    reference.mkdir()
    shutil.copy(tmp_photos / "a.jpg", reference / "a.jpg")

    result = find_duplicates(candidates, reference)

    assert "a_copy.jpg" in result
    assert result["a_copy.jpg"]["match"] == "a.jpg"
    assert result["a_copy.jpg"]["distance"] == 0
    assert "b.jpg" not in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest scripts/curation/tests/test_dedup.py -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.curation.dedup_phash'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/curation/dedup_phash.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest scripts/curation/tests/test_dedup.py -v
```

Expected: 4 PASSED.

- [ ] **Step 5: Run on real batch**

```bash
python scripts/curation/dedup_phash.py fb-photos-raw public/photos > /tmp/dedup.json
python -c "import json; d=json.load(open('/tmp/dedup.json')); print('vs_reference matches:', len(d['vs_reference'])); print('internal clusters:', len(d['internal_clusters']))"
```

Expected output gives concrete numbers — e.g., `vs_reference matches: 5-15` (raw FB photos that match the 23 curated ones via re-naming or being source of crop) and `internal clusters: 0-5` (groups of near-duplicates within the batch). Exact numbers will inform Task 9 report. **No assertion**, just capture.

- [ ] **Step 6: Commit**

```bash
git add scripts/curation/dedup_phash.py scripts/curation/tests/test_dedup.py
git commit -m "feat(curation): pHash dedup vs reference + internal clusters

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: PNG/WebP → JPEG converter — TDD

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\convert_to_jpeg.py`
- Test: `C:\Users\maxen\chauffageetmoi-v2\scripts\curation\tests\test_convert.py`

**Why:** Spec §6 — PNG Durlem et WebP Chevalier (si HD récupéré) doivent devenir JPEG q=85 pour cohérence avec `public/photos/` (100% JPEG). Alpha → fond blanc. Pas de redimensionnement.

- [ ] **Step 1: Write the failing test**

Create `scripts/curation/tests/test_convert.py`:

```python
"""Tests for PNG/WebP -> JPEG conversion."""
from pathlib import Path

import pytest
from PIL import Image

from scripts.curation.convert_to_jpeg import convert_to_jpeg, JPEG_QUALITY


def test_png_opaque_to_jpeg(tmp_path: Path):
    src = tmp_path / "opaque.png"
    Image.new("RGB", (100, 80), color=(200, 100, 50)).save(src)
    dst = tmp_path / "opaque.jpg"

    convert_to_jpeg(src, dst)

    with Image.open(dst) as out:
        assert out.format == "JPEG"
        assert out.size == (100, 80)
        assert out.mode == "RGB"


def test_png_with_alpha_gets_white_background(tmp_path: Path):
    src = tmp_path / "alpha.png"
    # Half-transparent red on transparent canvas
    img = Image.new("RGBA", (50, 50), color=(255, 0, 0, 128))
    img.save(src)
    dst = tmp_path / "alpha.jpg"

    convert_to_jpeg(src, dst)

    with Image.open(dst) as out:
        assert out.mode == "RGB"  # no alpha
        # Center pixel should be pink-ish (red blended with white)
        r, g, b = out.getpixel((25, 25))
        assert r > 200 and g > 100 and b > 100  # red dominant but lightened


def test_webp_to_jpeg(tmp_path: Path):
    src = tmp_path / "in.webp"
    Image.new("RGB", (60, 60), color=(50, 200, 80)).save(src, "WEBP")
    dst = tmp_path / "out.jpg"

    convert_to_jpeg(src, dst)

    with Image.open(dst) as out:
        assert out.format == "JPEG"
        assert out.size == (60, 60)


def test_output_quality_85(tmp_path: Path):
    """JPEG quality 85 produces files between 1-30KB for small simple images."""
    src = tmp_path / "in.png"
    Image.new("RGB", (300, 300), color=(120, 80, 60)).save(src)
    dst = tmp_path / "out.jpg"

    convert_to_jpeg(src, dst)

    assert dst.exists()
    # Sanity: a 300x300 solid-color JPEG at q=85 is under 30KB
    assert dst.stat().st_size < 30_000


def test_quality_constant_is_85():
    assert JPEG_QUALITY == 85
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest scripts/curation/tests/test_convert.py -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.curation.convert_to_jpeg'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/curation/convert_to_jpeg.py`:

```python
"""Convert PNG/WebP files to JPEG q=85, alpha->white background.

Spec §6. Single-file convert function + a CLI for batch use.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

JPEG_QUALITY = 85  # spec §6


def convert_to_jpeg(src: Path, dst: Path) -> None:
    """Convert one file to JPEG. Handles RGBA/LA/palette alpha by compositing on white."""
    with Image.open(src) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            # Composite onto a white background
            rgba = img.convert("RGBA")
            bg = Image.new("RGB", rgba.size, (255, 255, 255))
            bg.paste(rgba, mask=rgba.split()[-1])  # last channel = alpha
            bg.save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True)
        else:
            img.convert("RGB").save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True)


def convert_batch(src_dir: Path, dst_dir: Path, extensions: tuple[str, ...] = (".png", ".webp")) -> list[tuple[Path, Path]]:
    """Convert every file with matching extension. Returns [(src, dst)] pairs done."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    done = []
    for src in sorted(src_dir.iterdir()):
        if not src.is_file() or src.suffix.lower() not in extensions:
            continue
        dst = dst_dir / (src.stem + ".jpg")
        convert_to_jpeg(src, dst)
        done.append((src, dst))
    return done


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: convert_to_jpeg.py <src_dir> <dst_dir>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    pairs = convert_batch(src, dst)
    for s, d in pairs:
        print(f"{s.name} -> {d.name}")
    print(f"Total: {len(pairs)}", file=sys.stderr)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest scripts/curation/tests/test_convert.py -v
```

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/curation/convert_to_jpeg.py scripts/curation/tests/test_convert.py
git commit -m "feat(curation): PNG/WebP -> JPEG q=85 with alpha compositing

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase C — Visual curation & HD retrieval (Tasks 7-9)

### Task 7: Retrieve HD chevalier photos from Google Business reviews

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\fb-photos-raw\chevalier-hd\` (dir, gitignored as subdir)
- (Output) Inline notes for curation report

**Why:** Spec R8 — les 5 chevalier WebP sont des thumbnails 125×125. Versions HD requises. Source = avis Google de Chauffage & Moi posté par client "Chevalier".

**Note for executing agent:** Cette tâche utilise WebFetch (et fallback navigateur si nécessaire) — adapter selon outils dispo.

- [ ] **Step 1: Find the Google Business listing URL**

Try multiple queries via WebSearch / WebFetch:

```
WebSearch query: "Chauffage et Moi" Mons Hainaut avis Google
WebSearch query: site:google.com/maps "Chauffage & Moi" chauffagiste
```

Expected: Google Maps URL of the form `https://www.google.com/maps/place/...` for Chauffage & Moi. Record the URL.

- [ ] **Step 2: Fetch reviews + photos URLs**

```
WebFetch url=<google_maps_url> prompt="Liste tous les avis de clients qui contiennent des photos. Pour chacun donne : nom du client, date, nombre de photos, et si possible les URLs directes des photos en HD (clic 'plus' pour étendre)."
```

If WebFetch limited by Google's bot detection, fall back to:
- Manually open the URL in browser, find the "Chevalier" review
- Use computer-use MCP if granted, OR ask user to share the HD photos directly

- [ ] **Step 3: Match HD photos to chevalier1-5 thumbnails**

Once HD photos retrieved (in `fb-photos-raw/chevalier-hd/` or similar), use the dedup script:

```bash
python scripts/curation/dedup_phash.py fb-photos-raw/chevalier-hd fb-photos-raw > /tmp/chevalier_match.json
cat /tmp/chevalier_match.json
```

Expected: each chevalier-hd file matches one of `chevalier1.webp`..`chevalier5.webp` with distance ≤ 5 (despite resolution difference, pHash is robust to scaling).

- [ ] **Step 4: Document result for curation report**

Append to a working notes file `fb-photos-raw/chevalier-hd-notes.md` (gitignored):

```markdown
# Chevalier HD retrieval — 2026-05-25

Google Business URL: <found URL>
Reviewer name: <full name>
Review date: <date>
Photos retrieved: <count>

Matching (thumbnail -> HD filename):
- chevalier1.webp (125x125) -> chevalier-hd/<hd_filename>.jpg (<WIDTH>x<HEIGHT>)
- chevalier2.webp -> ...
...

Consent status: NOT_YET_REQUESTED
Action item: User must request consent from <reviewer name> via Google reviews reply
before any chevalier photo can be integrated.
```

- [ ] **Step 5: If retrieval fails (Google blocks, no review found, etc.)**

Document the failure in the notes file and flag **all 5 chevalier photos as REJECT** with reason `chevalier_hd_unavailable`. The PAC section will then depend on PAC photos found in the 62 FB-CDN batch (Task 8).

- [ ] **Step 6: Do NOT commit `chevalier-hd-notes.md` — it lives under gitignored `fb-photos-raw/`**

No commit needed for this task. Output is consumed by Task 9.

---

### Task 8: Visual curation pass — Claude inspects every photo

**Files:**
- (Output) `C:\Users\maxen\chauffageetmoi-v2\fb-photos-raw\curation-decisions.json` (gitignored working file)

**Why:** Rules §7.3 (quality), §7.4 (RGPD), §7.5 (out of scope), §7.6 (internal redundancy fine-grain), §7.7 (Durlem watermark), §7.8 (classification), §7.9 (resolution) require visual judgment. The executing agent reads each photo via the Read tool and records a decision.

**Note for executing agent:** This task is best executed by an agent that can read images. If using Claude Code, use the Read tool on each photo. If using subagent dispatch, use the Explore agent type with image-reading capability.

- [ ] **Step 1: Build the candidate list**

Skip TEST origin (auto-reject) and skip files already flagged as duplicates by Task 5:

```bash
python -c "
import json
inv = json.load(open('/tmp/inventory.json'))
dups = json.load(open('/tmp/dedup.json'))['vs_reference']
to_inspect = [f for f, o in inv['files'].items() if o != 'test' and f not in dups]
print(f'Files to inspect visually: {len(to_inspect)}')
open('/tmp/to_inspect.txt', 'w').write('\n'.join(to_inspect))
"
```

Expected: a number around 70-80 files to visually inspect (90 - 2 tests - ~10 duplicates).

- [ ] **Step 2: For each file in `/tmp/to_inspect.txt`, read the image and record a decision**

For every filename, use the Read tool with path `fb-photos-raw/<filename>`. Apply rules §7.3 through §7.9 in order. Record decision in the schema below.

Output schema for each file (appended to `fb-photos-raw/curation-decisions.json` — JSON Lines):

```json
{"filename": "505715303_..._n.jpg", "origin": "fb_cdn", "decision": "RETAIN", "section": "chauffage", "new_name": "chaudiere-vaillant-mur-pierre.jpg", "caption": "Chaudière Vaillant — mur en pierre", "reason": "clean install, finition propre", "gdpr_flag": false}
{"filename": "505739580_..._n.jpg", "origin": "fb_cdn", "decision": "REJECT", "section": null, "new_name": null, "caption": null, "reason": "quality_low:flou prononce", "gdpr_flag": false}
{"filename": "Capture d'écran ... 191033.png", "origin": "durlem", "decision": "REJECT", "section": null, "new_name": null, "caption": null, "reason": "branding_concern:durlem_watermark", "gdpr_flag": false}
{"filename": "chevalier2.webp", "origin": "chevalier", "decision": "GDPR_REVIEW", "section": "pac", "new_name": "pac-air-eau-brick.jpg", "caption": "PAC air-eau — installation extérieure", "reason": "resolution_low:125x125; needs HD from google reviews + client consent", "gdpr_flag": true}
```

Decision values: `RETAIN` | `REJECT` | `GDPR_REVIEW` (= flag for user).
Section values: `chauffage` | `sanitaire` | `adoucisseur` | `pac` | `equipe` | `null`.

- [ ] **Step 3: Build summary stats**

```bash
python -c "
import json, collections
decisions = [json.loads(l) for l in open('fb-photos-raw/curation-decisions.json') if l.strip()]
by_decision = collections.Counter(d['decision'] for d in decisions)
by_section = collections.Counter(d['section'] for d in decisions if d['decision'] == 'RETAIN')
by_reject = collections.Counter(d['reason'].split(':')[0] for d in decisions if d['decision'] == 'REJECT')
print('Decisions:', dict(by_decision))
print('RETAIN by section:', dict(by_section))
print('REJECT by reason:', dict(by_reject))
"
```

Expected output gives concrete totals — no assertion, just record for Task 9.

- [ ] **Step 4: Do NOT commit `curation-decisions.json` — it lives under gitignored `fb-photos-raw/`**

Working file. Final state goes into the markdown report at Task 9.

---

### Task 9: Generate curation report — gate utilisateur

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\docs\realisations-curation-2026-05-25.md`

**Why:** Spec §8 — un rapport markdown listant les 90 photos avec décision/section/nouveau-nom/caption/raison. Lecture utilisateur **bloquante** avant phase d'intégration.

- [ ] **Step 1: Generate the report from working files**

Create `scripts/curation/generate_report.py`:

```python
"""Generate the markdown curation report from inventory + dedup + decisions."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def render_table(decisions: list[dict], dups: dict) -> str:
    rows = ["| # | Filename source | Origin | Decision | Section | New name | Caption | Reason / notes |",
            "|---|---|---|---|---|---|---|---|"]
    for i, d in enumerate(decisions, 1):
        reason = d.get("reason") or ""
        if d["filename"] in dups:
            m = dups[d["filename"]]
            reason = f"duplicate_of:{m['match']} (phash dist {m['distance']})"
        rows.append(
            f"| {i} | {d['filename']} | {d['origin']} | {d['decision']} | "
            f"{d.get('section') or '—'} | {d.get('new_name') or '—'} | "
            f"{d.get('caption') or '—'} | {reason} |"
        )
    return "\n".join(rows)


def render_summary(decisions: list[dict]) -> str:
    by_decision = Counter(d["decision"] for d in decisions)
    by_section = Counter(d["section"] for d in decisions if d["decision"] == "RETAIN")
    by_reject = Counter(d["reason"].split(":")[0] for d in decisions if d["decision"] == "REJECT")
    gdpr = [d for d in decisions if d.get("gdpr_flag")]

    out = ["## Summary stats", ""]
    out.append(f"- **Total photos:** {len(decisions)}")
    for k in ("RETAIN", "REJECT", "GDPR_REVIEW"):
        out.append(f"- **{k}:** {by_decision.get(k, 0)}")
    out += ["", "### RETAIN by section", ""]
    for sec, n in sorted(by_section.items()):
        out.append(f"- {sec}: {n}")
    out += ["", "### REJECT by reason category", ""]
    for r, n in sorted(by_reject.items(), key=lambda x: -x[1]):
        out.append(f"- {r}: {n}")
    out += ["", "### GDPR / Consent flagged (user action required)", ""]
    if gdpr:
        for d in gdpr:
            out.append(f"- `{d['filename']}` — {d.get('reason') or ''}")
    else:
        out.append("- (none)")
    return "\n".join(out)


def main():
    inventory = json.load(open(sys.argv[1]))           # /tmp/inventory.json
    dups = json.load(open(sys.argv[2]))["vs_reference"] # /tmp/dedup.json
    decisions_path = Path(sys.argv[3])                  # curation-decisions.json
    decisions = [json.loads(l) for l in decisions_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    out_path = Path(sys.argv[4])                        # final report path

    body = f"""# Curation report — batch photos 2026-05-25

**Spec :** [`docs/superpowers/specs/2026-05-25-photos-realisations-design.md`](superpowers/specs/2026-05-25-photos-realisations-design.md)
**Plan :** [`docs/superpowers/plans/2026-05-25-photos-realisations.md`](superpowers/plans/2026-05-25-photos-realisations.md)
**Source archive :** `fb-photos-raw/` (gitignored, {inventory['total']} fichiers)
**Generated:** {Path(__file__).name} from inventory + dedup + decisions

---

## Action utilisateur requise

Avant d'intégrer les photos flagged GDPR (notamment les chevalier1-5),
contacter le client "Chevalier" via une réponse à son avis Google pour
demander son consentement explicite à la ré-utilisation des photos sur
le site web Chauffage & Moi. À défaut → REJECT toute la sous-série.

---

{render_summary(decisions)}

---

## Décisions détaillées (table)

{render_table(decisions, dups)}
"""
    out_path.write_text(body, encoding="utf-8")
    print(f"Report written: {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the generator**

```bash
python scripts/curation/generate_report.py \
  /tmp/inventory.json \
  /tmp/dedup.json \
  fb-photos-raw/curation-decisions.json \
  docs/realisations-curation-2026-05-25.md
```

Expected: `Report written: docs/realisations-curation-2026-05-25.md`.

- [ ] **Step 3: Open the report and sanity-check**

```bash
head -80 docs/realisations-curation-2026-05-25.md
wc -l docs/realisations-curation-2026-05-25.md
```

Expected: 90+ rows in the decisions table, summary stats present, GDPR section populated with chevalier entries.

- [ ] **Step 4: Commit the report and the generator script**

```bash
git add scripts/curation/generate_report.py docs/realisations-curation-2026-05-25.md
git commit -m "feat(curation): generate report from inventory/dedup/decisions

Le rapport docs/realisations-curation-2026-05-25.md liste les 90
photos du batch avec décision (RETAIN/REJECT/GDPR_REVIEW), section
cible, nouveau nom, caption FR et raison. Stats agrégées et liste
des photos GDPR-flagged en tête.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 5: 🚦 GATE — utilisateur lit le rapport et valide**

**STOP** — ne pas continuer Task 10 avant que l'utilisateur ait :

1. Ouvert et relu `docs/realisations-curation-2026-05-25.md`
2. Validé les décisions RETAIN (filename → section, new_name, caption)
3. Décidé pour chaque GDPR_REVIEW : autoriser après consentement OU rejeter
4. Confirmé "OK pour intégration"

Si modifications demandées : éditer `fb-photos-raw/curation-decisions.json`, re-générer (Step 2), re-commit (Step 4 avec message `fix(curation): update report per user feedback`).

---

## Phase D — Intégration Astro (Tasks 10-12)

### Task 10: Copy curated photos to `public/photos/` with new names

**Files:**
- Create: `C:\Users\maxen\chauffageetmoi-v2\public\photos\<new files>.jpg` (N nouveaux)

**Why:** Décisions RETAIN du rapport doivent se matérialiser comme fichiers dans `public/photos/`. PNG Durlem + WebP chevalier (si HD + consentement) → conversion via Task 6.

- [ ] **Step 1: Materialize copies for JPEG RETAIN (FB + WhatsApp)**

Create `scripts/curation/apply_decisions.py`:

```python
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
```

- [ ] **Step 2: Run the apply script**

```bash
python scripts/curation/apply_decisions.py \
  fb-photos-raw/curation-decisions.json \
  fb-photos-raw \
  public/photos \
  fb-photos-raw/chevalier-hd > /tmp/applied.json
cat /tmp/applied.json
```

Expected: `sections` dict mapping each of `chauffage`/`sanitaire`/`adoucisseur`/`pac`/`equipe` to its list of new filenames; `skipped` lists any files that couldn't be processed (e.g., chevalier HD not found — acceptable if §7 phase 7 failed).

- [ ] **Step 3: Verify new files on disk**

```bash
ls public/photos/ | wc -l
# Avant: 23. Après: 23 + N (where N = total length across sections)
git status --short public/photos/ | head -20
```

Expected: count = 23 + N. All new files appear as `??` (untracked).

- [ ] **Step 4: Commit the apply script and new photos**

```bash
git add scripts/curation/apply_decisions.py public/photos/
git commit -m "feat(realisations): add N curated photos to public/photos/

Photos issues du batch 2026-05-25 selon decisions du rapport
docs/realisations-curation-2026-05-25.md. Renommees selon convention
spec §4 (kebab-case, prefix par categorie).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

Replace `N` in the commit message with the actual number.

---

### Task 11: Extend `src/pages/realisations.astro` with new entries + PAC section

**Files:**
- Modify: `C:\Users\maxen\chauffageetmoi-v2\src\pages\realisations.astro`

**Why:** Spec §3.1 — étendre les `gal*` arrays, créer `galPAC` + nouvelle `<section>` si applicable, renommer titre Adoucisseurs.

- [ ] **Step 1: Build the new entries from `applied.json` + decisions**

For each `(section, new_name)` from `/tmp/applied.json`, look up the matching caption in `fb-photos-raw/curation-decisions.json`. Produce TypeScript object literals like:

```ts
{ src: '/photos/chaudiere-bulex-cave.jpg', caption: 'Chaudière Bulex — installation cave' },
```

Group by section. Save as scratch notes file (you'll paste these into the .astro file in next steps).

- [ ] **Step 2: Extend `galChauffage` array**

Open `src/pages/realisations.astro`. Locate the closing `];` of `galChauffage` (around line 12). **Before** the `];`, insert a comma after the last entry and add the new objects, one per line, matching the existing indentation (2 spaces). Example after edit:

```ts
const galChauffage = [
  { src: '/photos/chaudiere-vaillant-cave.jpg', caption: 'Chaudière Vaillant — installation cave' },
  { src: '/photos/chaudiere-vaillant-brique.jpg', caption: 'Chaudière Vaillant — mur brique' },
  { src: '/photos/chaudiere-vaillant-pierre.jpg', caption: 'Chaudière Vaillant — pierre apparente' },
  { src: '/photos/vaillant-avant-apres.jpg', caption: 'Vaillant — avant/après' },
  { src: '/photos/remplacement-avant-apres.jpg', caption: 'Remplacement chaudière — avant/après' },
  { src: '/photos/radiateur-design-noir.jpg', caption: 'Radiateur design vertical noir' },
  // NEW entries from batch 2026-05-25:
  { src: '/photos/<new1>.jpg', caption: '<caption1>' },
  // ... etc
];
```

- [ ] **Step 3: Extend `galSanitaire`, `galAdoucisseur`, `galEquipe` similarly**

Apply the same pattern to each remaining existing array. For `galAdoucisseur`, ensure Durlem entries (if any RETAIN) are appended after the existing Solucalc entries.

- [ ] **Step 4: If PAC section retained → add `galPAC` array + new `<section>` block**

If `sections.pac` exists and is non-empty in `applied.json`, add the array **after `galEquipe`** (around line 35 in current file) but **before** the `const totalPhotos` line:

```ts
const galPAC = [
  { src: '/photos/pac-air-eau-brick.jpg', caption: 'PAC air-eau — unité extérieure' },
  // ... entries from sections.pac
];
```

Update `totalPhotos` line to include `galPAC.length`:

```ts
const totalPhotos = galChauffage.length + galPAC.length + galSanitaire.length + galAdoucisseur.length + galEquipe.length;
```

Then add a new `<section>` block **between the Chauffage section (`</section>` around line 74) and the Sanitaire section** (spec §3.1: ordre logique chaud → froid → sanitaire). Copy the existing Chauffage section as template and rewrite eyebrow/title/lead:

```astro
  <!-- PAC -->
  <section class="py-20 lg:py-28 bg-stone-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Pompes à chaleur</span>
      <h2 class="section-title">Installations PAC</h2>
      <p class="section-lead">PAC air-eau, monoblocs et split — solution chauffage économique et durable.</p>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4">
        {galPAC.map(item => (
          <button type="button" data-lightbox="realisations" data-lightbox-src={item.src} data-lightbox-caption={item.caption} class="relative group overflow-hidden rounded-2xl aspect-square shadow-md cursor-zoom-in text-left bg-stone-200">
            <img src={item.src} alt={item.caption} class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
            <div class="absolute inset-0 bg-gradient-to-t from-marine/80 via-marine/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="absolute bottom-0 left-0 right-0 p-3 sm:p-4 text-white opacity-0 group-hover:opacity-100 transition-opacity">
              <p class="font-semibold text-xs sm:text-sm leading-tight" set:html={item.caption}></p>
            </div>
          </button>
        ))}
      </div>
    </div>
  </section>
```

**Important** : alterner les `bg-*` (Chauffage est `bg-white`, donc PAC est `bg-stone-50`, Sanitaire reste `bg-stone-50` actuel — il faut alors le passer à `bg-white` pour préserver l'alternance). Vérifier la séquence finale : Chauffage(white) → PAC(stone-50) → Sanitaire(white) → Adoucisseur(stone-50) → Équipe(white) → CTA(marine).

Edit Sanitaire section opening tag at current line ~77: change `class="py-20 lg:py-28 bg-stone-50"` → `class="py-20 lg:py-28 bg-white"`.

Edit Adoucisseur section opening tag at current line ~97: change `class="py-20 lg:py-28 bg-white"` → `class="py-20 lg:py-28 bg-stone-50"`.

Edit Équipe section opening tag at current line ~117: change `class="py-20 lg:py-28 bg-stone-50"` → `class="py-20 lg:py-28 bg-white"`.

If `sections.pac` is empty in `applied.json`, **SKIP all of Step 4** — leave the page as 4 sections.

- [ ] **Step 5: Update Adoucisseurs title & lead**

Locate the Adoucisseur `<section>` (around line 97 current, or shifted by PAC insertion). Change:

```astro
<h2 class="section-title">Installations Solucalc</h2>
<p class="section-lead">Chauffage &amp; Moi est installateur agréé Solucalc — adoucisseur écologique au CO₂.</p>
```

to:

```astro
<h2 class="section-title">Installations Solucalc &amp; Durlem</h2>
<p class="section-lead">Deux technologies au choix : Solucalc CO₂ (écologique, sans sel) ou Durlem (au sel, éprouvé). Chauffage &amp; Moi est installateur agréé pour les deux marques.</p>
```

If no Durlem photos were RETAINED, **SKIP** this Step 5 — leave the section title as-is.

- [ ] **Step 6: Quick visual review of the diff**

```bash
git diff src/pages/realisations.astro | head -100
```

Verify:
- All new entries are syntactically valid TypeScript object literals
- No leftover commas at end of arrays
- `totalPhotos` line correctly sums all gal* arrays
- PAC `<section>` correctly inserted between Chauffage and Sanitaire (if applicable)
- Adoucisseur title updated (if applicable)
- bg-* alternation preserved

- [ ] **Step 7: Commit**

```bash
git add src/pages/realisations.astro
git commit -m "feat(realisations): integrate N new photos + optional PAC section

Étend les tableaux galChauffage/galSanitaire/galAdoucisseur/galEquipe
avec les photos du batch 2026-05-25 retenues en curation. Si des
photos PAC sont retenues, ajoute galPAC + nouvelle section
'Pompes à chaleur' entre Chauffage et Sanitaire. Renomme la section
Adoucisseurs en 'Solucalc & Durlem' si des photos Durlem retenues.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 12: Build verification

**Files:** (none modified — just running build)

- [ ] **Step 1: Install Node dependencies if needed**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
npm install
```

Expected: `up to date` or installs missing deps.

- [ ] **Step 2: Run `npm run build`**

```bash
npm run build 2>&1 | tail -40
```

Expected: build succeeds, output ends with something like:
```
✓ Completed in XXXms.
  building client (vite) 
...
```

If build fails:
- TypeScript error → fix syntax in `realisations.astro` (likely a missing comma, mismatched quotes in caption)
- Missing image error → verify all `new_name` values in step 11 match actual files in `public/photos/`
- Re-run after fix

- [ ] **Step 3: Optional local preview**

```bash
npm run dev &
# wait ~3 seconds, then:
curl -s http://localhost:4321/realisations 2>&1 | grep -oE 'pac-[^"]*\.jpg|durlem-[^"]*\.jpg' | head -10
```

Expected: new image paths appear in the HTML output. Kill `npm run dev` after verifying.

- [ ] **Step 4: No commit needed for this verification task — just confirms previous commits work.**

---

## Phase E — Deploy & cleanup (Tasks 13-15)

### Task 13: Push feature branch and watch Vercel deploy

- [ ] **Step 1: Push the feature branch**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
git push -u origin feat/realisations-batch-2026-05
```

Expected: GitHub creates the remote branch. Output includes a URL hint to open a PR.

- [ ] **Step 2: Check Vercel preview deployment**

```bash
vercel ls chauffage-mirror 2>&1 | head -10
```

Expected: a new deployment with status `● Queued` or `● Building` linked to `feat/realisations-batch-2026-05`.

- [ ] **Step 3: Wait for preview ready and capture URL**

Vercel auto-deploys preview on push. Wait until status is `● Ready` (usually <2 min). Get the preview URL:

```bash
vercel ls chauffage-mirror 2>&1 | grep "● Ready" | head -1
```

Expected: a `https://chauffage-mirror-<hash>-unity01s-projects.vercel.app` URL.

- [ ] **Step 4: Smoke-test preview URL**

```bash
PREVIEW_URL="https://chauffage-mirror-<hash>-unity01s-projects.vercel.app"
curl -s -o /dev/null -w "%{http_code}\n" "$PREVIEW_URL/realisations"
```

Expected: `200`.

```bash
curl -s "$PREVIEW_URL/realisations" | grep -oE "totalPhotos[^<]*|/photos/[^\"]*" | head -20
```

Expected: increased photo count visible in markup, new image paths present.

- [ ] **Step 5: Open the preview URL in a browser for visual check**

Manual step — open the preview URL `/realisations` page and visually verify:
- Sections in expected order (Chauffage → PAC if present → Sanitaire → Adoucisseurs → Équipe)
- New photos display without 404 (open devtools, no red entries in Network tab)
- bg-* alternation looks visually balanced
- Lightbox still works (click a new photo)
- Adoucisseur title shows "Solucalc & Durlem" if applicable
- Hero shows new `{totalPhotos}` value

- [ ] **Step 6: Open the PR**

```bash
gh pr create --title "feat(realisations): integrate batch 2026-05-25 photos (N new)" \
  --body "$(cat <<'EOF'
## Summary

Enrichit la galerie /realisations avec les photos pertinentes du batch du 23/25 mai 2026.

## Spec & plan
- Spec : `docs/superpowers/specs/2026-05-25-photos-realisations-design.md`
- Plan : `docs/superpowers/plans/2026-05-25-photos-realisations.md`
- Curation report : `docs/realisations-curation-2026-05-25.md`

## Changes
- `+N` photos curées dans `public/photos/` (kebab-case, captions FR)
- `src/pages/realisations.astro` : tableaux gal* étendus, optionnellement galPAC + section, titre Adoucisseurs étendu Solucalc & Durlem si applicable
- `scripts/curation/` : tooling Python jetable (inventory, dedup phash, conversion JPEG, apply decisions, report generator) — tests inclus
- `.gitignore` : `fb-photos-raw/`

## Out of scope
- Aucune modif des autres pages (index, services, apropos, contact)
- Pas de migration astro:assets
- Pas d'API/CMS

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" --base main
```

Expected: PR URL printed.

---

### Task 14: Merge to main and verify production deploy

- [ ] **Step 1: Merge the PR**

Merge via GitHub UI or:

```bash
gh pr merge --squash --delete-branch
```

Expected: PR closed, branch deleted on remote.

- [ ] **Step 2: Wait for Vercel production deploy**

```bash
sleep 30  # Vercel typically picks up main commit within seconds
vercel ls chauffage-mirror 2>&1 | head -5
```

Expected: a new `production` deployment in `● Building` then `● Ready`.

- [ ] **Step 3: Smoke-test production URL**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://chauffage-mirror.vercel.app/realisations
```

Expected: `200`.

```bash
curl -s https://chauffage-mirror.vercel.app/realisations 2>&1 | grep -oE 'src="/photos/[^"]+"' | sort -u | wc -l
```

Expected: 23 + N unique image references.

- [ ] **Step 4: Visual production check**

Open `https://chauffage-mirror.vercel.app/realisations` in a browser:
- All photos load (no 404)
- New PAC section visible (if applicable)
- Adoucisseur title shows "Solucalc & Durlem" (if applicable)
- Lightbox works on new photos
- Lighthouse mobile score not catastrophically dropped (manual check: > 70 acceptable for this scope)

- [ ] **Step 5: Update local main**

```bash
cd "C:/Users/maxen/chauffageetmoi-v2"
git checkout main
git pull origin main
```

Expected: local main up to date with merged feature.

---

### Task 15: Delete `Photos/` from AI OS repo disk

**Files:**
- Delete: `C:\Users\maxen\Documents\Chauffage-et-moi-Site\Photos\`

**Why:** Spec §11 final done criteria — le dossier orphelin doit disparaître physiquement. Mais seulement après confirmation que la galerie tourne en prod et que `fb-photos-raw/` du repo Astro contient bien les 90 fichiers.

- [ ] **Step 1: Verify the archive is intact in the Astro repo**

```bash
ls "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/" | wc -l
du -sh "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/"
```

Expected: `90` files, `~19M`. **If count mismatches → abort, investigate.**

- [ ] **Step 2: Verify the production site is up and serving the new photos**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://chauffage-mirror.vercel.app/realisations
```

Expected: `200`. If anything else → investigate before deleting source.

- [ ] **Step 3: Merge the AI OS `.gitignore` PR (or fast-forward to master)**

The PR opened at Task 1 Step 5 needs to be merged so that `Photos/` is gitignored on master.

```bash
cd "C:/Users/maxen/Documents/Chauffage-et-moi-Site"
gh pr list --head chore/gitignore-photos-orphan
```

Expected: 1 PR shown. Merge via UI or `gh pr merge`. After merge:

```bash
git checkout master
git pull
git checkout phase-34-editable-policy
git rebase master  # optional, brings .gitignore change into phase-34 branch
```

Expected: phase-34 branch now has the `Photos/` gitignore line.

- [ ] **Step 4: Delete the physical Photos/ directory**

```bash
rm -rf "/c/Users/maxen/Documents/Chauffage-et-moi-Site/Photos/"
ls "/c/Users/maxen/Documents/Chauffage-et-moi-Site/" | grep -i photos
```

Expected: second command returns empty (no Photos/ folder).

- [ ] **Step 5: Verify nothing references Photos/ in either repo**

```bash
cd "/c/Users/maxen/Documents/Chauffage-et-moi-Site"
git grep -l "Photos/" 2>&1 | head -5
```

Expected: only `.gitignore` shows up (the gitignore rule itself). No code reference.

```bash
cd "/c/Users/maxen/chauffageetmoi-v2"
git grep -l "Chauffage-et-moi-Site/Photos" 2>&1 | head -5
```

Expected: empty (or only this plan + spec files mentioning the historical path).

- [ ] **Step 6: Verify `fb-photos-raw/` is still preserved**

```bash
ls "/c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/" | wc -l
```

Expected: still `90`. This is now the only copy — keep it safe.

- [ ] **Step 7: No further commits — the work is done**

The plan ends here. All spec §11 done criteria should be checkable as ✓.

---

## Done Criteria Verification (Spec §11)

After Task 15, verify every checkbox from spec §11:

```bash
# - Photos/ ne figure plus sur disque dans Chauffage-et-moi-Site/
test ! -d "/c/Users/maxen/Documents/Chauffage-et-moi-Site/Photos" && echo "✓ Photos/ deleted"

# - .gitignore du repo AI OS contient une ligne Photos/, commitée
cd "/c/Users/maxen/Documents/Chauffage-et-moi-Site" && \
  git log master --oneline | grep -i "gitignore.*photos" | head -1

# - Le commit .gitignore est sur une branche autre que phase-34-editable-policy
cd "/c/Users/maxen/Documents/Chauffage-et-moi-Site" && \
  git log --all --source --oneline | grep -i "gitignore.*photos" | head -1

# - chauffageetmoi-v2/fb-photos-raw/ contient les 90 fichiers source
test "$(ls /c/Users/maxen/chauffageetmoi-v2/fb-photos-raw/ | wc -l)" = "90" && echo "✓ 90 archived"

# - docs/realisations-curation-2026-05-25.md existe, validé
test -f "/c/Users/maxen/chauffageetmoi-v2/docs/realisations-curation-2026-05-25.md" && echo "✓ report exists"

# - N photos curées copiées dans public/photos/
ls /c/Users/maxen/chauffageetmoi-v2/public/photos/ | wc -l  # should be > 23

# - realisations.astro étendu — check at least the totals
grep -E "const gal[A-Z]" /c/Users/maxen/chauffageetmoi-v2/src/pages/realisations.astro | wc -l
# should be 4 (no PAC) or 5 (with PAC)

# - npm run build passe
cd /c/Users/maxen/chauffageetmoi-v2 && npm run build 2>&1 | tail -1 | grep -i "complet" && echo "✓ build OK"

# - Vercel deploy success
curl -s -o /dev/null -w "%{http_code}\n" https://chauffage-mirror.vercel.app/realisations  # 200

# - Aucune 404 image en prod — visual check via browser
echo "Visual check required: open https://chauffage-mirror.vercel.app/realisations"
```

If all checks ✓ → work complete. Otherwise, revisit the failing step.

---

## Notes for the executing agent

- **Idempotence:** Tasks 2, 3, 10, 11 should be re-runnable if interrupted. The scripts overwrite output files; the .astro patch is the only step that requires manual care to avoid duplicate insertions.
- **Working files:** Files under `fb-photos-raw/` (`curation-decisions.json`, `chevalier-hd-notes.md`, `chevalier-hd/`) are gitignored and never committed. They are working state for Tasks 7-10.
- **Naming consistency:** The `new_name` recorded in `curation-decisions.json` at Task 8 must be exactly the filename written to `public/photos/` at Task 10 and referenced in `realisations.astro` at Task 11. Apply the convention from spec §4 deterministically.
- **Section count contingency:** PAC section creation is conditional on `sections.pac` being non-empty after Task 10. Same for Durlem title rename. Both can be skipped safely.
- **Branch hygiene:** Always be on `feat/realisations-batch-2026-05` when in chauffageetmoi-v2 (Tasks 2-13). Always be on `chore/gitignore-photos-orphan` when modifying AI OS .gitignore (Task 1), and back to `phase-34-editable-policy` afterward.
- **No phase-34 contamination:** Never touch files outside the spec's scope when on the AI OS repo. Phase-34 work continues independently on its own branch.
