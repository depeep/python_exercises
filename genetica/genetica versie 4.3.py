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
    if kruisingstype == "m":   # misschien ook de losse functie, zie onder, gebruiken (wel aanpassen dan)
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
    print("\033c", end="")
    print ('Voer in welk kruisingstype je wilt gebruiken:')
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
# einde invoer genotypen ouders  TODO  Overlap/herhaling moeder en vaderop te splitsen naar aparte functie  om hem DRYer te krijgen

#  functie om gametenlijst te maken van een ouder
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

#  losgehaald functie om grote en kleine letter in de goede volgorde te zetten
def verbeterVolgorde(paar):
    if paar == "aA":
        return "Aa"
    elif paar =="bB":
        return "Bb"
    elif paar == "cC":
        return "Cc"
    else:
        return paar
    
# kruisen, vullen van de list of lists
def vulKruisingsschema (type,gametenVader, gametenMoeder):
    dimensie, paren = dimensieBepalen(type)
    kruisingsschema =[]  
    for v in range (dimensie):
        rij =[]
        for m in range (dimensie):
            gametenPa = gametenVader[v]
            gametenMa= gametenMoeder[m]
            genoKind =""
            for positie in range(paren):
                allelPa = gametenPa[positie]
                allelMa = gametenMa[positie]
                paar = allelPa + allelMa
                paar = verbeterVolgorde(paar)
                genoKind = genoKind + paar
                # print (genoKind)
            rij.append(genoKind)
        # print (rij)
        kruisingsschema.append(rij)
    # print (kruisingsschema)
    return (kruisingsschema)

# NEW losse functie om dimensies en aantal paren te bepalen aan de hand van het ingevoerde type kruising >> ABSTRACTER GEMAAKT MET 2**PAREN
def dimensieBepalen(type):
    if type == "m": #dimensies van het kruisingsschema goedzetten
        paren = 1
    elif type == "d":
        paren = 2
    else:
        paren =3
    dimensie = 2**paren
    return dimensie, paren

# NEW schaalbare functie om kruisingsschema'S te printen
def printSchema(type, schema, gametenVader, gametenMoeder):
    dimensie, paren =dimensieBepalen (type) 
    breedteVak = (paren *8 )
    tussenregel = ("-" * (breedteVak) + "|" + ("-" *breedteVak+"|")*dimensie)
    print (breedteVak*" "+"|", end='')
    for gameet in gametenVader:
        print (gameet.ljust(breedteVak)+"|", end='')
    print()
    print (tussenregel)
    for gameet in gametenMoeder:
        print (gameet + (breedteVak-paren)*" "+"|", end='')
        i = gametenMoeder.index(gameet)
        for j in range (dimensie):
            vakInhoud =schema[i][j]
            print (vakInhoud.ljust(breedteVak-1)+" |", end='')
        print()
        print (tussenregel)

# NEW wrapper voor printschema
def printSchemaWrapper(type, schema, genoVader, genoMoeder, gametenVader, gametenMoeder, soortSchema):
    print ("de verdeling van de", soortSchema,  "bij de kruising", genoVader , "x" ,genoMoeder, "is:")
    printSchema(type, schema, gametenVader, gametenMoeder)
    print()

# NEW genotype vertalen naar fenotype m.b.v. dictionary   >> wat op verzinnen, kan eenvoudiger
def vertaal(paar, fenoDict):
    if paar == "aa":
        fenotype = fenoDict ["a"]
    elif paar in ["AA", "Aa"]:
        fenotype = fenoDict ["A"]
    elif paar == "bb":
        fenotype = fenoDict ["b"]
    elif paar in ["BB", "Bb"]:
        fenotype = fenoDict["B"]
    elif paar == "cc":
        fenotype = fenoDict["c"]
    else:
        fenotype = fenoDict["C"]
    return fenotype
        
# NEW fenotypen array vullen en gereed maken voor printfunctie, schaalbaar gemaakt met dimensie/paren op basis van type >> verder abstraheren (dimensie = 2**paren)
def maakFenoArray(kruisingsschema, fenoDict, type):
    dimensie, paren =dimensieBepalen (type)
    Aantalletters=paren*2
    fenoArray =[]
    for rij in kruisingsschema:
        nieuweRij = []
        for genotype in rij:
            # print (genotype, end='')
            feno=''
            for letterpaar in range(0, Aantalletters, 2):
                begin = letterpaar
                eind  = letterpaar + 1
                letters = genotype[begin]+ genotype[eind]
                # print(letters)
                fenoplus = vertaal(letters, fenoDict)
                # print (fenoplus)
                feno = feno + ' ' + fenoplus
            #     print (feno)
            # print(feno)
            # print()
            nieuweRij.append(feno)
        # print (nieuweRij)
        fenoArray.append(nieuweRij)
    # print (fenoArray)
    return fenoArray

