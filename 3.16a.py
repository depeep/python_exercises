import random
number = random.randint(1, 3)
userInput = int(input("rock = 1, paper = 2, scissors = 3: "))

if userInput == number:
    print("It's a tie!")
elif (userInput == 1 and number == 3) or (userInput == 2 and number == 1) or (userInput == 3 and number == 2):
    print("You win!")
else:
    print("You lose!")  