def cleanUp(rawData):
    while rawData[0] == None:
        del (rawData [0])
    print (rawData)
    while (rawData[-1]== None):
        del (rawData[-1])
    print (rawData)

                

    if None in rawData:
        positie = rawData.index(None)
        getalNone = rawData[positie]
        print(positie)
        print(getalNone)
        getalVoorNone = rawData[positie - 1]
        print (getalVoorNone)
        getalNaNone = rawData[positie + 1]
        print (getalNaNone)
        if getalNaNone != None:
            print (rawData[positie])
            del rawData[positie]
            nieuwGetal = (getalVoorNone + getalNaNone)/2  #interpoleren
            rawData.insert(positie,  nieuwGetal)
        else:
            del getalNone #meerder instanties van None na elkaar verwijderen
              
    
    return rawData

       
 

rawData = [None, None, 1.0, 4.0, None, 6.0, 8.0, None, None, 10.0, None]

print ('Çleaned up data')
print()
print (cleanUp(rawData))


# Werkt nog niet naar behoren