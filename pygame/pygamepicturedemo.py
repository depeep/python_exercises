import pygame
import random
pygame.init()

size = (1600, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jos's demo2")
screen.fill((255, 255, 255))

corgi1 = pygame.image.load("corgi1.png")
corgi2 = pygame.image.load("corgi2.png")


corgi_images = [corgi1, corgi2]

for i in range(100):
    image = random.choice(corgi_images)
    x = random.randint(0, size[0] - image.get_width())
    y = random.randint(0, size[1] - image.get_height())
    screen.blit(image, (x, y))
    pygame.display.flip()
    wait_time = random.randint(0, 500)  # wacht tussen 0.5 en 1.5 seconden
    pygame.time.delay(wait_time)  # wacht de gegenereerde tijd voordat de volgende afbeelding wordt getoond

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     

pygame.quit()

