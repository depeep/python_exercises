from random import *
from robot import *

class RobotWorld:
    def __init__(self, cell_size, step_time_in_ms):
        self.cell = cell_size
        self.width = 0
        self.height = 0
        self.robot = None
        self.objects = None
        self.game_state = None
        self.level_number = 0
        self.delay = step_time_in_ms
        self.screen = None

    def create_level(self, level, world=None, robot=None, block=None, tile=None, wall_gap=None):
        if level not in [0, 1, 2, 3, 4, 5, 6]:
            print('create_level called with invalid level', level)
            return

        self.game_state = 'PLAYING'
        self.level_number = level
        # every world has at least a width, height and one robot
        if world is not None:
            self.width = world['width'] + 2
            self.height = world['height'] + 2
        if robot is not None:
            self.robot = Robot(robot['x'], self.height-robot['y']-1, robot['direction'], energy=robot['energy'], cargo = None)
        self.objects = []
        if level == 0:
            if world is None:
                self.width = randint(10, 15)
                self.height = randint(10, 15)
            if robot is None:
                self.robot = Robot(self.width // 2 - 1, self.height // 2, 'UP', cargo = None, energy=100)
            if block is not None:
                self.objects.append(Block(block['x'], self.height-block['y']-1, BLUE))
            if tile is not None:
                self.objects.append(Tile(tile['x'], self.height-tile['y']-1, PINK))
            if wall_gap is not None:
                for y in range(1, self.height):
                    if y != wall_gap['y']:
                        self.objects.append(Wall(wall_gap['x'], self.height-y-1))
            if block is None:
                self.objects.append(Block(self.robot.x + 2, self.robot.y, BLUE))
            if tile is None:
                self.objects.append(Tile(self.robot.x, self.robot.y - 2, PINK))

        if level == 1:  # walk around the world
            if world is None:
                self.width = randint(10, 15)
                self.height = randint(8, 12)
            if robot is None:
                self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            if block is not None:
                print("> level 1 does not have blocks, parameter 'block' is ignored")
            if tile is not None:
                print("> level 1 does not have tiles, parameter 'tile' is ignored")
            if wall_gap is not None:
                print("> level 1 does not have a wall gap, parameter 'wall_gap' is ignored")

        elif level == 2:  # switch rooms
            if world is None:
                self.width = randint(12, 15)
                self.height = randint(8, 12)
            if block is not None:
                print("> level 2 does not have blocks, parameter 'block' is ignored")
            if tile is not None:
                print("> level 2 does not have tiles, parameter 'tile' is ignored")
            if wall_gap is None:
                x_inner_wall = randint(4, self.width - 3)
                y_inner_wall_gap = randint(2, self.height-1)
                for y in range(1, self.height):
                    if y != y_inner_wall_gap:
                        self.objects.append(Wall(x_inner_wall, y))
                x_robot = x_inner_wall
                y_robot = randint(2, self.height - 2)
                while x_robot == x_inner_wall:
                    x_robot = randint(2, self.width - 2)
            else:
                for y in range(1, self.height):
                    if y != wall_gap['y']:
                        self.objects.append(Wall(wall_gap['x'], self.height-y-1))
            if robot is None:
                self.add_robot(x_robot, y_robot, direction='RANDOM', energy=100)

        elif level == 3:  # where is the tile?
            if world is None:
                self.width = randint(12, 15)
                self.height = randint(8, 12)
            if robot is None:
                self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            if block is not None:
                print("> level 3 does not have blocks, parameter 'block' is ignored")
            if tile is None:
                self.add_random_tiles(nr_of_tiles=1, color=RED)
            else:
                self.objects.append(Tile(tile['x'], self.height-tile['y']-1, PINK))
            if wall_gap is not None:
                print("> level 3 does not have a wall gap, parameter 'wall_gap' is ignored")

        elif level == 4:
            if world is None:
                self.width = randint(12, 15)
                self.height = randint(8, 12)
            if robot is None:
                self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            if block is None:
                x_blue, y_blue = self.robot.x, self.robot.y
                while self.robot.x - 1 <= x_blue <= self.robot.x + 1 or self.robot.y - 1 <= y_blue <= self.robot.y + 1:
                    x_blue, y_blue = randint(3, self.width - 3), randint(3, self.height - 3)
                self.objects.append(Block(x_blue, y_blue, BLUE))
            else:
                self.objects.append(Block(block['x'], self.height-block['y']-1, BLUE))
            if tile is not None:
                print("> level 4 does not have blocks, parameter 'block' is ignored")
            if wall_gap is not None:
                print("> level 4 does not have a wall gap, parameter 'wall_gap' is ignored")

        elif level == 5:
            if world is not None:
                print("> level 5 ignores parameter 'world'")
            if robot is not None:
                print("> level 5 ignores parameter 'robot'")
            if block is not None:
                print("> level 5 ignores parameter 'block'")
            if tile is not None:
                print("> level 5 ignores parameter 'tile'")
            if wall_gap is not None:
                print("> level 5 ignores parameter 'wall_gap'")
            # create world with random path of yellow tiles from left to right
            self.energy = 99
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            x = 1
            y = randint(2, self.height - 2)
            self.add_robot(x, y, direction='RANDOM', energy=100)
            self.objects.append(Tile(x, y, YELLOW))
            old_direction = 'RIGHT'
            while x < self.width - 2:
                # chose new direction
                if y == self.height - 2: # near bottom side
                    if old_direction == 'DOWN':
                        direction = 'RIGHT'
                    else:
                        direction = choice(['UP', 'RIGHT'])
                elif y == 1: # near top side
                    if old_direction == 'UP':
                        direction = 'RIGHT'
                    else:
                        direction = choice(['DOWN', 'RIGHT'])
                elif old_direction == 'DOWN':
                    direction = choice(['RIGHT', 'DOWN'])
                elif old_direction == 'UP':
                    direction = choice(['RIGHT', 'UP'])
                else:
                    direction = choice(['RIGHT', 'DOWN', 'UP'])

                # add 1 or 2 tiles depending on direction
                if direction == 'UP':
                    y = y - 1
                    self.objects.append(Tile(x, y, YELLOW))
                elif direction == 'DOWN':
                    y = y + 1
                    self.objects.append(Tile(x, y, YELLOW))
                else: # direction == 'RIGHT'
                    x = x + 1
                    self.objects.append(Tile(x, y, YELLOW))
                    x = x + 1
                    if x < self.width - 1:
                        self.objects.append(Tile(x, y, YELLOW))

                old_direction = direction

        elif level == 6:  # push the block over the tile
            if world is None:
                self.width = randint(10, 15)
                self.height = randint(10, 15)
            if robot is None:
                self.add_robot(x=0, y=0, direction='RANDOM', energy=1000)
            if block is not None:
                self.objects.append(Block(block['x'], self.height-block['y']-1, PINK))
            else:
                x_block, y_block = self.robot.x, self.robot.y
                while x_block == self.robot.x and y_block == self.robot.y:
                    x_block, y_block = randint(3, self.width - 3), randint(3, self.height - 3)
                self.objects.append(Block(x_block, y_block, PINK))
            if tile is not None:
                self.objects.append(Tile(tile['x'], self.height-tile['y']-1, PINK))
            else:
                x_tile, y_tile = self.robot.x, self.robot.y
                while (x_tile == self.robot.x and y_tile == self.robot.y)\
                        or (x_tile == x_block and y_tile == y_block):
                    x_tile, y_tile = randint(3, self.width - 3), randint(3, self.height - 3)
                self.objects.append(Tile(x_tile, y_tile, PINK))
            if wall_gap is not None:
                print("> level 6 ignores parameter 'wall_gap'")


        self.add_outer_walls()
        self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
        self.draw()
        print("\nClick on game window and press key to start script", self.level_number)
        print("Close window or press <ESC> to cancel\n")
        start_script = self.wait_until_start_or_cancel()
        return start_script

    def set_step_time(self, step_time_in_ms):
        if 25 <= step_time_in_ms <= 1000:
            self.delay = step_time_in_ms
        else:
            print("Step time must be between 25 and 1000 ms")

    def turn_right(self):
        self.robot.turn_right()
        self.calculate_new_game_state()
        self.draw()

    def turn_left(self):
        self.robot.turn_left()
        self.calculate_new_game_state()
        self.draw()

    def step_forward(self):
        self.robot.step_forward(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def step_back(self):
        self.robot.step_back(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def grab_release_block(self):
        self.robot.grab_release_block(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def scan_steps_ahead(self):
        # return the nr of step_forward actions the robot can do before encountering a Wall, Block or Tile
        return self.robot.steps_ahead(self.objects)

    def scan_object_ahead(self):
        # returns the first object the robot would encounter with repeated step_forward: Wall, Block or Tile
        return self.robot.object_ahead(self.objects)

    def scan_direction(self):
        # returns the current direction of the robot
        return self.robot.direction

    def scan_energy(self):
        # return the remaining energy of the robot
        return self.robot.energy

    def all_tiles_covered(self):
        # are all tiles covered by a block of the same color?
        # split into lists tiles and blocks to check
        tiles  = []
        blocks = []
        for obj in self.objects:
            if isinstance(obj, Tile):
                tiles.append(obj)
            elif isinstance(obj, Block):
                blocks.append(obj)

        if tiles == [] or blocks == []:
            return False

        for tile in tiles:
            covered = False
            for block in blocks:
                if tile.x == block.x and tile.y == block.y and tile.color == block.color:
                    covered = True
            if not covered:
                return False
        return True

    def calculate_new_game_state(self):
        # game state can only change from 'RUNNING' to 'FAILED' or 'COMPLETED'
        if self.game_state != 'PLAYING':
            return
        # energy ran out ?
        if self.robot.energy == 0:
            self.game_state = 'FAILED'
        # all tiles covered by same colored blocks?
        elif self.all_tiles_covered():
            self.game_state = 'COMPLETED'

    def object_at(self, x, y):
        for obj in self.objects:
            if obj.at_location(x, y):
                return obj
        return None

    def show_text(self, txt, x, y , color):
        my_font = pygame.font.SysFont("monospace", 20)
        lbl = my_font.render(txt, 1, color)
        self.screen.blit(lbl, (int(x * self.cell), int(y * self.cell)))

    def user_info(self):
        txt = " Lvl: " + str(self.level_number)
        self.show_text(txt, 2, 1.25, WHITE)

        txt = " Energy: "
        self.show_text(txt, 4.5, 1.25, WHITE)
        
        txt = str(self.robot.energy).rjust(3)
        if self.robot.energy > 0:
            self.show_text(txt, 7, 1.25, GREEN)
        else:
            self.show_text(txt, 7, 1.25, RED)
        
        txt = " Crashed: "
        self.show_text(txt, 8, 1.25, WHITE)
        if self.robot.crashed:
            self.show_text('YES', 11, 1.25, RED)
        else:
            self.show_text('no', 11, 1.25, GREEN)
        
        for x_value in range(self.width - 2):
            x_label = str(x_value + 1)
            self.show_text(x_label, x_value + 2.25, self.height + 0.25, WHITE)
        self.show_text('x', x_value + 3.25, self.height + 0.25, WHITE)

        for y_value in range(self.height - 2):
            y_label = str(y_value + 1)
            y_pos = self.height - y_value - 1.75
            self.show_text(y_label, 1.25, self.height - y_value - 0.75, WHITE)
        self.show_text('y', 1.25, self.height - y_value - 1.75, WHITE)

    def draw(self):
        self.screen.fill(BLACK)

        for obj in self.objects:
            obj.draw(self.screen, self.cell)

        # draw grid
        for w in range(self.width + 1):
            start = [self.cell * (w + 1) , self.cell]
            end   = [self.cell * (w + 1),  self.cell * (self.height + 1)]
            pygame.draw.line(self.screen, GREY, start, end, 1)
        for h in range(self.height + 1):
            start = [self.cell, self.cell * (h + 1)]
            end   = [self.cell * (self.width + 1), self.cell * (h + 1)]
            pygame.draw.line(self.screen, GREY, start, end, 1)

        self.robot.draw(self.screen, self.cell)
        self.user_info()

        pygame.display.flip()
        events = pygame.event.get() # hack to avoid 'application does not respond' in windows
        pygame.time.delay(self.delay)

    def add_outer_walls(self):
        for w in range(self.width):
            self.objects.append(Wall(w, 0))
            self.objects.append(Wall(w, self.height - 1))
        for h in range(1, self.height - 1):
            self.objects.append(Wall(0, h))
            self.objects.append(Wall(self.width - 1, h))

    def add_random_blocks(self, nr_of_blocks, color):
        desired_nr_objects = len(self.objects) + nr_of_blocks
        while len(self.objects) < desired_nr_objects:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if self.object_at(x, y) == None:
                self.objects.append(Block(x, y, color))

    def add_random_tiles(self, nr_of_tiles, color):
        desired_nr_objects = len(self.objects) + nr_of_tiles
        while len(self.objects) < desired_nr_objects:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if self.object_at(x, y) == None:
                self.objects.append(Tile(x, y, color))

    def add_robot(self, x, y, direction, energy):
        if x == 0:
            x = randint(1, self.width - 2)
        if y == 0:
            y = randint(1, self.height - 2)
        if direction == 'RANDOM':
            direction = choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.robot = Robot(x, y, direction, energy, cargo = None)

    def wait_until_start_or_cancel(self):
        # return == True means can_start, False means cancelled
        while True: # endless loop because we use returns to exit
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return False # cancelled
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False # cancelled
            elif event.type == pygame.KEYDOWN:
                return True
            else:
                continue  # ignore any other key or mouse event

    def stop_level(self, ran_script=True):
        self.game_state = 'NOT_PLAYING'
        if ran_script:
            print("\nClose game window to finish.", self.level_number)
            result = self.wait_until_start_or_cancel()  # we want to close so result is ignored
        else:
            print("\n*** You cancelled running script", self.level_number, "***")
        pygame.display.quit()

