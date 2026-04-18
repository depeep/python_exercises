import pygame
pygame.init()
size = (1600, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Jos's event_demo1")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()