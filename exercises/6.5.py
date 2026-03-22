def sumDigits(number):
    strNumber = str(number)
    length = len(strNumber)
    sum = 0
    for character in range (length):
        letter = (number[character])
        digit = int(letter)
        sum = sum + digit
    return sum

print (sumDigits('12345'))
