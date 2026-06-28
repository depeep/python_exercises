from entities.sprite import Sprite
import math
import random
        
class Prey1(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.reset()
        self.eatSound = self.game.assets.get_sound("eat")
        self.energy = self.game.prey1_start_energy
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.prey1_max_age:
            if self in self.game.prey1Population:
                self.game.prey1Population.remove(self)
            return

        self.energy -= self.game.prey1_energy_loss
        if self.energy <= 0:
            if self in self.game.prey1Population:
                self.game.prey1Population.remove(self)
            return

        target = self.game.engine.getClosestFood(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position
            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.prey1_speed * dx / dist
                self.position[1] += self.game.prey1_speed * dy / dist

        self.placeInScreen()

    def eat(self, food):
        self.energy += self.game.prey1_energy_gain
        self.eatSound.play()

        if self.energy > self.game.prey1_reproduction_energy:
            self.energy -= self.game.prey1_reproduction_cost
            self.game.factory.spawnPrey1()


    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]
