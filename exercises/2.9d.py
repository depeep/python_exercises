import math
x= float(input('please enter x: '))
m= float(input('please enter m: '))
s =float(input('please enter s: '))

z= round(((x-m)/s)**2, 2)
print ( "Z is", z)

P = round(1 / (s * math.sqrt(2 * math.pi)) * math.exp(-z), 6)
print ( "P(", x, ") is", P)

#hij verwachtte overigens P = (1 / (s * math.sqrt(2 * math.pi))) * math.exp(-z/ 2)