import turtle

# voorbeeld van een spiraal
# turtle.speed(0)
# turtle.color("red")
# for i in range(36):
#     turtle.forward(100)
#     turtle.left(170)
# turtle.done()

# 4 cirkels tekenen met een lijn ertussen, waarbij de gebruiker de straal van de cirkels en de kleuren van de cirkels en lijnen kan kiezen.

radius = int(input ("Enter the radius of the circles: "))
circlecolor = input ("Enter the color of the circles: ")
linecolor = input ("Enter the color of the lines: ")


turtle.color(circlecolor)
turtle.circle(radius)  

turtle.color(linecolor)   
turtle.forward(radius*2)

turtle.color(circlecolor)
turtle.circle(radius)   

turtle.color(linecolor)
turtle.right(180) 


turtle.color(circlecolor)     
turtle.circle(radius)

turtle.color(linecolor)
turtle.forward(radius*2)
turtle.color(circlecolor)
turtle.circle(radius)   

turtle.done()