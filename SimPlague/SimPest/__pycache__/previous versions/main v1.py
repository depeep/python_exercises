
import pygame
import random
from pathlib import Path #necessary for relative paths to assets
# from simClasses import *

#pointing to the folder where the code is located, so we can use relative paths to the assets and store them in variables for easy use.
base = Path(__file__).parent
prey1 = base / "assets" / "animated-rabbit.png" 
background = base / "assets" / "background.png"
food1 = base / "assets" / "lettuce.png"
food2 = base / "assets" / "carrot.png"
eatSound1 = base / "assets" / "eat-carrot.mp3"    

#superclass voor alle sprites
class Sprite:
    def __init__(self, image, game):
        self.image = image
        self.game = game
        self.position = [0, 0]
        self.reset()

    def reset(self):
        pass #to be done later in the subclasses, as the reset function is probably different for each sprite. 

    def update(self):
        pass

    def draw(self):
        self.game.surface.blit(self.image, self.position)
    
    #collision detection, returns True if collides with otherSprite >>naar game-engine\events verplaatsen?
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
    
    # Keeping the sprite within the screen boundaries, can be called in the update function of the subclasses. >> naar game-engine\movement verplaatsen ?
    def stayInScreen(self):
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[0] > self.game.width - self.image.get_width():
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1] > self.game.height - self.image.get_height():
            self.position[1] = self.game.height - self.image.get_height()


class Prey(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        eatSound = pygame.mixer.Sound(eatSound1)
        self.eatSound = eatSound
        self.__speed = 5 #TODO: make speed variable for each prey, so they move at different speeds.

    def reset(self):
        self.movingUp = False
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False
        x = (self.game.width - self.image.get_width()) // 2
        y = (self.game.height - self.image.get_height()) // 2
        self.position = [x, y]
        self.speed = 5 #TODO: make speed variable for each prey, so they move at different speeds.
 
    def update(self):
        if self.movingUp:
            self.position[1] -= self.speed
        if self.movingDown:
            self.position[1] += self.speed
        if self.movingRight:
            self.position[0] += self.speed
        if self.movingLeft:
            self.position[0] -= self.speed
        if self.game.food2Sprite.collidesWith(self):
            self.game.food2Sprite.reset() 
            self.playEatSound()
        
    def playEatSound(self):
            self.eatSound.play()
            
    
    # movement functions, TODO: make these functions more efficient, so we don't have to call stopMoveX() every time we want to change direction. Maybe a new function called setDirection(x, y) that takes in the direction as parameters and sets the movement accordingly. This way we can just call setDirection(-1, 0) to move left, setDirection(1, 0) to move right, setDirection(0, -1) to move up and setDirection(0, 1) to move down. This way we don't have to call stopMoveX() every time we want to change direction, which can be messy and inefficient.
    # def setDirection(self, x, y):
    #     self.movingUp = (y == -1)
    #     self.movingDown = (y == 1)
    #     self.movingRight = (x == 1)
    #     self.movingLeft = (x == -1)

    def startMoveUp(self): self.movingUp = True
    def stopMoveUp(self): self.movingUp = False

    def startMoveDown(self): self.movingDown = True
    def stopMoveDown(self): self.movingDown = False

    def startMoveRight(self): self.movingRight = True
    def stopMoveRight(self): self.movingRight = False

    def startMoveLeft(self): self.movingLeft = True
    def stopMoveLeft(self): self.movingLeft = False

    # #random movement of prey (replaces manual movement) and change direction when hitting the edge of the screen, can be called in the update function.
    # TODO: Find a way tot stop the loitering round the edges
    # TODO: make random movement more intelligent, so they don't just move randomly, but also try to move towards the food. Maybe a new function called moveTowardsFood() that is called when the prey is not moving randomly, but is moving towards the food. This function can be called in the update function, and can check the position of the food and move towards it. This way the prey will be more likely to find the food, instead of just moving randomly and hoping to find it.
    # TODO:  move to superclass and make it work for all sprites, not just prey. 
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

class Food2(Sprite):
    def reset(self):
        self.position[0] = random.randint(0, self.game.width - self.image.get_width())
        self.position[1] = random.randint(0, self.game.height - self.image.get_height())
   
class Food1(Sprite):
    def reset(self):
        self.position[0] = random.randint(0, self.game.width - self.image.get_width())
        self.position[1] = random.randint(0, self.game.height - self.image.get_height())

class SurvivalSim:
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
        self.preyImage = pygame.image.load(prey1).convert_alpha()
        self.food2Image = pygame.image.load(food2).convert_alpha()
        self.food1Image = pygame.image.load(food1).convert_alpha()

        # sprites aanmaken
        self.backgroundSprite = Sprite(backgroundImage, self)
        preyPopulation = []  # experimental list om meerdere prey's in te maken
        for i in range(3):
             preyPopulation.append(Prey(self.preyImage, self))
        self.food2Sprite = Food2(self.food2Image, self)
        self.food1Sprite = Food1(self.food1Image, self)

        # experimental nog meer sprites maken 
        food1Population = []
        for i in range(5):
            food1Population.append(Food1(self.food1Image, self))    

        # experimental new code to check collision with multiple treats in food1Population, can be called in the main game loop. If it works, move it to a separate function and call it in the update function of the prey, so it checks for collision with the treats every frame. This way we don't have to check for collision with the treats in the main game loop, which can be messy and inefficient.
        def checkCollisionWithFood1(self):
            for food in food1Population:
                for prey in preyPopulation:
                    if food.collidesWith(prey):
                        print("Collided with food in the food1!")
                        food.reset()
                        prey.playEatSound()
                        

        for prey in preyPopulation:
             prey.randomMovement()  # call random movement at the start of the game, can be called later to change direction randomly during the game
        
        # self.preySprite.randomMovement()  # call random movement at the start of the game, can be called later to change direction randomly during the game

        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)
            # self.preySprite.stayInScreen()  
            for prey in preyPopulation:
                 prey.changeDirection()   
            # self.preySprite.changeDirection()
            checkCollisionWithFood1(self)  # experimental code om collision te checken. Als het werkt ergens anders neerzetten

            # input events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            running = False
                                            
            # draw/update
            self.backgroundSprite.draw()

            for prey in preyPopulation:
                 prey.update() 
                 prey.draw()

            self.food2Sprite.draw() #TODO: update en draw in een loop zetten voor meerdere treats, maar eerst checken of de collision met meerdere treats werkt.
            for food in food1Population:
                food.draw()    
            
            pygame.display.flip()

        pygame.quit()


    

game = SurvivalSim()
game.playGame()