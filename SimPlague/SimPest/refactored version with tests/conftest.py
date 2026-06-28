"""
conftest.py – shared fixtures for the Survival Simulation test suite.

All pygame rendering is mocked so the tests run headlessly without a display.
The MagicMock-based `game` fixture mirrors the real SurvivalSim attribute
contract so each module can be tested in isolation.
"""

import sys
import types
from unittest.mock import MagicMock, patch
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Stub the entire pygame package before any simulation module is imported.
# This prevents "No video mode set" errors in headless CI environments.
# ---------------------------------------------------------------------------

def _make_pygame_stub():
    pg = types.ModuleType("pygame")

    # --- constants ---
    for name in ("QUIT", "MOUSEBUTTONDOWN", "MOUSEBUTTONUP", "MOUSEMOTION",
                 "KEYDOWN", "K_RETURN", "K_ESCAPE", "K_BACKSPACE"):
        setattr(pg, name, 0)

    # --- Rect ---
    class Rect:
        def __init__(self, x=0, y=0, w=0, h=0):
            self.x = x; self.y = y
            self.width = w; self.height = h
            self.left = x; self.top = y
            self.right = x + w; self.bottom = y + h
        def collidepoint(self, pos): return False
        def __iter__(self): return iter((self.x, self.y, self.width, self.height))
    pg.Rect = Rect

    # --- surface / image ---
    surf = MagicMock()
    surf.get_width.return_value = 32
    surf.get_height.return_value = 32
    pg.Surface = MagicMock(return_value=surf)

    img_mod = types.ModuleType("pygame.image")
    img_mod.load = MagicMock(return_value=surf)
    pg.image = img_mod

    transform_mod = types.ModuleType("pygame.transform")
    transform_mod.smoothscale = MagicMock(return_value=surf)
    pg.transform = transform_mod

    font_mod = types.ModuleType("pygame.font")
    font_obj = MagicMock()
    font_obj.render.return_value = surf
    font_mod.SysFont = MagicMock(return_value=font_obj)
    font_mod.Font   = MagicMock(return_value=font_obj)
    pg.font = font_mod

    mixer_mod = types.ModuleType("pygame.mixer")
    mixer_mod.init = MagicMock()
    mixer_mod.Sound = MagicMock(return_value=MagicMock())
    pg.mixer = mixer_mod

    pg.init = MagicMock()
    pg.quit = MagicMock()
    pg.display = MagicMock()
    pg.draw    = MagicMock()
    pg.event   = MagicMock(return_value=[])
    pg.mouse   = MagicMock()
    pg.time    = MagicMock()
    pg.Color   = MagicMock()
    return pg


_pygame_stub = _make_pygame_stub()
sys.modules["pygame"] = _pygame_stub
sys.modules["pygame.image"]     = _pygame_stub.image
sys.modules["pygame.transform"] = _pygame_stub.transform
sys.modules["pygame.font"]      = _pygame_stub.font
sys.modules["pygame.mixer"]     = _pygame_stub.mixer

# ---------------------------------------------------------------------------
# Put the project root on sys.path so `from core.xxx import …` works.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent / "split_module_version"
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Minimal fake surface that tracks blit calls
# ---------------------------------------------------------------------------
class FakeSurface:
    def __init__(self, w=32, h=32):
        self._w = w; self._h = h
        self.blits = []
    def get_width(self):  return self._w
    def get_height(self): return self._h
    def blit(self, src, pos): self.blits.append((src, pos))
    def convert(self):   return self
    def convert_alpha(self): return self


# ---------------------------------------------------------------------------
# Core game fixture — a MagicMock shaped like SurvivalSim
# ---------------------------------------------------------------------------
@pytest.fixture()
def fake_surface():
    return FakeSurface(w=32, h=32)


@pytest.fixture()
def game(fake_surface, tmp_path):
    """
    Lightweight stand-in for SurvivalSim.
    Provides every attribute referenced by entities, engine, factory, etc.
    """
    import pygame
    g = MagicMock()

    # layout
    g.sim_rect = pygame.Rect(400, 0, 1200, 960)
    g.surface  = fake_surface

    # populations
    g.prey1Population   = []
    g.prey2Population   = []
    g.predatorPopulation = []
    g.foodPopulation    = []
    g.preyPopulation    = g.prey1Population   # alias

    # history
    from collections import deque
    g.food_history  = deque(maxlen=340)
    g.prey1_history = deque(maxlen=340)
    g.prey2_history = deque(maxlen=340)
    g.pred_history  = deque(maxlen=340)

    # food params
    g.start_food        = 10
    g.food_speed        = 0.0
    g.food_max_age      = 1800
    g.food_spawn_chance = 0.0
    g.max_food          = 50

    # prey1 params
    g.prey1_speed              = 2.0
    g.prey1_max_age            = 1600
    g.prey1_start_energy       = 110.0
    g.prey1_reproduction_energy = 85.0
    g.prey1_energy_gain        = 20.0
    g.prey1_energy_loss        = 0.10
    g.prey1_reproduction_cost  = 55.0

    # prey2 params
    g.prey2_speed              = 4.8
    g.prey2_max_age            = 1100
    g.prey2_start_energy       = 95.0
    g.prey2_reproduction_energy = 110.0
    g.prey2_energy_gain        = 18.0
    g.prey2_energy_loss        = 0.18
    g.prey2_reproduction_cost  = 60.0

    # predator params
    g.predator_speed              = 2.6
    g.predator_max_age            = 950
    g.predator_start_energy       = 240.0
    g.predator_reproduction_energy = 700.0
    g.predator_energy_gain        = 55.0
    g.predator_energy_loss        = 1.8
    g.predator_reproduction_cost  = 500.0

    # services
    g.assets = MagicMock()
    g.assets.get_sound.return_value = MagicMock()

    g.logger = MagicMock()
    g.logger.timestep_counter = 0

    g.snapshot_engine = MagicMock()
    g.factory = MagicMock()
    g.engine  = MagicMock()

    # image stubs
    img = FakeSurface(32, 32)
    g.prey1Image = img
    g.prey2Image = img
    g.predImage  = img
    g.foodImage  = img

    # paths
    g.export_dir = tmp_path / "export"
    g.db_path    = tmp_path / "sim.db"

    return g


# ---------------------------------------------------------------------------
# Convenience: entity constructors with the fake game wired in
# ---------------------------------------------------------------------------
@pytest.fixture()
def make_food(game):
    from entities.food import Food
    def _make():
        return Food(game.foodImage, game)
    return _make


@pytest.fixture()
def make_prey1(game):
    from entities.prey1 import Prey1
    def _make():
        return Prey1(game.prey1Image, game)
    return _make


@pytest.fixture()
def make_prey2(game):
    from entities.prey2 import Prey2
    def _make():
        return Prey2(game.prey2Image, game)
    return _make


@pytest.fixture()
def make_predator(game):
    from entities.predator import Predator
    def _make():
        return Predator(game.predImage, game)
    return _make
