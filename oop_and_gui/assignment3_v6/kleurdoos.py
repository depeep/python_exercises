import random

''' deze functie maakt een kleurenlijst (kleurdoos) aan op basis van het aantal vierkanten om
iedere keer nieuwe kleuren te hebben, volgens de voorgeschreven regels, allemaal even vaak. Dat kan misschien mooier. '''

def vulKleurdoos(aantalVierkanten): # functie om de kleur te bepalen, nog dimensies toevoegen voor de kleur spelregels
    grens = aantalVierkanten//4
    extra = aantalVierkanten % 4
    kleurdoos = []
    aantalRood = 0
    aantalBlauw = 0
    aantalGroen = 0 
    aantalGeel =0
    aantalKleuren = 0
    while (aantalKleuren < grens*4):
        nummer = random.randint(0, 4)
        if (nummer == 0 and aantalRood < grens):
            kleurdoos.append('red')
            aantalRood +=1
            aantalKleuren +=1
        elif (nummer == 1 and aantalGroen < grens):
            kleurdoos.append('green')
            aantalGroen +=1
            aantalKleuren +=1
        elif (nummer == 2 and aantalBlauw < grens):
            kleurdoos.append('blue')
            aantalBlauw +=1
            aantalKleuren +=1
        elif (nummer == 3 and aantalGeel < grens):
            kleurdoos.append('yellow')
            aantalGeel +=1
            aantalKleuren +=1
    if extra == 1:
        kleurdoos.append('blue')
    return kleurdoos


