# main2.py
# Refactored single-file version with AssetManager integrated.
# Includes: Prey1 naming, Pause button, Step button, parameter export,
# 3-row button layout, speed slider, time slider, and SnapshotEngine integration.
# Load this file and run. Ensure pygame is installed and assets folder exists.

import csv
import pygame
import random
from pathlib import Path
import math
from collections import deque
from datetime import datetime
from snapshot_engine import SnapshotEngine

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
        img = pygame.image.load(path)
        img = img.convert_alpha() if convert_alpha else img.convert()

        if size:
            img = pygame.transform.smoothscale(img, size)

        self.images[key] = img
        return img

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path):
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


class Prey1(Sprite):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.eatSound = self.game.assets.get_sound("eat")
        self.energy = self.game.prey1_start_energy
        self.age = 0

    def reset(self):
        sim = self.game.sim_rect
        self.position = [
            random.randint(sim.left, sim.right - self.image.get_width()),
            random.randint(sim.top, sim.bottom - self.image.get_height())
        ]

    def update(self):
        self.age += 1

        if self.age > self.game.prey1_max_age:
            if self in self.game.prey1Population:
                self.game.prey1Population.remove(self)
            return

        self.energy -= self.game.prey1_energy_loss
        if self.energy <= 0:
            if self in self.game.prey1Population:
                self.game.prey1Population.remove(self)
            return

        target = self.game.engine.getClosestFood(self.position)
        if target:
            tx, ty = target.position
            px, py = self.position
            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)

            if dist > 0:
                self.position[0] += self.game.prey1_speed * dx / dist
                self.position[1] += self.game.prey1_speed * dy / dist

        self.placeInScreen()

    def eat(self, food):
        self.energy += self.game.prey1_energy_gain
        self.eatSound.play()

        if self.energy > self.game.prey1_reproduction_energy:
            self.energy -= self.game.prey1_reproduction_cost
            self.game.factory.spawnPrey1()


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

        target = self.game.engine.getClosestAnyPreyTarget(self.position)
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

                if target in self.game.prey1Population:
                    self.game.prey1Population.remove(target)
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
        self.csv_writer.writerow(["Timestep", "Food", "Prey1", "Prey2", "Predators"])
        self.csv_file.flush()

        self.full_data = []
        self.timestep_counter = 0

        self.export_message = f"Nieuwe CSV: {self.csv_path.name}"
        self.export_message_timer = 180

    def log_step(self, food, prey1_count, prey2_count, predators):
        row = [
            self.timestep_counter,
            food,
            prey1_count,
            prey2_count,
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
            writer.writerow(["Timestep", "Food", "Prey1", "Prey2", "Predators"])
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

    
    def spawnPrey1(self):
        self.game.prey1Population.append(Prey1(self.game.prey1Image, self.game))
        self.game.sync_prey1_aliases()

    def spawnPrey(self):  # compatibiliteit met snapshot_engine na wijzigen naam prey naar prey1
        self.spawnPrey1()

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

    def getClosestAnyPreyTarget(self, pos):
        all_targets = self.game.prey1Population + self.game.prey2Population
        if not all_targets:
            return None
        return min(all_targets, key=lambda p: distance(pos, p.position))

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
        for prey1_obj in list(self.game.prey1Population):
            prey1_obj.update()

        for prey2_obj in list(self.game.prey2Population):
            prey2_obj.update()

        for pred in list(self.game.predatorPopulation):
            pred.update()

        for food in list(self.game.foodPopulation):
            food.update()

        for food in list(self.game.foodPopulation):
            eaten = False

            for prey1_obj in list(self.game.prey1Population):
                if prey1_obj.collidesWith(food):
                    prey1_obj.eat(food)
                    food.reset()
                    eaten = True
                    break

            if eaten:
                continue

            for prey2_obj in list(self.game.prey2Population):
                if prey2_obj.collidesWith(food):
                    prey2_obj.eat(food)
                    food.reset()
                    eaten = True
                    break

        self.reproduceFood()

        self.game.food_history.append(len(self.game.foodPopulation))
        self.game.prey1_history.append(len(self.game.prey1Population))
        self.game.prey2_history.append(len(self.game.prey2Population))
        self.game.pred_history.append(len(self.game.predatorPopulation))

        self.game.logger.log_step(
            len(self.game.foodPopulation),
            len(self.game.prey1Population),
            len(self.game.prey2Population),
            len(self.game.predatorPopulation),
        )

        # Sla niet elke frame een snapshot op, maar bijvoorbeeld elke 10 stappen.
        if self.game.logger.timestep_counter % 10 == 0:
            self.game.snapshot_engine.save(self.game)


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

        # slider voor snelheid
        self.slider_rect = pygame.Rect(20, 810, 320, 20)
        self.slider_value = (self.game.sim_speed - 0.1) / 4.9
        self.slider_active = False

        # time slider voor snapshots
        self.time_slider_rect = pygame.Rect(20, 880, 320, 20)
        self.time_slider_value = 0.0
        self.time_slider_active = False
        self.available_snapshots = []
        self.last_loaded_snapshot_id = None

    def setup_ui(self):
        btn_w = 80
        btn_h = 42
        gap = 10
        x1, x2, x3, x4 = 20, 20 + btn_w + gap, 20 + 2 * (btn_w + gap), 20 + 3 * (btn_w + gap)
        y1, y2, y3 = 20, 70, 120

        self.buttons = [
            # Rij 1: start, pause, reset, step
            {"label": "Start", "rect": pygame.Rect(x1, y1, btn_w, btn_h), "action": "start", "color": (60, 140, 80)},
            {"label": "Pause", "rect": pygame.Rect(x2, y1, btn_w, btn_h), "action": "pause", "color": (160, 70, 70)},
            {"label": "Reset", "rect": pygame.Rect(x3, y1, btn_w, btn_h), "action": "reset", "color": (70, 90, 120)},
            {"label": "Step", "rect": pygame.Rect(x4, y1, btn_w, btn_h), "action": "step", "color": (120, 120, 200)},

            # Rij 2: spawn prey1, spawn prey2, spawn food, spawn predator
            {"label": "Spawn P1", "rect": pygame.Rect(x1, y2, btn_w, btn_h), "action": "spawn_prey1", "color": (70, 90, 120)},
            {"label": "Spawn P2", "rect": pygame.Rect(x2, y2, btn_w, btn_h), "action": "spawn_prey2", "color": (70, 90, 120)},
            {"label": "Food", "rect": pygame.Rect(x3, y2, btn_w, btn_h), "action": "spawn_food", "color": (70, 90, 120)},
            {"label": "Predator", "rect": pygame.Rect(x4, y2, btn_w, btn_h), "action": "spawn_pred", "color": (70, 90, 120)},

            # Rij 3: export csv, export parameters, clear snapshot, lege ruimte(gelijke breedte als andere knoppen)
            {"label": "CSV", "rect": pygame.Rect(x1, y3, btn_w, btn_h), "action": "export_csv", "color": (120,120,40)},
            {"label": "Params", "rect": pygame.Rect(x2, y3, btn_w, btn_h), "action": "export_params", "color": (100,70,140)},
            {"label": "Clear", "rect": pygame.Rect(x3, y3, btn_w, btn_h), "action": "clear_snapshots", "color": (140,60,60)},
        ]
        self.update_param_fields()

    def update_param_fields(self):
        start_y = 245
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
            ("Prey1 aantal", "start_prey1", "int"),
            ("Prey1 snelheid", "prey1_speed", "float"),
            ("Prey1 max leeftijd", "prey1_max_age", "int"),
            ("Prey1 reproduce energie", "prey1_reproduction_energy", "float"),
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

    def update_speed_slider_from_mouse(self, mx):
        rect = self.slider_rect
        mx = max(rect.left, min(mx, rect.right))
        self.slider_value = (mx - rect.left) / rect.width
        self.game.sim_speed = 0.1 + self.slider_value * 4.9

    def update_time_slider_from_mouse(self, mx):
        rect = self.time_slider_rect
        mx = max(rect.left, min(mx, rect.right))
        self.time_slider_value = (mx - rect.left) / rect.width

        self.available_snapshots = self.game.snapshot_engine.list_snapshots()

        if not self.available_snapshots:
            self.export_message = "Geen snapshots gevonden"
            self.export_message_timer = 120
            return

        index = int(self.time_slider_value * (len(self.available_snapshots) - 1))
        snapshot = self.available_snapshots[index]

        snapshot_id = snapshot[0]
        timestep = snapshot[1] if len(snapshot) > 1 else None

        if snapshot_id == self.last_loaded_snapshot_id:
            return

        self.game.paused = True
        loaded = self.game.snapshot_engine.load(self.game, snapshot_id)
        self.game.sync_prey1_aliases()

        if loaded is not False:
            self.last_loaded_snapshot_id = snapshot_id

            if timestep is not None:
                self.game.logger.timestep_counter = timestep

            self.export_message = f"Snapshot geladen: id {snapshot_id}, t={timestep}"
            self.export_message_timer = 120
        else:
            self.export_message = f"Snapshot {snapshot_id} kon niet geladen worden"
            self.export_message_timer = 120

    def ensure_run_started(self):
        if not self.game.simulation_started:
            self.game.logger.start_new_run()
            self.game.simulation_started = True

    def export_parameters(self):
        self.commit_active_field()
        export_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = export_dir / f"parameters-{timestamp}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Survival Simulation - parameters\n")
            f.write(f"Geexporteerd op: {datetime.now().isoformat(timespec='seconds')}\n")
            f.write("\n")

            for field in self.param_fields:
                attr = field["attr"]
                label = field["label"]
                value = getattr(self.game, attr)
                f.write(f"{label} ({attr}) = {value}\n")

            f.write("\n")
            f.write("Overig\n")
            f.write(f"sim_speed = {self.game.sim_speed}\n")
            f.write(f"max_food = {self.game.max_food}\n")
            f.write(f"timestep_counter = {self.game.logger.timestep_counter}\n")

        self.export_message = f"Parameters opgeslagen: {file_path.name}"
        self.export_message_timer = 180
        print(f"Parameters opgeslagen: {file_path}")
        return file_path.name

    def handle_button(self, action):
        self.commit_active_field()

        if action == "start":
            if not self.game.simulation_started:
                self.game.resetSimulation()
                self.game.logger.start_new_run()
                self.game.simulation_started = True
            self.game.paused = False

        elif action == "pause":
            self.game.paused = True

        elif action == "reset":
            self.game.paused = True
            self.game.simulation_started = False
            self.game.logger.close_csv()
            self.game.resetSimulation()
            self.export_message = "Simulatie gereset"
            self.export_message_timer = 120

        elif action == "step":
            self.ensure_run_started()
            self.game.paused = True
            self.game.engine.update()
            self.game.sync_prey1_aliases()
            self.export_message = "1 stap uitgevoerd"
            self.export_message_timer = 90

        elif action == "spawn_prey1":
            self.game.factory.spawnPrey1()

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

        elif action == "export_params":
            self.export_parameters()

        elif action == "clear_snapshots":
            self.game.snapshot_engine.clear_all()
            self.time_slider_value = 0.0
            self.available_snapshots = []
            self.last_loaded_snapshot_id = None
            self.export_message = "Alle snapshots verwijderd"
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
            txt = self.game.tinyFont.render(btn["label"], True, (255, 255, 255))
            txt_rect = txt.get_rect(center=btn["rect"].center)
            self.game.surface.blit(txt, txt_rect)

        y_sep1 = self.buttons[-1]["rect"].bottom + 15
        pygame.draw.line(self.game.surface, (80, 80, 80), (20, y_sep1), (self.game.panel_width - 20, y_sep1), 2)

        title = self.game.uiFont.render("Simulatie Parameters", True, (240, 240, 240))
        self.game.surface.blit(title, (20, 180))

        hint = self.game.tinyFont.render("Tune waarden, Start/Pause/Step", True, (210, 210, 210))
        self.game.surface.blit(hint, (20, 210))

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

        y_sep2 = self.param_fields[-1]["rect"].bottom + 12
        pygame.draw.line(self.game.surface, (80, 80, 80), (20, y_sep2), (self.game.panel_width - 20, y_sep2), 2)

        stats_y = self.game.graph_rect.y + 10
        stats_title = self.game.uiFont.render("Live Stats", True, (240, 240, 240))
        self.game.surface.blit(stats_title, (20, stats_y))

        status = "Running" if not self.game.paused else "Paused"
        status_txt = self.game.smallFont.render(f"Status: {status}", True, (230, 230, 230))
        self.game.surface.blit(status_txt, (20, stats_y + 35))

        stats = [
            ("Timestep", self.game.logger.timestep_counter, (200, 200, 200)),
            ("Food", len(self.game.foodPopulation), (80, 220, 120)),
            ("Prey1", len(self.game.prey1Population), (90, 180, 255)),
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

        self.available_snapshots = self.game.snapshot_engine.list_snapshots()

        # === SIM SPEED SLIDER ===
        label = self.game.smallFont.render("Sim Speed", True, (220, 220, 220))
        self.game.surface.blit(label, (20, self.slider_rect.y - 30))

        pygame.draw.rect(self.game.surface, (80, 80, 80), self.slider_rect, border_radius=6)
        handle_x = self.slider_rect.x + int(self.slider_value * self.slider_rect.width)
        handle_rect = pygame.Rect(handle_x - 6, self.slider_rect.y - 6, 12, 32)
        pygame.draw.rect(self.game.surface, (220, 220, 220), handle_rect, border_radius=5)

        speed_txt = self.game.smallFont.render(f"{self.game.sim_speed:.2f}x", True, (255, 255, 255))
        self.game.surface.blit(speed_txt, (250, self.slider_rect.y - 30))

        # === TIME SLIDER ===
        label = self.game.smallFont.render("Timeline / Snapshots", True, (220, 220, 220))
        self.game.surface.blit(label, (20, self.time_slider_rect.y - 30))

        pygame.draw.rect(self.game.surface, (80, 80, 80), self.time_slider_rect, border_radius=6)
        time_handle_x = self.time_slider_rect.x + int(self.time_slider_value * self.time_slider_rect.width)
        time_handle_rect = pygame.Rect(time_handle_x - 6, self.time_slider_rect.y - 6, 12, 32)
        pygame.draw.rect(self.game.surface, (255, 180, 90), time_handle_rect, border_radius=5)

        if self.available_snapshots:
            total = len(self.available_snapshots)
            index = int(self.time_slider_value * (total - 1))
            snapshot = self.available_snapshots[index]
            snapshot_id = snapshot[0]
            timestep = snapshot[1] if len(snapshot) > 1 else "?"
            time_txt = self.game.smallFont.render(
                f"id {snapshot_id} | t={timestep} | {index + 1}/{total}",
                True,
                (255, 255, 255)
            )
        else:
            time_txt = self.game.smallFont.render("Nog geen snapshots", True, (180, 180, 180))

        self.game.surface.blit(time_txt, (20, self.time_slider_rect.y + 28))


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
            + list(self.game.prey1_history)
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
        prey1_points = make_points(self.game.prey1_history)
        prey2_points = make_points(self.game.prey2_history)
        pred_points = make_points(self.game.pred_history)

        if len(food_points) >= 2:
            pygame.draw.lines(self.game.surface, (80, 220, 120), False, food_points, 2)
        if len(prey1_points) >= 2:
            pygame.draw.lines(self.game.surface, (90, 180, 255), False, prey1_points, 2)
        if len(prey2_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 210, 90), False, prey2_points, 2)
        if len(pred_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 90, 90), False, pred_points, 2)


