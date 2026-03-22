import random

# class Coin simulates a coin that can be flipped.
class Coin:
    def __init__(self):
        # The __init__ method initializes the
        # __sideup data attribute with 'Heads'.
        self.__sideup = 'Heads'

    def toss(self):
    # The toss method generates a random number in the range of 0 through 1.
    # If the number is 0, then sideup is set to 'Heads',
    # Otherwise, sideup is set to 'Tails'.
        if random.randint(0, 1) == 0:
            self.__sideup = 'Heads'
        else:
            self.__sideup = 'Tails'

    def get_sideup(self):
        # The get_sideup method returns the value of __sideup.
        return self.__sideup

def main():
    print("I am going to create a coin object ...")
    my_coin = Coin()
    print('This side is up:', my_coin.get_sideup())

    print('I am going to toss the coin five times:')
    for count in range(1, 6):
        my_coin.toss()
        print("After toss", count, "side", my_coin.get_sideup(), "is up.")

main()

"""My prediction: depending on how random the random function generates numbers there will be about as many heads
as tails. However this was not the case, it returned heads five times...

Copy the code into a visualiser (e.g. https://pythontutor.com/visualize.html#mode=edit),
 and step through the code . 
 
 Strangely enough it works as predicted now... It seems that the results from my first run were coincidental """
