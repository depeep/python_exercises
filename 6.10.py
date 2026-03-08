import turtle
import math


turtle.shape('turtle')
turtle.speed(10)

def bepaalHoek(x1,y1,x2,y2):
    aangrenzend = x2 -x1
    overliggend = y2 - y1
    tangens = overliggend / aangrenzend
    hoekrad = math.atan(tangens)
    hoekDeg = hoekrad / math.pi * 360
    print (hoekrad)
    print (hoekDeg)




def drawLineFout(x1, y1, x2, y2):
    turtle.setposition(x1, y1)
    turtle.goto(x2, y2)

def drawLineFout(x1, y1, x2, y2):
    turtle.setposition(x1, y1)

t=turtle.Turtle()


x1 = float(input('Enter starting point X coordinate: '))
y1 = float(input('Enter starting point Y-coordinate: '))
x2 = float(input('Enter target X-coordinate: '))
y2 = float(input('Enter target Y-coordinate: '))

# drawLineFout(x1, y1, x2, y2)

bepaalHoek (x1, y1, x2, y2)

turtle.done()

