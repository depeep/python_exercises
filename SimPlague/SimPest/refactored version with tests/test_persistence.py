"""
tests/test_persistence.py
Tests for persistence/data_logger.py and persistence/snapshot_engine.py
"""

import csv
import sqlite3
import pytest
from pathlib import Path
from unittest.mock import MagicMock


# ============================================================
# DataLogger
# ============================================================

class TestDataLogger:

    @pytest.fixture()
    def logger(self, tmp_path):
        from persistence.data_logger import DataLogger
        return DataLogger(tmp_path / "export")

    def test_initial_timestep_counter_zero(self, logger):
        assert logger.timestep_counter == 0

    def test_start_new_run_creates_csv(self, logger):
        logger.start_new_run()
        assert logger.csv_path.exists()

    def test_start_new_run_creates_export_dir(self, tmp_path):
        from persistence.data_logger import DataLogger
        export = tmp_path / "new" / "subdir"
        dl = DataLogger(export)
        dl.start_new_run()
        assert export.exists()

    def test_start_new_run_resets_counter(self, logger):
        logger.start_new_run()
        logger.log_step(1, 2, 3, 4)
        logger.start_new_run()
        assert logger.timestep_counter == 0

    def test_start_new_run_resets_full_data(self, logger):
        logger.start_new_run()
        logger.log_step(1, 2, 3, 4)
        logger.start_new_run()
        assert logger.full_data == []

    def test_log_step_increments_counter(self, logger):
        logger.start_new_run()
        logger.log_step(5, 3, 2, 1)
        assert logger.timestep_counter == 1

    def test_log_step_returns_row(self, logger):
        logger.start_new_run()
        row = logger.log_step(10, 5, 3, 2)
        assert row == [0, 10, 5, 3, 2]

    def test_log_step_appends_to_full_data(self, logger):
        logger.start_new_run()
        logger.log_step(1, 2, 3, 4)
        logger.log_step(5, 6, 7, 8)
        assert len(logger.full_data) == 2

    def test_log_step_writes_to_csv(self, logger):
        logger.start_new_run()
        logger.log_step(10, 5, 3, 1)
        logger.close_csv()

        with open(logger.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            rows = list(reader)

        # row 0 = header, row 1 = data
        assert rows[0] == ["Timestep", "Food", "Prey1", "Prey2", "Predators"]
        assert rows[1] == ["0", "10", "5", "3", "1"]

    def test_multiple_steps_all_written(self, logger):
        logger.start_new_run()
        for i in range(5):
            logger.log_step(i, i, i, i)
        logger.close_csv()

        with open(logger.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            rows = list(reader)

        assert len(rows) == 6   # 1 header + 5 data rows

    def test_close_csv_is_idempotent(self, logger):
        logger.start_new_run()
        logger.close_csv()
        logger.close_csv()   # second call must not raise

    def test_log_step_without_run_does_not_crash(self, logger):
        # csv_writer is None — should not raise
        row = logger.log_step(1, 2, 3, 4)
        assert row is not None

    def test_export_snapshot_creates_file(self, logger, tmp_path):
        logger.start_new_run()
        logger.log_step(5, 3, 2, 1)
        name = logger.export_snapshot()
        assert (logger.export_dir / name).exists()

    def test_export_snapshot_file_contains_data(self, logger):
        logger.start_new_run()
        logger.log_step(7, 4, 3, 2)
        name = logger.export_snapshot()

        with open(logger.export_dir / name, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter=";"))

        assert rows[0] == ["Timestep", "Food", "Prey1", "Prey2", "Predators"]
        assert rows[1][0] == "0"   # first timestep

    def test_timestep_monotonically_increases(self, logger):
        logger.start_new_run()
        for _ in range(3):
            logger.log_step(1, 1, 1, 1)
        assert logger.full_data[0][0] == 0
        assert logger.full_data[1][0] == 1
        assert logger.full_data[2][0] == 2


# ============================================================
# SnapshotEngine
# ============================================================

class TestSnapshotEngine:

    @pytest.fixture()
    def se(self, tmp_path):
        from persistence.snapshot_engine import SnapshotEngine
        engine = SnapshotEngine(tmp_path / "sim.db")
        yield engine
        engine.close()

    @pytest.fixture()
    def populated_game(self, game, make_food, make_prey1, make_prey2, make_predator):
        """Game with one of each entity type in populations."""
        f = make_food();  f.age = 5;    game.foodPopulation = [f]
        p1 = make_prey1(); p1.energy = 80.0; p1.age = 10; game.prey1Population = [p1]
        p2 = make_prey2(); p2.energy = 60.0; p2.age = 20; game.prey2Population = [p2]
        pr = make_predator(); pr.energy = 200.0; pr.age = 15; game.predatorPopulation = [pr]
        game.preyPopulation = game.prey1Population   # alias
        game.logger.timestep_counter = 42
        return game

    # --- table creation ---

    def test_tables_exist(self, se):
        se.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='snapshots'").fetchone()
        se.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entities'").fetchone()

    # --- save ---

    def test_save_returns_integer_id(self, se, populated_game):
        sid = se.save(populated_game)
        assert isinstance(sid, int)
        assert sid >= 1

    def test_save_records_timestep(self, se, populated_game):
        sid = se.save(populated_game)
        row = se.cur.execute(
            "SELECT timestep FROM snapshots WHERE id=?", (sid,)
        ).fetchone()
        assert row[0] == 42

    def test_save_stores_all_entity_types(self, se, populated_game):
        sid = se.save(populated_game)
        rows = se.cur.execute(
            "SELECT type FROM entities WHERE snapshot_id=?", (sid,)
        ).fetchall()
        types = {r[0] for r in rows}
        assert "food"     in types
        assert "prey"     in types   # prey1 stored as "prey"
        assert "prey2"    in types
        assert "predator" in types

    def test_save_stores_positions(self, se, populated_game):
        populated_game.foodPopulation[0].position = [612.5, 333.0]
        sid = se.save(populated_game)
        row = se.cur.execute(
            "SELECT x, y FROM entities WHERE snapshot_id=? AND type='food'", (sid,)
        ).fetchone()
        assert row[0] == pytest.approx(612.5)
        assert row[1] == pytest.approx(333.0)

    def test_save_stores_energy(self, se, populated_game):
        populated_game.prey1Population[0].energy = 77.5
        sid = se.save(populated_game)
        row = se.cur.execute(
            "SELECT energy FROM entities WHERE snapshot_id=? AND type='prey'", (sid,)
        ).fetchone()
        assert row[0] == pytest.approx(77.5)

    def test_multiple_saves_create_multiple_snapshots(self, se, populated_game):
        se.save(populated_game)
        se.save(populated_game)
        rows = se.cur.execute("SELECT COUNT(*) FROM snapshots").fetchone()
        assert rows[0] == 2

    # --- list_snapshots ---

    def test_list_snapshots_empty_initially(self, se):
        assert se.list_snapshots() == []

    def test_list_snapshots_returns_all(self, se, populated_game):
        se.save(populated_game)
        se.save(populated_game)
        snaps = se.list_snapshots()
        assert len(snaps) == 2

    def test_list_snapshots_ordered_by_id(self, se, populated_game):
        populated_game.logger.timestep_counter = 1
        se.save(populated_game)
        populated_game.logger.timestep_counter = 2
        se.save(populated_game)
        snaps = se.list_snapshots()
        assert snaps[0][0] < snaps[1][0]

    def test_list_snapshots_contains_timestep(self, se, populated_game):
        populated_game.logger.timestep_counter = 99
        se.save(populated_game)
        snaps = se.list_snapshots()
        assert snaps[0][1] == 99

    # --- get_latest_snapshot_id ---

    def test_get_latest_snapshot_id_none_when_empty(self, se):
        assert se.get_latest_snapshot_id() is None

    def test_get_latest_snapshot_id_returns_max(self, se, populated_game):
        id1 = se.save(populated_game)
        id2 = se.save(populated_game)
        assert se.get_latest_snapshot_id() == max(id1, id2)

    # --- load ---

    def test_load_restores_prey1_count(self, se, populated_game, game):
        from core.factory import EntityFactory
        game.factory = EntityFactory(game)
        sid = se.save(populated_game)
        # clear populations
        game.prey1Population.clear()
        game.prey2Population.clear()
        game.predatorPopulation.clear()
        game.foodPopulation.clear()
        game.preyPopulation = game.prey1Population

        se.load(game, sid)
        assert len(game.prey1Population) == 1

    def test_load_restores_food_count(self, se, populated_game, game):
        from core.factory import EntityFactory
        game.factory = EntityFactory(game)
        sid = se.save(populated_game)
        game.foodPopulation.clear()
        game.prey1Population.clear()
        game.prey2Population.clear()
        game.predatorPopulation.clear()
        game.preyPopulation = game.prey1Population

        se.load(game, sid)
        assert len(game.foodPopulation) == 1

    def test_load_restores_predator_count(self, se, populated_game, game):
        from core.factory import EntityFactory
        game.factory = EntityFactory(game)
        sid = se.save(populated_game)
        game.predatorPopulation.clear()
        game.foodPopulation.clear()
        game.prey1Population.clear()
        game.prey2Population.clear()
        game.preyPopulation = game.prey1Population

        se.load(game, sid)
        assert len(game.predatorPopulation) == 1

    def test_load_restores_prey1_position(self, se, populated_game, game):
        from core.factory import EntityFactory
        game.factory = EntityFactory(game)
        original_pos = list(populated_game.prey1Population[0].position)
        sid = se.save(populated_game)

        game.prey1Population.clear()
        game.prey2Population.clear()
        game.predatorPopulation.clear()
        game.foodPopulation.clear()
        game.preyPopulation = game.prey1Population

        se.load(game, sid)
        assert game.prey1Population[0].position == pytest.approx(original_pos)

    def test_load_clears_existing_populations(self, se, populated_game, game,
                                              make_prey1):
        from core.factory import EntityFactory
        game.factory = EntityFactory(game)
        sid = se.save(populated_game)
        # Add extra entities that should be wiped by load
        game.prey1Population.append(make_prey1())
        game.prey1Population.append(make_prey1())
        game.preyPopulation = game.prey1Population

        se.load(game, sid)
        assert len(game.prey1Population) == 1   # only the restored one

    # --- clear_all ---

    def test_clear_all_empties_snapshots(self, se, populated_game):
        se.save(populated_game)
        se.clear_all()
        assert se.list_snapshots() == []

    def test_clear_all_empties_entities(self, se, populated_game):
        se.save(populated_game)
        se.clear_all()
        rows = se.cur.execute("SELECT COUNT(*) FROM entities").fetchone()
        assert rows[0] == 0

    def test_clear_all_allows_new_save_after(self, se, populated_game):
        se.save(populated_game)
        se.clear_all()
        sid = se.save(populated_game)
        assert sid is not None
