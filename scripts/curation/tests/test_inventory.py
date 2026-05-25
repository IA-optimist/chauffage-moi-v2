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
