# dit programma voert mono-, di- of trihybride kruisingen uit
import sys

# Welkomsboodschap == licht aangepast
def welkom():
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    print ("welkom bij de het antwoordcontroleprogramma voor kruisingen")
    print ()
    print ("Dit programma helpt je om de uitkomsten van een  kruising te controleren")
    print ()
    print ('het volgt de logische stappen bij het oplossen van een kruisingsvraagstuk:')
    print ('-schrijf per allel (dominant en recessief) het bijbehorende fenotype op')
    print ('-schrijf het genotype van de ouders op')
    print ('-bepaal de mogelijke genotypen in de gameten (geslachtscellen van beide ouderdieren)')
    print ('-vul het kruisingsschema in en bepaal de genotypen van de nakomelingen')
    print ('-bepaal de mogelijke fentoypen van de nakomelingen')
    print ()
    
# NEW invoer fenotypen obv type kruising
def invoerFenotypen(kruisingstype):
    fenoDict = {}
    opties = ['A','a', 'B', 'b', 'C', 'c']
    print ('Voer eerst de fenotypen in die horen bij de verschillende allelen')
    print()
    if kruisingstype == "m":
        aantAllelen = 2
    elif kruisingstype == "d":
        aantAllelen = 4
    elif kruisingstype == "t":
        aantAllelen = 6
    for allel in opties [:aantAllelen]:
        string = "Geef het fenotype dat hoort bij het allel " + allel + ": "
        feno = input (string)
        fenoDict[allel] = feno
    return (fenoDict)
        
# NEW keuzemenu kruisingstypen en template vullen
def invoerKruisingstype():
    keuze = None
    while keuze not in ["m", "d", "t"]:
        keuze = input ('Kies "m" voor een monohybride, "d" voor een dihybride of "t" voor een trihybride kruising :')
        if keuze == "m":
            template = "aa"
        elif keuze == "d":
            template = "aabb"
        elif keuze == "t":
            template = "aabbcc"
        else:
            print ('kies "m", "d" of "t:')
    return keuze, template

# NEW  invoer genotypen ouders, schaalbaar, template = aa/aabb/aabbcc afhankelijk van mono-di-of trihybride kruising
def invoerVader(template):
    genoVader = None
    while genoVader == None or genoVader.lower() != template:
        genoVader = input ("geef het genotype van vader: ")
        if genoVader.lower()  != template:
            print ("probeer het nog een keer, in de vorm", template )
    return (genoVader)

def invoerMoeder(template):
    genoMoeder = None          
    while genoMoeder == None or genoMoeder.lower()  != template:
        genoMoeder = input ("geef het genotype van moeder: ")
        if genoMoeder.lower()  != template:
            print ("probeer het nog een keer, in de vorm ", template)
    return (genoMoeder)
# einde invoer genotypen ouders  TODO letters omdraaien bij aA enz, Nice to have, maar niet strikt noodzakelijk. Overlap/herhaling op te splitsen naar aparte functie  om hem DRYer te krijgen

# NEW functie om gametenlijst te maken van een ouder
def maakGametenLijst(kruisingstype, genotype):
    gametenLijst = []
    if kruisingstype == "m":
        for i in range (2):
            gameet= genotype[i]
            gametenLijst.append(gameet) 
    
    elif kruisingstype == "d":
        for i in range (0,2):
            for k in range (2,4):
                gameet = genotype[i]+genotype[k]
                # print (gameet)
                gametenLijst.append(gameet) 
    elif kruisingstype == "t":
        for i in range (0,2):
                for k in range (2,4):
                    gameet = genotype[i]+genotype[k]
                    for l in range (4,6):
                        gameet = genotype[i]+genotype[k]+genotype[l]
                        gametenLijst.append(gameet) 
    return gametenLijst
    
    
