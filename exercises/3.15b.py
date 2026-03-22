a = input("Enter number 1: ")
b = input("Enter number 2: ")
c = input("Enter number 3: ")

if a < b and a < c:
    if b < c:
        print("correct order is: ", a, b, c)
    else:
        print("correct order is: ", a, c, b)
elif b < a and b < c:
    if a < c:
        print("correct order is: ", b, a, c)
    else:
        print("correct order is: ", b, c, a)
else:
    print("correct order is: ", c,  b, a)