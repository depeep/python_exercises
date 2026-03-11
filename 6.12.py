# opdracht a
def number_of_separators(text, separators):
    aantalSeparators = 0
    for teken in text:
        if teken in separators:
            aantalSeparators += 1
    return aantalSeparators

# opdracht b
def number_of_words(text): #separators niet nodig
    wordList = text.split()
    numberOfWords = len (wordList)
    return numberOfWords

#opdracht c !
def expand_acronyms(text, acronyms):
    wordList = text.split()
    # print (wordList)
    for word in wordList:
        index = wordList.index(word)
        for short in acronyms:
            if short == word:
                del wordList[index]
                long = acronyms[short]
                wordList.insert(index, long)
    # print (wordList)
                
    sentence = ' '.join(wordList)
    return sentence

def inputKeuze():
    print ("--- program text analyser --- \n options: \n e - (e)nter a text tot analyse \n s - to count the number of separators ")
    print (" w - to count the number of words \n a - to expand acronyms \n q to quit.")
    keuze = input ("Please enter your choice: ")
    return keuze

def enterNewText():
    text=input ("enter your text here: \n")
    return text

def menu(keuze,text, separators, acronyms):
    if keuze == "e":
        text = enterNewText()
        # inputKeuze()
    elif keuze == "s":
        print ('the number of separators is:', number_of_separators(text, separators))
    elif keuze == "w":
        print ('the number of words is:', number_of_words(text))
    elif keuze == "a":
        print (text)
        print ("expands to: ")
        print (expand_acronyms(text, acronyms))
    elif keuze == "q":
        return "q"
    else:
        print ("invalid input, please try again")
        inputKeuze()


def main():
    menureturn = None
    separators = ['.', ',', ';', ':', '?', '!', ' ']
    acronyms = {'fyi': 'for your information',
            'imho': 'in my humble opinion',
            'ty': 'thank you',
            'lol': 'laughing out loud'}
    
    text = enterNewText()
    keuze = inputKeuze()
    
    while menureturn != "q":
        menureturn = menu(keuze, text, separators, acronyms)
    print ("Bye!")

if __name__ == "__main__":
    main()





# # voorbereiding (a tot en met c)
# def main():
# #opdracht a
    # separators = ['.', ',', ';', ':', '?', '!', ' ']

    # text1 = 'Here are 7 words, and 8 separators.'
    # nr1 = number_of_separators(text1, separators)
    # print(nr1)

    # text2 = '... hi, aaand  goodbye;did I forgot 1 space?? lol'
    # nr2 = number_of_separators(text2, separators)
    # print(nr2)

# # opdracht b
#     separators = ['.', ',', ';', ':', '?', '!', ' ']

#     text1 = 'Here are 7 words, and 8 separators.'
#     nr1 = number_of_words(text1, separators)
#     print(nr1)

#     text2 = '... hi, aaand  goodbye;did I forgot 1 space?? lol'
#     nr2 = number_of_words(text2, separators)
#     print(nr2)

#opdracht c
    # acronyms = {'fyi': 'for your information',
    #         'imho': 'in my humble opinion',
    #         'ty': 'thank you',
    #         'lol': 'laughing out loud'}

    # text1 = 'Here are 7 words, and 8 separators.'
    # expanded1 = expand_acronyms(text1, acronyms)
    # print('expanded text: "' + expanded1 + '"')

    # text2 = '... hi, aaand  goodbye;did I forgot 1 space?? lol'
    # expanded2 = expand_acronyms(text2, acronyms)
    # print('expanded text: "' + expanded2 + '"')


