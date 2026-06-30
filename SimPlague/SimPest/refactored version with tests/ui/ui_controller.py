import pygame
from datetime import datetime
from pathlib import Path

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
            {"label": "Reset", "rect": pygame.Rect(x3, y1, btn_w, btn_h), "action": "reset", "color": (40,40,140)},
            {"label": "Step", "rect": pygame.Rect(x4, y1, btn_w, btn_h), "action": "step", "color": (128,128,30)},

            # Rij 2: spawn prey1, spawn prey2, spawn food, spawn predator
            {"label": "Spawn Rabb", "rect": pygame.Rect(x1, y2, btn_w, btn_h), "action": "spawn_prey1", "color": (70, 90, 120)},
            {"label": "Spawn Goat", "rect": pygame.Rect(x2, y2, btn_w, btn_h), "action": "spawn_prey2", "color": (70, 90, 120)},
            {"label": "Spawn Food", "rect": pygame.Rect(x3, y2, btn_w, btn_h), "action": "spawn_food", "color": (70, 90, 120)},
            {"label": "Spawn Wolf", "rect": pygame.Rect(x4, y2, btn_w, btn_h), "action": "spawn_pred", "color": (70, 90, 120)},

            # Rij 3: export csv, export parameters, clear snapshot, lege ruimte(gelijke breedte als andere knoppen)
            {"label": "Save CSV", "rect": pygame.Rect(x1, y3, btn_w, btn_h), "action": "export_csv", "color": (100,70,140)},
            {"label": "Save Params", "rect": pygame.Rect(x2, y3, btn_w, btn_h), "action": "export_params", "color": (100,70,140)},
            {"label": "Clear Snap", "rect": pygame.Rect(x3, y3, btn_w, btn_h), "action": "clear_snapshots", "color": (100,70,140)},
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
            ("Food number", "start_food", "int"),
            ("Food speed", "food_speed", "float"),
            ("Food max age", "food_max_age", "int"),
            ("Food repro chance", "food_spawn_chance", "float"),
            ("Rabbit number", "start_prey1", "int"),
            ("Rabbit speed", "prey1_speed", "float"),
            ("Rabbit max age", "prey1_max_age", "int"),
            ("Rabbit repro threshold ", "prey1_reproduction_energy", "float"),
            ("Goat number", "start_prey2", "int"),
            ("Goat speed", "prey2_speed", "float"),
            ("Goat max age", "prey2_max_age", "int"),
            ("Goat repro threshold", "prey2_reproduction_energy", "float"),
            ("Wolf number", "start_predators", "int"),
            ("Wolf speed", "predator_speed", "float"),
            ("Wolf max age", "predator_max_age", "int"),
            ("Wolf repro threshold", "predator_reproduction_energy", "float"),
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

        # ✅ gebruik export_dir uit SurvivalSim
        self.game.export_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.game.export_dir / f"parameters-{timestamp}.txt"

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
            ("Rabbits", len(self.game.prey1Population), (90, 180, 255)),
            ("Goats", len(self.game.prey2Population), (255, 210, 90)),
            ("Wolves", len(self.game.predatorPopulation), (255, 90, 90)),
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