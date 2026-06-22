import pygame
import random
import math

# =========================
# PYGAME INSTELLINGEN
# =========================
pygame.init()

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Habitat Simulation")

CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (245, 245, 245)
GREEN = (0, 180, 0)
BLUE = (50, 100, 255)
RED = (220, 50, 50)
BLACK = (20, 20, 20)

# =========================
# HELPER FUNCTIES
# =========================
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def distance_xy(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def random_move(x, y, speed):
    dx = random.uniform(-5, 5)
    dy = random.uniform(-5, 5)

    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return x, y

    dx /= length
    dy /= length

    x += dx * speed
    y += dy * speed

    x = clamp(x, 0, WIDTH)
    y = clamp(y, 0, HEIGHT)

    return x, y

# placeholders zoals jij ze gebruikte
def f_x(x, y, speed=1):
    new_x, _ = random_move(x, y, speed)
    return new_x

def f_y(x, y, speed=1):
    _, new_y = random_move(x, y, speed)
    return new_y


# =========================
# IMAGE CLASS
# =========================
class Image:
    def __init__(self, sprite, size):
        self.__sprite = sprite
        self.__size = size

    def get_sprite(self):
        return self.__sprite

    def get_size(self):
        return self.__size


# =========================
# FOOD
# =========================
class Food:
    def __init__(self, x, y, image, stamina, growth_speed):
        self.__x = x
        self.__y = y
        self.__image = Image(image.get_sprite(), image.get_size())
        self.__stamina = stamina
        self.__growth_speed = growth_speed
        self.__alive = True

    def time_step(self):
        # Food beweegt niet; kan eventueel aangroeien
        self.feeding()

    def feeding(self):
        self.__stamina += self.__growth_speed

    def is_alive(self):
        return self.__alive and self.__stamina > 0

    def consume(self):
        self.__alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.__x), int(self.__y)), 6)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_stamina(self):
        return self.__stamina


# =========================
# PREY
# =========================
class Prey:
    def __init__(self, x, y, image, stamina, speed, age, max_age):
        self.__stamina = stamina
        self.__x = x
        self.__y = y
        self.__image = Image(image.get_sprite(), image.get_size())
        self.__speed = speed
        self.__age = age
        self.__max_age = max_age
        self.__alive = True

    def time_step(self):
        self.move()
        self.__stamina -= self.__speed * 0.1
        self.__age += 1

        if self.__stamina <= 0 or self.__age >= self.__max_age:
            self.__alive = False

    def move(self):
        self.__x, self.__y = random_move(self.__x, self.__y, self.__speed)

    def feed(self, amount):
        self.__stamina += amount

    def can_eat(self, food):
        return distance_xy(self.__x, self.__y, food.get_x(), food.get_y()) < 15

    def eat(self, food):
        self.feed(food.get_stamina())
        food.consume()

    def is_alive(self):
        return self.__alive

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.__x), int(self.__y)), 10)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_stamina(self):
        return self.__stamina


# =========================
# PREDATOR
# =========================
class Predator:
    def __init__(self, x, y, image, stamina, speed, age, max_age):
        self.__stamina = stamina
        self.__x = x
        self.__y = y
        self.__image = Image(image.get_sprite(), image.get_size())
        self.__age = age
        self.__max_age = max_age
        self.__speed = speed
        self.__alive = True

    def time_step(self):
        self.move()
        self.__stamina -= self.__speed * 0.15
        self.__age += 1

        if self.__stamina <= 0 or self.__age >= self.__max_age:
            self.__alive = False

    def move(self):
        self.__x, self.__y = random_move(self.__x, self.__y, self.__speed)

    def feed(self, amount):
        self.__stamina += amount

    def can_eat(self, prey):
        return distance_xy(self.__x, self.__y, prey.get_x(), prey.get_y()) < 18

    def eat(self, prey):
        self.feed(prey.get_stamina())
        prey.die()

    def is_alive(self):
        return self.__alive

    def die(self):
        self.__alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.__x), int(self.__y)), 13)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_stamina(self):
        return self.__stamina


# extra methode voor prey na class-definitie nodig? liever hier direct:
def prey_die(self):
    self._Prey__alive = False

Prey.die = prey_die


# =========================
# HABITAT
# =========================
class Habitat:
    def __init__(self, preys, predators, foods):
        self.__preys = preys
        self.__predators = predators
        self.__foods = foods

    def time_step(self):
        self.time_steps()
        self.feeding()
        self.dying()

        # Optioneel: af en toe nieuw voedsel laten verschijnen
        if random.random() < 0.03:
            self.__foods.append(
                Food(
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT),
                    Image("food", (10, 10)),
                    stamina=3,
                    growth_speed=0
                )
            )

    def time_steps(self):
        for food in self.__foods:
            food.time_step()

        for prey in self.__preys:
            prey.time_step()

        for predator in self.__predators:
            predator.time_step()

    def dying(self):
        self.__foods = [food for food in self.__foods if food.is_alive()]
        self.__preys = [prey for prey in self.__preys if prey.is_alive()]
        self.__predators = [predator for predator in self.__predators if predator.is_alive()]

    def feeding(self):
        # Prey eet food
        for prey in self.__preys:
            for food in self.__foods:
                if prey.can_eat(food):
                    prey.eat(food)
                    break

        # Predator eet prey
        for predator in self.__predators:
            for prey in self.__preys:
                if predator.can_eat(prey):
                    predator.eat(prey)
                    break

    def draw(self, screen):
        for food in self.__foods:
            food.draw(screen)

        for prey in self.__preys:
            prey.draw(screen)

        for predator in self.__predators:
            predator.draw(screen)

    def get_counts(self):
        return len(self.__foods), len(self.__preys), len(self.__predators)


# =========================
# TEST / MAIN
# =========================
def create_random_food(n):
    foods = []
    for _ in range(n):
        foods.append(
            Food(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                Image("food", (10, 10)),
                stamina=10,
                growth_speed=1
            )
        )
    return foods

def create_random_preys(n):
    preys = []
    for _ in range(n):
        preys.append(
            Prey(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                Image("prey", (20, 20)),
                stamina=100,
                speed=5,
                age=0,
                max_age=6000
            )
        )
    return preys

def create_random_predators(n):
    predators = []
    for _ in range(n):
        predators.append(
            Predator(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                Image("predator", (20, 20)),
                stamina=120,
                speed=10,
                age=0,
                max_age=6000
            )
        )
    return predators


def draw_text(screen, text, x, y, color=BLACK, size=24):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


if __name__ == "__main__":
    foods = create_random_food(200)
    preys = create_random_preys(12)
    predators = create_random_predators(4)

    habitat = Habitat(preys, predators, foods)

    running = True
    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # update simulatie
        habitat.time_step()

        # tekenen
        SCREEN.fill(WHITE)
        habitat.draw(SCREEN)

        food_count, prey_count, predator_count = habitat.get_counts()
        draw_text(SCREEN, f"Food: {food_count}", 10, 10)
        draw_text(SCREEN, f"Prey: {prey_count}", 10, 40)
        draw_text(SCREEN, f"Predators: {predator_count}", 10, 70)

        pygame.display.flip()

    pygame.quit()
