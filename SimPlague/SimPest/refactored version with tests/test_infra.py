"""
tests/test_infra.py
Tests for infra/helpers.py and infra/asset_manager.py
"""

import math
import pytest
from unittest.mock import MagicMock, patch

from infra.helpers import distance, clamp
from infra.asset_manager import AssetManager, DummySound


# ============================================================
# helpers.py
# ============================================================

class TestDistance:
    def test_same_point_is_zero(self):
        assert distance([0, 0], [0, 0]) == 0.0

    def test_horizontal(self):
        assert distance([0, 0], [3, 0]) == pytest.approx(3.0)

    def test_vertical(self):
        assert distance([0, 0], [0, 4]) == pytest.approx(4.0)

    def test_diagonal_pythagorean(self):
        # 3-4-5 triangle
        assert distance([0, 0], [3, 4]) == pytest.approx(5.0)

    def test_symmetry(self):
        a, b = [1, 2], [5, 9]
        assert distance(a, b) == pytest.approx(distance(b, a))

    def test_negative_coordinates(self):
        assert distance([-1, -1], [2, 3]) == pytest.approx(5.0)

    def test_float_coordinates(self):
        assert distance([0.0, 0.0], [1.0, 1.0]) == pytest.approx(math.sqrt(2))


class TestClamp:
    def test_below_min_returns_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_above_max_returns_max(self):
        assert clamp(20, 0, 10) == 10

    def test_within_range_unchanged(self):
        assert clamp(5, 0, 10) == 5

    def test_at_min_boundary(self):
        assert clamp(0, 0, 10) == 0

    def test_at_max_boundary(self):
        assert clamp(10, 0, 10) == 10

    def test_float_values(self):
        assert clamp(0.5, 0.0, 1.0) == pytest.approx(0.5)

    def test_negative_range(self):
        assert clamp(-15, -10, -1) == -10


# ============================================================
# asset_manager.py – DummySound
# ============================================================

class TestDummySound:
    def test_play_does_not_raise(self):
        ds = DummySound()
        ds.play()   # must not raise

    def test_play_returns_none(self):
        ds = DummySound()
        assert ds.play() is None


# ============================================================
# asset_manager.py – AssetManager
# ============================================================

class TestAssetManager:
    def test_get_image_missing_key_returns_none(self):
        am = AssetManager()
        assert am.get_image("nonexistent") is None

    def test_load_and_get_image(self, tmp_path):
        am = AssetManager()
        fake_img = MagicMock()
        fake_img.convert_alpha.return_value = fake_img
        fake_img.convert.return_value = fake_img

        with patch("pygame.image.load", return_value=fake_img), \
             patch("pygame.transform.smoothscale", return_value=fake_img):
            result = am.load_image("rabbit", tmp_path / "rabbit.png", size=(32, 32))

        assert result is fake_img
        assert am.get_image("rabbit") is fake_img

    def test_load_image_without_size_skips_scale(self, tmp_path):
        am = AssetManager()
        fake_img = MagicMock()
        fake_img.convert_alpha.return_value = fake_img

        with patch("pygame.image.load", return_value=fake_img) as mock_load, \
             patch("pygame.transform.smoothscale") as mock_scale:
            am.load_image("x", tmp_path / "x.png")

        mock_scale.assert_not_called()

    def test_get_sound_missing_key_returns_dummy(self):
        am = AssetManager()
        result = am.get_sound("missing")
        assert isinstance(result, DummySound)

    def test_load_sound_success(self, tmp_path):
        am = AssetManager()
        fake_snd = MagicMock()

        with patch("pygame.mixer.Sound", return_value=fake_snd):
            result = am.load_sound("eat", tmp_path / "eat.mp3")

        assert result is fake_snd
        assert am.get_sound("eat") is fake_snd

    def test_load_sound_failure_stores_dummy(self, tmp_path):
        am = AssetManager()
        with patch("pygame.mixer.Sound", side_effect=Exception("no audio")):
            result = am.load_sound("eat", tmp_path / "missing.mp3")

        assert isinstance(result, DummySound)
        assert isinstance(am.get_sound("eat"), DummySound)

    def test_images_dict_accumulates_keys(self, tmp_path):
        am = AssetManager()
        fake_img = MagicMock()
        fake_img.convert_alpha.return_value = fake_img

        with patch("pygame.image.load", return_value=fake_img), \
             patch("pygame.transform.smoothscale", return_value=fake_img):
            am.load_image("a", tmp_path / "a.png", size=(10, 10))
            am.load_image("b", tmp_path / "b.png", size=(10, 10))

        assert "a" in am.images
        assert "b" in am.images
