"""
tests/test_entities.py
Tests for entities/sprite.py, food.py, prey1.py, prey2.py, predator.py
"""

import pytest
from unittest.mock import MagicMock, patch


# ============================================================
# Sprite (base class)
# ============================================================

class TestSprite:
    def test_position_initialised(self, game):
        from entities.sprite import Sprite
        s = Sprite(game.foodImage, game)
        assert isinstance(s.position, list)
        assert len(s.position) == 2

    def test_draw_blits_to_surface(self, game, fake_surface):
        from entities.sprite import Sprite
        game.surface = fake_surface
        s = Sprite(game.foodImage, game)
        s.draw()
        assert len(fake_surface.blits) == 1

    def test_place_in_screen_clamps_left(self, game):
        from entities.sprite import Sprite
        s = Sprite(game.foodImage, game)
        s.position = [game.sim_rect.left - 100, game.sim_rect.top + 10]
        s.placeInScreen()
        assert s.position[0] >= game.sim_rect.left

    def test_place_in_screen_clamps_top(self, game):
        from entities.sprite import Sprite
        s = Sprite(game.foodImage, game)
        s.position = [game.sim_rect.left + 10, game.sim_rect.top - 100]
        s.placeInScreen()
        assert s.position[1] >= game.sim_rect.top

    def test_place_in_screen_clamps_right(self, game):
        from entities.sprite import Sprite
        s = Sprite(game.foodImage, game)
        right_max = game.sim_rect.right - s.image.get_width()
        s.position = [game.sim_rect.right + 999, game.sim_rect.top + 10]
        s.placeInScreen()
        assert s.position[0] <= right_max

    def test_place_in_screen_clamps_bottom(self, game):
        from entities.sprite import Sprite
        s = Sprite(game.foodImage, game)
        bottom_max = game.sim_rect.bottom - s.image.get_height()
        s.position = [game.sim_rect.left + 10, game.sim_rect.bottom + 999]
        s.placeInScreen()
        assert s.position[1] <= bottom_max

    # --- collidesWith ---
    def test_collides_with_overlapping_sprite(self, game):
        from entities.sprite import Sprite
        a = Sprite(game.foodImage, game)
        b = Sprite(game.foodImage, game)
        a.position = [500, 500]
        b.position = [500, 500]    # exact overlap
        assert a.collidesWith(b) is True

    def test_no_collision_far_apart(self, game):
        from entities.sprite import Sprite
        a = Sprite(game.foodImage, game)
        b = Sprite(game.foodImage, game)
        a.position = [500, 500]
        b.position = [900, 900]    # far away
        assert a.collidesWith(b) is False

    def test_no_collision_just_right_of(self, game):
        from entities.sprite import Sprite
        a = Sprite(game.foodImage, game)
        b = Sprite(game.foodImage, game)
        # b starts exactly where a ends → no overlap
        a.position = [500, 500]
        b.position = [500 + a.image.get_width() + 1, 500]
        assert a.collidesWith(b) is False

    def test_collision_is_symmetric(self, game):
        from entities.sprite import Sprite
        a = Sprite(game.foodImage, game)
        b = Sprite(game.foodImage, game)
        a.position = [500, 500]
        b.position = [510, 510]
        assert a.collidesWith(b) == b.collidesWith(a)


# ============================================================
# Food
# ============================================================

class TestFood:
    def test_initial_age_zero(self, make_food):
        f = make_food()
        assert f.age == 0

    def test_position_within_sim_rect(self, make_food, game):
        f = make_food()
        assert game.sim_rect.left <= f.position[0] <= game.sim_rect.right
        assert game.sim_rect.top  <= f.position[1] <= game.sim_rect.bottom

    def test_update_increments_age(self, make_food):
        f = make_food()
        f.update()
        assert f.age == 1

    def test_update_removes_when_too_old(self, make_food, game):
        f = make_food()
        game.foodPopulation.append(f)
        f.age = game.food_max_age   # one step away from dying
        f.update()
        assert f not in game.foodPopulation

    def test_update_still_alive_below_max_age(self, make_food, game):
        f = make_food()
        game.foodPopulation.append(f)
        f.age = game.food_max_age - 5
        f.update()
        assert f in game.foodPopulation

    def test_reset_sets_age_zero(self, make_food):
        f = make_food()
        f.age = 999
        f.reset()
        assert f.age == 0

    def test_food_moves_when_speed_nonzero(self, make_food, game):
        game.food_speed = 5.0
        f = make_food()
        original = list(f.position)
        # update many times to statistically guarantee movement
        moved = False
        for _ in range(20):
            f.update()
            if f.position != original:
                moved = True
                break
        assert moved

    def test_food_stays_put_when_speed_zero(self, make_food, game):
        game.food_speed = 0.0
        f = make_food()
        original = list(f.position)
        f.update()
        assert f.position == original


# ============================================================
# Prey1
# ============================================================

