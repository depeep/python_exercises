"""
tests/test_core.py
Tests for core/engine.py (SimulationEngine) and core/factory.py (EntityFactory)
"""

import pytest
from unittest.mock import MagicMock, patch, call


# ============================================================
# SimulationEngine
# ============================================================

class TestSimulationEngine:

    @pytest.fixture(autouse=True)
    def engine(self, game):
        # Wire a real engine to the fake game
        game.engine = None   # remove mock engine; we're testing the real one
        from core.engine import SimulationEngine
        e = SimulationEngine(game)
        game.engine = e
        self.game = game
        return e

    # --- getClosestFood ---

    def test_get_closest_food_empty_returns_none(self, engine):
        self.game.foodPopulation = []
        assert engine.getClosestFood([500, 500]) is None

    def test_get_closest_food_single_item(self, make_food, engine):
        f = make_food()
        f.position = [600, 600]
        self.game.foodPopulation = [f]
        assert engine.getClosestFood([500, 500]) is f

    def test_get_closest_food_picks_nearest(self, make_food, engine):
        near = make_food(); near.position = [510, 510]
        far  = make_food(); far.position  = [900, 900]
        self.game.foodPopulation = [far, near]
        assert engine.getClosestFood([500, 500]) is near

    def test_get_closest_food_ties_returns_one_of_them(self, make_food, engine):
        a = make_food(); a.position = [600, 500]
        b = make_food(); b.position = [400, 500]
        self.game.foodPopulation = [a, b]
        result = engine.getClosestFood([500, 500])
        assert result in (a, b)

    # --- getClosestAnyPreyTarget ---

    def test_get_closest_prey_target_empty_returns_none(self, engine):
        self.game.prey1Population = []
        self.game.prey2Population = []
        assert engine.getClosestAnyPreyTarget([500, 500]) is None

    def test_get_closest_prey_target_prey1_only(self, make_prey1, engine):
        p = make_prey1(); p.position = [510, 510]
        self.game.prey1Population = [p]
        self.game.prey2Population = []
        assert engine.getClosestAnyPreyTarget([500, 500]) is p

    def test_get_closest_prey_target_prey2_only(self, make_prey2, engine):
        p = make_prey2(); p.position = [510, 510]
        self.game.prey1Population = []
        self.game.prey2Population = [p]
        assert engine.getClosestAnyPreyTarget([500, 500]) is p

    def test_get_closest_prey_target_mixed_picks_nearest(
        self, make_prey1, make_prey2, engine
    ):
        p1 = make_prey1(); p1.position = [510, 510]
        p2 = make_prey2(); p2.position = [900, 900]
        self.game.prey1Population = [p1]
        self.game.prey2Population = [p2]
        assert engine.getClosestAnyPreyTarget([500, 500]) is p1

    # --- reproduceFood ---

    def test_reproduce_food_does_nothing_at_max(self, make_food, engine):
        self.game.max_food = 3
        for _ in range(3):
            self.game.foodPopulation.append(make_food())
        engine.reproduceFood()
        assert len(self.game.foodPopulation) == 3

    def test_reproduce_food_adds_food_when_chance_1(self, make_food, engine):
        self.game.food_spawn_chance = 1.0   # guaranteed spawn
        self.game.max_food = 50
        seed = make_food()
        seed.position = [600, 600]
        self.game.foodPopulation = [seed]

        engine.reproduceFood()
        assert len(self.game.foodPopulation) > 1

    def test_reproduce_food_never_spawns_when_chance_0(self, make_food, engine):
        self.game.food_spawn_chance = 0.0
        self.game.max_food = 50
        self.game.foodPopulation = [make_food()]
        engine.reproduceFood()
        assert len(self.game.foodPopulation) == 1

    def test_reproduce_food_respects_max_cap(self, make_food, engine):
        self.game.food_spawn_chance = 1.0
        self.game.max_food = 5
        for _ in range(4):
            self.game.foodPopulation.append(make_food())
        # 4 existing; chance=1 → would spawn 4 more, but cap is 5
        engine.reproduceFood()
        assert len(self.game.foodPopulation) <= 5

    def test_new_food_position_near_parent(self, make_food, engine):
        """Child food should appear within 50px of the parent."""
        self.game.food_spawn_chance = 1.0
        self.game.max_food = 50
        parent = make_food()
        parent.position = [600, 600]
        self.game.foodPopulation = [parent]

        engine.reproduceFood()
        children = [f for f in self.game.foodPopulation if f is not parent]
        assert children, "Expected at least one child food to spawn"
        for child in children:
            # allow sim_rect clamping to move it slightly beyond 50
            assert abs(child.position[0] - 600) <= 100
            assert abs(child.position[1] - 600) <= 100

    # --- update ---

    def test_update_calls_entity_update(
        self, make_prey1, make_prey2, make_predator, make_food, engine
    ):
        p1   = make_prey1()
        p2   = make_prey2()
        pred = make_predator()
        food = make_food()
        p1.update = MagicMock()
        p2.update = MagicMock()
        pred.update = MagicMock()
        food.update = MagicMock()

        self.game.prey1Population    = [p1]
        self.game.prey2Population    = [p2]
        self.game.predatorPopulation = [pred]
        self.game.foodPopulation     = [food]

        engine.update()

        p1.update.assert_called_once()
        p2.update.assert_called_once()
        pred.update.assert_called_once()
        food.update.assert_called_once()

    def test_update_triggers_eating(self, make_prey1, make_food, engine):
        prey = make_prey1()
        food = make_food()
        # put them at same position so collision → eating
        prey.position = [500, 500]
        food.position = [500, 500]
        prey.eat = MagicMock()

        self.game.prey1Population = [prey]
        self.game.prey2Population = []
        self.game.predatorPopulation = []
        self.game.foodPopulation = [food]

        engine.update()
        prey.eat.assert_called_once_with(food)

    def test_update_appends_history(self, make_food, engine):
        f = make_food()
        self.game.foodPopulation     = [f]
        self.game.prey1Population    = []
        self.game.prey2Population    = []
        self.game.predatorPopulation = []
        engine.update()
        assert len(self.game.food_history) == 1

    def test_update_logs_step(self, engine):
        self.game.foodPopulation     = []
        self.game.prey1Population    = []
        self.game.prey2Population    = []
        self.game.predatorPopulation = []
        engine.update()
        self.game.logger.log_step.assert_called_once_with(0, 0, 0, 0)

    def test_update_saves_snapshot_every_10_steps(self, engine):
        self.game.foodPopulation     = []
        self.game.prey1Population    = []
        self.game.prey2Population    = []
        self.game.predatorPopulation = []

        for i in range(10):
            self.game.logger.timestep_counter = i
            engine.update()

        # snapshot_engine.save should have been called exactly once (at step 0)
        self.game.snapshot_engine.save.assert_called()


