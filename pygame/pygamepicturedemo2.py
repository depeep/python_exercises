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

for i in range(10):
    image = random.choice(corgi_images)
    x = random.randint(0, size[0] - image.get_width())
    y = random.randint(0, size[1] - image.get_height())
    for xx in range(x, x+100, 1):  # animatie van links naar rechts
        clock = pygame.time.Clock()  # clock object om de framerate te regelen
        clock.tick(120)  # stel de framerate in op 60 frames per seconde
        screen.fill((255, 255, 255))  # scherm leegmaken voordat de afbeelding wordt getoond, zodat er geen oude afbeeldingen blijven staan
        screen.blit(image, (xx, y))  # verschil in y-richting voor animatie
        pygame.display.flip()
        y=y+1  # verschil in y-richting voor animatie
    wait_time = random.randint(0, 500)  # wacht tussen 0.5 en 1.5 seconden
    pygame.time.delay(wait_time)  # wacht de gegenereerde tijd voordat de volgende afbeelding wordt getoond

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     

pygame.quit()

