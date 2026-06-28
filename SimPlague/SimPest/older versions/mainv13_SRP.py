# mainv13_SRP_assets.py
# Refactored single-file version with AssetManager integrated.
# Load this file and run. Ensure pygame is installed and assets folder exists.

import csv
import pygame
import random
from pathlib import Path
import math
from collections import deque
from datetime import datetime

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


# ==================================================
# ASSET MANAGER
# ==================================================
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, key, path, size=None, convert_alpha=True):
        """
        Load an image and optionally scale it.
        Returns the pygame.Surface stored under key.
        """
        img = pygame.image.load(path)
        img = img.convert_alpha() if convert_alpha else img.convert()

        if size:
            # Use smoothscale for better quality
            img = pygame.transform.smoothscale(img, size)

        self.images[key] = img
        return img

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path):
        """
        Load a sound. If mixer or file fails, store DummySound.
        """
        try:
            snd = pygame.mixer.Sound(path)
            self.sounds[key] = snd
        except Exception:
            self.sounds[key] = DummySound()
        return self.sounds[key]

    def get_sound(self, key):
        return self.sounds.get(key, DummySound())


# ==================================================
# SPRITES
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
        # image is a Surface
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


class Prey(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        # Use AssetManager sound
        self.eatSound = self.game.assets.get_sound("eat")
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

        target = self.game.engine.getClosestFood(self.position)
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
            self.game.factory.spawnPrey()


class Prey2(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.eatSound = self.game.assets.get_sound("eat")
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

        target = self.game.engine.getClosestFood(self.position)
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
            self.game.factory.spawnPrey2()


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

        target = self.game.engine.getClosestAnyPrey(self.position)
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
            self.game.factory.spawnPredator()

        self.placeInScreen()


# ==================================================
# DATA LOGGER
# ==================================================
class DataLogger:
    def __init__(self, export_dir: Path):
        self.export_dir = export_dir
        self.csv_file = None
        self.csv_writer = None
        self.csv_path = None
        self.full_data = []
        self.timestep_counter = 0
        self.export_message = ""
        self.export_message_timer = 0

    def close_csv(self):
        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()
            self.csv_file.close()
        self.csv_file = None
        self.csv_writer = None

    def start_new_run(self):
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.close_csv()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = self.export_dir / f"simulation_run_{timestamp}.csv"
        self.csv_file = open(self.csv_path, "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file, delimiter=";")
        self.csv_writer.writerow(["Timestep", "Food", "Prey", "Prey2", "Predators"])
        self.csv_file.flush()

        self.full_data = []
        self.timestep_counter = 0

        self.export_message = f"Nieuwe CSV: {self.csv_path.name}"
        self.export_message_timer = 180

    def log_step(self, food, prey, prey2, predators):
        row = [
            self.timestep_counter,
            food,
            prey,
            prey2,
            predators,
        ]
        self.full_data.append(row)

        if self.csv_writer is not None and self.csv_file is not None and not self.csv_file.closed:
            self.csv_writer.writerow(row)
            self.csv_file.flush()

        self.timestep_counter += 1
        return row

    def export_snapshot(self):
        self.export_dir.mkdir(parents=True, exist_ok=True)

        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.export_dir / f"simulation_full_export_{timestamp}_t{self.timestep_counter}.csv"

        with open(snapshot_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Timestep", "Food", "Prey", "Prey2", "Predators"])
            writer.writerows(self.full_data)

        self.export_message = f"Volledige export: {snapshot_path.name}"
        self.export_message_timer = 180
        print(f"Volledige CSV-export gemaakt: {snapshot_path}")
        return snapshot_path.name


# ==================================================
# ENTITY FACTORY
# ==================================================
class EntityFactory:
    def __init__(self, game):
        self.game = game

    def spawnPrey(self):
        self.game.preyPopulation.append(Prey(self.game.preyImage, self.game))

    def spawnPrey2(self):
        self.game.prey2Population.append(Prey2(self.game.prey2Image, self.game))

    def spawnPredator(self):
        self.game.predatorPopulation.append(Predator(self.game.predImage, self.game))

    def spawnFood(self):
        if len(self.game.foodPopulation) < self.game.max_food:
            self.game.foodPopulation.append(Food(self.game.foodImage, self.game))


# ==================================================
# SIMULATION ENGINE
# ==================================================
class SimulationEngine:
    def __init__(self, game):
        self.game = game

    def getClosestFood(self, pos):
        if not self.game.foodPopulation:
            return None
        return min(self.game.foodPopulation, key=lambda f: distance(pos, f.position))

    def getClosestAnyPrey(self, pos):
        all_prey = self.game.preyPopulation + self.game.prey2Population
        if not all_prey:
            return None
        return min(all_prey, key=lambda p: distance(pos, p.position))

    def reproduceFood(self):
        if len(self.game.foodPopulation) >= self.game.max_food:
            return

        new_food = []
        for food in self.game.foodPopulation:
            if len(self.game.foodPopulation) + len(new_food) >= self.game.max_food:
                break

            if random.random() < self.game.food_spawn_chance:
                f = Food(self.game.foodImage, self.game)
                offset = 50

                f.position = [
                    clamp(
                        food.position[0] + random.randint(-offset, offset),
                        self.game.sim_rect.left,
                        self.game.sim_rect.right - f.image.get_width()
                    ),
                    clamp(
                        food.position[1] + random.randint(-offset, offset),
                        self.game.sim_rect.top,
                        self.game.sim_rect.bottom - f.image.get_height()
                    )
                ]
                new_food.append(f)

        self.game.foodPopulation.extend(new_food)

    def update(self):
        for prey in list(self.game.preyPopulation):
            prey.update()

        for prey2 in list(self.game.prey2Population):
            prey2.update()

        for pred in list(self.game.predatorPopulation):
            pred.update()

        for food in list(self.game.foodPopulation):
            food.update()

        for food in list(self.game.foodPopulation):
            eaten = False

            for prey in list(self.game.preyPopulation):
                if prey.collidesWith(food):
                    prey.eat(food)
                    food.reset()
                    eaten = True
                    break

            if eaten:
                continue

            for prey2 in list(self.game.prey2Population):
                if prey2.collidesWith(food):
                    prey2.eat(food)
                    food.reset()
                    eaten = True
                    break

        self.reproduceFood()

        self.game.food_history.append(len(self.game.foodPopulation))
        self.game.prey_history.append(len(self.game.preyPopulation))
        self.game.prey2_history.append(len(self.game.prey2Population))
        self.game.pred_history.append(len(self.game.predatorPopulation))

        self.game.logger.log_step(
            len(self.game.foodPopulation),
            len(self.game.preyPopulation),
            len(self.game.prey2Population),
            len(self.game.predatorPopulation),
        )


# ==================================================
# UI CONTROLLER
# ==================================================
class UIController:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.param_fields = []
        self.active_field = None
        self.input_text = ""
        self.export_message = ""
        self.export_message_timer = 0

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
            ("Food aantal", "start_food", "int"),
            ("Food snelheid", "food_speed", "float"),
            ("Food max leeftijd", "food_max_age", "int"),
            ("Food reproduce kans", "food_spawn_chance", "float"),
            ("Prey aantal", "start_prey", "int"),
            ("Prey snelheid", "prey_speed", "float"),
            ("Prey max leeftijd", "prey_max_age", "int"),
            ("Prey reproduce energie", "prey_reproduction_energy", "float"),
            ("Prey2 aantal", "start_prey2", "int"),
            ("Prey2 snelheid", "prey2_speed", "float"),
            ("Prey2 max leeftijd", "prey2_max_age", "int"),
            ("Prey2 reproduce energie", "prey2_reproduction_energy", "float"),
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
        value = getattr(self.game, attr)

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

            setattr(self.game, attr, value)
        except ValueError:
            pass

        self.active_field = None
        self.input_text = ""

    def handle_text_input(self, event):
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

    def handle_button(self, action):
        self.commit_active_field()

        if action == "start":
            if not self.game.simulation_started:
                self.game.resetSimulation()
                self.game.logger.start_new_run()
                self.game.simulation_started = True
            self.game.paused = False
        elif action == "stop":
            self.game.paused = True
        elif action == "reset":
            self.game.paused = True
            self.game.simulation_started = False
            self.game.logger.close_csv()
            self.game.resetSimulation()
        elif action == "spawn_prey":
            self.game.factory.spawnPrey()
        elif action == "spawn_prey2":
            self.game.factory.spawnPrey2()
        elif action == "spawn_food":
            self.game.factory.spawnFood()
        elif action == "spawn_pred":
            self.game.factory.spawnPredator()
        elif action == "export_csv":
            name = self.game.logger.export_snapshot()
            self.export_message = f"Volledige export: {name}"
            self.export_message_timer = 180

    def draw_panel(self):
        panel_rect = pygame.Rect(0, 0, self.game.panel_width, self.game.height)
        pygame.draw.rect(self.game.surface, (30, 34, 40), panel_rect)
        pygame.draw.line(self.game.surface, (70, 74, 82),
                         (self.game.panel_width, 0),
                         (self.game.panel_width, self.game.height), 2)

        for btn in self.buttons:
            btn_color = btn.get("color", (70, 90, 120))
            pygame.draw.rect(self.game.surface, btn_color, btn["rect"], border_radius=8)
            pygame.draw.rect(self.game.surface, (190, 200, 220), btn["rect"], 2, border_radius=8)
            txt = self.game.smallFont.render(btn["label"], True, (255, 255, 255))
            txt_rect = txt.get_rect(center=btn["rect"].center)
            self.game.surface.blit(txt, txt_rect)

                
        # scheiding onder knoppen
        y_sep1 = self.buttons[-1]["rect"].bottom + 15
        pygame.draw.line(self.game.surface, (80, 80, 80), (20, y_sep1), (self.game.panel_width - 20, y_sep1), 2)


        title = self.game.uiFont.render("Control Panel", True, (240, 240, 240))
        self.game.surface.blit(title, (20, 230))

        hint = self.game.tinyFont.render("Tune eerst de waarden, klik daarna op Start", True, (210, 210, 210))
        self.game.surface.blit(hint, (20, 260))

        for i, field in enumerate(self.param_fields):
            rect = field["rect"]
            label = self.game.tinyFont.render(field["label"], True, (220, 220, 220))
            self.game.surface.blit(label, field["label_pos"])

            if self.active_field == i:
                box_color = (255, 245, 190)
                border_color = (255, 210, 80)
            else:
                box_color = (245, 245, 245)
                border_color = (180, 180, 180)

            pygame.draw.rect(self.game.surface, box_color, rect, border_radius=5)
            pygame.draw.rect(self.game.surface, border_color, rect, 2, border_radius=5)

            value_text = self.get_field_value_text(i)
            value = self.game.tinyFont.render(value_text, True, (50, 50, 50))
            self.game.surface.blit(value, (rect.x + 7, rect.y + 4))

        # scheiding onder parameters        
        y_sep2 = self.param_fields[-1]["rect"].bottom + 15
        pygame.draw.line(self.game.surface, (80, 80, 80), (20, y_sep2), (self.game.panel_width - 20, y_sep2), 2)

        stats_y = self.game.graph_rect.y + 10
        stats_title = self.game.uiFont.render("Live Stats", True, (240, 240, 240))
        self.game.surface.blit(stats_title, (20, stats_y))

        status = "Running" if not self.game.paused else "Stopped"
        status_txt = self.game.smallFont.render(f"Status: {status}", True, (230, 230, 230))
        self.game.surface.blit(status_txt, (20, stats_y + 35))

        stats = [
            ("Timestep", self.game.logger.timestep_counter, (200, 200, 200)),
            ("Food", len(self.game.foodPopulation), (80, 220, 120)),
            ("Prey", len(self.game.preyPopulation), (90, 180, 255)),
            ("Prey2", len(self.game.prey2Population), (255, 210, 90)),
            ("Predators", len(self.game.predatorPopulation), (255, 90, 90)),
        ]


        y = stats_y + 65
        for label, value, color in stats:
            txt = self.game.smallFont.render(f"{label}: {value}", True, color)
            self.game.surface.blit(txt, (20, y))
            y += 27

        if self.export_message_timer > 0:
            msg = self.game.tinyFont.render(self.export_message, True, (255, 230, 120))
            self.game.surface.blit(msg, (20, self.game.height - 25))
            self.export_message_timer -= 1


# ==================================================
# GRAPH RENDERER
# ==================================================
class GraphRenderer:
    def __init__(self, game):
        self.game = game

    def draw(self):
        x, y, w, h = self.game.graph_rect

        pygame.draw.rect(self.game.surface, (25, 28, 34), self.game.graph_rect)
        pygame.draw.line(self.game.surface, (80, 80, 80), (x, y), (x + w, y), 2)

        padding = 20
        gx = x + padding
        gy = y + 30
        gw = w - padding * 2
        gh = h - 70

        title = self.game.uiFont.render("Population Over Time", True, (240, 240, 240))
        self.game.surface.blit(title, (x + 10, y + 4))

        values = (
            list(self.game.food_history)
            + list(self.game.prey_history)
            + list(self.game.prey2_history)
            + list(self.game.pred_history)
        )
        max_val = max(values) if values else 10
        max_val = max(max_val, 10)

        def make_points(history):
            pts = []
            data = list(history)
            if len(data) < 2:
                return pts

            for i, val in enumerate(data):
                px = gx + int(i * (gw / max(1, self.game.max_history - 1)))
                py = gy + gh - int((val / max_val) * gh)
                pts.append((px, py))
            return pts

        for i in range(5):
            yy = gy + int(i * gh / 4)
            pygame.draw.line(self.game.surface, (50, 50, 50), (gx, yy), (gx + gw, yy), 1)
            label_val = int(max_val - i * (max_val / 4))
            label = self.game.smallFont.render(str(label_val), True, (180, 180, 180))
            self.game.surface.blit(label, (gx + 5, yy - 10))

        food_points = make_points(self.game.food_history)
        prey_points = make_points(self.game.prey_history)
        prey2_points = make_points(self.game.prey2_history)
        pred_points = make_points(self.game.pred_history)

        if len(food_points) >= 2:
            pygame.draw.lines(self.game.surface, (80, 220, 120), False, food_points, 2)
        if len(prey_points) >= 2:
            pygame.draw.lines(self.game.surface, (90, 180, 255), False, prey_points, 2)
        if len(prey2_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 210, 90), False, prey2_points, 2)
        if len(pred_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 90, 90), False, pred_points, 2)


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
# !!!!! aangepast met behulp van ai om te proberen tot een evenwichtssituatie te komen, dat werkt nog niet.
        # Food parameters
        self.start_food = 45
        self.food_speed = 0.0
        self.food_max_age = 1800
        self.food_spawn_chance = 0.0046   # net onder 0.004
        self.max_food = 120               # iets meer buffer

        # Prey parameters (minder explosief, minder kwetsbaar)
        self.start_prey = 14
        self.prey_speed = 2.0
        self.prey_max_age = 1600
        self.prey_start_energy = 110
        self.prey_reproduction_energy = 85
        self.prey_energy_gain = 20        # lager dan 35
        self.prey_energy_loss = 0.10      # iets hoger dan 0.12
        self.prey_reproduction_cost = 55

        # Prey2 parameters (extra beschermd tegen uitsterven)
        self.start_prey2 = 10
        self.prey2_speed = 4.8
        self.prey2_max_age = 1100
        self.prey2_start_energy = 95
        self.prey2_reproduction_energy = 110
        self.prey2_energy_gain = 18       # iets lager dan 25
        self.prey2_energy_loss = 0.18     # lager dan 0.22
        self.prey2_reproduction_cost = 60

        # Predator parameters (minder harde klap op prooien)
        self.start_predators = 3
        self.predator_speed = 2.6
        self.predator_max_age = 950
        self.predator_start_energy = 240
        self.predator_reproduction_energy = 700
        self.predator_energy_gain = 55    # véél lager dan 140
        self.predator_energy_loss = 1.8   # lager dan 2.2
        self.predator_reproduction_cost = 500




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

        # managers & modules
        self.assets = AssetManager()
        self.logger = DataLogger(export_dir)
        self.factory = EntityFactory(self)
        self.engine = SimulationEngine(self)
        self.ui = UIController(self)
        self.graph = GraphRenderer(self)

        # images will be loaded after display is set (see main)
        self.preyImage = None
        self.prey2Image = None
        self.predImage = None
        self.foodImage = None
        self.backgroundImage = None

    def load_assets(self):
        """
        Load and scale assets. Must be called AFTER pygame.display.set_mode(...)
        """
        # Choose sizes appropriate for your sim_rect; tweak as needed
        self.preyImage = self.assets.load_image("prey", prey1, size=(48, 48))
        self.prey2Image = self.assets.load_image("prey2", prey2, size=(64, 64))
        self.predImage = self.assets.load_image("pred", pred1, size=(72, 72))
        self.foodImage = self.assets.load_image("food", food1, size=(32, 32))
        # background: keep native size or scale to sim_rect if desired
        bg = pygame.image.load(background)
        # If background is not same size as sim_rect, scale it to fit simulation area:
        bg = bg.convert()
        bg = pygame.transform.smoothscale(bg, (self.sim_rect.width, self.sim_rect.height))
        self.backgroundImage = bg

        # Sounds
        # Initialize mixer safely (ignore errors)
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.assets.load_sound("eat", eatSound1)

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
    # CSV helpers (kept for backward compatibility)
    # --------------------------------------------------
    def close_csv(self):
        self.logger.close_csv()

    def open_new_csv_run(self):
        self.logger.start_new_run()

    def export_csv_now(self):
        return self.logger.export_snapshot()

    # --------------------------------------------------
    # SIMULATIE
    # --------------------------------------------------
    def timestep(self):
        if self.paused:
            return

        self.engine.update()

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self):
        # draw background in simulation rect
        self.surface.blit(self.backgroundImage, self.sim_rect)

        for food in self.foodPopulation:
            food.draw()
        for prey in self.preyPopulation:
            prey.draw()
        for prey2 in self.prey2Population:
            prey2.draw()
        for pred in self.predatorPopulation:
            pred.draw()

        self.ui.draw_panel()
        self.graph.draw()


# ==================================================
# MAIN
# ==================================================
def main():
    pygame.init()
    sim = SurvivalSim()

    # Create display BEFORE loading images
    sim.surface = pygame.display.set_mode((sim.width, sim.height))
    pygame.display.set_caption("Survival Simulation")

    # Fonts
    sim.clock = pygame.time.Clock()
    sim.debugFont = pygame.font.SysFont("Consolas", 16)
    sim.uiFont = pygame.font.SysFont("Segoe UI", 22)
    sim.smallFont = pygame.font.SysFont("Segoe UI", 18)
    sim.tinyFont = pygame.font.SysFont("Segoe UI", 14)

    # Load assets now that display exists
    sim.load_assets()

    # Setup UI and initial simulation state
    sim.ui.setup_ui()
    sim.resetSimulation()

    running = True
    while running:
        sim.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sim.logger.close_csv()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # check param fields
                for i, field in enumerate(sim.ui.param_fields):
                    if field["rect"].collidepoint(pos):
                        sim.ui.active_field = i
                        sim.ui.input_text = ""
                        break
                # check buttons
                for btn in sim.ui.buttons:
                    if btn["rect"].collidepoint(pos):
                        sim.ui.handle_button(btn["action"])
            elif event.type == pygame.KEYDOWN:
                sim.ui.handle_text_input(event)

        sim.timestep()
        sim.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
