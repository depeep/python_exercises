# assignment 2

from asyncio import create_subprocess_shell
from robot_world import *

def show_duo_names():
    print()
    print('┌─────────────────────┬───────────────────────┐')
    print('│ 0HV120 assignment 2 │ Robot World           │')
    print('├─────────────────────┼───────────────────────┤')
    print('│ duo partner 1       │ name 1                │')
    print('├─────────────────────┼───────────────────────┤')
    print('│ duo partner 2       │ name 2                │')
    print('└─────────────────────┴───────────────────────┘')


def script_0_demo(robot):
    # demo script to show the capabilities of the robot
    # read the assignment instructions for details
        
    # demo of scans
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of stepping and turning
    for _ in range(3):
        robot.step_forward()
    robot.turn_left()
    robot.turn_right()
    robot.turn_right()
    for _ in range(4):
        robot.step_forward()
    for _ in range(4):
        robot.step_back()
    robot.turn_left()
    robot.step_back()
    robot.step_back()
    robot.turn_right()

    # demo of scans
    print()
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of grabbing, pushing forward, dragging backward and releasing of a block
    robot.step_forward() # when the robot faces and touches the block it can grab it
    robot.grab_release_block()

    # moving the block
    for _ in range(5):
        robot.step_forward()
    for _ in range(3):
        robot.step_back()

    robot.grab_release_block()  # releasing the block

    robot.step_back()
    robot.turn_right()
    robot.turn_right()
    robot.turn_right()
    for _ in range(3): # finally, crash robot into the wall
        robot.step_back()

    return # end of demo

################################################
#   helper functions defined by you can go here:
#   start of helper function part



#   end of helper function part
################################################

def script_1(robot):   # Walk around the World
    # your solution here:

    return # end of script_1


def script_2(robot):  # Switch Rooms
    # your solution here:

    return # end of script_2


def script_3(robot): # Where is the Tile
    # your solution here:

    return # end of script_3


def script_4(robot):  # Walk around the Block
    # your solution here:

    return # end of script_4


def script_5(robot):  # Follow the Tile Path
    # your solution here:

    return # end of script_5


def script_6(robot):  # Push the Block over the Tile
    # your solution here:

    return # end of script_6
