class Person:
    def __init__(self, name, age, weight, height):
        self.__name = name
        self.__age = age
        self.__weight = weight
        self.__height = height

    def getBMI(self):
        bmi = self.__weight / (self.__height * self.__height)
        return bmi

    def getStatus(self):
        bmi = self.getBMI()
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def getName(self):
        return self.__name

    def getAge(self):
        return self.__age

    def getWeight(self):
        return self.__weight

    def getHeight(self):
        return self.__height

def main():
    # Your code:

    # create person with fields "John", 20, 75 and 1.70
    persoon = Person("John", 20, 75, 1.70)
    Person2= Person("Mary", 19, 60 , 1.68)
    Person3=Person("Bill", 55, 10, 1.80)
    # print persons properties and BMI status
    for persoon in [persoon, Person2, Person3]:
        name =persoon.getName()
        age = persoon.getAge()
        weight = persoon.getWeight()
        height = persoon.getHeight()
        bmi = persoon.getBMI()
        status = persoon.getStatus()

        print ("name: ", name,"\nAge: ", age, "\nWeight: ", weight, "\nHeigt: ", height,"\nBMI: ", bmi)
        print (name, 'is', status)
        print()
    # create person with fields "Mary", 19, 60 and 1.68
    # print persons properties and BMI status

    # create person with fields "Bill", 55, 100 and 1.80
    # print persons properties and BMI status

main()