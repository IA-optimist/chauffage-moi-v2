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
