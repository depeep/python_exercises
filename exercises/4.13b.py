size = int(input("Enter the width of the rectangle: "))


for i in range (size):
    for j in range (i,0,-1):
        print ('*', end = '')
    print()
    