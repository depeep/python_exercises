import random


aantalVierkanten = 4
grens = aantalVierkanten//4
extra = aantalVierkanten % 4
kleurdoos = []
aantalRood = 0
aantalBlauw = 0
aantalGroen = 0 
aantalGeel =0
aantalKleuren = 0
print (aantalKleuren)
while (aantalKleuren < grens*4):
    nummer = random.randint(0, 4)
    if (nummer == 0 and aantalRood < grens):
        kleurdoos.append('red')
        print ("rood")
        aantalRood +=1
        aantalKleuren +=1
    elif (nummer == 1 and aantalGroen < grens):
        kleurdoos.append('green')
        print ("groen")
        aantalGroen +=1
        aantalKleuren +=1
    elif (nummer == 2 and aantalBlauw < grens):
        kleurdoos.append('blue')
        print ("blauw")
        aantalBlauw +=1
        aantalKleuren +=1
    elif (nummer == 3 and aantalGeel < grens):
        print ("geel")
        kleurdoos.append('yellow')
        aantalGeel +=1
        aantalKleuren +=1
    
print (aantalKleuren, len(kleurdoos), aantalRood, aantalGroen,aantalBlauw, aantalGeel)
if extra == 1:
    kleurdoos.append('blue')
print (kleurdoos)