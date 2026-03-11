# assignment 2

from robot_world import *

start_conditions = {
    100: (1, {'width': 10, 'height': 7}, {'x': 3, 'y': 4, 'direction': 'DOWN', 'energy': 50})
    }

def create_level(robot, level):
    if 100 <= level < 200: # Walk around the World
        robot.create_level(*start_conditions[100])

    elif 200 <= level < 300:  # Switch Rooms
        robot.create_level(level=2,
            world={'width': 12, 'height': 8}, 
            robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
            wall_gap={'x': 7, 'y': 3}) 

    elif 300 <= level < 400:  # Where is the Tile?
        robot.create_level(level=3,
            world={'width': 12, 'height': 8}, 
            robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
            tile={'x': 5, 'y': 5})

    elif 400 <= level < 500:  # walk around the block
        robot.create_level(level=4,
            world={'width': 12, 'height': 8}, 
            robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
            block={'x': 4, 'y': 3},
            tile={'x': 5, 'y': 5},
            wall_gap={'x': 7, 'y': 3}) 

    elif 500 <= level < 600:  # walk the tile path
        robot.create_level(level=5)  # tile path is always random

    elif 600 <= level < 700:  # push the block over the tile
        robot.create_level(level=6,
            world={'width': 12, 'height': 8}, 
            robot={'x': 2, 'y': 2, 'direction': 'UP', 'energy': 101},
            block={'x': 4, 'y': 3},
            tile={'x': 5, 'y': 5})
