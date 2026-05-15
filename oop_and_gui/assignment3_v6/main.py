''' Memory Test Game
versie 6, 2026-05-15
Functioneel tot en met opdracht 8 (levels toegevoegd, schaalbaar gemaakt)
NB geel is superhinderlijk bij grotere aantallen, daar is één kleur eigenlijk veel makkelijker. 
Wat ik zelf ook nog irritant vind is bij ieder level een nieuwe kleuren layout => de kleurdoos eerder aan laten maken, bijvoorbeeld na aanklikken start.>> DONE
losse functies waar code te uitgebreid is (startTest!!!), netjes opsplitsen in meerdere bestanden. >> DONEan
Parameters als dimensie en sequenceLength netjes bij elkaar. >> in config>> DONE
DRYer maken. >> DONE, functies als BlinkSquare() en handleSquareClick() maken het geheel al een stuk DRYer, maar er is nog steeds wat herhaling in de code, bijvoorbeeld in prepareObservationPhase() en userResponsePhase(), dit kan worden verbeterd door meer functies te maken die specifieke taken uitvoeren, zoals het tonen van de vierkanten, het verbergen van de vierkanten, het bijwerken van de statuslabel, etc.  
Eventueel een knopje of keuzelijstje erbij voor de dimensies. TODO nice to have
Tekst onderaan nog mee laten gaan met dimensies enz.>> DONE 
klassendiagrammen enz reverse engineeren DONE
pytest testbestanden aanmaken DONE, maar nog beperkt, alleen checkUserResponse() met de hand geschreven. 
de directory test bevat voorbeelden van uitgebreidere tests die door AI gegenereerd zijn op basis van de code in de modules, klassen en methoden
'''

import tkinter
import random 
import config
import vormen
from kleurdoos import  vulKleurdoos

config = config.Config()

class MemoryTestWindow:
    def __init__(self):
        
        windowGeometry, canvasWidth, canvasHeight, basisLettertype = config.getWindowConfig()
        maxLevels, timeVisible, timeBetween = config.getStartTestSettings()#maxLevels wordt hier nog niet gebruikt.
        size = config.getSize()
        sizeLabelText = (size, "x", size)
        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("Memory Test")
        self.mainWindow.geometry(windowGeometry)
       
        # Create frames for better organization of widgets
        self.topframe = tkinter.Frame(self.mainWindow)
        self.topframe.pack(side=tkinter.TOP)
        self.middleframe = tkinter.Frame(self.mainWindow)
        self.middleframe.pack(side=tkinter.TOP)
        self.bottomframe = tkinter.Frame(self.mainWindow)
        self.bottomframe.pack(side=tkinter.BOTTOM)

        # Create and pack the widgets in the top frame
        self.statusInfoLabel = tkinter.Label(self.topframe, text="Click start to begin the memory test.", font=basisLettertype) 
        self.statusInfoLabel.pack(pady=20)

        # Create and pack the widgets in the bottom frame
        self.StartButton = tkinter.Button(self.bottomframe, text="Start", font =basisLettertype, command=self.runTest)
        self.StartButton.pack(side='left', pady=10)
        self.timeVisibleLabel = tkinter.Label(self.bottomframe, text="ms visible", font =basisLettertype) 
        self.timeVisibleLabel.pack(side='left', pady=20)
        self.timeVisibleValueLabel = tkinter.Label(self.bottomframe, text=str(timeVisible), font =basisLettertype) 
        self.timeVisibleValueLabel.pack(side='left', pady=20)
        self.timeBetweenLabel = tkinter.Label(self.bottomframe, text="ms between", font =basisLettertype) 
        self.timeBetweenLabel.pack(side='left', pady=20)
        self.timeBetweenValueLabel = tkinter.Label(self.bottomframe, text=str(timeBetween), font =basisLettertype) 
        self.timeBetweenValueLabel.pack(side='left', pady=20)
        self.sequenceLengthLabel = tkinter.Label(self.bottomframe, text="Sequence length", font =basisLettertype) 
        self.sequenceLengthLabel.pack(side='left', pady=20)  
        self.sequenceLengthValueLabel = tkinter.Label(self.bottomframe, text="1", font =basisLettertype ) 
        self.sequenceLengthValueLabel.pack(side='left', pady=20)
        self.sequenceSizeLabel = tkinter.Label(self.bottomframe, text="Size", font =basisLettertype ) 
        self.sequenceSizeLabel.pack(side='left', pady=20)
        self.sequenceSizeValueLabel = tkinter.Label(self.bottomframe, text= sizeLabelText, font =basisLettertype ) 
        self.sequenceSizeValueLabel.pack(side='left', pady=20)

        self.canvas = tkinter.Canvas(self.middleframe, width = canvasWidth, height = canvasHeight)    
        self.canvas.config(bg="white")
        self.canvas.pack()                 
          
        tkinter.mainloop()
    
    def runTest(self):
        size = config.getSize()
        kleurdoos= vulKleurdoos(size*size)
        self.countDown(3)  #tijd meegeven voor de countdown, nu 3 seconden TODO naar config.py
        maxLevels, timeVisible, timeBetween = config.getStartTestSettings()
        for level in range (maxLevels): # TODO naar aparte functie?
            vierkanten = self.prepareObservationPhase(kleurdoos) # prepareObservationPhase() returnt de vierkanten zodat ze kunnen worden gebruikt in runObservationPhase() om ze te verbergen/tonen
            getoondeReeks =self.runObservationPhase(vierkanten, level+1, timeVisible, timeBetween) # runObservationPhase() returnt de getoondeReeks zodat deze kan worden vergeleken met de userSequence in checkUserResponse(), parameters voor lengte van de sequence en tijd dat de vakken zichtbaar zijn en tijd tussen het tonen van de vakken, nu hardcoded maar dit kan worden aangepast naar variabelen die worden ingesteld in de GUI
            userSequence =self.userResponsePhase(vierkanten, level+1) # userResponsePhase() returnt de userSequence zodat deze kan worden vergeleken met de getoondeReeks in checkUserResponse(), parameter voor lengte van de sequence, nu hardcoded maar dit kan worden aangepast naar een variabele die wordt ingesteld in de GUI
            result =self.checkUserResponse(userSequence, getoondeReeks)  
            if result == True:
                self.statusInfoLabel.config(text="Correct!")  
                self.canvas.update()
                self.canvas.after(1000)  # geeft gebruiker tijd heeft om zich voor te bereiden (=>variabele van maken in config of GUI?)
            else:
                self.statusInfoLabel.config(text="Incorrect. You reached level " + str(level+1) + " Click start to try again.")  
                break  

    def countDown(self, time):  
        message = "Counting down:" 
        for i in range (time+1, 0, -1):
            message = "Counting down: " + "." * (i-1) #(verdwijnende stippen)
            self.statusInfoLabel.config(text=message)# )
            self.statusInfoLabel.update() 
            self.statusInfoLabel.after(1000) 

