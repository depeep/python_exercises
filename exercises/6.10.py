import turtle
import math


# turtle.shape('turtle')
# turtle.speed(10)

def writeText(s, x, y):
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    turtle.write(s,move=True, align="left", font=("Arial", 10, "normal"))
    

# opdracht a
def bepaalHoek(x1,y1,x2,y2):
    aangrenzend = x2 -x1
    overliggend = y2 - y1
    tangens = overliggend / aangrenzend
    hoekrad = math.atan(tangens)
    hoekDeg = hoekrad / (2*math.pi)  * 360
    print (hoekrad)
    print (hoekDeg)
    return hoekDeg

def bepaalAfstand(x1, y1, x2, y2): 
    hor = x2 - x1
    vertical = y2 - y1
    diag = math.sqrt( hor**2 + vertical**2)
    print (hor)
    print (vertical)
    print (hor **2)
    print (vertical ** 2)
    print (diag) 
    return diag
 
def drawLineJos(x1, y1, x2, y2): # eigen functie eerst richting en afstand bepalen, dan bewegen
    turtle.penup()
    turtle.setposition(x1, y1)
    turtle.pendown()
    hoek = bepaalHoek(x1,y1, x2, y2)
    afstand =bepaalAfstand(x1, y1, x2, y2)
    turtle.left(hoek)
    turtle.forward(afstand)

def drawLine(x1, y1, x2, y2):  # werkt kennelijk toch... maar leuk geoefend met tan en pythagoras
    turtle.penup()
    turtle.setposition(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)

# opdracht c
def drawPoint(x,y):
    turtle.penup()
    turtle.setposition(x, y)
    turtle.pendown()
    turtle.color("blue", "red")
    turtle.begin_fill()
    turtle.circle(4)
    turtle.end_fill()
    
# opdracht d
def drawCircle(x,y,r):
    turtle.penup()
    turtle.setposition(x, y-r)
    turtle.pendown()
    turtle.circle(r)

# opdracht e
def drawRectangle(x, y, width, height):
    turtle.penup()
    turtle.setposition(x-width/2, y-height/2)
    turtle.pendown()
    for i in range(2):
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
    
    

# t=turtle.Turtle()

def main():
    # opdracht a
    # x1 = float(input('Enter starting point X coordinate: '))
    # y1 = float(input('Enter starting point Y-coordinate: '))
    # x2 = float(input('Enter target X-coordinate: '))
    # y2 = float(input('Enter target Y-coordinate: '))
    # print ( x1, y1, x2, y2)

    # drawLine(x1,y1, x2, y2) #opdracht a
    # drawLineJos(x1, y1, x2, y2) #opdracht a

    # opdracht b
    # tekst = input ("voer tekst in: ")
    # xtekst = float(input("voer x-coordinaat voor tekst in: "))
    # ytekst = float(input("voer y-coordinaat voorde tekst in: "))
    # writeText( tekst, xtekst, ytekst)

    # opdracht c
    # xPunt= float(input ("voer x-coordinaat van het punt in: "))
    # yPunt= float(input ("voer y-coordinaat van het punt in: "))
    # drawPoint (xPunt, yPunt)

    #opdracht d
    # xCirkel= float(input ("voer x-coordinaat van het middelpunt van de cirkel in: "))
    # yCirkel= float(input ("voer y-coordinaat van het middelpunt van de cirkel in: "))
    # radius= float(input("Voer de straal van de cirkel in: "))
    # drawCircle(xCirkel, yCirkel, radius)

    # # opdracht e
    # xRect = float(input("voer de x-coordinaat van de rechthoek in: "))
    # yRect = float(input("voer de y-coordinaat van de rechthoek in: "))
    # widthRect = float(input("voer de breedte van de rechthoek in: "))
    # heightRect = float(input("voer de hoogte van de rechthoek in: "))
    # drawRectangle(xRect, yRect, widthRect, heightRect)

   # Draw a pentagon
    drawLine(100, 0, 31,-95)
    drawLine(31, -95, -81,-59)
    drawLine(-81, -59, -81, 59)
    drawLine(-81, 59, 31, 95)
    drawLine(31, 95, 100, 0)

    # Draw points at the corners of the pentagon
    drawPoint(100, 0)
    drawPoint(31, -95)
    drawPoint(-81, -59)
    drawPoint(-81, 59)
    drawPoint(31, 95)

    # Draw a circle at (0, 0) with radius 80
    drawCircle(0, 0, 81)

    # Draw a rectangle at (0, 0)
    # with width 60 and height 40
    drawRectangle(10, 2, 182, 190)

    # Write text at (-50, -60)
    writeText("Functions make programs shorter !", -80, -120)

    turtle.hideturtle()
    turtle.done()    


    
if __name__=="__main__":
    main()
