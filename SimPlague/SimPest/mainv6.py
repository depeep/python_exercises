import pygame
import random
from pathlib import Path
import math
from collections import deque

# PATHS
base = Path(__file__).parent
prey1 = base / "assets" / "animated-rabbit.png"
pred1 = base / "assets" / "wolf.png"
background = base / "assets" / "background.png"
food1 = base / "assets" / "lettuce.png"
eatSound1 = base / "assets" / "eat-carrot.mp3"


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def distance(a, b):
    return math.dist(a, b)


def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))


# --------------------------------------------------
# BASE SPRITE CLASS
# --------------------------------------------------
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

    def placeInScreen(self):
        """
        Zorg dat sprites binnen het simulatiegebied blijven
        (dus NIET in het linkerpaneel).
        """
        sim = self.game.sim_rect
        self.position[0] = clamp(
            self.position[0],
            sim.left,
            sim.right - self.image.get_width()
        )
        self.position[1] = clamp(
            self.position[1],
            sim.top,
            sim.bottom - self.image.get_height()
        )


# --------------------------------------------------
# FOOD CLASS
# --------------------------------------------------
class Food(Sprite):
    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]


# --------------------------------------------------
# PREY CLASS (AI + ENERGY + REPRODUCTION)
# --------------------------------------------------
class Prey(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.eatSound = pygame.mixer.Sound(eatSound1)
        self.speed = 3
        self.energy = 100

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        # energieverlies
        self.energy -= 0.1
        if self.energy <= 0:
            if self in self.game.preyPopulation:
                self.game.preyPopulation.remove(self)
            return

        # AI: zoek dichtstbijzijnde voedsel
        target = self.game.getClosestFood(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position

            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.speed * dx / dist
                self.position[1] += self.speed * dy / dist

        self.placeInScreen()

    def eat(self, food):
        self.energy += 30
        self.eatSound.play()

        # voortplanting
        if self.energy > 50:
            self.energy -= 20
            self.game.spawnPrey()


# --------------------------------------------------
# PREDATOR CLASS (AI + ENERGY)
# --------------------------------------------------
class Predator(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.speed = 4
        self.energy = 200

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        # energieverlies
        self.energy -= 2
        if self.energy <= 0:
            if self in self.game.predatorPopulation:
                self.game.predatorPopulation.remove(self)
            return

        # AI: zoek dichtstbijzijnde prey
        target = self.game.getClosestPrey(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position

            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.speed * dx / dist
                self.position[1] += self.speed * dy / dist

            # eet prey
            if target in self.game.preyPopulation and self.collidesWith(target):
                self.energy += 120
                self.game.preyPopulation.remove(target)

        # voortplanting
        if self.energy > 1000:
            self.energy -= 500
            self.game.spawnPredator()

        self.placeInScreen()


# --------------------------------------------------
# MAIN GAME CLASS
# --------------------------------------------------
class SurvivalSim:
    def __init__(self):
        # Layout
        self.width = 1600
        self.height = 1000
        self.panel_width = 320

        # Wordt gezet na pygame init
        self.surface = None
        self.clock = None
        self.debugFont = None
        self.uiFont = None
        self.smallFont = None

        # Simulatiegebied (rechts van het paneel)
        self.sim_rect = pygame.Rect(self.panel_width, 0, self.width - self.panel_width, self.height)

        # UI dummy componenten
        self.buttons = []
        self.param_fields = []

        # Grafiekhistorie
        self.max_history = 220
        self.food_history = deque(maxlen=self.max_history)
        self.prey_history = deque(maxlen=self.max_history)
        self.pred_history = deque(maxlen=self.max_history)

    # -----------------------------
    # SIM HELPERS
    # -----------------------------
    def getClosestFood(self, pos):
        if not self.foodPopulation:
            return None
        return min(self.foodPopulation, key=lambda f: distance(pos, f.position))

    def getClosestPrey(self, pos):
        if not self.preyPopulation:
            return None
        return min(self.preyPopulation, key=lambda p: distance(pos, p.position))

    def spawnPrey(self):
        self.preyPopulation.append(Prey(self.preyImage, self))

    def spawnPredator(self):
        self.predatorPopulation.append(Predator(self.predImage, self))

    # -----------------------------
    # UI SETUP
    # -----------------------------
    def setup_ui(self):
        # Dummy knoppen
        self.buttons = [
            {"label": "Start / Stop", "rect": pygame.Rect(20, 20, 130, 42)},
            {"label": "Reset",        "rect": pygame.Rect(165, 20, 130, 42)},
            {"label": "Spawn Prey",   "rect": pygame.Rect(20, 72, 130, 42)},
            {"label": "Spawn Food",   "rect": pygame.Rect(165, 72, 130, 42)},
        ]

        # Dummy parametervelden
        self.param_fields = [
            {"label": "Prey speed",      "value": "3.0",   "rect": pygame.Rect(20, 150, 275, 36)},
            {"label": "Predator speed",  "value": "4.0",   "rect": pygame.Rect(20, 205, 275, 36)},
            {"label": "Food amount",     "value": "12",    "rect": pygame.Rect(20, 260, 275, 36)},
            {"label": "Spawn chance",    "value": "0.10",  "rect": pygame.Rect(20, 315, 275, 36)},
            {"label": "Energy loss",     "value": "dummy", "rect": pygame.Rect(20, 370, 275, 36)},
        ]

    # -----------------------------
    # SIMULATION STEP
    # -----------------------------
    def timestep(self):
        for prey in list(self.preyPopulation):
            prey.update()

        for pred in list(self.predatorPopulation):
            pred.update()

        # prey eet food
        for food in list(self.foodPopulation):
            for prey in list(self.preyPopulation):
                if prey.collidesWith(food):
                    prey.eat(food)
                    food.reset()
                    break  # dit food-item is al "gegeten"

        # update historische grafiekdata
        self.food_history.append(len(self.foodPopulation))
        self.prey_history.append(len(self.preyPopulation))
        self.pred_history.append(len(self.predatorPopulation))

    # -----------------------------
    # DRAW UI PANEL
    # -----------------------------
    def drawPanel(self):
        panel_rect = pygame.Rect(0, 0, self.panel_width, self.height)

        # Achtergrond paneel
        pygame.draw.rect(self.surface, (30, 34, 40), panel_rect)
        pygame.draw.line(self.surface, (70, 74, 82), (self.panel_width, 0), (self.panel_width, self.height), 2)

        # Titel
        title = self.uiFont.render("Control Panel", True, (240, 240, 240))
        self.surface.blit(title, (20, 120))

        # Dummy knoppen
        for btn in self.buttons:
            pygame.draw.rect(self.surface, (70, 90, 120), btn["rect"], border_radius=8)
            pygame.draw.rect(self.surface, (110, 130, 170), btn["rect"], 2, border_radius=8)
            txt = self.smallFont.render(btn["label"], True, (255, 255, 255))
            txt_rect = txt.get_rect(center=btn["rect"].center)
            self.surface.blit(txt, txt_rect)

        # Sectietitel parameters
        param_title = self.uiFont.render("Parameters", True, (240, 240, 240))
        self.surface.blit(param_title, (20, 435))

        # Dummy parametervelden
        for field in self.param_fields:
            label = self.smallFont.render(field["label"], True, (220, 220, 220))
            self.surface.blit(label, (field["rect"].x, field["rect"].y - 22))

            pygame.draw.rect(self.surface, (245, 245, 245), field["rect"], border_radius=6)
            pygame.draw.rect(self.surface, (180, 180, 180), field["rect"], 1, border_radius=6)

            value = self.smallFont.render(field["value"], True, (50, 50, 50))
            self.surface.blit(value, (field["rect"].x + 10, field["rect"].y + 8))

        # Grafiek
        self.drawPopulationGraph(20, 560, 280, 390)

    # -----------------------------
    # DRAW GRAPH
    # -----------------------------
    def drawPopulationGraph(self, x, y, w, h):
        graph_rect = pygame.Rect(x, y, w, h)

        # Achtergrond
        pygame.draw.rect(self.surface, (20, 24, 30), graph_rect, border_radius=8)
        pygame.draw.rect(self.surface, (100, 100, 100), graph_rect, 1, border_radius=8)

        # Titel
        title = self.uiFont.render("Population Graph", True, (240, 240, 240))
        self.surface.blit(title, (x, y - 30))

        # Binnenmarges
        pad = 12
        gx = x + pad
        gy = y + pad
        gw = w - 2 * pad
        gh = h - 2 * pad - 30  # ruimte voor legend onderin

        # Assen / raster
        for i in range(5):
            yy = gy + int(i * gh / 4)
            pygame.draw.line(self.surface, (50, 55, 65), (gx, yy), (gx + gw, yy), 1)

        # Max waarde voor schaling
        values = list(self.food_history) + list(self.prey_history) + list(self.pred_history)
        max_val = max(values) if values else 10
        max_val = max(max_val, 10)

        def make_points(history):
            data = list(history)
            if len(data) < 2:
                return []

            points = []
            for i, val in enumerate(data):
                px = gx + int(i * (gw / max(1, self.max_history - 1)))
                py = gy + gh - int((val / max_val) * gh)
                points.append((px, py))
            return points

        # Lijnen tekenen
        food_points = make_points(self.food_history)
        prey_points = make_points(self.prey_history)
        pred_points = make_points(self.pred_history)

        if len(food_points) >= 2:
            pygame.draw.lines(self.surface, (80, 220, 120), False, food_points, 2)
        if len(prey_points) >= 2:
            pygame.draw.lines(self.surface, (90, 180, 255), False, prey_points, 2)
        if len(pred_points) >= 2:
            pygame.draw.lines(self.surface, (255, 90, 90), False, pred_points, 2)

        # Y-labels
        for i in range(5):
            val = int(max_val - i * (max_val / 4))
            yy = gy + int(i * gh / 4)
            label = self.smallFont.render(str(val), True, (180, 180, 180))
            self.surface.blit(label, (gx + 4, yy - 10))

        # Legenda
        legend_y = y + h - 22

        pygame.draw.line(self.surface, (80, 220, 120), (x + 10, legend_y + 8), (x + 30, legend_y + 8), 3)
        self.surface.blit(self.smallFont.render("Food", True, (220, 220, 220)), (x + 36, legend_y))

        pygame.draw.line(self.surface, (90, 180, 255), (x + 90, legend_y + 8), (x + 110, legend_y + 8), 3)
        self.surface.blit(self.smallFont.render("Prey", True, (220, 220, 220)), (x + 116, legend_y))

        pygame.draw.line(self.surface, (255, 90, 90), (x + 170, legend_y + 8), (x + 190, legend_y + 8), 3)
        self.surface.blit(self.smallFont.render("Pred", True, (220, 220, 220)), (x + 196, legend_y))

    # -----------------------------
    # DRAW MAIN
    # -----------------------------
    def draw(self):
        # Vul achtergrond volledig
        self.surface.fill((0, 0, 0))

        # Achtergrond simulatiegebied
        self.surface.blit(self.backgroundImage, self.sim_rect.topleft)

        # Sprites
        for prey in self.preyPopulation:
            prey.draw()

        for pred in self.predatorPopulation:
            pred.draw()

        for food in self.foodPopulation:
            food.draw()

        # Linkerpaneel
        self.drawPanel()

        # Debug overlay rechtsboven in simulatiegebied
        fps = int(self.clock.get_fps())
        debug_text = (
            f"FPS: {fps} | Prey: {len(self.preyPopulation)} | "
            f"Predators: {len(self.predatorPopulation)} | Food: {len(self.foodPopulation)}"
        )
        text = self.debugFont.render(debug_text, True, (255, 255, 255))
        self.surface.blit(text, (self.panel_width + 10, 10))

        pygame.display.flip()

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def playGame(self):
        pygame.init()
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ecosystem Simulation")

        self.clock = pygame.time.Clock()
        self.debugFont = pygame.font.SysFont("consolas", 22)
        self.uiFont = pygame.font.SysFont("arial", 24, bold=True)
        self.smallFont = pygame.font.SysFont("arial", 18)

        self.setup_ui()

        # Load assets
        raw_background = pygame.image.load(background).convert()
        self.preyImage = pygame.image.load(prey1).convert_alpha()
        self.predImage = pygame.image.load(pred1).convert_alpha()
        self.foodImage = pygame.image.load(food1).convert_alpha()

        # Schaal background naar simulatiegebied
        self.backgroundImage = pygame.transform.scale(
            raw_background, (self.sim_rect.width, self.sim_rect.height)
        )

        # Create sprites
        self.preyPopulation = [Prey(self.preyImage, self) for _ in range(6)]
        self.predatorPopulation = [Predator(self.predImage, self) for _ in range(2)]
        self.foodPopulation = [Food(self.foodImage, self) for _ in range(12)]

        # Startgeschiedenis initialiseren
        for _ in range(10):
            self.food_history.append(len(self.foodPopulation))
            self.prey_history.append(len(self.preyPopulation))
            self.pred_history.append(len(self.predatorPopulation))

        running = True
        while running:
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                # Dummy interactie voor knoppen
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mx, my):
                            print(f"Dummy knop aangeklikt: {btn['label']}")

            self.timestep()
            self.draw()

        pygame.quit()


game = SurvivalSim()
game.playGame()