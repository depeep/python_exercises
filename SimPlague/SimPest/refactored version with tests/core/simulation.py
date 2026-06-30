import pygame
from pathlib import Path
from collections import deque

from core.engine import SimulationEngine
from core.factory import EntityFactory
from ui.ui_controller import UIController
from ui.graph import GraphRenderer
from persistence.data_logger import DataLogger
from persistence.snapshot_engine import SnapshotEngine
from infra.asset_manager import AssetManager

from entities.food import Food
from entities.prey1 import Prey1
from entities.prey2 import Prey2
from entities.predator import Predator


class SurvivalSim:
    def __init__(self):
        # ==================================================
        # BASE PATHS
        # ==================================================
        self.base = Path(__file__).parent.parent
        self.assets_dir = self.base / "assets"
        self.export_dir = self.base / "exportdata"
        self.db_path = self.base / "simulation.db"

        # ==================================================
        # LAYOUT
        # ==================================================
        self.width = 1600
        self.height = 1200
        self.panel_width = 390
        self.graph_height = 240

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

        # ==================================================
        # RUNTIME STATE
        # ==================================================
        self.sim_speed = 1.0
        self.paused = True
        self.simulation_started = False

        self.surface = None
        self.clock = None
        self.debugFont = None
        self.uiFont = None
        self.smallFont = None
        self.tinyFont = None

             # ==================================================
        # FOOD PARAMETERS
        # ==================================================
        self.start_food = 45
        self.food_speed = 0.0
        self.food_max_age = 1800
        self.food_spawn_chance = 0.0046
        self.max_food = 120

        # ==================================================
        # PREY1 PARAMETERS
        # ==================================================
        self.start_prey1 = 14
        self.prey1_speed = 2.0
        self.prey1_max_age = 1600
        self.prey1_start_energy = 110
        self.prey1_reproduction_energy = 85
        self.prey1_energy_gain = 20
        self.prey1_energy_loss = 0.10
        self.prey1_reproduction_cost = 55

        # Compatibility aliases voor oude snapshot_engine / oudere code
        self.start_prey = self.start_prey1
        self.prey_speed = self.prey1_speed
        self.prey_max_age = self.prey1_max_age
        self.prey_start_energy = self.prey1_start_energy
        self.prey_reproduction_energy = self.prey1_reproduction_energy
        self.prey_energy_gain = self.prey1_energy_gain
        self.prey_energy_loss = self.prey1_energy_loss
        self.prey_reproduction_cost = self.prey1_reproduction_cost

        # ==================================================
        # PREY2 PARAMETERS
        # ==================================================
        self.start_prey2 = 10
        self.prey2_speed = 4.8
        self.prey2_max_age = 1100
        self.prey2_start_energy = 95
        self.prey2_reproduction_energy = 110
        self.prey2_energy_gain = 18
        self.prey2_energy_loss = 0.18
        self.prey2_reproduction_cost = 60

        # ==================================================
        # PREDATOR PARAMETERS
        # ==================================================
        self.start_predators = 3
        self.predator_speed = 2.6
        self.predator_max_age = 950
        self.predator_start_energy = 240
        self.predator_reproduction_energy = 700
        self.predator_energy_gain = 55
        self.predator_energy_loss = 1.8
        self.predator_reproduction_cost = 500
        
        # ==================================================
        # POPULATIONS
        # ==================================================
        self.prey1Population = []
        self.preyPopulation = self.prey1Population  # compatibility alias
        self.prey2Population = []
        self.predatorPopulation = []
        self.foodPopulation = []

        # ==================================================
        # HISTORY / GRAPH DATA
        # ==================================================
        self.max_history = 340
        self.food_history = deque(maxlen=self.max_history)
        self.prey1_history = deque(maxlen=self.max_history)
        self.prey2_history = deque(maxlen=self.max_history)
        self.pred_history = deque(maxlen=self.max_history)

        # ==================================================
        # CLASS REFERENCES FOR SNAPSHOT ENGINE
        # ==================================================
        self.food_class = Food
        self.prey1_class = Prey1
        self.prey_class = Prey1      # compatibility alias
        self.prey2_class = Prey2
        self.predator_class = Predator

        # ==================================================
        # IMAGES PLACEHOLDERS
        # ==================================================
        self.prey1Image = None
        self.preyImage = None        # compatibility alias
        self.prey2Image = None
        self.predImage = None
        self.foodImage = None
        self.backgroundImage = None

        # ==================================================
        # SYSTEMS / SERVICES
        # ==================================================
        self.assets = AssetManager()
        self.logger = DataLogger(self.export_dir)
        self.snapshot_engine = SnapshotEngine(self.db_path)

        self.engine = SimulationEngine(self)
        self.factory = EntityFactory(self)
        self.graph = GraphRenderer(self)
        self.ui = UIController(self)

    # ==================================================
    # COMPATIBILITY HELPERS
    # ==================================================
    def sync_prey1_aliases(self):
        """
        Houd oude prey-namen gelijk aan nieuwe prey1-namen.
        Nodig zolang snapshot_engine of oude code nog preyPopulation,
        preyImage of prey_* velden verwacht.
        """
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

    # ==================================================
    # ASSET LOADING
    # ==================================================
    def load_assets(self):
        """
        Laadt alle afbeeldingen en geluiden.
        Moet worden aangeroepen nadat display mode is ingesteld.
        """
        self.prey1Image = self.assets.load_image(
            "prey1",
            self.assets_dir / "animated-rabbit.png",
            size=(32, 32)
        )

        self.preyImage = self.prey1Image  # compatibility alias

        self.prey2Image = self.assets.load_image(
            "prey2",
            self.assets_dir / "goat.png",
            size=(40, 40)
        )

        self.predImage = self.assets.load_image(
            "pred",
            self.assets_dir / "wolf.png",
            size=(48, 48)
        )

        self.foodImage = self.assets.load_image(
            "food",
            self.assets_dir / "lettuce.png",
            size=(24, 24)
        )

        bg = pygame.image.load(self.assets_dir / "background.png")
        bg = bg.convert()
        bg = pygame.transform.smoothscale(
            bg,
            (self.sim_rect.width, self.sim_rect.height)
        )
        self.backgroundImage = bg

        try:
            pygame.mixer.init()
        except Exception:
            pass

        self.assets.load_sound(
            "eat",
            self.assets_dir / "eat-carrot.mp3"
        )

        self.sync_prey1_aliases()

    # ==================================================
    # RESET SIMULATION
    # ==================================================
    def resetSimulation(self):
        """
        Zet de simulatie terug naar startpopulaties en reset grafiekdata.
        """
        self.sync_prey1_aliases()

        self.prey1Population = [
            self.prey1_class(self.prey1Image, self)
            for _ in range(int(self.start_prey1))
        ]

        self.preyPopulation = self.prey1Population

        self.prey2Population = [
            self.prey2_class(self.prey2Image, self)
            for _ in range(int(self.start_prey2))
        ]

        self.predatorPopulation = [
            self.predator_class(self.predImage, self)
            for _ in range(int(self.start_predators))
        ]

        self.foodPopulation = [
            self.food_class(self.foodImage, self)
            for _ in range(int(self.start_food))
        ]

        self.food_history.clear()
        self.prey1_history.clear()
        self.prey2_history.clear()
        self.pred_history.clear()

        for _ in range(30):
            self.food_history.append(len(self.foodPopulation))
            self.prey1_history.append(len(self.prey1Population))
            self.prey2_history.append(len(self.prey2Population))
            self.pred_history.append(len(self.predatorPopulation))

        self.logger.timestep_counter = 0
        self.sync_prey1_aliases()

    # ==================================================
    # SIMULATION STEP
    # ==================================================
    def timestep(self):
        if self.paused:
            return

        self.sync_prey1_aliases()
        self.engine.update()
        self.sync_prey1_aliases()

    # ==================================================
    # MAIN LOOP
    # ==================================================
    def run(self):
        pygame.init()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Survival Simulation")

        self.clock = pygame.time.Clock()
        self.debugFont = pygame.font.SysFont("Consolas", 16)
        self.uiFont = pygame.font.SysFont("Segoe UI", 22)
        self.smallFont = pygame.font.SysFont("Segoe UI", 18)
        self.tinyFont = pygame.font.SysFont("Segoe UI", 14)

        self.load_assets()
        self.ui.setup_ui()
        self.resetSimulation()

        running = True

        while running:
            self.clock.tick(max(1, int(60 * self.sim_speed)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.logger.close_csv()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # speed slider
                    if self.ui.slider_rect.collidepoint(pos):
                        self.ui.slider_active = True
                        self.ui.update_speed_slider_from_mouse(pos[0])

                    # time slider
                    if self.ui.time_slider_rect.collidepoint(pos):
                        self.ui.time_slider_active = True
                        self.ui.update_time_slider_from_mouse(pos[0])

                    # parameter fields
                    for i, field in enumerate(self.ui.param_fields):
                        if field["rect"].collidepoint(pos):
                            self.ui.active_field = i
                            self.ui.input_text = ""
                            break

                    # buttons
                    for btn in self.ui.buttons:
                        if btn["rect"].collidepoint(pos):
                            self.ui.handle_button(btn["action"])

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.ui.slider_active = False
                    self.ui.time_slider_active = False

                elif event.type == pygame.MOUSEMOTION:
                    mx = pygame.mouse.get_pos()[0]

                    if self.ui.slider_active:
                        self.ui.update_speed_slider_from_mouse(mx)

                    if self.ui.time_slider_active:
                        self.ui.update_time_slider_from_mouse(mx)

                elif event.type == pygame.KEYDOWN:
                    self.ui.handle_text_input(event)

            self.timestep()
            self.draw()
            pygame.display.flip()

        self.logger.close_csv()
        self.snapshot_engine.close()
        pygame.quit()

    # ==================================================
    # DRAWING
    # ==================================================
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