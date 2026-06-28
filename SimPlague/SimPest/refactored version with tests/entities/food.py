from entities.sprite import Sprite
import math
import random

class Food(Sprite):
    
    
    def __init__(self, image, game):
        super().__init__(image, game)
        self.reset()

    
    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]
        self.age = 0

    def update(self):
        self.age += 1

        if self.age > self.game.food_max_age:
            if self in self.game.foodPopulation:
                self.game.foodPopulation.remove(self)
            return

        if self.game.food_speed > 0:
            self.position[0] += random.uniform(-self.game.food_speed, self.game.food_speed)
            self.position[1] += random.uniform(-self.game.food_speed, self.game.food_speed)
            self.placeInScreen()