class TestPrey1:
    def test_initial_energy(self, make_prey1, game):
        p = make_prey1()
        assert p.energy == game.prey1_start_energy

    def test_initial_age_zero(self, make_prey1):
        p = make_prey1()
        assert p.age == 0

    def test_update_increments_age(self, make_prey1):
        p = make_prey1()
        p.update()
        assert p.age == 1

    def test_update_loses_energy(self, make_prey1, game):
        p = make_prey1()
        initial = p.energy
        p.update()
        assert p.energy == pytest.approx(initial - game.prey1_energy_loss)

    def test_dies_of_old_age(self, make_prey1, game):
        p = make_prey1()
        game.prey1Population.append(p)
        p.age = game.prey1_max_age
        p.update()
        assert p not in game.prey1Population

    def test_dies_of_starvation(self, make_prey1, game):
        p = make_prey1()
        game.prey1Population.append(p)
        p.energy = 0.05   # will be ≤0 after energy_loss
        p.update()
        assert p not in game.prey1Population

    def test_moves_toward_food(self, make_prey1, game):
        from entities.food import Food
        p = make_prey1()
        food = Food(game.foodImage, game)
        food.position = [600, 600]
        p.position    = [500, 500]
        game.engine.getClosestFood.return_value = food

        old_pos = list(p.position)
        p.update()
        # should have moved closer to (600, 600)
        dx_old = food.position[0] - old_pos[0]
        dy_old = food.position[1] - old_pos[1]
        dx_new = food.position[0] - p.position[0]
        dy_new = food.position[1] - p.position[1]
        assert dx_new ** 2 + dy_new ** 2 < dx_old ** 2 + dy_old ** 2

    def test_eat_increases_energy(self, make_prey1, game):
        p = make_prey1()
        p.energy = 50.0
        food_stub = MagicMock()
        p.eat(food_stub)
        assert p.energy == pytest.approx(50.0 + game.prey1_energy_gain)

    def test_eat_triggers_reproduction_when_enough_energy(self, make_prey1, game):
        p = make_prey1()
        # set energy just above reproduction threshold - energy_gain will push it over
        p.energy = game.prey1_reproduction_energy - game.prey1_energy_gain + 1
        food_stub = MagicMock()
        p.eat(food_stub)
        game.factory.spawnPrey1.assert_called_once()

    def test_eat_deducts_reproduction_cost(self, make_prey1, game):
        p = make_prey1()
        p.energy = game.prey1_reproduction_energy + 1   # already enough before eating
        food_stub = MagicMock()
        # make eat push it past the threshold
        expected_after_gain = p.energy + game.prey1_energy_gain
        p.eat(food_stub)
        assert p.energy == pytest.approx(expected_after_gain - game.prey1_reproduction_cost)

    def test_eat_plays_sound(self, make_prey1, game):
        p = make_prey1()
        p.eat(MagicMock())
        p.eatSound.play.assert_called_once()

    def test_no_reproduction_below_threshold(self, make_prey1, game):
        p = make_prey1()
        p.energy = 10.0    # well below reproduction threshold
        p.eat(MagicMock())
        game.factory.spawnPrey1.assert_not_called()

    def test_reset_randomises_position(self, make_prey1, game):
        p = make_prey1()
        positions = set()
        for _ in range(10):
            p.reset()
            positions.add(tuple(p.position))
        # at least two distinct positions over 10 resets
        assert len(positions) > 1


# ============================================================
# Prey2
# ============================================================

class TestPrey2:
    def test_initial_energy(self, make_prey2, game):
        p = make_prey2()
        assert p.energy == game.prey2_start_energy

    def test_initial_age_zero(self, make_prey2):
        p = make_prey2()
        assert p.age == 0

    def test_update_loses_energy(self, make_prey2, game):
        p = make_prey2()
        initial = p.energy
        p.update()
        assert p.energy == pytest.approx(initial - game.prey2_energy_loss)

    def test_dies_of_old_age(self, make_prey2, game):
        p = make_prey2()
        game.prey2Population.append(p)
        p.age = game.prey2_max_age
        p.update()
        assert p not in game.prey2Population

    def test_dies_of_starvation(self, make_prey2, game):
        p = make_prey2()
        game.prey2Population.append(p)
        p.energy = 0.1
        p.update()
        assert p not in game.prey2Population

    def test_eat_increases_energy(self, make_prey2, game):
        p = make_prey2()
        p.energy = 30.0
        p.eat(MagicMock())
        assert p.energy == pytest.approx(30.0 + game.prey2_energy_gain)

    def test_eat_triggers_reproduction(self, make_prey2, game):
        p = make_prey2()
        p.energy = game.prey2_reproduction_energy - game.prey2_energy_gain + 1
        p.eat(MagicMock())
        game.factory.spawnPrey2.assert_called_once()

    def test_no_reproduction_below_threshold(self, make_prey2, game):
        p = make_prey2()
        p.energy = 10.0
        p.eat(MagicMock())
        game.factory.spawnPrey2.assert_not_called()

    def test_eat_plays_sound(self, make_prey2):
        p = make_prey2()
        p.eat(MagicMock())
        p.eatSound.play.assert_called_once()

    def test_moves_toward_food(self, make_prey2, game):
        from entities.food import Food
        p = make_prey2()
        food = Food(game.foodImage, game)
        food.position = [700, 700]
        p.position    = [500, 500]
        game.engine.getClosestFood.return_value = food

        old_dist_sq = (700 - 500) ** 2 + (700 - 500) ** 2
        p.update()
        new_dist_sq = (food.position[0] - p.position[0]) ** 2 + \
                      (food.position[1] - p.position[1]) ** 2
        assert new_dist_sq < old_dist_sq

    def test_prey2_faster_than_prey1(self, game):
        """Prey2 speed parameter should be higher than Prey1's."""
        assert game.prey2_speed > game.prey1_speed


