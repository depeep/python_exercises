import random

doorgaan = "y"

while doorgaan != "n":
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b

    print ( a ,"+" , b  ,"= ?" )
    answer = input("What is the answer? ")
    if int(answer) == c:
        print("Correct!")
    else:
        print("Incorrect. You need more practice.")
    doorgaan = input("Enter n to stop, anything else to continue: ")