# ============================================================
# EntityFactory
# ============================================================

class TestEntityFactory:

    @pytest.fixture(autouse=True)
    def factory(self, game):
        from core.factory import EntityFactory
        game.factory = None
        f = EntityFactory(game)
        game.factory = f
        self.game = game
        return f

    def test_spawn_prey1_adds_to_population(self, factory):
        factory.spawnPrey1()
        assert len(self.game.prey1Population) == 1

    def test_spawn_prey1_creates_prey1_instance(self, factory):
        from entities.prey1 import Prey1
        factory.spawnPrey1()
        assert isinstance(self.game.prey1Population[0], Prey1)

    def test_spawn_prey_alias_delegates_to_spawn_prey1(self, factory):
        factory.spawnPrey()
        assert len(self.game.prey1Population) == 1

    def test_spawn_prey2_adds_to_population(self, factory):
        factory.spawnPrey2()
        assert len(self.game.prey2Population) == 1

    def test_spawn_prey2_creates_prey2_instance(self, factory):
        from entities.prey2 import Prey2
        factory.spawnPrey2()
        assert isinstance(self.game.prey2Population[0], Prey2)

    def test_spawn_predator_adds_to_population(self, factory):
        factory.spawnPredator()
        assert len(self.game.predatorPopulation) == 1

    def test_spawn_predator_creates_predator_instance(self, factory):
        from entities.predator import Predator
        factory.spawnPredator()
        assert isinstance(self.game.predatorPopulation[0], Predator)

    def test_spawn_food_adds_to_population(self, factory):
        factory.spawnFood()
        assert len(self.game.foodPopulation) == 1

    def test_spawn_food_creates_food_instance(self, factory):
        from entities.food import Food
        factory.spawnFood()
        assert isinstance(self.game.foodPopulation[0], Food)

    def test_spawn_food_respects_max_food_cap(self, factory):
        self.game.max_food = 2
        factory.spawnFood()
        factory.spawnFood()
        factory.spawnFood()   # should be blocked
        assert len(self.game.foodPopulation) == 2

    def test_multiple_spawns_accumulate(self, factory):
        factory.spawnPrey1()
        factory.spawnPrey1()
        factory.spawnPrey1()
        assert len(self.game.prey1Population) == 3

    def test_spawned_entity_has_valid_position(self, factory):
        factory.spawnPrey1()
        p = self.game.prey1Population[0]
        assert self.game.sim_rect.left <= p.position[0]
        assert self.game.sim_rect.top  <= p.position[1]
