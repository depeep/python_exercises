class Habitat:
    def __init__(self, preys, predators, foods):
      self.__preys = preys
      self.__predators = predators
      self.__foods = foods
 
    def time_step(self):
      self.time_steps()
      self.dying()
      self.feeding()
 
 
    def time_steps(self):
      for food in self.__foods:
         food.time_step()
 
      for prey in self.__preys:
         prey.time_step()
 
      for predator in self.__predators:
         predator.time_step()
 
    def dying(self):
        print ('TODO: dying')
        # for food in self.__foods:
        #      if not food.is_alive():
        #         self.__foods.remove(food)
     
        # for prey in self.__preys:
        #      if not prey.is_alive():
        #         self.__preys.remove(prey)
     
        # for predator in self.__predators:
        #      if not predator.is_alive():
        #         self.__predators.remove(predator)
 
 
    def feeding(self):
        print ('TODO: feeding')
        # for prey in self.__preys:
        #      for food in self.__foods:
        #         if prey.can_eat(food):
        #          prey.eat(food)
        #          self.__foods.remove(food)
        #          break
     
        # for predator in self.__predators:
        #      for prey in self.__preys:
        #         if predator.can_eat(prey):
        #          predator.eat(prey)
        #          self.__preys.remove(prey)
        #          break


class Prey:
    def __init__(self, x, y, image, stamina,speed, age, max_age):
       self.__stamina = stamina
       self.__x = x
       self.__y = y	
       self.__image = Image(image._Image__sprite, image._Image__size) # moet nog een functie voor maken die dit doet, maar dit werkt voorlopig wel
       self.__speed = speed
       self.__age = age
       self.__max_age = max_age
 
    def time_step(self):
       ''' gedrag van de prooi '''
       self.move()
       self.__stamina -= self.__speed
       self.__age += 1
 
    def move(self):
       self.__x = f_x(self.__x, self.__y) # moet misschien zijn zijn f_x(self.__x, self.__y, self.__stamina) maar dat is nog niet geïmplementeerd
       self.__y = f_y(self.__x, self.__y)
       self.__stamina -= self.__speed # bewegen kost energie nog functie voor maken
 
 
    def feed(self):
       self.__stamina += 1
 
 
class Predator:
    def __init__(self, x, y, image, stamina,speed, age, max_age):
       self.__stamina = stamina
       self.__x = x
       self.__y = y
       self.__image = Image(image._Image__sprite, image._Image__size) # moet nog een functie voor maken die dit doet, maar dit werkt voorlopig wel
       self.__age = age
       self.__max_age = max_age
       self.__speed = speed
           
 
    def time_step(self):
       ''' gedrag van de predator '''
       self.move()
       self.__stamina -= self.__speed
       self.__age += 1
 
    def move(self):
       self.__x = f_x(self.__x, self.__y)
       self.__y = f_y(self.__x, self.__y)
 
    def feeding(self):
       self.__stamina += 1
 
 
class Food:
    def __init__(self, x, y, image, stamina, growth_speed):
       self.__x = x
       self.__y = y
       self.__image =Image(image, (10, 10))
       self.__stamina = stamina
       self.__growth_speed = growth_speed
 
    def time_step(self):
       return
 
    def feeding(self):
       self.__stamina += self.__growth_speed
 
 
class Image:
    def __init__(self, sprite, size):
         self.__sprite = sprite
         self.__size = size

#opgevulde placeholders voor functies die nog niet geïmplementeerd zijn, maar wel nodig zijn voor de testcode
def f_x(x, y):
    return x + 1

def f_y(x, y):
    return y + 1  
# Testcode
if __name__ == "__main__":
    food1 = Food(0, 0, Image("assets.food.bmp", (10, 10)), 5, 1)
    prey1 = Prey(10, 10, Image("assets.prey.bmp", (20, 20)), 10, 2, 0, 100)
    predator1 = Predator(20, 20, Image("assets.predator.bmp",(20, 20)), 20, 20, 0, 150)
  

    habitat = Habitat([prey1], [predator1], [food1])
    for _ in range(10):
        habitat.time_step()     
 