# ==================================================
# MAIN GAME CLASS
# ==================================================
class SurvivalSim:
    def __init__(self):
        self.width = 1600
        self.height = 1200
        self.panel_width = 390
        self.graph_height = 240

        self.sim_speed = 1.0

        self.surface = None
        self.clock = None
        self.debugFont = None
        self.uiFont = None
        self.smallFont = None
        self.tinyFont = None

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

        self.buttons = []
        self.param_fields = []
        self.active_field = None
        self.input_text = ""
        self.paused = True
        self.simulation_started = False
        self.export_message = ""
        self.export_message_timer = 0

        # Food parameters
        self.start_food = 45
        self.food_speed = 0.0
        self.food_max_age = 1800
        self.food_spawn_chance = 0.0046
        self.max_food = 120

        # Prey1 parameters
        self.start_prey1 = 14
        self.prey1_speed = 2.0
        self.prey1_max_age = 1600
        self.prey1_start_energy = 110
        self.prey1_reproduction_energy = 85
        self.prey1_energy_gain = 20
        self.prey1_energy_loss = 0.10
        self.prey1_reproduction_cost = 55

        # Compatibility aliases for older code or SnapshotEngine versions.
        self.start_prey = self.start_prey1
        self.prey_speed = self.prey1_speed
        self.prey_max_age = self.prey1_max_age
        self.prey_start_energy = self.prey1_start_energy
        self.prey_reproduction_energy = self.prey1_reproduction_energy
        self.prey_energy_gain = self.prey1_energy_gain
        self.prey_energy_loss = self.prey1_energy_loss
        self.prey_reproduction_cost = self.prey1_reproduction_cost

        # Prey2 parameters
        self.start_prey2 = 10
        self.prey2_speed = 4.8
        self.prey2_max_age = 1100
        self.prey2_start_energy = 95
        self.prey2_reproduction_energy = 110
        self.prey2_energy_gain = 18
        self.prey2_energy_loss = 0.18
        self.prey2_reproduction_cost = 60

        # Predator parameters
        self.start_predators = 3
        self.predator_speed = 2.6
        self.predator_max_age = 950
        self.predator_start_energy = 240
        self.predator_reproduction_energy = 700
        self.predator_energy_gain = 55
        self.predator_energy_loss = 1.8
        self.predator_reproduction_cost = 500

        self.max_history = 340
        self.food_history = deque(maxlen=self.max_history)
        self.prey1_history = deque(maxlen=self.max_history)
        self.prey2_history = deque(maxlen=self.max_history)
        self.pred_history = deque(maxlen=self.max_history)

        self.full_data = []

        # classes voor SnapshotEngine
        self.food_class = Food
        self.prey1_class = Prey1
        self.prey_class = Prey1  # compatibility alias
        self.prey2_class = Prey2
        self.predator_class = Predator

        self.snapshot_engine = SnapshotEngine(base / "simulation.db")

        self.prey1Population = []
        self.preyPopulation = self.prey1Population  # compatibility alias
        self.prey2Population = []
        self.predatorPopulation = []
        self.foodPopulation = []

        self.csv_file = None
        self.csv_writer = None
        self.csv_path = None
        self.timestep_counter = 0

        self.assets = AssetManager()
        self.logger = DataLogger(export_dir)
        self.factory = EntityFactory(self)
        self.engine = SimulationEngine(self)
        self.ui = UIController(self)
        self.graph = GraphRenderer(self)

        self.prey1Image = None
        self.preyImage = None  # compatibility alias
        self.prey2Image = None
        self.predImage = None
        self.foodImage = None
        self.backgroundImage = None

    def sync_prey1_aliases(self):
        # Keep older SnapshotEngine versions working if they use preyPopulation.
        self.preyPopulation = self.prey1Population
        self.preyImage = self.prey1Image

        self.start_prey = self.start_prey1
        self.prey_speed = self.prey1_speed
        self.prey_max_age = self.prey1_max_age
        self.prey_start_energy = self.prey1_start_energy
        self.prey_reproduction_energy = self.prey1_reproduction_energy
        self.prey_energy_gain = self.prey1_energy_gain
        self.prey_energy_loss = self.prey1_energy_loss
        self.prey_reproduction_cost = self.prey1_reproduction_cost

    def load_assets(self):
        self.prey1Image = self.assets.load_image("prey1", prey1, size=(32, 32))
        self.preyImage = self.prey1Image  # compatibility alias
        self.prey2Image = self.assets.load_image("prey2", prey2, size=(40, 40))
        self.predImage = self.assets.load_image("pred", pred1, size=(48, 48))
        self.foodImage = self.assets.load_image("food", food1, size=(24, 24))

        bg = pygame.image.load(background)
        bg = bg.convert()
        bg = pygame.transform.smoothscale(bg, (self.sim_rect.width, self.sim_rect.height))
        self.backgroundImage = bg

        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.assets.load_sound("eat", eatSound1)

    def resetSimulation(self):
        self.sync_prey1_aliases()
        self.prey1Population = [Prey1(self.prey1Image, self) for _ in range(int(self.start_prey1))]
        self.preyPopulation = self.prey1Population
        self.prey2Population = [Prey2(self.prey2Image, self) for _ in range(int(self.start_prey2))]
        self.predatorPopulation = [Predator(self.predImage, self) for _ in range(int(self.start_predators))]
        self.foodPopulation = [Food(self.foodImage, self) for _ in range(int(self.start_food))]

        self.food_history.clear()
        self.prey1_history.clear()
        self.prey2_history.clear()
        self.pred_history.clear()

        for _ in range(30):
            self.food_history.append(len(self.foodPopulation))
            self.prey1_history.append(len(self.prey1Population))
            self.prey2_history.append(len(self.prey2Population))
            self.pred_history.append(len(self.predatorPopulation))

        self.timestep_counter = 0
        self.logger.timestep_counter = 0

    def close_csv(self):
        self.logger.close_csv()

    def open_new_csv_run(self):
        self.logger.start_new_run()

    def export_csv_now(self):
        return self.logger.export_snapshot()

    def timestep(self):
        if self.paused:
            return
        self.sync_prey1_aliases()
        self.engine.update()
        self.sync_prey1_aliases()

    def draw(self):
        self.surface.blit(self.backgroundImage, self.sim_rect)

        for food in self.foodPopulation:
            food.draw()
        for prey1_obj in self.prey1Population:
            prey1_obj.draw()
        for prey2_obj in self.prey2Population:
            prey2_obj.draw()
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

    sim.surface = pygame.display.set_mode((sim.width, sim.height))
    pygame.display.set_caption("Survival Simulation")

    sim.clock = pygame.time.Clock()
    sim.debugFont = pygame.font.SysFont("Consolas", 16)
    sim.uiFont = pygame.font.SysFont("Segoe UI", 22)
    sim.smallFont = pygame.font.SysFont("Segoe UI", 18)
    sim.tinyFont = pygame.font.SysFont("Segoe UI", 14)

    sim.load_assets()
    sim.ui.setup_ui()
    sim.resetSimulation()

    running = True
    while running:
        sim.clock.tick(int(60 * sim.sim_speed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sim.logger.close_csv()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if sim.ui.slider_rect.collidepoint(pos):
                    sim.ui.slider_active = True
                    sim.ui.update_speed_slider_from_mouse(pos[0])

                if sim.ui.time_slider_rect.collidepoint(pos):
                    sim.ui.time_slider_active = True
                    sim.ui.update_time_slider_from_mouse(pos[0])

                for i, field in enumerate(sim.ui.param_fields):
                    if field["rect"].collidepoint(pos):
                        sim.ui.active_field = i
                        sim.ui.input_text = ""
                        break

                for btn in sim.ui.buttons:
                    if btn["rect"].collidepoint(pos):
                        sim.ui.handle_button(btn["action"])

            elif event.type == pygame.MOUSEBUTTONUP:
                sim.ui.slider_active = False
                sim.ui.time_slider_active = False

            elif event.type == pygame.MOUSEMOTION:
                mx = pygame.mouse.get_pos()[0]

                if sim.ui.slider_active:
                    sim.ui.update_speed_slider_from_mouse(mx)

                if sim.ui.time_slider_active:
                    sim.ui.update_time_slider_from_mouse(mx)

            elif event.type == pygame.KEYDOWN:
                sim.ui.handle_text_input(event)

        sim.timestep()
        sim.draw()
        pygame.display.flip()

    sim.snapshot_engine.close()
    pygame.quit()


if __name__ == "__main__":
    main()
