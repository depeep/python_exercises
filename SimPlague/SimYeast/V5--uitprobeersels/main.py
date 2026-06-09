import pygame
from simulation import Simulation

pygame.init()

WIDTH, HEIGHT = 1500,1000
SIM_WIDTH = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yeast Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

sim = Simulation(SIM_WIDTH, HEIGHT)
running = True

while running:
    clock.tick(2200)# verhoogde tickrate voor snellere simulatie 60 werkt echt te sloom
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
        screen.blit(text, (520, 40 + i * 40))

# new code for drawing graphs
    max_value=max(1, max(sim.population_history, default=1))
    pop_his=sim.population_history
    alco_his=sim.alcohol_history
    sim.draw_graph(screen, pop_his, (100, 220, 255), 520, 360, 1000, 220, max_value)
    sim.draw_graph(screen, alco_his, (255, 140, 100), 520, 680, 1000, 220, 15)

    pygame.display.flip()

pygame.quit()
