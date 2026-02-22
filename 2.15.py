import turtle

# voorbeeld van een spiraal
# turtle.speed(0)
# turtle.color("red")
# for i in range(36):
#     turtle.forward(100)
#     turtle.left(170)
# turtle.done()

turtle.speed(0) # zet de snelheid van de turtle op het hoogste niveau, zodat de tekening sneller gaat.
side = int(input("Enter the length of the sides of the square: "))
color = input("Enter the color of the square: ")
turtle.color(color)
for i in range(4):
    turtle.forward(side)
    turtle.right(90)


turtle.done()