import math
a = float(input('please enter a: '))
b = float(input('please enter b: '))
c = float(input('please enter c: '))
d = (b ** 2) - (4 * a * c)

print ( "the discriminant is", d)
x1 = (-b + math.sqrt(d)) / (2 * a)
x2 = (-b - math.sqrt(d)) / (2 * a) 

print('solution: 1')
print ( "x1 is", x1) 
print ( "x2 is", x2)

# geeft nog fouten als de discrtiminant negatief is. (wortel van negatief getal)