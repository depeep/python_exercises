# test reading of shortened words

# missing code here for function first_last_letter

def first_last_letter(word):
    first = word [0]
    last = word[-1]
    short = first + reversedWord(word) + last
    return short

def reversedWord (word):
    eind = len(word)-2
    first = 0
    reversedMiddle = ''
    for i in range(eind, first, -1):
        reversedMiddle = reversedMiddle + word[i]
    return reversedMiddle

    

def main():
    test_input = "Can you still read this text with only first and last letters ? Yes I can ! He can too ..."

    words = test_input.split(' ') # create list of words

    short_words = []
    for word in words:
        short_word = first_last_letter(word)
        short_words.append(short_word)

    # join is an easy way to glue strings together, separated by ' '
    test_output = ' '.join(short_words)
    print(test_output)


#start of program

main()