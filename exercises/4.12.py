print (' Move the turtle using action inputs:')
print (' f: Move 30 px forward')
print (' l: Turn 45 degrees left') 
print (' r: Turn 45 degrees right')
print ('u: lift the pen up')
print ('d: put the pen down')
print (' q: Quit')
print ('------------------------------------------------------')
import turtle
turtle.shape('turtle')
turtle.speed(10)

action = input('Enter your action: ')
while action != 'q':
    if action == 'f':
        turtle.forward(30)
    elif action == 'l':
        turtle.left(45)
    elif action == 'r':
        turtle.right(45)
    elif action == 'u':
        turtle.penup()
    elif action == 'd':
        turtle.pendown()
    else:
        print('I don\'t know action ', action, '. Please try again.')
    
    action = input('Enter your action: ')
    
print('Good bye!')
turtle.done()


