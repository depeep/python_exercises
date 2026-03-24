"""Write the code for a class Allergy with private variables __name and __foods_to_avoid,
 and the following methods:
__init__(self, name, foods), with name the name of the allergy and foods a list of names of foods that should be avoided by a person with that allergy
add_food(self, food), adds food to the list of foods to avoid (if the food is not in the list yet)
remove_food(self, food), removes food from the list of foods to avoid. If food is not in the list, then nothing should happen.
get_foods(self), returns a list of all foods to avoid.
Make sure your code does not crash if parameter values are invalid. 
In that case the code should simply do nothing."""

class Allergy:

    def __init__(self, name, foods):
        self.__name = name
        self.__foods = foods

    def getName(self):
        return self.__name

    def addFood(self, food):
        if food not in self.__foods:
            self.__foods.append(food)

    def removeFood(self, food):
        if food in self.__foods:
            self.__foods.remove(food)

    def getFoods(self):
        return self.__foods
# def test():
#     1
#     myAllergy = Allergy("leerstofallergie",["boeken", "schriften"])
#     print()
#     print (myAllergy.getName())
#     print (myAllergy.getFoods())
#     myAllergy.addFood("penneworst")
#     print (myAllergy.getFoods())
#     myAllergy.removeFood("boeken")
#     print (myAllergy.getFoods())

# test()

