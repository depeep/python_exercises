import turtle

number = int(input("How many zigzags do you want? "))

turtle.speed(10)
turtle.right(60)
for i in range(number):
    turtle.left(120)
    turtle.forward(100)
    turtle.right(120)
    turtle.forward(100)
                 
turtle.done()