# NOG AAN TE PASSEN / VERVANGEN  :
# menu
def menu(genoVader, genoMoeder,dominantA,recessiefA,dominantB,recessiefB):
    print()
    print ("MENU:")
    print ('"t" om het type kruising te kiezen')
    print ('"g" om de allelen binnen de gameten van beide ouders te laten zien')
    print ('"k" voor het kruisingsschema' )
    print ('"f" voor fenotypen van de nakomelingen bij deze kruising' )
    print ('"o" om opnieuw te beginnen, met een nieuwe kruising')
    print ('"s" om te stoppen')
    menuInput = input ('voer je keuze in, gevolgd door ENTER: ')
    if  menuInput == "t":
        keuze, template = invoerKruisingstype()
    elif menuInput == "g":
        gametenPrinten(genoVader, genoMoeder)
    elif menuInput == "k":
        kruisingsschemaPrinten(genoVader, genoMoeder)
    elif menuInput == "f": 
        schemaTranslate(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)
    elif menuInput == "o":
        main() 
    elif menuInput == "s":
        return "stop"
    else:
        menu(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)

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

# MAIN UITGESCHAKELD OM DE FUNCTIES TE TESTEN
# def main():
    # print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    # welkom() 
    # keuze = None
    # dominantA, recessiefA, dominantB, recessiefB =invoerFenotypen()
    # genoVader = invoerVader()
    # genoMoeder = invoerMoeder()
    # while keuze != "stop":
    #     keuze = menu(genoVader, genoMoeder,dominantA,recessiefA,dominantB,recessiefB)
    # bye()



# if __name__ == "__main__":
#     main()

# FUNCTIE VOOR DE TESTRUNS >> BASIS VOOR DE NIEUWE MAIN

def runme1():
    type, template = invoerKruisingstype()  # template haalt op of het de vorm aa, aabb, of aabbcc moet hebben
    print (type)
    #invoer
    fenoDict = invoerFenotypen(type)
    genoVader=invoerVader(template)
    genoMoeder = invoerMoeder(template)
    # verwerking 
    gametenVader = maakGametenLijst(type, genoVader)
    gametenMoeder = maakGametenLijst(type, genoMoeder)
    print()
    print ("Ingevoerde gegevens in hun de vorm van hun variabelen" ) # misschien leuk om met type ook het type af te drukken
    print ('fenotype dictionary: ', fenoDict) # dictionary --- op letten bij het vertalen van genotype naar fenotype
    print ('genovader ', genoVader) #string
    print ('genomoeder ', genoMoeder) #string
    print ('genotype gameten vader: ', gametenVader) #array
    print ('genotype gameten Moeder: ', gametenMoeder) #array
    print()


runme1()



# vervangen code:

# OUD hardcoded
# def invoerFenotypen():
#     print ('Voer eerst de fenotypen in die horen bij de verschillende allelen')
#     print()
#     dominantA = input ("geef het fenotype dat bij het dominante allel A hoort: ")
#     recessiefA = input ("geef het fenotype dat bij het recessieve allel a hoort: ")
#     dominantB = input ("geef het fenotype dat bij het dominante allel B hoort: ")
#     recessiefB = input ("geef het fenotype dat bij allel recessieve allel b hoort: ")
#     print()
#     return dominantA,recessiefA,dominantB,recessiefB

# OUD: invoer genotypen ouders hardcoded
# def invoerVader():
#     genoVader = None
#     while genoVader == None or genoVader.lower() != "aabb":
#         genoVader = input ("geef het genotype van vader: ")
#         if genoVader.lower()  != "aabb":
#             print ("probeer het nog een keer, in de vorm AaBb")
#     return (genoVader)

# def invoerMoeder():
#     genoMoeder = None          
#     while genoMoeder == None or genoMoeder.lower()  != "aabb":
#         genoMoeder = input ("geef het genotype van moeder: ")
#         if genoMoeder.lower()  != "aabb":
#             print ("probeer het nog een keer, in de vorm AaBb")
#     return (genoMoeder)

# # functie om gametenlijst te maken van een ouder
# def maakGametenLijst(genotype):
#     gametenLijst = []
#     for i in range (0,2):
#         for k in range (2,4):
#             gameet = genotype[i]+genotype[k]
#             # print (gameet)
#             gametenLijst.append(gameet) 
#     return gametenLijst
