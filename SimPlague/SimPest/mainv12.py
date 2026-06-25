import csv
import pygame
import random
from pathlib import Path
import math
from collections import deque
from datetime import datetime


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
        self.energy = self.game.prey_start_energy
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
        self.energy = self.game.prey2_start_energy
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
        self.energy = self.game.predator_start_energy
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
        self.height = 1200
        self.panel_width = 390
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
        self.export_message = ""
        self.export_message_timer = 0

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
        self.prey_start_energy = 100
        self.prey_reproduction_energy = 60
        self.prey_energy_gain = 30
        self.prey_energy_loss = 0.10
        self.prey_reproduction_cost = 45

        # Prey2 parameters
        self.prey2_speed = 6.0
        self.prey2_max_age = 1200
        self.prey2_start_energy = 80
        self.prey2_reproduction_energy = 65
        self.prey2_energy_gain = 20
        self.prey2_energy_loss = 0.15
        self.prey2_reproduction_cost = 40

        # Predator parameters
        self.predator_speed = 3.0
        self.predator_max_age = 700
        self.predator_start_energy = 200
        self.predator_reproduction_energy = 1000
        self.predator_energy_gain = 120
        self.predator_energy_loss = 2.0
        self.predator_reproduction_cost = 800

        # grafiekhistorie: alleen voor de grafiek, mag maxlen hebben
        self.max_history = 340
        self.food_history = deque(maxlen=self.max_history)
        self.prey_history = deque(maxlen=self.max_history)
        self.prey2_history = deque(maxlen=self.max_history)
        self.pred_history = deque(maxlen=self.max_history)

        # volledige dataset: zonder maxlen, dus compleet voor CSV-export
        self.full_data = []

        # populaties
        self.preyPopulation = []
        self.prey2Population = []
        self.predatorPopulation = []
        self.foodPopulation = []

        # csv
        self.csv_file = None
        self.csv_writer = None
        self.csv_path = None
        self.timestep_counter = 0

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def getClosestFood(self, pos):
        if not self.foodPopulation:
            return None
        return min(self.foodPopulation, key=lambda f: distance(pos, f.position))

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
    # CSV
    # --------------------------------------------------
    def close_csv(self):
        """Sluit het CSV-bestand veilig af."""
        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()
            self.csv_file.close()
        self.csv_file = None
        self.csv_writer = None

    def open_new_csv_run(self):
        """
        Start een nieuw hoofdbestand voor deze run.
        Belangrijk: dit wordt pas gedaan bij Start, zodat CSV precies bij timestep 0 begint.
        """
        export_dir.mkdir(parents=True, exist_ok=True)
        self.close_csv()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = export_dir / f"simulation_run_{timestamp}.csv"
        self.csv_file = open(self.csv_path, "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file, delimiter=";")
        self.csv_writer.writerow(["Timestep", "Food", "Prey", "Prey2", "Predators"])
        self.csv_file.flush()

        self.full_data = []
        self.timestep_counter = 0

        self.export_message = f"Nieuwe CSV: {self.csv_path.name}"
        self.export_message_timer = 180

    def export_csv_now(self):
        """
        Maakt direct een extra CSV-export van de volledige simulatie.
        Deze gebruikt self.full_data, niet de grafiek-deques, zodat oude timesteps niet verdwijnen.
        """
        export_dir.mkdir(parents=True, exist_ok=True)

        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = export_dir / f"simulation_full_export_{timestamp}_t{self.timestep_counter}.csv"

        with open(snapshot_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Timestep", "Food", "Prey", "Prey2", "Predators"])
            writer.writerows(self.full_data)

        self.export_message = f"Volledige export: {snapshot_path.name}"
        self.export_message_timer = 180
        print(f"Volledige CSV-export gemaakt: {snapshot_path}")

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def setup_ui(self):
        self.buttons = [
            {"label": "Start",       "rect": pygame.Rect(20, 20, 160, 42),  "action": "start",      "color": (60, 140, 80)},
            {"label": "Stop",        "rect": pygame.Rect(200, 20, 160, 42), "action": "stop",       "color": (160, 70, 70)},
            {"label": "Reset",       "rect": pygame.Rect(20, 72, 160, 42),  "action": "reset",      "color": (70, 90, 120)},
            {"label": "Spawn Prey",  "rect": pygame.Rect(200, 72, 160, 42), "action": "spawn_prey", "color": (70, 90, 120)},
            {"label": "Spawn Prey2", "rect": pygame.Rect(20, 124, 160, 42), "action": "spawn_prey2","color": (70, 90, 120)},
            {"label": "Spawn Food",  "rect": pygame.Rect(200, 124, 160, 42),"action": "spawn_food", "color": (70, 90, 120)},
            {"label": "Spawn Pred",  "rect": pygame.Rect(20, 176, 160, 42), "action": "spawn_pred", "color": (70, 90, 120)},
            {"label": "Export CSV",  "rect": pygame.Rect(200, 176, 160, 42),"action": "export_csv", "color": (120, 120, 40)},
        ]
        self.update_param_fields()

    def update_param_fields(self):
        start_y = 285
        row_h = 31
        box_w = 120
        box_h = 23
        label_x = 20
        box_x = 245
        fields = [
            # FOOD
            ("Food aantal", "start_food", "int"),
            ("Food snelheid", "food_speed", "float"),
            ("Food max leeftijd", "food_max_age", "int"),
            ("Food reproduce kans", "food_spawn_chance", "float"),

            # PREY 1
            ("Prey aantal", "start_prey", "int"),
            ("Prey snelheid", "prey_speed", "float"),
            ("Prey max leeftijd", "prey_max_age", "int"),
            ("Prey reproduce energie", "prey_reproduction_energy", "float"),

            # PREY 2
            ("Prey2 aantal", "start_prey2", "int"),
            ("Prey2 snelheid", "prey2_speed", "float"),
            ("Prey2 max leeftijd", "prey2_max_age", "int"),
            ("Prey2 reproduce energie", "prey2_reproduction_energy", "float"),

            # PREDATOR
            ("Predator aantal", "start_predators", "int"),
            ("Predator snelheid", "predator_speed", "float"),
            ("Predator max leeftijd", "predator_max_age", "int"),
            ("Predator reproduce energie", "predator_reproduction_energy", "float"),
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
                self.open_new_csv_run()
                self.simulation_started = True
            self.paused = False
        elif action == "stop":
            self.paused = True
        elif action == "reset":
            self.paused = True
            self.simulation_started = False
            self.close_csv()
            self.full_data = []
            self.resetSimulation()
        elif action == "spawn_prey":
            self.spawnPrey()
        elif action == "spawn_prey2":
            self.spawnPrey2()
        elif action == "spawn_food":
            self.spawnFood()
        elif action == "spawn_pred":
            self.spawnPredator()
        elif action == "export_csv":
            self.export_csv_now()

    def drawPanel(self):
        panel_rect = pygame.Rect(0, 0, self.panel_width, self.height)
        pygame.draw.rect(self.surface, (30, 34, 40), panel_rect)
        pygame.draw.line(self.surface, (70, 74, 82), (self.panel_width, 0), (self.panel_width, self.height), 2)

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

        stats_y = 850
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

        y = stats_y + 65
        for label, value, color in stats:
            txt = self.smallFont.render(f"{label}: {value}", True, color)
            self.surface.blit(txt, (20, y))
            y += 27

        if self.export_message_timer > 0:
            msg = self.tinyFont.render(self.export_message, True, (255, 230, 120))
            self.surface.blit(msg, (20, self.height - 25))
            self.export_message_timer -= 1

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

        row = [
            self.timestep_counter,
            len(self.foodPopulation),
            len(self.preyPopulation),
            len(self.prey2Population),
            len(self.predatorPopulation),
        ]

        # Complete dataset onthouden. Deze lijst heeft GEEN maxlen.
        self.full_data.append(row)

        if self.csv_writer is not None and self.csv_file is not None and not self.csv_file.closed:
            self.csv_writer.writerow(row)
            self.csv_file.flush()

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
        self.tinyFont = pygame.font.SysFont("arial", 14)

        self.setup_ui()

        raw_background = pygame.image.load(background).convert()
        self.preyImage = pygame.transform.scale(pygame.image.load(prey1).convert_alpha(), (20, 20))
        self.prey2Image = pygame.transform.scale(pygame.image.load(prey2).convert_alpha(), (40, 40))
        self.predImage = pygame.transform.scale(pygame.image.load(pred1).convert_alpha(), (60, 70))
        self.foodImage = pygame.transform.scale(pygame.image.load(food1).convert_alpha(), (25, 25))

        self.backgroundImage = pygame.transform.scale(
            raw_background,
            (self.sim_rect.width, self.sim_rect.height)
        )

        export_dir.mkdir(parents=True, exist_ok=True)

        # Toon alvast startpopulatie terwijl de simulatie nog stilstaat.
        # CSV begint pas wanneer je op Start klikt.
        self.resetSimulation()

        running = True

        try:
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

        finally:
            # Altijd sluiten, ook bij foutmelding of sluiten van het venster.
            self.close_csv()
            pygame.quit()


# ==================================================
# START
# ==================================================
if __name__ == "__main__":
    game = SurvivalSim()
    game.playGame()

