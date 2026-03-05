def cleanUp(rawData):
    while rawData[0] == None:
        del (rawData [0])
    print (rawData)
    while (rawData[-1]== None):
        del (rawData[-1])
    print (rawData)

                

    while None in rawData:
        positie = rawData.index(None)
        print(positie)
        getalVoor = rawData[positie - 1]
        print (getalVoor)
        getalNa = rawData[positie + 1]
        while getalNa != None:
            del (rawData[positie])
            nieuwGetal = (getalVoor + getalNa)/2  #interpoleren
            rawData.insert(positie,  nieuwGetal)

        # print (getalNa)
        # if getalNa != None:  
        #     nieuwGetal = (getalVoor + getalNa)/2  #interpoleren
        #     rawData[positie] = nieuwGetal
        # else:
        #     del(getalNa) #meerder instanties van None na elkaar verwijderen
              
    
    return rawData

       
 

rawData = [None, None, 1.0, 4.0, None, 6.0, 8.0, None, None, 10.0, None]

print ('Çleaned up data')
print()
print (cleanUp(rawData))


Werkt nog niet naar behoren