import pygame
import random

class Sprite:
    def __init__(self, image, game):
        self.image = image
        self.game = game
        self.position = [0, 0]
        self.reset()

    def reset(self):
        pass

    def update(self):
        pass

    def draw(self):
        self.game.surface.blit(self.image, self.position)
    
    def collidesWith(self, otherSprite):
        maxX = self.position[0] + self.image.get_width()
        maxY = self.position[1] + self.image.get_height()
        otherMaxX = otherSprite.position[0] + otherSprite.image.get_width()
        otherMaxY = otherSprite.position[1] + otherSprite.image.get_height()

        if self.position[0] > otherMaxX:
            return False
        if self.position[1] > otherMaxY:
            return False
        if otherSprite.position[0] > maxX:
            return False
        if otherSprite.position[1] > maxY:
            return False

        return True


class Corgi(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        barkSound = pygame.mixer.Sound("bark.wav")
        self.barkSound = barkSound

    def reset(self):
        self.movingUp = False
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False

        x = (self.game.width - self.image.get_width()) // 2
        y = (self.game.height - self.image.get_height()) // 2
        self.position = [x, y]

        self.speed = 5

    def update(self):
        if self.movingUp:
            self.position[1] -= self.speed
        if self.movingDown:
            self.position[1] += self.speed
        if self.movingRight:
            self.position[0] += self.speed
        if self.movingLeft:
            self.position[0] -= self.speed
        if self.game.singleTreatSprite.collidesWith(self):
            self.game.singleTreatSprite.reset() 
            self.barkPlay()
            
    def barkPlay(self):
            
        self.barkSound.play()


        # binnen scherm houden
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[0] > self.game.width - self.image.get_width():
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1] > self.game.height - self.image.get_height():
            self.position[1] = self.game.height - self.image.get_height()

    def startMoveUp(self): self.movingUp = True
    def stopMoveUp(self): self.movingUp = False

    def startMoveDown(self): self.movingDown = True
    def stopMoveDown(self): self.movingDown = False

    def startMoveRight(self): self.movingRight = True
    def stopMoveRight(self): self.movingRight = False

    def startMoveLeft(self): self.movingLeft = True
    def stopMoveLeft(self): self.movingLeft = False

class SingleTreat(Sprite):
    def reset(self):
        self.position[0] = random.randint(0, self.game.width - self.image.get_width())
        self.position[1] = random.randint(0, self.game.height - self.image.get_height())


class TreatHunt:
    def playGame(self):
        initResult = pygame.init()
        if initResult[1] != 0:
            print("pygame not installed properly")
            return

        self.width, self.height = 1600, 1000
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Corgi's cookie chasing adventure")

        # assets 1x laden
        backgroundImage = pygame.image.load("background.png").convert()
        self.corgiImage = pygame.image.load("corgi1.png").convert_alpha()
        self.singleTreatImage = pygame.image.load("singletreatsmall.png").convert_alpha()

        # sprites maken
        self.backgroundSprite = Sprite(backgroundImage, self)
        self.corgiSprite = Corgi(self.corgiImage, self)
        self.singleTreatSprite = SingleTreat(self.singleTreatImage, self)

        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                    elif e.key == pygame.K_UP:
                        self.corgiSprite.startMoveUp()
                    elif e.key == pygame.K_DOWN:
                        self.corgiSprite.startMoveDown()
                    elif e.key == pygame.K_RIGHT:
                        self.corgiSprite.startMoveRight()
                    elif e.key == pygame.K_LEFT:
                        self.corgiSprite.startMoveLeft()

                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_UP:
                        self.corgiSprite.stopMoveUp()
                    elif e.key == pygame.K_DOWN:
                        self.corgiSprite.stopMoveDown()
                    elif e.key == pygame.K_RIGHT:
                        self.corgiSprite.stopMoveRight()
                    elif e.key == pygame.K_LEFT:
                        self.corgiSprite.stopMoveLeft()

            # draw/update
            self.backgroundSprite.draw()
            self.corgiSprite.update()
            self.corgiSprite.draw()

            self.singleTreatSprite.draw()

            pygame.display.flip()

        pygame.quit()



game = TreatHunt()
game.playGame()