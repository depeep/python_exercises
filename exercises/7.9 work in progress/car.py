class Car:
    def __init__(self, model, color):
        self.__model = str(model)
        self.__color = str(color)

    def get_model(self):
        return self.__model
    
    def get_color(self):
        return self.__color
    