# DEMO (was eerst functie voor de test runs )>> dictionary fenotypen en genotypen ouders zijn al ingevuld
def demo():
    print("\033c", end="")
    print ('Welkom bij de demonstratie van het programma')
    print()
    type, template = invoerKruisingstype()  # template haalt op of het de vorm aa, aabb, of aabbcc moet hebben
    print (type)
    #invoer
    fenoDict = {'A':'zwart', 'a':  'rood', 'B' : 'bont', 'b': 'egaal', 'C' : 'gehoornd', 'c' : 'hoornloos'} # in nieuwe versie van invoer aanpassen!
    genoVader='AaBbCc'
    genoMoeder = 'AaBbCc'
    # verwerking 
    gametenVader = maakGametenLijst(type, genoVader)
    gametenMoeder = maakGametenLijst(type, genoMoeder)
    kruisingsschema = vulKruisingsschema (type,gametenVader, gametenMoeder)
    fenoSchema=maakFenoArray(kruisingsschema, fenoDict, type)
    # afdrukken
    print()
    print ("Deze demo maakt gebruik van de volgende gegevens:" ) 
    print ('Allelen met bijbehorende fenotypen: ', fenoDict) # dictionary --- op letten bij het vertalen van genotype naar fenotype
    print ('Genotype van de vader: ', genoVader) #string
    print ('Genotype van de moeder: ', genoMoeder) #string
    print ('genotype in de gameten van de vader: ', gametenVader) #array
    print ('genotype in de gameten van de moeder: ', gametenMoeder) #array
    print()
    printSchemaWrapper(type, kruisingsschema, genoVader, genoMoeder, gametenVader, gametenMoeder, "genotypen")
    printSchemaWrapper(type, fenoSchema, genoVader, genoMoeder, gametenVader, gametenMoeder, "fenotypen")
    nogEens = None
    while nogEens != "n":
        nogEens = input('Wil je nog een demo? j/n: ')
        if nogEens == "j":
            demo()
    main()
    
# NEW menu
def menu(type, kruisingsschema,fenoSchema, genoVader, genoMoeder, gametenVader, gametenMoeder):
    print()
    print ("MENU:")
    # print ('"t" om het type kruising te kiezen')
    print ('"g" om de genotypen van beide ouders te laten zien')
    print ('"a" om de allelen binnen de gameten van beide ouders te laten zien')
    print ('"k" voor het kruisingsschema' )
    print ('"f" voor fenotypen van de nakomelingen bij deze kruising' )
    print ('"o" om opnieuw te beginnen, met een nieuwe kruising')
    print ('"s" om te stoppen')
    menuInput = input ('voer je keuze in, gevolgd door ENTER: ')
    if  menuInput == "a":
        print("\033c", end="") 
        gametenPrinten(gametenVader, gametenMoeder)
    elif menuInput == "g":
        print("\033c", end="") 
        genotypeOudersPrinten(genoVader, genoMoeder) 
    elif menuInput == "k":
        print("\033c", end="") 
        printSchemaWrapper(type, kruisingsschema, genoVader, genoMoeder, gametenVader, gametenMoeder, "genotypen")
    elif menuInput == "f": 
        print("\033c", end="") 
        printSchemaWrapper(type, fenoSchema, genoVader, genoMoeder, gametenVader, gametenMoeder, "fenotypen")
    elif menuInput == "o":
        main() 
    elif menuInput == "s":
        return "stop"
    else:
        menu(type, kruisingsschema, genoVader, genoMoeder, gametenVader, gametenMoeder)

def gametenPrinten(gametenVader, gametenMoeder):
    print ("Gameten van de ouders:")
    print ('vader: ', gametenVader)
    print ('moeder: ',gametenMoeder)

def genotypeOudersPrinten(genoVader, genoMoeder):
    print ('Genotypen van de ouders')
    print ('vader: ', genoVader)
    print ('moeder: ', genoMoeder)

def bye():
    print("\033c", end="")
    print ("Bedankt voor het gebruik van dit programma")
    print ("Veel succes met het nog meer leren over genetica")

def startKeuze():
    welkom()
    keuze = input ('kies "d" voor demo of "z" om zelf gegevens in te voeren: ')
    if keuze == "d":
        demo()
   

    
def main():
    print("\033c", end="") # ansi escapecodes om venster leeg te trappen
    #demo afspelen of door
    startKeuze() 
    type, template = invoerKruisingstype()  # template haalt op of het de vorm aa, aabb, of aabbcc moet hebben
    print (type)
    # invoeren
    print ('Voer eerst de gegevens voor de kruising in: ')
    genoVader = invoerVader(template)
    genoMoeder = invoerMoeder(template)
    fenoDictionary =invoerFenotypen(type)
    gametenVader = maakGametenLijst(type, genoVader)
    gametenMoeder = maakGametenLijst(type, genoMoeder)
    print()
    # print ('genotype gameten vader: ', gametenVader) #array
    # print ('genotype gameten Moeder: ', gametenMoeder) #array
    print()
    kruisingsschema = vulKruisingsschema (type,gametenVader, gametenMoeder)
    fenoSchema=maakFenoArray(kruisingsschema, fenoDictionary, type)
    keuze = None
    while keuze != "stop":
        keuze = menu(type, kruisingsschema,fenoSchema, genoVader, genoMoeder, gametenVader, gametenMoeder)
    bye()

 
if __name__ == "__main__":
    main()


