import pygame
from simulation import Simulation

pygame.init()

WIDTH, HEIGHT = 1000, 600
SIM_WIDTH = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yeast Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

sim = Simulation(SIM_WIDTH, HEIGHT)
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.time.get_ticks() % 200 == 0:
        sim.update()

    screen.fill((30, 18, 10))
    pygame.draw.rect(screen, (60, 30, 15), (0, 0, SIM_WIDTH, HEIGHT))
    pygame.draw.rect(screen, (20, 20, 30), (SIM_WIDTH, 0, WIDTH - SIM_WIDTH, HEIGHT))

    for cell in sim.cells:
        if sim.alcohol < 8:
            color = (240, 240, 180)
        elif sim.alcohol < 10:
            color = (255, 180, 80)
        else:
            color = (200, 80, 80)
        pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), 4)

    lines = [
        f"Tijd: {sim.time_step}",
        f"Levende cellen: {len(sim.cells)}",
        f"Alcohol: {sim.alcohol:.2f}%"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (240, 240, 240))
        screen.blit(text, (720, 40 + i * 40))

    pygame.display.flip()

pygame.quit()
