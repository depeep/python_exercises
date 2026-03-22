import random

doorgaan = "y"

while doorgaan != "n":
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b
    answer = "-1"
    while int(answer) != c:
        print ( a ,"+" , b  ,"= ?" )
        answer = input("What is the answer? ")
        if int(answer) == c:
            print("Correct!")
        else:
            print("Incorrect. Try again.")
    doorgaan = input("Enter n to stop, anything else to continue: ")
