class Fan:
    def __init__(self):
        self.__speed = 1
        self.__on = False
        self.__radius = 5
        self.__color = "blue"

    def getSpeed(self):
        return self.__speed
    
    def getOn(self):
        return self.__on
    
    def getRadius(self):
        return self.__radius
    
    def getColor(self):
        return self.__color
    
    def setSpeed(self, speed):
        if speed >0:
            self.__speed = speed
    
    def setOn(self, onoff):
        self.__on = onoff # True of False

    def setRadius(self, radius):
        if radius >0:
            self.__radius = radius
        else: 
            print('No negative numbgers allowed')
            print ('Radius stays at', self.__radius)
            print()

    def setColor(self, color):
        self.__color = color
    

def printFan(fan1):
    
    print ('actuele waarden:')
    print ('speed: ', fan1.getSpeed())
    print ('on: ', fan1.getOn())
    print ('radius: ', fan1.getRadius())
    print ('color: ', fan1.getColor() )
    print()

  

def main():
    fan1 = Fan()
    printFan(fan1)
    print()
    fan1.setSpeed(3)
    fan1.setOn(True)
    fan1.setColor('red')
    fan1.setRadius(20)
    printFan(fan1)
    fan1.setRadius(-2) 
    printFan(fan1)
    # print(fan1.speed) geeft een erro, zoals de bedoeling was










if __name__=="__main__":
    main()