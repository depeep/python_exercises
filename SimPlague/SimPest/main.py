from email.mime import image

import pygame
import random
from simClasses import Prey, Predator, Food, Habitat, Image


pygame.init()

size = (1600, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jos's demo2")
screen.fill((255, 255, 255))

preyimage = Image("assets.prey.bmp", (20, 20))
foodimage = Image("assets.food.bmp", (10, 10))
predatorimage = Image("assets.predator.bmp", (20, 20))

food1 = Food(0, 0, foodimage, 5, 1)
prey1 = Prey(10, 10, preyimage, 10, 2, 0, 100)
predator1 = Predator(20, 20, predatorimage, 20, 20, 0, 150)



for i in range(10):
    # image = random.choice([food1, prey1, predator1]).Image
    image = "assets.predator.bmp"
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

