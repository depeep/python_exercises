'''Zoveel mogelijk variabelen in deze module zetten die betrekking hebben op de instellingen van de test, zodat ze makkelijk aan te passen zijn zonder dat je door de hele code hoeft te zoeken.
TODO Nice to have: misschien sommige van deze variabelen laten aanpassen via de GUI, 
zoals de grootte van het raster, de tijd dat de vierkanten zichtbaar zijn, etc. Dan methoden  toevoegen aan deze Config klasse om die variabelen aan te passen en op te halen.'''

class Config: 
    def __init__(self):  
        # show and click  
        self.__maxLevels = 12 
        self.__timeVisible=500
        self.__timeBetween = 500
        # guisettings
        self.__basislettertype =  ("Arial", 20, "bold")
        self.__windowGeometry = "1920x900"
        self.__canvasWidth = 1200
        self.__canvasHeight = 700
        # squares horizontal
        self.__size = 6 #aantal vierkanten op een rij



    def getStartTestSettings(self):
        settings = (self.__maxLevels, self.__timeVisible, self.__timeBetween)
        return settings
    
    def getWindowConfig(self):
        settings= (self.__windowGeometry, self.__canvasWidth, self.__canvasHeight, self.__basislettertype )
        return settings
    
    def getSize(self):
        settings=self.__size
        return settings
    
    def setSize(self,size):
        self.__size = size
        # mocht ik het aantal vierkanten in het venster zelf willen veranderen met een knopje of zo
        

