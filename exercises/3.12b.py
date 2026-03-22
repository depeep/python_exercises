import math
a = float(input('please enter a: '))
b = float(input('please enter b: '))
c = float(input('please enter c: '))
d = (b ** 2) - (4 * a * c)

if d < 0:
    print ( "the discriminant is", d)
    print ( "there are no real solutions")
elif d == 0:
    print ( "the discriminant is", d)
    x = -b / (2 * a)
    print('solution: 1')
    print ( "x is", x)
else:
    print ( "the discriminant is", d)
    x1 = (-b + math.sqrt(d)) / (2 * a)
    x2 = (-b - math.sqrt(d)) / (2 * a) 

    print('solution: 1')
    print ( "x1 is", x1) 
    print ( "x2 is", x2)

# geeft foutmelding  als de discriminant negatief is. (wortel van negatief getal)\
# geeft 1 oplossing als de discriminant 0 is. (wortel van 0 is 0)
