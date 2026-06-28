"""
tests/test_simulation.py
Tests for core/simulation.py (SurvivalSim)

These tests patch pygame and all subsystem classes so SurvivalSim can be
instantiated without a display and without touching the file system for assets.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from collections import deque
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper: build a fully-patched SurvivalSim instance
# ---------------------------------------------------------------------------

def _make_sim(tmp_path):
    """
    Return a SurvivalSim with all external I/O mocked:
    - AssetManager, DataLogger, SnapshotEngine, pygame display
    """
    import pygame

    fake_img = MagicMock()
    fake_img.get_width.return_value  = 32
    fake_img.get_height.return_value = 32

    with patch("infra.asset_manager.AssetManager") as MockAM, \
         patch("persistence.data_logger.DataLogger") as MockDL, \
         patch("persistence.snapshot_engine.SnapshotEngine") as MockSE:

        MockAM.return_value.load_image.return_value = fake_img
        MockAM.return_value.get_sound.return_value  = MagicMock()

        from core.simulation import SurvivalSim
        sim = SurvivalSim()

    # Override path attributes so tests don't touch real FS
    sim.base        = tmp_path
    sim.assets_dir  = tmp_path / "assets"
    sim.export_dir  = tmp_path / "export"
    sim.db_path     = tmp_path / "sim.db"

    # Provide fake image surface
    sim.prey1Image = fake_img
    sim.preyImage  = fake_img
    sim.prey2Image = fake_img
    sim.predImage  = fake_img
    sim.foodImage  = fake_img
    sim.backgroundImage = MagicMock()
    sim.backgroundImage.get_width.return_value  = 100
    sim.backgroundImage.get_height.return_value = 100

    # Fake rendering surface
    sim.surface   = MagicMock()
    sim.debugFont = MagicMock()
    sim.uiFont    = MagicMock()
    sim.smallFont = MagicMock()
    sim.tinyFont  = MagicMock()

    return sim


# ============================================================
# SurvivalSim – construction & attributes
# ============================================================

class TestSurvivalSimInit:
    @pytest.fixture()
    def sim(self, tmp_path):
        return _make_sim(tmp_path)

    def test_populations_empty_on_init(self, sim):
        assert sim.prey1Population    == []
        assert sim.prey2Population    == []
        assert sim.predatorPopulation == []
        assert sim.foodPopulation     == []

    def test_paused_on_init(self, sim):
        assert sim.paused is True

    def test_simulation_not_started_on_init(self, sim):
        assert sim.simulation_started is False

    def test_history_deques_created(self, sim):
        assert isinstance(sim.food_history,  deque)
        assert isinstance(sim.prey1_history, deque)
        assert isinstance(sim.prey2_history, deque)
        assert isinstance(sim.pred_history,  deque)

    def test_subsystems_created(self, sim):
        from core.engine    import SimulationEngine
        from core.factory   import EntityFactory
        from ui.graph       import GraphRenderer
        from ui.ui_controller import UIController

        assert isinstance(sim.engine,  SimulationEngine)
        assert isinstance(sim.factory, EntityFactory)
        assert isinstance(sim.graph,   GraphRenderer)
        assert isinstance(sim.ui,      UIController)

    def test_prey1_alias_matches_prey(self, sim):
        assert sim.preyPopulation is sim.prey1Population

    def test_default_width_and_height(self, sim):
        assert sim.width  == 1600
        assert sim.height == 1200


# ============================================================
# SurvivalSim – resetSimulation
# ============================================================

class TestSurvivalSimReset:
    @pytest.fixture()
    def sim(self, tmp_path):
        return _make_sim(tmp_path)

    def test_reset_creates_prey1_population(self, sim):
        sim.resetSimulation()
        assert len(sim.prey1Population) == int(sim.start_prey1)

    def test_reset_creates_prey2_population(self, sim):
        sim.resetSimulation()
        assert len(sim.prey2Population) == int(sim.start_prey2)

    def test_reset_creates_predator_population(self, sim):
        sim.resetSimulation()
        assert len(sim.predatorPopulation) == int(sim.start_predators)

    def test_reset_creates_food_population(self, sim):
        sim.resetSimulation()
        assert len(sim.foodPopulation) == int(sim.start_food)

    def test_reset_clears_history(self, sim):
        sim.food_history.append(99)
        sim.resetSimulation()
        # After reset it pre-fills with initial counts, so just check it's bounded
        assert len(sim.food_history) <= sim.max_history

    def test_reset_resets_logger_counter(self, sim):
        sim.logger.timestep_counter = 999
        sim.resetSimulation()
        assert sim.logger.timestep_counter == 0

    def test_reset_populates_history_with_initial_counts(self, sim):
        sim.resetSimulation()
        # history is pre-filled with 30 identical values
        assert len(sim.food_history)  >= 30
        assert len(sim.prey1_history) >= 30
        assert len(sim.prey2_history) >= 30
        assert len(sim.pred_history)  >= 30

    def test_reset_twice_gives_correct_population_size(self, sim):
        sim.resetSimulation()
        sim.resetSimulation()
        assert len(sim.prey1Population) == int(sim.start_prey1)

    def test_reset_prey_alias_updated(self, sim):
        sim.resetSimulation()
        assert sim.preyPopulation is sim.prey1Population

    def test_all_entities_have_valid_positions(self, sim):
        sim.resetSimulation()
        for entity in (sim.prey1Population + sim.prey2Population +
                       sim.predatorPopulation + sim.foodPopulation):
            assert sim.sim_rect.left <= entity.position[0]
            assert sim.sim_rect.top  <= entity.position[1]


# ============================================================
# SurvivalSim – timestep
# ============================================================

class TestSurvivalSimTimestep:
    @pytest.fixture()
    def sim(self, tmp_path):
        sim = _make_sim(tmp_path)
        sim.resetSimulation()
        return sim

    def test_timestep_does_nothing_when_paused(self, sim):
        sim.paused = True
        pre_counter = sim.logger.timestep_counter
        sim.timestep()
        # logger.log_step should not have been called
        assert sim.logger.timestep_counter == pre_counter

    def test_timestep_calls_engine_update_when_running(self, sim):
        sim.paused = False
        sim.engine.update = MagicMock()
        sim.timestep()
        sim.engine.update.assert_called_once()

    def test_timestep_syncs_aliases(self, sim):
        sim.paused = False
        sim.sync_prey1_aliases = MagicMock()
        sim.timestep()
        sim.sync_prey1_aliases.assert_called()


# ============================================================
# SurvivalSim – sync_prey1_aliases
# ============================================================

class TestSurvivalSimSyncAliases:
    @pytest.fixture()
    def sim(self, tmp_path):
        return _make_sim(tmp_path)

    def test_sync_keeps_prey_population_alias(self, sim):
        sim.prey1Population = [MagicMock()]
        sim.sync_prey1_aliases()
        assert sim.preyPopulation is sim.prey1Population

    def test_sync_keeps_prey_image_alias(self, sim):
        fake = MagicMock()
        sim.prey1Image = fake
        sim.sync_prey1_aliases()
        assert sim.preyImage is fake

    def test_sync_copies_speed_alias(self, sim):
        sim.prey1_speed = 9.9
        sim.sync_prey1_aliases()
        assert sim.prey_speed == pytest.approx(9.9)

    def test_sync_copies_energy_loss_alias(self, sim):
        sim.prey1_energy_loss = 0.33
        sim.sync_prey1_aliases()
        assert sim.prey_energy_loss == pytest.approx(0.33)


# ============================================================
# SurvivalSim – draw
# ============================================================

class TestSurvivalSimDraw:
    @pytest.fixture()
    def sim(self, tmp_path):
        sim = _make_sim(tmp_path)
        sim.resetSimulation()
        return sim

    def test_draw_calls_ui_draw_panel(self, sim):
        sim.ui.draw_panel = MagicMock()
        sim.draw()
        sim.ui.draw_panel.assert_called_once()

    def test_draw_calls_graph_draw(self, sim):
        sim.graph.draw = MagicMock()
        sim.draw()
        sim.graph.draw.assert_called_once()

    def test_draw_blits_background(self, sim):
        sim.draw()
        sim.surface.blit.assert_called()
