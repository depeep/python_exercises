import random

class YeastCell:
    def __init__(self, x, y, vx=None, vy=None):
        self.x = x
        self.y = y
        self.vx = vx if vx is not None else random.uniform(-0.8, 0.8)
        self.vy = vy if vy is not None else random.uniform(-0.8, 0.8)
        self.age = 0
        self.divisions = 0
        self.max_age = 120
        self.max_divisions = 25
        self.alive = True

    def move(self, width, height, alcohol):
        stress_factor = max(0.3, 1 - alcohol / 15)
        self.x += self.vx * stress_factor
        self.y += self.vy * stress_factor

        if self.x < 10 or self.x > width - 10:
            self.vx *= -1
        if self.y < 10 or self.y > height - 10:
            self.vy *= -1


    def step(self, alcohol):
        self.age += 1
        if self.age > self.max_age:
            self.alive = False
            return
        survival = 0.99
        if alcohol >= 12:
            survival = 0.20
        elif alcohol >= 10:
            survival = 0.85
        elif alcohol >= 8:
            survival = 0.95
        if random.random() > survival:
            self.alive = False

    def can_divide(self, alcohol):
        return self.alive and self.divisions < self.max_divisions and alcohol < 10 and random.random() < 0.03

    def divide(self, width, height):
        self.divisions += 1
        nx = max(10, min(width - 10, self.x + random.randint(-12, 12)))
        ny = max(10, min(height - 10, self.y + random.randint(-12, 12)))
        return YeastCell(nx, ny)
