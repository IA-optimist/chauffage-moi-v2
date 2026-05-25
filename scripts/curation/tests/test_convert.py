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
