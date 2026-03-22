secret = 67

guess = int(input("Guess the secret number: "))
while guess != secret:
    if guess < secret:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
    guess = int(input("Guess the secret number: "))
print("Congratulations! You guessed the secret number.")