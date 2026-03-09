# opdracht a
def number_of_separators(text, separators):
    aantalSeparators = 0
    for teken in text:
        if teken in separators:
            aantalSeparators += 1
    return aantalSeparators

# opdracht b
def number_of_words(text, separators): #separators niet nodig
    wordList = text.split()
    numberOfWords = len (wordList)
    return numberOfWords

#opdracht c AFMAKEN!
def expand_acronyms(text, acronyms):
    wordList = text.split()
    print (wordList)
    for word in wordList:
        index = wordList.index(word)
        for short in acronyms:
            if short == word:
                del wordlist[index]
                long= acronyms(short)
                insert wordList(index, long )
                
    sentence = wordList.join()
    return sentence
            # else: 
            #     return ("no acronyms found")

def main():
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
    acronyms = {'fyi': 'for your information',
            'imho': 'in my humble opinion',
            'ty': 'thank you',
            'lol': 'laughing out loud'}

    text1 = 'Here are 7 words, and 8 separators.'
    expanded1 = expand_acronyms(text1, acronyms)
    print('expanded text: "' + expanded1 + '"')

    text2 = '... hi, aaand  goodbye;did I forgot 1 space?? lol'
    expanded2 = expand_acronyms(text2, acronyms)
    print('expanded text: "' + expanded2 + '"')

if __name__ == "__main__":
    main()
