import csv
import pygame
import random
from pathlib import Path
import math
from collections import deque


# ==================================================
# PATHS
# ==================================================
base = Path(__file__).parent
prey1 = base / "assets" / "animated-rabbit.png"
prey2 = base / "assets" / "goat.png"
pred1 = base / "assets" / "wolf.png"
background = base / "assets" / "background.png"
food1 = base / "assets" / "lettuce.png"
eatSound1 = base / "assets" / "eat-carrot.mp3"
export_dir = base / "exportdata"
exportbestand = export_dir / "simulation_data.csv"


# ==================================================
# HELPERS
# ==================================================
def distance(a, b):
    return math.dist(a, b)


def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))


class DummySound:
    def play(self):
        pass


def load_sound_safe(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return DummySound()


# ==================================================
# BASE SPRITE CLASS
# ==================================================
class Sprite:
    def __init__(self, image, game):
        self.image = image
        self.game = game
        self.position = [0.0, 0.0]
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
        """Zorg dat sprites binnen het simulatiegebied blijven."""
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


# ==================================================
# FOOD
# ==================================================
class Food(Sprite):
    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]
        self.age = 0

    def update(self):
        self.age += 1

        if self.age > self.game.food_max_age:
            if self in self.game.foodPopulation:
                self.game.foodPopulation.remove(self)
            return

        # Food kan optioneel bewegen. Bij speed 0 blijft food stilstaan.
        if self.game.food_speed > 0:
            self.position[0] += random.uniform(-self.game.food_speed, self.game.food_speed)
            self.position[1] += random.uniform(-self.game.food_speed, self.game.food_speed)
            self.placeInScreen()


