''' Dit is de licht aangepaste code van de corgi game, met als doel om te experimenteren met meerdere prey's en treats. 
    De code is nog niet helemaal af, maar het is een begin. De code is ook nog niet geoptimaliseerd, dus er zijn waarschijnlijk veel verbeteringen mogelijk.
    Deze code ga ik samenvoegen met de code van de classes  zodat  de simulatie er ook nog enigszins aantrekkelijk uitziet. De code is ook nog niet helemaal af, maar het is een begin. De code is ook nog niet geoptimaliseerd, dus er zijn waarschijnlijk veel verbeteringen mogelijk.'''
import pygame
import random
from pathlib import Path #nodig voor relatieve verwijzingen naar assets

#weg wijzen naar assets
base = Path(__file__).parent        # map waar main.py staat

#assets in variables zetten zodat ze makkelijk te gebruiken zijn in de code
corgi1 = base / "assets" / "corgi1.png"  # volledig pad naar afbeelding 
background = base / "assets" / "background.png"
multiTreat = base / "assets" / "multitreatsmall.png"
singleTreat = base / "assets" / "singletreatsmall.png"
barkSoundFile = base / "assets" / "bark.wav"    

# from simClasses import *

#superclass voor alle sprites
class Sprite:
    def __init__(self, image, game):
        self.image = image
        self.game = game
        self.position = [0, 0]
        self.reset()

    def reset(self):
        pass #doen we later, want niet alle sprites hebben een reset nodig. De reset functie wordt overschreven in de subclasses.

    def update(self):
        pass

    def draw(self):
        self.game.surface.blit(self.image, self.position)
    
    #collision detection, returns True if collides with otherSprite
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
    
    # binnen scherm houden
    def stayInScreen(self):
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[0] > self.game.width - self.image.get_width():
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1] > self.game.height - self.image.get_height():
            self.position[1] = self.game.height - self.image.get_height()


class Corgi(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        barkSound = pygame.mixer.Sound(barkSoundFile)
        self.barkSound = barkSound

    def reset(self):
        self.movingUp = False
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False

        x = (self.game.width - self.image.get_width()) // 2
        y = (self.game.height - self.image.get_height()) // 2
        self.position = [x, y]

        self.speed = 5 #variabele van maken?
 
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

    def startMoveUp(self): self.movingUp = True
    def stopMoveUp(self): self.movingUp = False

    def startMoveDown(self): self.movingDown = True
    def stopMoveDown(self): self.movingDown = False

    def startMoveRight(self): self.movingRight = True
    def stopMoveRight(self): self.movingRight = False

    def startMoveLeft(self): self.movingLeft = True
    def stopMoveLeft(self): self.movingLeft = False

    # #random movement of corgi (replaces manual movement)
    def randomMovement(self):
        x = random.randint(-1,1)
        print (x)
        if x == -1: 
            self.startMoveLeft()
            self.stopMoveRight()
        elif x == 1:
            self.startMoveRight()
            self.stopMoveLeft()
        else:
            self.stopMoveLeft()
            self.stopMoveRight()    

        y = random.randint(-1,1)
        print (y)
        if y == -1: 
            self.startMoveUp()
            self.stopMoveDown() 
        elif y == 1:
            self.startMoveDown()
            self.stopMoveUp()
        else:
            self.stopMoveUp()
            self.stopMoveDown()  

    def changeDirection(self):
        if self.position[0] < 0:
            self.randomMovement()  # random movement when hitting the left edge
        if self.position[1] < 0:
            self.randomMovement()  # random movement when hitting the top edge  
        if self.position[0] > self.game.width - self.image.get_width()+10:
            self.randomMovement()  # random movement when hitting the right edge   
        if self.position[1] > self.game.height - self.image.get_height()+10:
            self.randomMovement()  # random movement when hitting the bottom edge

class SingleTreat(Sprite):
    def reset(self):
        self.position[0] = random.randint(0, self.game.width - self.image.get_width())
        self.position[1] = random.randint(0, self.game.height - self.image.get_height())
   
class MultiTreat(Sprite):
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
        backgroundImage = pygame.image.load(background).convert()
        self.corgiImage = pygame.image.load(corgi1).convert_alpha()
        self.singleTreatImage = pygame.image.load(singleTreat).convert_alpha()
        self.multiTreatImage = pygame.image.load(multiTreat).convert_alpha()

        # sprites 1x maken
        self.backgroundSprite = Sprite(backgroundImage, self)
        corgiKennel = []  # experimental list om meerdere corgi's in te maken
        for i in range(3):
             corgiKennel.append(Corgi(self.corgiImage, self))

        
        # self.corgiSprite = Corgi(self.corgiImage, self)
        self.singleTreatSprite = SingleTreat(self.singleTreatImage, self)
        self.multiTreatSprite = MultiTreat(self.multiTreatImage, self)

        # experimental nog meer sprites maken 
        kookyJar = []
        for i in range(5):
            kookyJar.append(MultiTreat(self.multiTreatImage, self))    

        # experimental new code to check collision with multiple treats in kookyJar
        def checkCollisionWithKookyJar(self):
            for treat in kookyJar:
                for corgi in corgiKennel:
                    if treat.collidesWith(corgi):
                        print("Collided with a treat in the kooky jar!")
                        treat.reset()
                        corgi.barkPlay()
                        

        for corgi in corgiKennel:
             corgi.randomMovement()  # call random movement at the start of the game, can be called later to change direction randomly during the game
        
        # self.corgiSprite.randomMovement()  # call random movement at the start of the game, can be called later to change direction randomly during the game

        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)
            # self.corgiSprite.stayInScreen()  
            for corgi in corgiKennel:
                 corgi.changeDirection()   
            # self.corgiSprite.changeDirection()
            checkCollisionWithKookyJar(self)  # experimental code om collision te checken. Als het werkt ergens anders neerzetten

            #handmatige corgi besturing en quit events, verplaatsen naar aparte functie als het werkt    
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            running = False
            '''
            # besturing        
            #       elif e.key == pygame.K_UP:
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
                        self.corgiSprite.stopMoveLeft()'''
            
            
              
            

            # draw/update
            self.backgroundSprite.draw()
            # self.corgiSprite.update()
            # self.corgiSprite.draw()
            for corgi in corgiKennel:
                 corgi.update() 
                 corgi.draw()
            self.singleTreatSprite.draw()
            # self.drawKooky()  # experimental code om meerdere koekjes te tekenen.   
            for treat in kookyJar:
                treat.draw()    
            
            pygame.display.flip()

        pygame.quit()



game = TreatHunt()
game.playGame()