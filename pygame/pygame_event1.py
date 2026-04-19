import pygame
pygame.init()
size = (1600, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Jos's event_demo1")

corgi = pygame.image.load("corgi1.png")
corgiX = 100
corgiY = 100

corgiMovingUp = False
corgiMovingDown = False 
corgiMovingRight = False
corgiMovingLeft = False

corgiSpeed = 5

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:    
            pygame.quit()
            exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                corgiMovingUp = True
            elif e.key == pygame.K_DOWN:
                corgiMovingDown = True
            elif e.key ==  pygame.K_RIGHT:
                corgiMovingRight = True
            elif e.key == pygame.K_LEFT:
                corgiMovingLeft = True  
        
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                corgiMovingUp = False
            elif e.key == pygame.K_DOWN:
                corgiMovingDown = False
            elif e.key ==  pygame.K_RIGHT:
                corgiMovingRight = False
            elif e.key == pygame.K_LEFT:
                corgiMovingLeft = False

    if corgiMovingUp:
        corgiY -= corgiSpeed
    if corgiMovingDown:
        corgiY += corgiSpeed
    if corgiMovingRight:
        corgiX += corgiSpeed
    if corgiMovingLeft:
        corgiX -= corgiSpeed


    screen.fill((255, 255, 255))
    screen.blit(corgi, (corgiX, corgiY))    
    pygame.display.update()



