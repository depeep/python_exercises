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
    
# NEW invoer fenotypen obv type kruising>> aanpassen om te schalen
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

# NEW schaalbaar invoer kruisingstype geeft aantal paren terug en template voor invoer genotypen
def invoerKruisingstype():
    paren = None
    print ("voer het aantal allelenparen in dat  je wilt gebruiken voor je kruising")
    getalOpties =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    templateOptions = "aabbccddeeffgghhiijj"
    while paren not in getalOpties:
        paren = int(input ('Kies "1" voor een monohybride, "2" voor een dihybride of "3" voor een trihybride kruising enz. :'))
        if paren in getalOpties:
            template= templateOptions[0:paren*2]
            print (template)
        else:
            print ('kies een getal tussen 0 en 10')
    return paren, template



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

# NEW functie om gametenlijst te maken van een ouder
def maakGametenLijst(kruisingstype, genotype):
    gametenLijst = []
    if kruisingstype == 1:
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

# V NEW losgehaald functie om grote en kleine letter in de goede volgorde te zetten, geschaald naar max 10 paren
def verbeterVolgorde(paar):
    if paar == "aA":
        return "Aa"
    elif paar =="bB":
        return "Bb"
    elif paar == "cC":
        return "Cc"
    elif paar == "dD":
        return "Dd"
    elif paar == "eE":
        return "Ee"
    elif paar == "fF":
        return "Ff"
    elif paar == "gG":
        return "Gg"
    elif paar == "hH":
        return "hH"
    elif paar == "iI":
        return "Ii"
    elif paar == "jJ":
        return "Jj"
    else:
        return paar
    
# NEW kruisen, vullen van de list of lists
def vulKruisingsschema (type,gametenVader, gametenMoeder):
    dimensie, paren = dimensieBepalen(type)
    print (dimensie, paren)  #check
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

# NEW losse functie om dimensies en aantal paren te bepalen aan de hand van het ingevoerde type kruising verbeterd
def dimensieBepalen(type):
    paren = type
    dimensie = 2**paren
    return dimensie, paren

def OLDdimensieBepalen(type):
    if type == "1": #dimensies van het kruisingsschema goedzetten
        dimensie = 2    # ABSTRACTER TE MAKEN MET 2**PAREN!!! scheelt een parameter
        paren = 1
    elif type == "2":
        dimensie = 4 
        paren = 2
    else:
        dimensie = 8  
        paren =3
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
        

# schaalbaar gemaakt met dimensie/paren op basis van type >> verder abstraheren (dimensie = 2**paren)
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

# FUNCTIE VOOR DE TESTRUNS >> dictionary fenotypen en genovader ingevuld

def demo1():
    type, template = invoerKruisingstype()  # template haalt op of het de vorm aa, aabb, of aabbcc moet hebben
    print (type, template)
    #invoer
    fenoDict = {'A':'zwart', 'a':  'rood', 'B' : 'bont', 'b': 'egaal', 'C' : 'gehoornd', 'c' : 'hoornloos'}
    genoVader='AaBbCc'
    genoMoeder = 'AaBbCc'
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
   
    kruisingsschema = vulKruisingsschema (type,gametenVader, gametenMoeder)
    # print(kruisingsschema)
    print ("het kruisingsschema van de kruising", genoVader , "x" ,genoMoeder, "is:")
    printSchema(type, kruisingsschema, gametenVader, gametenMoeder)
    maakFenoArray(kruisingsschema, fenoDict, type)
    fenoSchema=maakFenoArray(kruisingsschema, fenoDict, type)
    print()
    print("op basis van dit kruisingsschema is de verdeling van de fenotypen als volgt: ")
    print()
    printSchema(type, fenoSchema, gametenVader, gametenMoeder)
    
demo1()    

# # FUNCTIE VOOR DE TESTRUNS >> BASIS VOOR DE NIEUWE MAIN() EN MENU()
# def runme():
#     type, template = invoerKruisingstype()  # template haalt op of het de vorm aa, aabb, of aabbcc moet hebben
#     print (type)
#     #invoer
#     fenoDict = invoerFenotypen(type)
#     genoVader=invoerVader(template)
#     genoMoeder = invoerMoeder(template)
#     # verwerking 
#     gametenVader = maakGametenLijst(type, genoVader)
#     gametenMoeder = maakGametenLijst(type, genoMoeder)
#     print()
#     print ("Ingevoerde gegevens in hun de vorm van hun variabelen" ) # misschien leuk om met type ook het type af te drukken
#     print ('fenotype dictionary: ', fenoDict) # dictionary --- op letten bij het vertalen van genotype naar fenotype
#     print ('genovader ', genoVader) #string
#     print ('genomoeder ', genoMoeder) #string
#     print ('genotype gameten vader: ', gametenVader) #array
#     print ('genotype gameten Moeder: ', gametenMoeder) #array
#     print()
#     kruisingsschema = vulKruisingsschema (type,gametenVader, gametenMoeder)
#     print ("het kruisingsschema van deze kruising is")
#     printSchema(type, kruisingsschema, gametenVader, gametenMoeder)
#     # maakFenoArray(kruisingsschema, fenoDict, type)
#     fenoSchema=maakFenoArray(kruisingsschema, fenoDict, type)
#     print()
#     print("op basis van dit kruisingsschema is de verdeling van de fenotypen als volgt (werkt nog niet bij di- en trihybride kruisingen)")
#     print()
#     printSchema(type, fenoSchema, gametenVader, gametenMoeder)
    
