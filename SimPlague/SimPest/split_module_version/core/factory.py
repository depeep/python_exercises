from entities.prey1 import Prey1
from entities.prey2 import Prey2
from entities.predator import Predator
from entities.food import Food


class EntityFactory:
    def __init__(self, game):
        self.game = game

    def spawnPrey1(self):
        self.game.prey1Population.append(
            Prey1(self.game.prey1Image, self.game)
        )

    def spawnPrey(self):  # alias voor oudere code / snapshot
        self.spawnPrey1()

   
    def spawnPrey2(self):
        self.game.prey2Population.append(
            Prey2(self.game.prey2Image, self.game)
        )

    def spawnPredator(self):
        self.game.predatorPopulation.append(
            Predator(self.game.predImage, self.game)
        )

    def spawnFood(self):
        if len(self.game.foodPopulation) < self.game.max_food:
            self.game.foodPopulation.append(
                Food(self.game.foodImage, self.game)
            )
