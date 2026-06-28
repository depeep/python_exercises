"""
tests/test_ui.py
Tests for ui/ui_controller.py (UIController) and ui/graph.py (GraphRenderer)
"""

import pytest
from unittest.mock import MagicMock, patch, call
from collections import deque


# ============================================================
# UIController
# ============================================================

class TestUIController:

    @pytest.fixture(autouse=True)
    def ui(self, game):
        import pygame
        from ui.ui_controller import UIController
        game.paused = True
        game.simulation_started = False
        game.sim_speed = 1.0
        game.panel_width = 390
        game.height = 1200
        game.tinyFont  = MagicMock()
        game.smallFont = MagicMock()
        game.uiFont    = MagicMock()
        ctrl = UIController(game)
        ctrl.setup_ui()
        self.game = game
        self.ui   = ctrl
        return ctrl

    # --- initial state ---

    def test_buttons_created_after_setup(self, ui):
        assert len(ui.buttons) > 0

    def test_param_fields_created_after_setup(self, ui):
        assert len(ui.param_fields) > 0

    def test_active_field_initially_none(self, ui):
        assert ui.active_field is None

    def test_slider_value_in_range(self, ui):
        assert 0.0 <= ui.slider_value <= 1.0

    # --- handle_button: start ---

    def test_start_unpauses_game(self, ui):
        self.game.paused = True
        self.game.simulation_started = True
        ui.handle_button("start")
        assert self.game.paused is False

    def test_start_calls_reset_when_not_started(self, ui):
        self.game.simulation_started = False
        ui.handle_button("start")
        self.game.resetSimulation.assert_called_once()

    def test_start_calls_logger_start_new_run_when_not_started(self, ui):
        self.game.simulation_started = False
        ui.handle_button("start")
        self.game.logger.start_new_run.assert_called_once()

    def test_start_does_not_reset_when_already_started(self, ui):
        self.game.simulation_started = True
        ui.handle_button("start")
        self.game.resetSimulation.assert_not_called()

    # --- handle_button: pause ---

    def test_pause_sets_paused_true(self, ui):
        self.game.paused = False
        ui.handle_button("pause")
        assert self.game.paused is True

    # --- handle_button: reset ---

    def test_reset_pauses_game(self, ui):
        self.game.paused = False
        ui.handle_button("reset")
        assert self.game.paused is True

    def test_reset_calls_reset_simulation(self, ui):
        ui.handle_button("reset")
        self.game.resetSimulation.assert_called_once()

    def test_reset_marks_not_started(self, ui):
        self.game.simulation_started = True
        ui.handle_button("reset")
        assert self.game.simulation_started is False

    def test_reset_closes_csv(self, ui):
        ui.handle_button("reset")
        self.game.logger.close_csv.assert_called_once()

    # --- handle_button: step ---

    def test_step_calls_engine_update(self, ui):
        ui.handle_button("step")
        self.game.engine.update.assert_called_once()

    def test_step_keeps_game_paused(self, ui):
        self.game.paused = False
        ui.handle_button("step")
        assert self.game.paused is True

    def test_step_syncs_aliases(self, ui):
        ui.handle_button("step")
        self.game.sync_prey1_aliases.assert_called()

    # --- handle_button: spawn ---

    def test_spawn_prey1(self, ui):
        ui.handle_button("spawn_prey1")
        self.game.factory.spawnPrey1.assert_called_once()

    def test_spawn_prey2(self, ui):
        ui.handle_button("spawn_prey2")
        self.game.factory.spawnPrey2.assert_called_once()

    def test_spawn_food(self, ui):
        ui.handle_button("spawn_food")
        self.game.factory.spawnFood.assert_called_once()

    def test_spawn_predator(self, ui):
        ui.handle_button("spawn_pred")
        self.game.factory.spawnPredator.assert_called_once()

    # --- handle_button: export ---

    def test_export_csv_calls_logger(self, ui):
        self.game.logger.export_snapshot.return_value = "run.csv"
        ui.handle_button("export_csv")
        self.game.logger.export_snapshot.assert_called_once()

    def test_export_params_creates_file(self, ui, tmp_path):
        self.game.export_dir = tmp_path / "exports"
        self.game.export_dir.mkdir()
        self.game.sim_speed = 1.5
        self.game.max_food  = 100
        self.game.logger.timestep_counter = 50
        ui.handle_button("export_params")
        files = list((tmp_path / "exports").glob("parameters-*.txt"))
        assert len(files) == 1

    def test_export_params_file_contains_params(self, ui, tmp_path):
        self.game.export_dir = tmp_path / "exports"
        self.game.export_dir.mkdir()
        self.game.logger.timestep_counter = 7
        ui.handle_button("export_params")
        txt = list((tmp_path / "exports").glob("parameters-*.txt"))[0].read_text()
        assert "sim_speed" in txt
        assert "max_food"  in txt

    # --- handle_button: clear_snapshots ---

    def test_clear_snapshots_calls_engine(self, ui):
        ui.handle_button("clear_snapshots")
        self.game.snapshot_engine.clear_all.assert_called_once()

    def test_clear_snapshots_resets_slider(self, ui):
        ui.time_slider_value = 0.8
        ui.handle_button("clear_snapshots")
        assert ui.time_slider_value == 0.0

    # --- text input ---

    def test_text_input_ignored_when_no_active_field(self, ui):
        event = MagicMock()
        event.key     = 0
        event.unicode = "5"
        ui.active_field = None
        ui.handle_text_input(event)
        assert ui.input_text == ""

    def test_text_input_adds_digit(self, ui):
        import pygame
        ui.active_field = 0
        ui.input_text   = ""
        event = MagicMock()
        event.key     = 0
        event.unicode = "7"
        ui.handle_text_input(event)
        assert "7" in ui.input_text

    def test_text_input_backspace(self, ui):
        import pygame
        ui.active_field = 0
        ui.input_text   = "42"
        event = MagicMock()
        event.key     = pygame.K_BACKSPACE
        event.unicode = ""
        ui.handle_text_input(event)
        assert ui.input_text == "4"

    def test_text_input_escape_clears_field(self, ui):
        import pygame
        ui.active_field = 0
        ui.input_text   = "99"
        event = MagicMock()
        event.key     = pygame.K_ESCAPE
        event.unicode = ""
        ui.handle_text_input(event)
        assert ui.active_field is None
        assert ui.input_text == ""

    def test_commit_int_field(self, ui):
        import pygame
        # food_max_age is int
        idx = next(
            i for i, f in enumerate(ui.param_fields) if f["attr"] == "start_food"
        )
        ui.active_field = idx
        ui.input_text   = "25"
        event = MagicMock()
        event.key     = pygame.K_RETURN
        event.unicode = ""
        ui.handle_text_input(event)
        assert self.game.start_food == 25

    def test_commit_negative_value_clamped_to_zero(self, ui):
        import pygame
        idx = next(
            i for i, f in enumerate(ui.param_fields) if f["attr"] == "start_food"
        )
        ui.active_field = idx
        ui.input_text   = "-5"
        event = MagicMock()
        event.key     = pygame.K_RETURN
        event.unicode = ""
        ui.handle_text_input(event)
        assert self.game.start_food == 0

    def test_commit_invalid_text_leaves_value_unchanged(self, ui):
        import pygame
        self.game.start_food = 10
        idx = next(
            i for i, f in enumerate(ui.param_fields) if f["attr"] == "start_food"
        )
        ui.active_field = idx
        ui.input_text   = "abc"
        event = MagicMock()
        event.key     = pygame.K_RETURN
        event.unicode = ""
        ui.handle_text_input(event)
        assert self.game.start_food == 10

    # --- speed slider ---

    def test_speed_slider_min(self, ui):
        import pygame
        ui.update_speed_slider_from_mouse(ui.slider_rect.left)
        assert self.game.sim_speed == pytest.approx(0.1)

    def test_speed_slider_max(self, ui):
        import pygame
        ui.update_speed_slider_from_mouse(ui.slider_rect.right)
        assert self.game.sim_speed == pytest.approx(5.0)

    def test_speed_slider_clamped_below(self, ui):
        ui.update_speed_slider_from_mouse(ui.slider_rect.left - 9999)
        assert self.game.sim_speed >= 0.1

    def test_speed_slider_clamped_above(self, ui):
        ui.update_speed_slider_from_mouse(ui.slider_rect.right + 9999)
        assert self.game.sim_speed <= 5.0


