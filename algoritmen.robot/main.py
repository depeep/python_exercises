# 0HV120 2022 assignment 2
# menu to test your solutions from 'assignment2.py' 

STEP_TIME = 250  # in ms

from robot_world import *
from create_level import create_level
from assignment2 import show_duo_names, script_0_demo, script_1, script_2, script_3, script_4, script_5, script_6

def show_menu():
    print()
    print("options:")
    print("  (0) demo script")
    print("  (1) walk around the room")
    print("  (2) switch rooms")
    print("  (3) where is the tile?")
    print("  (4) around the block")
    print("  (5) walk the tile path")
    print("  (6) move the block on top of the tile")
    print("  (q) quit")

def main():
    pygame.init()
    robot = RobotWorld(cell_size = 40, step_time_in_ms = STEP_TIME)

    show_duo_names()
    show_menu()
    option = input("your choice: ")
    while option != 'q':
        if option.isdigit():
            level = int(option)
            if level == 0:
                create_level(robot, 0)
                script_0_demo(robot)
            elif level == 1:
                create_level(robot, 1)
                script_1(robot)
            elif level == 2:
                create_level(robot, 2)
                script_2(robot)
            elif level == 3:
                create_level(robot, 3)
                script_3(robot)
            elif level == 4:
                create_level(robot, 4)
                script_4(robot)
            elif level == 5:
                create_level(robot, 5)
                script_5(robot)
            elif level == 6:
                create_level(robot, 6)
                script_6(robot)
            robot.stop_level()  # closure of game window
        elif option == 'q':
            print("thank you for playing")
        else:
            print("i did not recognise option '" + option + "'.")
            show_menu()
        show_menu()
        option = input("option: ")

    # 'q' pressed: exit program
    pygame.quit()

main()
