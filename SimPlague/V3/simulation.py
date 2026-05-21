from yeast import YeastCell
import random

class Simulation:
    def __init__(self, width, height, start_count=80):
        self.width = width
        self.height = height
        self.cells = [YeastCell(random.randint(20, width - 20), random.randint(20, height - 20)) for _ in range(start_count)]
        self.alcohol = 0.0
        self.time_step = 0
        self.population_history = []
        self.alcohol_history = []

    def update(self):
        self.time_step += 1
        new_cells = []
        alive_cells = []

        for cell in self.cells:
            cell.move(self.width, self.height, self.alcohol)
            cell.step(self.alcohol)
            if cell.alive:
                alive_cells.append(cell)
                if cell.can_divide(self.alcohol):
                    new_cells.append(cell.divide(self.width, self.height))

        self.cells = alive_cells + new_cells
        self.alcohol += len(alive_cells) * 0.0002
        self.alcohol = min(self.alcohol, 15)
        self.population_history.append(len(self.cells))
        self.alcohol_history.append(self.alcohol)

    