# ============================================================
# Predator
# ============================================================

class TestPredator:
    def test_initial_energy(self, make_predator, game):
        pred = make_predator()
        assert pred.energy == game.predator_start_energy

    def test_initial_age_zero(self, make_predator):
        pred = make_predator()
        assert pred.age == 0

    def test_update_loses_energy(self, make_predator, game):
        pred = make_predator()
        game.engine.getClosestAnyPreyTarget.return_value = None
        initial = pred.energy
        pred.update()
        assert pred.energy == pytest.approx(initial - game.predator_energy_loss)

    def test_dies_of_old_age(self, make_predator, game):
        pred = make_predator()
        game.predatorPopulation.append(pred)
        game.engine.getClosestAnyPreyTarget.return_value = None
        pred.age = game.predator_max_age
        pred.update()
        assert pred not in game.predatorPopulation

    def test_dies_of_starvation(self, make_predator, game):
        pred = make_predator()
        game.predatorPopulation.append(pred)
        game.engine.getClosestAnyPreyTarget.return_value = None
        pred.energy = 0.5
        pred.update()
        assert pred not in game.predatorPopulation

    def test_moves_toward_prey(self, make_predator, game, make_prey1):
        prey = make_prey1()
        prey.position = [700, 700]
        pred = make_predator()
        pred.position = [500, 500]
        game.engine.getClosestAnyPreyTarget.return_value = prey

        old_dist_sq = (700 - 500) ** 2 + (700 - 500) ** 2
        pred.update()
        new_dist_sq = (prey.position[0] - pred.position[0]) ** 2 + \
                      (prey.position[1] - pred.position[1]) ** 2
        assert new_dist_sq < old_dist_sq

    def test_kills_prey1_on_collision(self, make_predator, game, make_prey1):
        prey = make_prey1()
        prey.position = [500, 500]
        pred = make_predator()
        pred.position = [500, 500]          # same position → collision
        game.prey1Population.append(prey)
        game.engine.getClosestAnyPreyTarget.return_value = prey

        pred.update()
        assert prey not in game.prey1Population

    def test_kills_prey2_on_collision(self, make_predator, game, make_prey2):
        prey = make_prey2()
        prey.position = [500, 500]
        pred = make_predator()
        pred.position = [500, 500]
        game.prey2Population.append(prey)
        game.engine.getClosestAnyPreyTarget.return_value = prey

        pred.update()
        assert prey not in game.prey2Population

    def test_gains_energy_after_eating(self, make_predator, game, make_prey1):
        prey = make_prey1()
        prey.position = [500, 500]
        game.prey1Population.append(prey)
        pred = make_predator()
        pred.position = [500, 500]
        pred.energy = 50.0
        game.engine.getClosestAnyPreyTarget.return_value = prey

        pred.update()
        # Energy after = 50 - loss + gain (collision happened)
        assert pred.energy > 50.0 - game.predator_energy_loss

    def test_reproduces_when_energy_high(self, make_predator, game):
        pred = make_predator()
        game.engine.getClosestAnyPreyTarget.return_value = None
        # Set energy above reproduction threshold
        pred.energy = game.predator_reproduction_energy + game.predator_energy_loss + 1
        pred.update()
        game.factory.spawnPredator.assert_called_once()

    def test_no_reproduction_below_threshold(self, make_predator, game):
        pred = make_predator()
        game.engine.getClosestAnyPreyTarget.return_value = None
        pred.energy = game.predator_start_energy   # well below reproduction
        pred.update()
        game.factory.spawnPredator.assert_not_called()

    def test_stays_within_sim_bounds(self, make_predator, game, make_prey1):
        prey = make_prey1()
        prey.position = [1500, 900]
        pred = make_predator()
        pred.position = [game.sim_rect.right - 10, game.sim_rect.bottom - 10]
        game.engine.getClosestAnyPreyTarget.return_value = prey

        pred.update()
        assert pred.position[0] <= game.sim_rect.right
        assert pred.position[1] <= game.sim_rect.bottom