# ============================================================
# GraphRenderer
# ============================================================

class TestGraphRenderer:

    @pytest.fixture(autouse=True)
    def graph(self, game):
        import pygame
        from ui.graph import GraphRenderer
        game.graph_rect = pygame.Rect(390, 960, 1210, 240)
        game.uiFont    = MagicMock()
        game.smallFont = MagicMock()
        game.max_history = 340

        # Provide history data
        game.food_history  = deque([5, 10, 8, 6], maxlen=340)
        game.prey1_history = deque([3,  4, 3, 2], maxlen=340)
        game.prey2_history = deque([2,  3, 2, 1], maxlen=340)
        game.pred_history  = deque([1,  1, 1, 1], maxlen=340)

        gr = GraphRenderer(game)
        self.game = game
        self.gr   = gr
        return gr

    def test_draw_does_not_raise(self, graph):
        graph.draw()   # should complete without exceptions

    def test_draw_renders_title(self, graph):
        graph.draw()
        self.game.uiFont.render.assert_called()

    def test_draw_with_empty_history_does_not_crash(self, graph):
        self.game.food_history.clear()
        self.game.prey1_history.clear()
        self.game.prey2_history.clear()
        self.game.pred_history.clear()
        graph.draw()   # must not raise

    def test_draw_with_single_entry_does_not_crash(self, graph):
        self.game.food_history  = deque([5])
        self.game.prey1_history = deque([3])
        self.game.prey2_history = deque([2])
        self.game.pred_history  = deque([1])
        graph.draw()

    def test_graph_renderer_holds_game_reference(self, graph):
        assert self.gr.game is self.game
