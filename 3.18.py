hand = input ("Enter hand " )

def checkinput(hand):
    if len(hand) != 10:
        return False
    for i in range (0, 10, 2):
        if hand[i] not in "A23456789TJQK":
            return False
    for i in range (1, 10, 2):
        if hand[i] not in "CDHS":
            return False
    return True


def checkFlush(hand):
    kleur = hand[1]
    for i in range (3, 10, 2):
        # print (hand[i])
        if hand[i] != kleur:
            return False    
    return True

def checkFourOfAKind(hand):
    for i in range (0, 10, 2):
        count = 0
        for j in range (0, 10, 2):
            if hand[i] == hand[j]:
                count += 1
        if count == 4:
            return True
    return False


if not checkinput(hand):
    print ("Invalid hand")
else:
    print ("Valid hand")
    if checkFlush(hand):
        print ("Flush")
    elif checkFourOfAKind(hand):
        print ("Four of a kind")
    else: print ("No flush or four-of-a-kind, better luck next time!")
