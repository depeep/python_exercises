# car factory ui (menu driven program)
# responsibility: input/output from/to the user in order
#                 to use a CarFactory object
from car_factory import CarFactory

def print_menu():
    print()
    print("available commands")
    print("(p)roduce a number of cars")
    print("(f)ind cars of a certain model and/or color in inventory")
    print("(s)hip a car")
    print("(q)uit")

def description_of(car):
    return car.get_color() + " " + car.get_model()

def produce_cars(factory):
    nr_of_cars = int(input("nr of cars to produce: "))
    cars_produced = factory.produce_cars(nr_of_cars)
    print()
    if cars_produced == []:
        print("No cars were produced")
    else:
        print("The following cars were produced:")
        for n, car in enumerate(cars_produced):
            print(n+1, description_of(car))

def find_in_inventory(factory):
    model = input("model (<enter> = all models): ")
    color = input("color (<enter> = all colors): ")
    cars_found = factory.find_cars(model, color)
    print()
    if cars_found == []:
        print("No cars of the right model or color were found in the inventory.")
    else:
        print("The following cars were found in the inventory:")
        for n, car in enumerate(cars_found):
            print(n+1, description_of(car))

def ship_model_color(factory):
    model = input("model to ship: ")
    color = input("color to ship: ")
    shipped_car = factory.ship_one_car(model, color)
    print()
    if shipped_car == None:
        print("No", color, model, "was found in the inventory.")
    else:
        print("A", description_of(shipped_car), "was shipped.")

def main():
    factory = CarFactory()
    print("Welcome to the car factory")

    print_menu()
    command = ""
    while command != 'q':
        print()
        command = input("command: ")
        if "produce".startswith(command):
            produce_cars(factory)
        elif command == 'f':
            find_in_inventory(factory)
        elif command == 's':
            ship_model_color(factory)
        elif command == 'q':
            print("Quitting the program ...")
        else:
            print("I did not recognise command '" + command + "'.")
            print_menu()


if __name__ == "__main__":
    main()