# NEW schaalbaar gemaakt, TODO eventueel verder parametriseren van de getallen en die in de config.py module stoppen
#   Vervolgens  met formules die het geheel passend houden bij andere dimensies van het venster en het canvas. 
    def prepareObservationPhase(self, kleurdoos):
        self.canvas.delete("all")  # Canvas leegmaken voordat de vierkanten worden getoond, zodat er geen oude vierkanten blijven staan als de test opnieuw wordt gestart
        self.statusInfoLabel.config(text="Get ready!") 
        size= config.getSize()
        zijde = 600/size
        vierkanten = []
        kleurnummer = 0
        for horizontaal in range (size):
            for verticaal in range (size):
                kleur = kleurdoos[kleurnummer]
                x= 300 + zijde *horizontaal
                y= 50 + zijde * verticaal
                vierkant = vormen.Vierkant(self.canvas, x, y, kleur, zijde -10)
                vierkant.show()
                vierkanten.append(vierkant)
                kleurnummer += 1
        self.canvas.update()  #bijwerken om de vierkanten te laten zien  
        # print (vierkanten) 
        return vierkanten

#   NEW schaalbaar gemaakt voor meerdere levels en tijd  toegevoegd als parameters
    def runObservationPhase(self, vierkanten, sequenceLength, timeVisible, timeBetween):
        getoondeReeks =[]
        self.statusInfoLabel.config(text="Get ready for level: " + str(sequenceLength))  
        self.sequenceLengthValueLabel.config(text = str(sequenceLength))
        self.canvas.update()
        self.canvas.after(1000)  
        aantalNummers = (len(vierkanten)-1)
        for i in range(sequenceLength):  
            nummer = random.randint(0, aantalNummers)  
            getoondeReeks.append(nummer)
            self.BlinkSquare(vierkanten, nummer, timeVisible)
            self.canvas.after(timeBetween)
        return getoondeReeks
    
    def BlinkSquare(self, vierkanten, nummer, timeVisible):
        vierkanten[nummer].hide()
        self.canvas.update()  
        self.canvas.after(timeVisible)  
        vierkanten[nummer].show()
        self.canvas.update()
        

    def userResponsePhase(self, vierkanten, sequenceLength):
        self.statusInfoLabel.config(text="Repeat the sequence by clicking the squares in the correct order!")
        userSequence = []
        while len(userSequence) < sequenceLength : 
            for vierkant in vierkanten:
                vierkant.show() 
                vierkant.canvas.tag_bind(vierkant.canvas.create_rectangle(vierkant.x1, vierkant.y1, vierkant.x2, vierkant.y2, fill=vierkant.color, outline=vierkant.color), "<Button-1>", lambda event, index=vierkanten.index(vierkant): self.handleSquareClick(vierkanten,index, userSequence))  # Bind a click event to each square to handle user responses, TODO: implement the handleSquareClick method to record user responses and check them against the correct sequence
            self.canvas.update()  
        return userSequence 
           

    def checkUserResponse(self, userSequence, getoondeReeks):
        if userSequence == getoondeReeks:
            self.canvas.after(500)  # wacht 0,5 seconden voordat het volgende level begint, TODO naar config.py of GUI variabele
            return True
        else:
            return False
        
   
    def handleSquareClick(self, vierkanten, nummer, userSequence):
        userSequence.append(nummer)
        self.BlinkSquare(vierkanten, nummer, 500) # tijd dat het vakje knippert als de gebruiker erop klikt, nu nog hardcoded op 500ms TODO naar config.py of GUI variabele
        return userSequence     

    
# class Vierkant: >> verplaatst naar module "vormen"
 


if __name__ == "__main__":
    my_gui = MemoryTestWindow()

