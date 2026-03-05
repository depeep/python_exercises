def sumDigits(number):
    strNumber = str(number)
    length = len(strNumber)
    sum = 0
    for character in range (length):
        letter = (number[character])
        digit = int(letter)
        sum = sum + digit
    return sum

def main():
    invoer = None
    while invoer != "s":
        invoer = input ('voer een getal van meerdere cijfers in: (s om te stoppen)')
        if invoer != "s":
            print (sumDigits (invoer))

if __name__ == "__main__":
    main()