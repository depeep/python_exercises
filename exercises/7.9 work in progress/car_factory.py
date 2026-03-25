from random import choice
from car import Car

class CarFactory:

    def __init__(self):
        inventory = []
        self.__inventory = inventory
        
# import random
    def produce_cars(nr_to_produce):
        available_models =['Ford', 'Maseratti', 'Renault', 'Tesla', 'Volkswagen', 'Volvo']
        available_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        # print ('The following cars were produced')
        for i in range (nr_to_produce):
            model = choice(available_models)
            color = choice(available_colors)
            carToAdd = Car(model, color)
            return carToAdd
        





# def test():
#     produce_cars(3)

# test()

        # print("The following cars were produced:")
        # for n, car in enumerate(cars_produced):
        #     print(n+1, description_of(car))