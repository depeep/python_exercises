# opdracht a
def removeEndPunctuation(poem):
    punctuation = ['.', ',', ';', '?', '!', ':']
    for sentence in poem:
        index = poem.index(sentence)
        # print(index)
        end = sentence[-1]
        if end in punctuation:
            newsentence = sentence[:-1]
            # print newsentence
            del poem[index]
            poem.insert(index, newsentence)
    return poem
            
# opdracht b en c
def lastWord(poem):
    lastWordList = []
    for sentence in poem:
        wordList =  sentence.split()      
        lastWord = wordList[-1]
        # print (lastWord)
        lastWordList.append(lastWord)
    return lastWordList

# opdracht d
def checkRhyme(word1, word2):
    if word1[-2:] == word2 [-2:]:
        # print (word1, "rijmt op", word2)
        return True
    else:
        # print (word1, "rijmt niet op", word2)
        return False


# opdracht e
def pairRhyme(wordlist):
    # versie 1
    # for word1 in wordlist:
    #     print()
    #     aantalWoorden = len(wordlist)
    #     for i in range(1,aantalWoorden):
    #         word2 = wordlist[i]
    #         print (word1, ' ', word2)
    # versie 2
    # for word1 in wordlist:
    #     index1 = wordlist.index(word1)
    #     for word2 in wordlist:
    #         index2 = wordlist.index(word2)
    #         if index1 != index2:
    #             if checkRhyme(word1, word2):
    #                 print (word1, word2)
    print ('Rhyming words:')
    print ()
    for word1 in wordlist:
        index1 = wordlist.index(word1)
        for word2 in wordlist:
            index2 = wordlist.index(word2)
            if index1 < index2:
                if checkRhyme(word1, word2):
                    print (word1, word2)
    print()
            
            
def printRegelVoorRegel(poem):
    print()
    print('Text of the poem:')
    print()
    for regel in poem:
        print (regel)
    print()


def main():
    poem = ["Shall I compare thee to a summer's day?",
    "Thou art more lovely and more temperate.",
    "Rough winds do shake the darling buds of May,",
    "And summer's lease hath all too short a date.",
    "Sometime too hot the eye of heaven shines,",
    "And often is his gold complexion dimmed;",
    "And every fair from fair sometime declines,",
    "By chance, or nature's changing course, untrimmed;"]
    printRegelVoorRegel(poem)

    poemWithoutEndPunctuation =removeEndPunctuation(poem)
    # print (poemWithoutEndPunctuation)
    lastWordList = lastWord(poemWithoutEndPunctuation)
    # print (lastWordList)
    # print(checkRhyme("stoep", "poep"))
    pairRhyme(lastWordList)




if __name__=="__main__":
    main()



