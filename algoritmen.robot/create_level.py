# assignment 2

from robot_world import *

def create_level(robot, level):

    RANDOM_START = False  # change to True for random positions

    if level == 0:  # Demo
        if RANDOM_START:
            robot.create_level(level=0)
        else:
            robot.create_level(level=0,
                world={'width': 12, 'height': 8}, 
                robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
                block={'x': 4, 'y': 3},
                tile={'x': 5, 'y': 5},
                wall_gap={'x': 7, 'y': 3}) 

    elif level == 1: # Walk around the World
        if RANDOM_START:
            robot.create_level(level=1)
        else:
            robot.create_level(level=1,
                world={'width': 10, 'height': 7}, 
                robot={'x': 3, 'y': 4, 'direction': 'DOWN', 'energy': 50})

    elif level == 2:  # Switch Rooms
        if RANDOM_START:
            robot.create_level(level=2)
        else:
            robot.create_level(level=2,
                world={'width': 12, 'height': 8}, 
                robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
                wall_gap={'x': 7, 'y': 3}) 

    elif level == 3:  # Where is the Tile?
        if RANDOM_START:
            robot.create_level(level=3)
        else:
            robot.create_level(level=3,
                world={'width': 12, 'height': 8}, 
                robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
                tile={'x': 5, 'y': 5})

    elif level == 4:  # walk around the block
        if RANDOM_START:
            robot.create_level(level=4)
        else:
            robot.create_level(level=4,
                world={'width': 12, 'height': 8}, 
                robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
                block={'x': 4, 'y': 3},
                tile={'x': 5, 'y': 5},
                wall_gap={'x': 7, 'y': 3}) 

    elif level == 5:  # walk the tile path
        robot.create_level(level=5)  # tile path is always random

    elif level == 6:  # push the block over the tile
        if RANDOM_START:
            robot.create_level(level=6)  # for random start
        else:
            robot.create_level(level=6,
                world={'width': 12, 'height': 8}, 
                robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
                block={'x': 4, 'y': 3},
                tile={'x': 5, 'y': 5})
