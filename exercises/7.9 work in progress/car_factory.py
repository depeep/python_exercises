from random import choice
from car import Car

class CarFactory:

    def __init__(self):
        inventory = []
        self.__inventory = inventory
        
# import random
    def produce_cars(self, nr_to_produce):
        available_models =['Ford', 'Maseratti', 'Renault', 'Tesla', 'Volkswagen', 'Volvo']
        available_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        list = []
        # print ('The following cars were produced')
        for i in range (nr_to_produce):
            model = choice(available_models)
            color = choice(available_colors)
            carToAdd = Car(model, color)
            self.__inventory.append(carToAdd)
            list.append(carToAdd)
        return list
        
    def find_cars(self,model, color):  
        list =[]
        for car in self.__inventory:
            if car.get_model()== model or model =='':
                if car.get_color() == color or color == '':
                    list.append(car) 
        return list            

    def ship_one_car(self, model, color):
        shippedCar = None
        for car in self.__inventory:
            if car.get_model()== model and car.get_color() == color:
                shippedCar = car
                continue
        if shippedCar != None:
            self.__inventory.remove(shippedCar)  
        else: 
            print ("no such car in inventory") 
                
        
                


# def test():
#     produce_cars(3)

# test()

        # print("The following cars were produced:")
        # for n, car in enumerate(cars_produced):
        #     print(n+1, description_of(car))