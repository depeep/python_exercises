import random

from infra.helpers import distance, clamp
from entities.food import Food


class SimulationEngine:
    def __init__(self, game):
        self.game = game

    def getClosestFood(self, pos):
        if not self.game.foodPopulation:
            return None

        return min(
            self.game.foodPopulation,
            key=lambda f: distance(pos, f.position)
        )

    def getClosestAnyPreyTarget(self, pos):
        all_targets = self.game.prey1Population + self.game.prey2Population

        if not all_targets:
            return None

        return min(
            all_targets,
            key=lambda p: distance(pos, p.position)
        )

    def reproduceFood(self):
        if len(self.game.foodPopulation) >= self.game.max_food:
            return

        new_food = []

        for food in self.game.foodPopulation:
            if len(self.game.foodPopulation) + len(new_food) >= self.game.max_food:
                break

            if random.random() < self.game.food_spawn_chance:
                f = Food(self.game.foodImage, self.game)
                offset = 50

                f.position = [
                    clamp(
                        food.position[0] + random.randint(-offset, offset),
                        self.game.sim_rect.left,
                        self.game.sim_rect.right - f.image.get_width()
                    ),
                    clamp(
                        food.position[1] + random.randint(-offset, offset),
                        self.game.sim_rect.top,
                        self.game.sim_rect.bottom - f.image.get_height()
                    )
                ]

                new_food.append(f)

        self.game.foodPopulation.extend(new_food)

    def update(self):

        # update entities
        for prey1_obj in list(self.game.prey1Population):
            prey1_obj.update()

        for prey2_obj in list(self.game.prey2Population):
            prey2_obj.update()

        for pred in list(self.game.predatorPopulation):
            pred.update()

        for food in list(self.game.foodPopulation):
            food.update()

        # eating logic
        for food in list(self.game.foodPopulation):
            eaten = False

            for prey1_obj in list(self.game.prey1Population):
                if prey1_obj.collidesWith(food):
                    prey1_obj.eat(food)
                    food.reset()
                    eaten = True
                    break

            if eaten:
                continue

            for prey2_obj in list(self.game.prey2Population):
                if prey2_obj.collidesWith(food):
                    prey2_obj.eat(food)
                    food.reset()
                    eaten = True
                    break

        # reproduce
        self.reproduceFood()

        # stats
        self.game.food_history.append(len(self.game.foodPopulation))
        self.game.prey1_history.append(len(self.game.prey1Population))
        self.game.prey2_history.append(len(self.game.prey2Population))
        self.game.pred_history.append(len(self.game.predatorPopulation))

        # logging
        self.game.logger.log_step(
            len(self.game.foodPopulation),
            len(self.game.prey1Population),
            len(self.game.prey2Population),
            len(self.game.predatorPopulation),
        )

        # snapshots (elke 10 stappen)
        if self.game.logger.timestep_counter % 10 == 0:
            self.game.snapshot_engine.save(self.game)