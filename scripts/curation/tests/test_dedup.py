"""Tests for the perceptual-hash deduplication logic."""
import shutil
from pathlib import Path

import imagehash
import numpy as np
import pytest
from PIL import Image

from scripts.curation.dedup_phash import (
    DEDUP_THRESHOLD,
    hash_file,
    find_duplicates,
)


def _make_checkerboard(size: int = 200, cell: int = 10) -> Image.Image:
    """Create a fine checkerboard with strong DCT content for pHash."""
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(0, size, cell):
        for x in range(0, size, cell):
            if (x // cell + y // cell) % 2 == 0:
                arr[y : y + cell, x : x + cell] = 255
    return Image.fromarray(arr)


@pytest.fixture
def tmp_photos(tmp_path: Path) -> Path:
    """Create a tiny test photoset: two near-identical + one different.

    pHash operates on DCT; uniform-color blocks collapse to the same hash
    regardless of hue. We use structured images (checkerboard vs all-black)
    to get a reliable hamming distance >> DEDUP_THRESHOLD.
    """
    folder = tmp_path / "photos"
    folder.mkdir()
    # Image A: checkerboard (strong spatial structure)
    img_a = _make_checkerboard()
    img_a.save(folder / "a.jpg")
    # Image A': identical pixel data -> dist=0
    img_a.save(folder / "a_copy.jpg")
    # Image B: all-black (different DCT profile, dist >> DEDUP_THRESHOLD)
    Image.new("RGB", (200, 200), color=(0, 0, 0)).save(folder / "b.jpg")
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
