import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
SIM_WIDTH = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yeast Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

class YeastCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.divisions = 0
        self.max_age = 120
        self.max_divisions = 25
        self.alive = True

    def step(self, alcohol):
        self.age += 1
        if self.age > self.max_age:
            self.alive = False
            return

        survival = 0.99
        if alcohol >= 12:
            survival = 0.2
        elif alcohol >= 10:
            survival = 0.85
        elif alcohol >= 8:
            survival = 0.95

        if random.random() > survival:
            self.alive = False

    def can_divide(self, alcohol):
        return self.alive and self.divisions < self.max_divisions and alcohol < 10 and random.random() < 0.03

    def divide(self):
        self.divisions += 1
        nx = self.x + random.randint(-12, 12)
        ny = self.y + random.randint(-12, 12)
        nx = max(10, min(SIM_WIDTH - 10, nx))
        ny = max(10, min(HEIGHT - 10, ny))
        return YeastCell(nx, ny)

    def draw(self, surface, alcohol):
        if alcohol < 8:
            color = (240, 240, 180)
        elif alcohol < 10:
            color = (255, 180, 80)
        else:
            color = (200, 80, 80)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 4)

cells = [YeastCell(random.randint(20, SIM_WIDTH - 20), random.randint(20, HEIGHT - 20)) for _ in range(80)]
alcohol = 0.0
time_step = 0
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.time.get_ticks() % 200 == 0:
        time_step += 1
        new_cells = []
        alive_cells = []

        for cell in cells:
            cell.step(alcohol)
            if cell.alive:
                alive_cells.append(cell)
                if cell.can_divide(alcohol):
                    new_cells.append(cell.divide())

        cells = alive_cells + new_cells
        alcohol += len(alive_cells) * 0.0002
        if alcohol > 15:
            alcohol = 15

    screen.fill((30, 18, 10))
    pygame.draw.rect(screen, (60, 30, 15), (0, 0, SIM_WIDTH, HEIGHT))
    pygame.draw.rect(screen, (20, 20, 30), (SIM_WIDTH, 0, WIDTH - SIM_WIDTH, HEIGHT))

    for cell in cells:
        cell.draw(screen, alcohol)

    lines = [
        f"Tijd: {time_step}",
        f"Levende cellen: {len(cells)}",
        f"Alcohol: {alcohol:.2f}%"
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, (240, 240, 240))
        screen.blit(text, (720, 40 + i * 40))

    pygame.display.flip()

pygame.quit()