# ==================================================
# PREY 1
# ==================================================
class Prey(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.eatSound = load_sound_safe(eatSound1)
        self.speed = self.game.prey_speed
        self.energy = 100
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.prey_max_age:
            if self in self.game.preyPopulation:
                self.game.preyPopulation.remove(self)
            return

        self.energy -= self.game.prey_energy_loss
        if self.energy <= 0:
            if self in self.game.preyPopulation:
                self.game.preyPopulation.remove(self)
            return

        target = self.game.getClosestFood(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position

            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.prey_speed * dx / dist
                self.position[1] += self.game.prey_speed * dy / dist

        self.placeInScreen()

    def eat(self, food):
        self.energy += self.game.prey_energy_gain
        self.eatSound.play()

        if self.energy > self.game.prey_reproduction_energy:
            self.energy -= self.game.prey_reproduction_cost
            self.game.spawnPrey()


# ==================================================
# PREY 2
# ==================================================
class Prey2(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.eatSound = load_sound_safe(eatSound1)
        self.speed = self.game.prey2_speed
        self.energy = 80
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.prey2_max_age:
            if self in self.game.prey2Population:
                self.game.prey2Population.remove(self)
            return

        self.energy -= self.game.prey2_energy_loss
        if self.energy <= 0:
            if self in self.game.prey2Population:
                self.game.prey2Population.remove(self)
            return

        target = self.game.getClosestFood(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position

            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.prey2_speed * dx / dist
                self.position[1] += self.game.prey2_speed * dy / dist

        self.placeInScreen()

    def eat(self, food):
        self.energy += self.game.prey2_energy_gain
        self.eatSound.play()

        if self.energy > self.game.prey2_reproduction_energy:
            self.energy -= self.game.prey2_reproduction_cost
            self.game.spawnPrey2()


# ==================================================
# PREDATOR
# ==================================================
class Predator(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.speed = self.game.predator_speed
        self.energy = 200
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.predator_max_age:
            if self in self.game.predatorPopulation:
                self.game.predatorPopulation.remove(self)
            return

        self.energy -= self.game.predator_energy_loss
        if self.energy <= 0:
            if self in self.game.predatorPopulation:
                self.game.predatorPopulation.remove(self)
            return

        target = self.game.getClosestAnyPrey(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position

            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.predator_speed * dx / dist
                self.position[1] += self.game.predator_speed * dy / dist

            if self.collidesWith(target):
                self.energy += self.game.predator_energy_gain

                if target in self.game.preyPopulation:
                    self.game.preyPopulation.remove(target)
                elif target in self.game.prey2Population:
                    self.game.prey2Population.remove(target)

        if self.energy > self.game.predator_reproduction_energy:
            self.energy -= self.game.predator_reproduction_cost
            self.game.spawnPredator()

        self.placeInScreen()


# ==================================================
# MAIN GAME CLASS
# ==================================================
class SurvivalSim:
    def __init__(self):
        # layout
        self.width = 1600
        self.height = 1100
        self.panel_width = 360
        self.graph_height = 240

        # pygame refs
        self.surface = None
        self.clock = None
        self.debugFont = None
        self.uiFont = None
        self.smallFont = None
        self.tinyFont = None

        # simulatie en grafiek
        self.sim_rect = pygame.Rect(
            self.panel_width,
            0,
            self.width - self.panel_width,
            self.height - self.graph_height
        )
        self.graph_rect = pygame.Rect(
            self.panel_width,
            self.height - self.graph_height,
            self.width - self.panel_width,
            self.graph_height
        )

        # UI
        self.buttons = []
        self.param_fields = []
        self.active_field = None
        self.input_text = ""
        self.paused = True
        self.simulation_started = False

        # --------------------------------------------------
        # STARTWAARDEN, VOORAF TE TUNEN IN LINKER PANEEL
        # --------------------------------------------------
        self.start_food = 12
        self.start_prey = 6
        self.start_prey2 = 4
        self.start_predators = 2

        # Food parameters
        self.food_speed = 0.0
        self.food_max_age = 2000
        self.food_spawn_chance = 0.002
        self.max_food = 50

        # Prey parameters
        self.prey_speed = 3.0
        self.prey_max_age = 1600
        self.prey_reproduction_energy = 60
        self.prey_energy_gain = 30
        self.prey_energy_loss = 0.10
        self.prey_reproduction_cost = 45

        # Prey2 parameters
        self.prey2_speed = 6.0
        self.prey2_max_age = 1200
        self.prey2_reproduction_energy = 65
        self.prey2_energy_gain = 20
        self.prey2_energy_loss = 0.15
        self.prey2_reproduction_cost = 40

        # Predator parameters
        self.predator_speed = 3.0
        self.predator_max_age = 700
        self.predator_reproduction_energy = 1000
        self.predator_energy_gain = 120
        self.predator_energy_loss = 2.0
        self.predator_reproduction_cost = 800

        # grafiekhistorie
        self.max_history = 340
        self.food_history = deque(maxlen=self.max_history)
        self.prey_history = deque(maxlen=self.max_history)
        self.prey2_history = deque(maxlen=self.max_history)
        self.pred_history = deque(maxlen=self.max_history)

        # populaties
        self.preyPopulation = []
        self.prey2Population = []
        self.predatorPopulation = []
        self.foodPopulation = []

        # csv
        self.csv_file = None
        self.csv_writer = None
        self.timestep_counter = 0

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def getClosestFood(self, pos):
        if not self.foodPopulation:
            return None
        return min(self.foodPopulation, key=lambda f: distance(pos, f.position))

    def getClosestPrey(self, pos):
        if not self.preyPopulation:
            return None
        return min(self.preyPopulation, key=lambda p: distance(pos, p.position))

    def getClosestAnyPrey(self, pos):
        all_prey = self.preyPopulation + self.prey2Population
        if not all_prey:
            return None
        return min(all_prey, key=lambda p: distance(pos, p.position))

    def spawnPrey(self):
        self.preyPopulation.append(Prey(self.preyImage, self))

    def spawnPrey2(self):
        self.prey2Population.append(Prey2(self.prey2Image, self))

    def spawnPredator(self):
        self.predatorPopulation.append(Predator(self.predImage, self))

    def spawnFood(self):
        if len(self.foodPopulation) < self.max_food:
            self.foodPopulation.append(Food(self.foodImage, self))

    def reproduceFood(self):
        """
        Food kan zichzelf voortplanten met een kleine kans per frame.
        Nieuwe food spawn dicht bij bestaand food.
        """
        if len(self.foodPopulation) >= self.max_food:
            return

        new_food = []
        for food in self.foodPopulation:
            if len(self.foodPopulation) + len(new_food) >= self.max_food:
                break

            if random.random() < self.food_spawn_chance:
                f = Food(self.foodImage, self)
                offset = 50

                f.position = [
                    clamp(
                        food.position[0] + random.randint(-offset, offset),
                        self.sim_rect.left,
                        self.sim_rect.right - f.image.get_width()
                    ),
                    clamp(
                        food.position[1] + random.randint(-offset, offset),
                        self.sim_rect.top,
                        self.sim_rect.bottom - f.image.get_height()
                    )
                ]
                new_food.append(f)

        self.foodPopulation.extend(new_food)

    def resetSimulation(self):
        self.preyPopulation = [Prey(self.preyImage, self) for _ in range(int(self.start_prey))]
        self.prey2Population = [Prey2(self.prey2Image, self) for _ in range(int(self.start_prey2))]
        self.predatorPopulation = [Predator(self.predImage, self) for _ in range(int(self.start_predators))]
        self.foodPopulation = [Food(self.foodImage, self) for _ in range(int(self.start_food))]

        self.food_history.clear()
        self.prey_history.clear()
        self.prey2_history.clear()
        self.pred_history.clear()

        for _ in range(30):
            self.food_history.append(len(self.foodPopulation))
            self.prey_history.append(len(self.preyPopulation))
            self.prey2_history.append(len(self.prey2Population))
            self.pred_history.append(len(self.predatorPopulation))

        self.timestep_counter = 0

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def setup_ui(self):
        self.buttons = [
            {"label": "Start",       "rect": pygame.Rect(20, 20, 150, 42),  "action": "start",      "color": (60, 140, 80)},
            {"label": "Stop",        "rect": pygame.Rect(190, 20, 150, 42), "action": "stop",       "color": (160, 70, 70)},
            {"label": "Reset",       "rect": pygame.Rect(20, 72, 150, 42),  "action": "reset",      "color": (70, 90, 120)},
            {"label": "Spawn Prey",  "rect": pygame.Rect(190, 72, 150, 42), "action": "spawn_prey", "color": (70, 90, 120)},
            {"label": "Spawn Prey2", "rect": pygame.Rect(20, 124, 150, 42), "action": "spawn_prey2","color": (70, 90, 120)},
            {"label": "Spawn Food",  "rect": pygame.Rect(190, 124, 150, 42),"action": "spawn_food", "color": (70, 90, 120)},
            {"label": "Spawn Pred",  "rect": pygame.Rect(20, 176, 150, 42), "action": "spawn_pred", "color": (70, 90, 120)},
        ]
        self.update_param_fields()

    def update_param_fields(self):
        start_y = 285
        row_h = 36
        box_w = 120
        box_h = 24
        label_x = 20
        box_x = 215

        fields = [
            ("Start food", "start_food", "int"),
            ("Start prey", "start_prey", "int"),
            ("Start prey2", "start_prey2", "int"),
            ("Start predators", "start_predators", "int"),

            ("Food speed", "food_speed", "float"),
            ("Food max age", "food_max_age", "int"),
            ("Food spawn chance", "food_spawn_chance", "float"),
            ("Max food", "max_food", "int"),

            ("Prey speed", "prey_speed", "float"),
            ("Prey max age", "prey_max_age", "int"),
            ("Prey reproduce energy", "prey_reproduction_energy", "float"),

            ("Prey2 speed", "prey2_speed", "float"),
            ("Prey2 max age", "prey2_max_age", "int"),
            ("Prey2 reproduce energy", "prey2_reproduction_energy", "float"),

            ("Pred speed", "predator_speed", "float"),
            ("Pred max age", "predator_max_age", "int"),
            ("Pred reproduce energy", "predator_reproduction_energy", "float"),
        ]

        self.param_fields = []
        for i, (label, attr, field_type) in enumerate(fields):
            self.param_fields.append({
                "label": label,
                "attr": attr,
                "type": field_type,
                "label_pos": (label_x, start_y + i * row_h + 3),
                "rect": pygame.Rect(box_x, start_y + i * row_h, box_w, box_h)
            })

    def get_field_value_text(self, index):
        if self.active_field == index:
            return self.input_text

        attr = self.param_fields[index]["attr"]
        value = getattr(self, attr)

        if isinstance(value, float):
            return str(round(value, 4))
        return str(value)

    def commit_active_field(self):
        if self.active_field is None:
            return

        field = self.param_fields[self.active_field]
        attr = field["attr"]
        field_type = field["type"]
        text = self.input_text.replace(",", ".")

        try:
            if field_type == "int":
                value = int(float(text))
            else:
                value = float(text)

            if value < 0:
                value = 0

            setattr(self, attr, value)
        except ValueError:
            pass

        self.active_field = None
        self.input_text = ""

    def handleTextInput(self, event):
        if self.active_field is None:
            return

        if event.key == pygame.K_RETURN:
            self.commit_active_field()
        elif event.key == pygame.K_ESCAPE:
            self.active_field = None
            self.input_text = ""
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            char = event.unicode
            if char.isdigit() or char in [".", ","]:
                self.input_text += char

    def handleButton(self, action):
        self.commit_active_field()

        if action == "start":
            if not self.simulation_started:
                self.resetSimulation()
                self.simulation_started = True
            self.paused = False
        elif action == "stop":
            self.paused = True
        elif action == "reset":
            self.paused = True
            self.simulation_started = False
            self.resetSimulation()
        elif action == "spawn_prey":
            self.spawnPrey()
        elif action == "spawn_prey2":
            self.spawnPrey2()
        elif action == "spawn_food":
            self.spawnFood()
        elif action == "spawn_pred":
            self.spawnPredator()

    def drawPanel(self):
        panel_rect = pygame.Rect(0, 0, self.panel_width, self.height)
        pygame.draw.rect(self.surface, (30, 34, 40), panel_rect)
        pygame.draw.line(self.surface, (70, 74, 82), (self.panel_width, 0), (self.panel_width, self.height), 2)

        # knoppen
        for btn in self.buttons:
            btn_color = btn.get("color", (70, 90, 120))
            pygame.draw.rect(self.surface, btn_color, btn["rect"], border_radius=8)
            pygame.draw.rect(self.surface, (190, 200, 220), btn["rect"], 2, border_radius=8)
            txt = self.smallFont.render(btn["label"], True, (255, 255, 255))
            txt_rect = txt.get_rect(center=btn["rect"].center)
            self.surface.blit(txt, txt_rect)

        title = self.uiFont.render("Control Panel", True, (240, 240, 240))
        self.surface.blit(title, (20, 230))

        hint = self.tinyFont.render("Tune eerst de waarden, klik daarna op Start", True, (210, 210, 210))
        self.surface.blit(hint, (20, 260))

        for i, field in enumerate(self.param_fields):
            rect = field["rect"]
            label = self.tinyFont.render(field["label"], True, (220, 220, 220))
            self.surface.blit(label, field["label_pos"])

            if self.active_field == i:
                box_color = (255, 245, 190)
                border_color = (255, 210, 80)
            else:
                box_color = (245, 245, 245)
                border_color = (180, 180, 180)

            pygame.draw.rect(self.surface, box_color, rect, border_radius=5)
            pygame.draw.rect(self.surface, border_color, rect, 2, border_radius=5)

            value_text = self.get_field_value_text(i)
            value = self.tinyFont.render(value_text, True, (50, 50, 50))
            self.surface.blit(value, (rect.x + 7, rect.y + 4))

        # status en live stats onderaan
        stats_y = 920
        stats_title = self.uiFont.render("Live Stats", True, (240, 240, 240))
        self.surface.blit(stats_title, (20, stats_y))

        status = "Running" if not self.paused else "Stopped"
        status_txt = self.smallFont.render(f"Status: {status}", True, (230, 230, 230))
        self.surface.blit(status_txt, (20, stats_y + 35))

        stats = [
            ("Food", len(self.foodPopulation), (80, 220, 120)),
            ("Prey", len(self.preyPopulation), (90, 180, 255)),
            ("Prey2", len(self.prey2Population), (255, 210, 90)),
            ("Predators", len(self.predatorPopulation), (255, 90, 90)),
        ]

        y = stats_y + 70
        for label, value, color in stats:
            txt = self.smallFont.render(f"{label}: {value}", True, color)
            self.surface.blit(txt, (20, y))
            y += 27

    # --------------------------------------------------
    # SIMULATIE
    # --------------------------------------------------
    def timestep(self):
        if self.paused:
            return

        for prey in list(self.preyPopulation):
            prey.update()

        for prey2 in list(self.prey2Population):
            prey2.update()

        for pred in list(self.predatorPopulation):
            pred.update()

        for food in list(self.foodPopulation):
            food.update()

        # prey eet food
        for food in list(self.foodPopulation):
            eaten = False

            for prey in list(self.preyPopulation):
                if prey.collidesWith(food):
                    prey.eat(food)
                    food.reset()
                    eaten = True
                    break

            if eaten:
                continue

            for prey2 in list(self.prey2Population):
                if prey2.collidesWith(food):
                    prey2.eat(food)
                    food.reset()
                    eaten = True
                    break

        self.reproduceFood()

        self.food_history.append(len(self.foodPopulation))
        self.prey_history.append(len(self.preyPopulation))
        self.prey2_history.append(len(self.prey2Population))
        self.pred_history.append(len(self.predatorPopulation))

        if self.csv_writer is not None:
            self.csv_writer.writerow([
                self.timestep_counter,
                len(self.foodPopulation),
                len(self.preyPopulation),
                len(self.prey2Population),
                len(self.predatorPopulation),
            ])
            self.timestep_counter += 1

    # --------------------------------------------------
    # GRAFIEK
    # --------------------------------------------------
    def drawBottomGraph(self):
        x, y, w, h = self.graph_rect

        pygame.draw.rect(self.surface, (25, 28, 34), self.graph_rect)
        pygame.draw.line(self.surface, (80, 80, 80), (x, y), (x + w, y), 2)

        padding = 20
        gx = x + padding
        gy = y + 30
        gw = w - padding * 2
        gh = h - 70

        title = self.uiFont.render("Population Over Time", True, (240, 240, 240))
        self.surface.blit(title, (x + 10, y + 4))

        values = (
            list(self.food_history)
            + list(self.prey_history)
            + list(self.prey2_history)
            + list(self.pred_history)
        )
        max_val = max(values) if values else 10
        max_val = max(max_val, 10)

        def make_points(history):
            pts = []
            data = list(history)
            if len(data) < 2:
                return pts

            for i, val in enumerate(data):
                px = gx + int(i * (gw / max(1, self.max_history - 1)))
                py = gy + gh - int((val / max_val) * gh)
                pts.append((px, py))
            return pts

        for i in range(5):
            yy = gy + int(i * gh / 4)
            pygame.draw.line(self.surface, (50, 50, 50), (gx, yy), (gx + gw, yy), 1)
            label_val = int(max_val - i * (max_val / 4))
            label = self.smallFont.render(str(label_val), True, (180, 180, 180))
            self.surface.blit(label, (gx + 5, yy - 10))

        food_points = make_points(self.food_history)
        prey_points = make_points(self.prey_history)
        prey2_points = make_points(self.prey2_history)
        pred_points = make_points(self.pred_history)

        if len(food_points) >= 2:
            pygame.draw.lines(self.surface, (80, 220, 120), False, food_points, 2)
        if len(prey_points) >= 2:
            pygame.draw.lines(self.surface, (90, 180, 255), False, prey_points, 2)
        if len(prey2_points) >= 2:
            pygame.draw.lines(self.surface, (255, 210, 90), False, prey2_points, 2)
        if len(pred_points) >= 2:
            pygame.draw.lines(self.surface, (255, 90, 90), False, pred_points, 2)

        ly = y + h - 20
        pygame.draw.line(self.surface, (80, 220, 120), (x + 15, ly), (x + 35, ly), 3)
        self.surface.blit(self.smallFont.render("Food", True, (220, 220, 220)), (x + 42, ly - 9))
        pygame.draw.line(self.surface, (90, 180, 255), (x + 100, ly), (x + 120, ly), 3)
        self.surface.blit(self.smallFont.render("Prey", True, (220, 220, 220)), (x + 127, ly - 9))
        pygame.draw.line(self.surface, (255, 210, 90), (x + 180, ly), (x + 200, ly), 3)
        self.surface.blit(self.smallFont.render("Prey2", True, (220, 220, 220)), (x + 207, ly - 9))
        pygame.draw.line(self.surface, (255, 90, 90), (x + 280, ly), (x + 300, ly), 3)
        self.surface.blit(self.smallFont.render("Predators", True, (220, 220, 220)), (x + 307, ly - 9))

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.backgroundImage, self.sim_rect.topleft)

        for prey in self.preyPopulation:
            prey.draw()
        for prey2 in self.prey2Population:
            prey2.draw()
        for pred in self.predatorPopulation:
            pred.draw()
        for food in self.foodPopulation:
            food.draw()

        self.drawPanel()
        self.drawBottomGraph()

        fps = int(self.clock.get_fps())
        debug_text = (
            f"FPS: {fps} | Food: {len(self.foodPopulation)} | "
            f"Prey: {len(self.preyPopulation)} | "
            f"Prey2: {len(self.prey2Population)} | "
            f"Predators: {len(self.predatorPopulation)}"
        )
        text = self.debugFont.render(debug_text, True, (255, 255, 255))
        self.surface.blit(text, (self.panel_width + 10, 10))

        pygame.display.flip()

    # --------------------------------------------------
    # MAIN
    # --------------------------------------------------
    def playGame(self):
        pygame.init()

        try:
            pygame.mixer.init()
        except Exception:
            pass

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ecosystem Simulation")

        self.clock = pygame.time.Clock()
        self.debugFont = pygame.font.SysFont("consolas", 22)
        self.uiFont = pygame.font.SysFont("arial", 24, bold=True)
        self.smallFont = pygame.font.SysFont("arial", 18)
        self.tinyFont = pygame.font.SysFont("arial", 15)

        self.setup_ui()

        export_dir.mkdir(parents=True, exist_ok=True)

        raw_background = pygame.image.load(background).convert()
        self.preyImage = pygame.transform.scale(pygame.image.load(prey1).convert_alpha(), (20, 20))
        self.prey2Image = pygame.transform.scale(pygame.image.load(prey2).convert_alpha(), (40, 40))
        self.predImage = pygame.transform.scale(pygame.image.load(pred1).convert_alpha(), (60, 70))
        self.foodImage = pygame.transform.scale(pygame.image.load(food1).convert_alpha(), (25, 25))

        self.backgroundImage = pygame.transform.scale(
            raw_background,
            (self.sim_rect.width, self.sim_rect.height)
        )

        # Toon alvast startpopulatie terwijl de simulatie nog stilstaat.
        self.resetSimulation()

        self.csv_file = open(exportbestand, "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file, delimiter=';')
        self.csv_writer.writerow(["Timestep", "Food", "Prey", "Prey2", "Predators"])
        self.timestep_counter = 0

        running = True
        while running:
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                elif e.type == pygame.KEYDOWN:
                    self.handleTextInput(e)

                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos

                    clicked_field = False
                    for i, field in enumerate(self.param_fields):
                        if field["rect"].collidepoint(mx, my):
                            self.commit_active_field()
                            self.active_field = i
                            self.input_text = str(getattr(self, field["attr"]))
                            clicked_field = True
                            break

                    if clicked_field:
                        continue

                    self.commit_active_field()

                    for btn in self.buttons:
                        if btn["rect"].collidepoint(mx, my):
                            self.handleButton(btn["action"])
                            break

            self.timestep()
            self.draw()

        if self.csv_file:
            self.csv_file.close()
        pygame.quit()


# ==================================================
# START
# ==================================================
if __name__ == "__main__":
    game = SurvivalSim()
    game.playGame()

