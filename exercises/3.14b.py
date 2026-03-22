import random

# def generate_random_number():
#     return random.randint(1, 100)
# beetje overdreven om hier een functie voor te maken...

a = random.randint(1, 100)
b = random.randint(1, 100)
c = a + b

answer = input(str(a) + " + " + str(b)  + " = ")
if int(answer) == c:
    print("Correct!")
else:
    print("Incorrect. You need more practice.")

