from entities.sprite import Sprite
import math
import random

class Predator(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.reset()
        self.energy = self.game.predator_start_energy
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.predator_max_age:
            if self in self.game.predatorPopulation:
                self.game.predatorPopulation.remove(self)
            return

        self.energy -= self.game.predator_energy_loss
        if self.energy <= 0:
            if self in self.game.predatorPopulation:
                self.game.predatorPopulation.remove(self)
            return

        target = self.game.engine.getClosestAnyPreyTarget(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position
            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.predator_speed * dx / dist
                self.position[1] += self.game.predator_speed * dy / dist

            if self.collidesWith(target):
                self.energy += self.game.predator_energy_gain

                if target in self.game.prey1Population:
                    self.game.prey1Population.remove(target)
                elif target in self.game.prey2Population:
                    self.game.prey2Population.remove(target)

        if self.energy > self.game.predator_reproduction_energy:
            self.energy -= self.game.predator_reproduction_cost
            self.game.factory.spawnPredator()

        self.placeInScreen()

    
    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

