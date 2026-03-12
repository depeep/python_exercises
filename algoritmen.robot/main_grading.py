# 0HV120 2022 assignment 2
# menu to test your solutions from 'assignment2.py' 

STEP_TIME = 250  # in ms

from robot_world import *
from create_level_grading import create_level, start_conditions

############# IMPORT OF THE SUBMITTED SOLUTION ############
from assignment2_solution import show_duo_names, script_1, script_2, script_3, script_4, script_5, script_6
############# IMPORT OF THE SUBMITTED SOLUTION ############

def show_menu():
    print()
    print("options:")
    print("  (1xx) walk around the room")
    print("  (2xx) switch rooms")
    print("  (3xx) where is the tile?")
    print("  (4xx) around the block")
    print("  (5xx) walk the tile path")
    print("  (6xx) move the block on top of the tile")
    print("  (q) quit")

def parse_answer(option):
    try:
        if '-' in option:  # range of levels
            nrs = option.split('-')
            min_lvl = int(nrs[0])
            max_lvl = int(nrs[1])
        else:
            min_lvl = max_lvl = int(option)            
        if 100 <= min_lvl < 700 and 100 <= max_lvl < 700:
            return min_lvl, max_lvl
        else:
            print("levels are outside range of 100 - 699")
            return None, None
    except:
        return None, None

def test_level(robot, lvl):
    create_level(robot, lvl)
    if 100 <= lvl < 200:
        script_1(robot)
    elif 200 <= lvl < 300:
        script_2(robot)
    elif 300 <= lvl < 400:
        script_3(robot)
    elif 400 <= lvl < 500:
        script_4(robot)
    elif 500 <= lvl < 600:
        script_5(robot)
    elif 600 <= lvl < 700:
        script_6(robot)
    robot.stop_level()

def main():
    pygame.init()
    robot = RobotWorld(cell_size = 40, step_time_in_ms = STEP_TIME)

    show_duo_names()
    print("\n***** GRADING VERSION *****\n")
    show_menu()
    
    option = input("your choice: ")
    while option != 'q':
        if option == 'q':
            print("thank you for playing")
        else:
            min_lvl, max_lvl = parse_answer(option)
            print(min_lvl, max_lvl)
            if min_lvl is not None:
                levels_to_run = [lvl for lvl in \
                    start_conditions if min_lvl <= lvl <= max_lvl]
                for lvl in levels_to_run:
                    test_level(robot, lvl)
            else:
                print("i did not recognise option '" + option + "'.")
        show_menu()
        option = input("option: ")

    # 'q' pressed: exit program
    pygame.quit()

main()
