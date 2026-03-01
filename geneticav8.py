# dit programma voert dihybride kruisingen uit
import sys

# Welkomsboodschap
def welkom():
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    print ("welkom bij de het antwoordcontroleprogramma voor  dihybride kruisingen")
    print ()
    print ("Dit programma helpt je om de uitkomsten van een dihybride kruising te controleren")
    print ()
    print ('het volgt de logische stappen bij het oplossen van een kruisingsvraagstuk:')
    print ('-schrijf per allel (dominant en recessief) het bijbehorende fenotype op')
    print ('-schrijf het genotype van de ouders op')
    print ('-bepaal de mogelijke genotypen in de gameten (geslachtscellen van beide ouderdieren)')
    print ('-vul het kruisingsschema in en bepaal de genotypen van de nakomelingen')
    print ('-bepaal de mogelijke fentoypen van de nakomelingen')
    print ()
    

def invoerFenotypen():
    print ('Voer eerst de fenotypen in die horen bij de verschillende allelen')
    print()
    dominantA = input ("geef het fenotype dat bij het dominante allel A hoort: ")
    recessiefA = input ("geef het fenotype dat bij het recessieve allel a hoort: ")
    dominantB = input ("geef het fenotype dat bij het dominante allel B hoort: ")
    recessiefB = input ("geef het fenotype dat bij allel recessieve allel b hoort: ")
    print()
    return dominantA,recessiefA,dominantB,recessiefB


#  invoer genotypen ouders
def invoerVader():
    genoVader = None
    while genoVader == None or genoVader.lower() != "aabb":
        genoVader = input ("geef het genotype van vader: ")
        if genoVader.lower()  != "aabb":
            print ("probeer het nog een keer, in de vorm AaBb")
    return (genoVader)

def invoerMoeder():
    genoMoeder = None          
    while genoMoeder == None or genoMoeder.lower()  != "aabb":
        genoMoeder = input ("geef het genotype van moeder: ")
        if genoMoeder.lower()  != "aabb":
            print ("probeer het nog een keer, in de vorm AaBb")
    return (genoMoeder)


# menu
def menu(genoVader, genoMoeder,dominantA,recessiefA,dominantB,recessiefB):
    print()
    print ("MENU:")
    print ('"g" om de allelen binnen de gameten van beide ouders te laten zien')
    print ('"k" voor het kruisingsschema' )
    print ('"f" voor fenotypen van de nakomelingen bij deze kruising' )
    print ('"o" om opnieuw te beginnen, met een nieuwe kruising')
    print ('"s" om te stoppen')
    menuInput = input ('voer je keuze in, gevolgd door ENTER: ')
    if  menuInput == "g":
        gametenPrinten(genoVader, genoMoeder)
    elif menuInput == "k":
        kruisingsschemaPrinten(genoVader, genoMoeder)
    elif menuInput == "f": 
        schemaTranslate(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)
    elif menuInput == "o":
        return main()
    elif menuInput == "s":
        return "stop"
    else:
        menu(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)

# functie om gametenlijst te maken van een ouder
def maakGametenLijst(genotype):
    gametenLijst = []
    for i in range (0,2):
        for k in range (2,4):
            gameet = genotype[i]+genotype[k]
            # print (gameet)
            gametenLijst.append(gameet) 
    return gametenLijst

# kruisen, vullen van de list of lists
def vulKruisingsschema (gametenVader, gametenMoeder):
    kruisingsschema =[]  
    for v in range (4):
        rij =[]
        for m in range(4):
            gametenPa = gametenVader[v]
            gametenMa= gametenMoeder[m]
            # volgorde grote en kleine letters goedzetten
            if (gametenPa[0] == 'a') and (gametenMa[0] =='A'):
                paar1 = gametenMa[0]+gametenPa[0]
            else:
                paar1 = gametenPa[0] + gametenMa[0]
            if (gametenPa[1] == 'b') and (gametenMa[1] =='B'):
                paar2 = gametenMa[1]+gametenPa[1]
            else:
                paar2 = gametenPa[1] + gametenMa[1]          
            genoKind = paar1 + paar2
            rij.append(genoKind)
            # print (rij[m])
        kruisingsschema.append(rij)
        # print (kruisingsschema)
    return (kruisingsschema)

def printSchema(schema, gametenVader, gametenMoeder):
    print ("   ", "|", end='')
    for gameet in gametenVader:
        print (" ",gameet, " |", end='')
    print()
    print ("-" * 33)
    for i in range (4):
        print (gametenMoeder[i], " |",end='')
        for j in range (4):
            print (schema[i][j], " |", end='')
        print()
        print ("-" * 33)

def kruisingsschemaPrinten(genoVader, genoMoeder):
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    print ("Kruisingsschema bij de kruising", genoVader, " x ", genoMoeder)
    print ()
    gametenVader = maakGametenLijst(genoVader)
    gametenMoeder = maakGametenLijst(genoMoeder)
    kruisingsschema = vulKruisingsschema(gametenVader,gametenMoeder)
    printSchema (kruisingsschema,gametenVader,gametenMoeder)
    print()

def gametenPrinten(genoVader,genoMoeder):
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    print ("Gameten van de ouders bij de kruising", genoVader, " x ", genoMoeder)
    print ()
    gametenVader = maakGametenLijst(genoVader)
    gametenMoeder = maakGametenLijst(genoMoeder)
    print ('gameten van vader:  ',gametenVader)
    print ('gameten van moeder: ',gametenMoeder)


def bye():
    print ("Bedankt voor het gebruik van dit programma")
    print ("Veel succes met het nog meer leren over genetica")
   

# genotype vertalen naar fenotype
def translateFenotype(genotype, dominantA,  recessiefA, dominantB, recessiefB):
    if genotype == "aabb":
        feno = recessiefA + "-" + recessiefB
        return feno
    elif genotype[:1]=="aa" and genotype[2] =="B":
        feno = recessiefA + "-" + dominantB
        return feno
    elif genotype[0] == "A"and genotype[2:]=="bb":
        feno = dominantA + "-" + recessiefB
        return feno
    else: 
        feno = dominantA + "-" + dominantB
        return feno

# kruisingsschema vullen, ieder genotype naar de vertaler sturen, de placeholders voor fenotype printen in het schema
def schemaTranslate(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB):
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    print ("fenotype printen")
    print()
    gametenVader = maakGametenLijst(genoVader)
    gametenMoeder = maakGametenLijst(genoMoeder)
    kruisingsschema = vulKruisingsschema(gametenVader,gametenMoeder)
    print ("   ", "|", end='')
    for gameet in gametenVader:
        print ("       ",gameet.ljust(6), " |", end='')
    print()
    print ("-" * 72 )
    for i in range (4):
        print (gametenMoeder[i], " |",end='')
        for j in range (4):
            fenotype=translateFenotype(kruisingsschema[i][j],dominantA,recessiefA,dominantB,recessiefB)
            print (fenotype.rjust(15), "|", end='')
        print()
        print ("-" * 72 )

def main():
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    welkom() 
    keuze = None
    dominantA, recessiefA, dominantB, recessiefB =invoerFenotypen()
    genoVader = invoerVader()
    genoMoeder = invoerMoeder()
    while (keuze !="stop"):
        keuze = menu(genoVader, genoMoeder, dominantA, recessiefA, dominantB, recessiefB)
    bye()

if __name__ == "__main__":
    main()