# runme()    

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#                                                               NOG AAN TE PASSEN / VERVANGEN  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# menu
# def menu(genoVader, genoMoeder,dominantA,recessiefA,dominantB,recessiefB):
#     print()
#     print ("MENU:")
#     print ('"t" om het type kruising te kiezen')
#     print ('"g" om de allelen binnen de gameten van beide ouders te laten zien')
#     print ('"k" voor het kruisingsschema' )
#     print ('"f" voor fenotypen van de nakomelingen bij deze kruising' )
#     print ('"o" om opnieuw te beginnen, met een nieuwe kruising')
#     print ('"s" om te stoppen')
#     menuInput = input ('voer je keuze in, gevolgd door ENTER: ')
#     if  menuInput == "t":
#         keuze, template = invoerKruisingstype()
#     elif menuInput == "g":
#         gametenPrinten(genoVader, genoMoeder)
#     elif menuInput == "k":
#         kruisingsschemaPrinten(genoVader, genoMoeder)
#     elif menuInput == "f": 
#         schemaTranslate(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)
#     elif menuInput == "o":
#         main() 
#     elif menuInput == "s":
#         return "stop"
#     else:
#         menu(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB)


# def bye():
#     print ("Bedankt voor het gebruik van dit programma")
#     print ("Veel succes met het nog meer leren over genetica")
   

# MAIN, UITGESCHAKELD OM DE FUNCTIES TE TESTEN
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





# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#                                                               RECYCLE BIN   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# vervangen code:
# # NEW keuzemenu kruisingstypen en template vullen
# def invoerKruisingstypeOUD():
#     keuze = None
#     while keuze not in ["m", "d", "t"]:
#         keuze = input ('Kies "m" voor een monohybride, "d" voor een dihybride of "t" voor een trihybride kruising :')
#         if keuze == "m":
#             template = "aa"
#         elif keuze == "d":
#             template = "aabb"
#         elif keuze == "t":
#             template = "aabbcc"
#         else:
#             print ('kies "m", "d" of "t:')
#     return keuze, template


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

# # kruisen, vullen van de list of lists
# def vulKruisingsschema (gametenVader, gametenMoeder):
#     kruisingsschema =[]  
#     for v in range (4):
#         rij =[]
#         for m in range(4):
#             gametenPa = gametenVader[v]
#             gametenMa= gametenMoeder[m]
#             # volgorde grote en kleine letters goedzetten
#             if (gametenPa[0] == 'a') and (gametenMa[0] =='A'):
#                 paar1 = gametenMa[0]+gametenPa[0]
#             else:
#                 paar1 = gametenPa[0] + gametenMa[0]
#             if (gametenPa[1] == 'b') and (gametenMa[1] =='B'):
#                 paar2 = gametenMa[1]+gametenPa[1]
#             else:
#                 paar2 = gametenPa[1] + gametenMa[1]          
#             genoKind = paar1 + paar2
#             rij.append(genoKind)
#             # print (rij[m])
#         kruisingsschema.append(rij)
#         # print (kruisingsschema)
#     return (kruisingsschema)

# MISSCHIEN NOG DEELS RECYCLEN
# oude verzamelfunctie eruit omdat dan dingen dubbel gebeuren?
# def kruisingsschemaPrinten(genoVader, genoMoeder):
#     print("\033c", end="") # ansi escapecodes om venster leeg te trappen
#     print ("Kruisingsschema bij de kruising", genoVader, " x ", genoMoeder)
#     print ()
#     gametenVader = maakGametenLijst(genoVader)
#     gametenMoeder = maakGametenLijst(genoMoeder)
#     kruisingsschema = vulKruisingsschema(gametenVader,gametenMoeder)
#     printSchema (kruisingsschema,gametenVader,gametenMoeder)
#     print()

# # OUD
# def gametenPrinten(genoVader,genoMoeder):
#     print("\033c", end="") # ansi escapecodes om venster leeg te trappen
#     print ("Gameten van de ouders bij de kruising", genoVader, " x ", genoMoeder)
#     print ()
#     gametenVader = maakGametenLijst(genoVader)
#     gametenMoeder = maakGametenLijst(genoMoeder)
#     print ('gameten van vader:  ',gametenVader)
#     print ('gameten van moeder: ',gametenMoeder)

# OUDE manier om genotype vertalen naar fenotype .. vervangen door met dictionary waarden in list of lists vervangen
# def translateFenotype(genotype, dominantA,  recessiefA, dominantB, recessiefB):
#     if genotype == "aabb":
#         feno = recessiefA + "-" + recessiefB
#         return feno
#     elif genotype[:1]=="aa" and genotype[2] =="B":
#         feno = recessiefA + "-" + dominantB
#         return feno
#     elif genotype[0] == "A"and genotype[2:]=="bb":
#         feno = dominantA + "-" + recessiefB
#         return feno
#     else: 
#         feno = dominantA + "-" + dominantB
#         return feno

# OUD kruisingsschema vullen, ieder genotype naar de vertaler sturen, de placeholders voor fenotype printen in het schema
# def schemaTranslate(genoVader, genoMoeder, dominantA,recessiefA,dominantB,recessiefB):
#     print("\033c", end="") # ansi escapecodes om venster leeg te trappen
#     print ("fenotype printen")
#     print()
#     gametenVader = maakGametenLijst(genoVader)
#     gametenMoeder = maakGametenLijst(genoMoeder)
#     kruisingsschema = vulKruisingsschema(gametenVader,gametenMoeder)
#     print ("   ", "|", end='')
#     for gameet in gametenVader:
#         print ("       ",gameet.ljust(6), " |", end='')
#     print()
#     print ("-" * 72 )
#     for i in range (4):
#         print (gametenMoeder[i], " |",end='')
#         for j in range (4):
#             fenotype=translateFenotype(kruisingsschema[i][j],dominantA,recessiefA,dominantB,recessiefB)
#             print (fenotype.rjust(15), "|", end='')
#         print()
#         print ("-" * 72 )