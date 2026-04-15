import tkinter
import random

class MemoryTestWindow:
    def __init__(self):
        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("Memory Test")
        self.mainWindow.geometry("1920x900")
        # self.mainWindow.configure(bg="lightgray") #niet nodig
        basisLettertype = ("Arial", 20, "bold") #niet nodig, kan per widget worden ingesteld maar handiger hier zodat het overal hetzelfde is


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
        self.StartButton = tkinter.Button(self.bottomframe, text="Start", font =basisLettertype, command=self.startTest)
        self.StartButton.pack(side='left', pady=10)
        self.timeVisibleLabel = tkinter.Label(self.bottomframe, text="ms visible", font =basisLettertype) 
        self.timeVisibleLabel.pack(side='left', pady=20)
        self.timeVisibleValueLabel = tkinter.Label(self.bottomframe, text="500", font =basisLettertype) 
        self.timeVisibleValueLabel.pack(side='left', pady=20)
        self.timeBetweenLabel = tkinter.Label(self.bottomframe, text="ms between", font =basisLettertype) 
        self.timeBetweenLabel.pack(side='left', pady=20)
        self.timeBetweenValueLabel = tkinter.Label(self.bottomframe, text="500", font =basisLettertype) 
        self.timeBetweenValueLabel.pack(side='left', pady=20)
        self.sequenceLengthLabel = tkinter.Label(self.bottomframe, text="Sequence length", font =basisLettertype) 
        self.sequenceLengthLabel.pack(side='left', pady=20)  
        self.sequenceLengthValueLabel = tkinter.Label(self.bottomframe, text="3", font =basisLettertype ) 
        self.sequenceLengthValueLabel.pack(side='left', pady=20)

        self.canvas = tkinter.Canvas(self.middleframe, width = 1200, height = 700)     #niet de lekkerste maten om netjes te verdelen  TODO: aanpassen, misschien in de vulling
        self.canvas.config(bg="white")
        self.canvas.pack()                 
          

        tkinter.mainloop()
    
    def startTest(self):
        self.countDown(3)  #tijd meegeven voor de countdown, nu 5 seconden
        vierkanten = self.prepareObservationPhase() # prepareObservationPhase() returnt de vierkanten zodat ze kunnen worden gebruikt in runObservationPhase() om ze te verbergen/tonen
        getoondeReeks =self.runObservationPhase(vierkanten)   
        userSequence =self.userResponsePhase(vierkanten)
        self.checkUserResponse(userSequence, getoondeReeks)  

    def countDown(self, time):  
        message = "Counting down:" 
        for i in range (time+1, 0, -1):
            message = "Counting down: " + "." * (i-1) #(verdwijnende stippen)
            self.statusInfoLabel.config(text=message)# )
            self.statusInfoLabel.update()  # overbodig?
            self.statusInfoLabel.after(1000) 

    def prepareObservationPhase(self):
        self.canvas.delete("all")  # Canvas leegmaken voordat de vierkanten worden getoond, zodat er geen oude vierkanten blijven staan als de test opnieuw wordt gestart
        self.statusInfoLabel.config(text="Watch the sequence!") 
        roodVierkant =  Vierkant(self.canvas, 300, 25, "red", 300)  # kan nog verder worden geparametriseerd zodat het makkelijker is om de grootte en positie van de vakken aan te passen
        blauwVierkant = Vierkant(self.canvas, 625, 25, "blue", 300)
        groenVierkant = Vierkant(self.canvas, 300, 375, "green", 300)
        geelVierkant = Vierkant(self.canvas, 625, 375, "yellow", 300)
        roodVierkant.show() 
        blauwVierkant.show()
        groenVierkant.show()
        geelVierkant.show()
        self.canvas.update()  #bijwerken om de vierkanten te laten zien
        return [roodVierkant, blauwVierkant, groenVierkant, geelVierkant]

    def runObservationPhase(self, vierkanten):
        getoondeReeks =[]
        for i in range(3):  #aantal vakken in de sequence, nu 3 maar dit kan worden aangepast naar een variabele die wordt ingesteld in de GUI
            nummer = random.randint(0, 3)  #  random index voor de vierkanten, nu 6 omdat er 6 vakken in de sequence moeten worden getoond, maar dit kan worden aangepast naar een variabele die wordt ingesteld in de GUI 
            getoondeReeks.append(nummer)
            self.canvas.after(500)  # wacht 500ms
            vierkanten[nummer].hide()
            self.canvas.update()  # weergave bijwerken
            self.canvas.after(500)  
            vierkanten[nummer].show()
            self.canvas.update()  
        # tijdelijk sequence tonen, later verwijderen
        # self.statusInfoLabel.config(text="The sequence was: " + str(getoondeReeks))  # Update the status label to show the sequence that was displayed, TODO: remove this line later, nu alleen voor testdoeleinden
        return getoondeReeks

    def userResponsePhase(self, vierkanten):
        self.statusInfoLabel.config(text="Repeat the sequence by clicking the squares in the correct order!")
        userSequence = []
        while len(userSequence) < 3 : #len(getoondeReeks): #nog parametriseren en meenemen in de aanroep
            # self.statusInfoLabel.config(text="usersequence: " + str(userSequence) + " Length: " + str(len(userSequence))) # voor testdoeleinden, toont de huidige userSequence en de lengte ervan, TODO: weghalen als het goed werkt
            for vierkant in vierkanten:
                vierkant.show() 
                # complexe suggestie van VS-code: bind een click event aan elk vierkant dat de index van het vierkant doorgeeft aan een handler functie die de userSequence bijwerkt en de status label update. 
                # MISSCHIEN KAN HET BINDEN VAN DE EVENTS BETER IN EEN APARTE FUNCTIE DIE WORDT AANGEROEPEN NA DE OBSERVATION PHASE, ZODAT DE EVENTS PAS WORDEN GEBIND NA DAT DE VIERKANTEN VOOR HET EERST ZIJN GETOOND, 
                # OM TE VOORKOMEN DAT ER AL CLICK EVENTS WORDEN OPGEVANGEN TIJDENS DE OBSERVATION PHASE
                vierkant.canvas.tag_bind(vierkant.canvas.create_rectangle(vierkant.x1, vierkant.y1, vierkant.x2, vierkant.y2, fill=vierkant.color, outline=vierkant.color), "<Button-1>", lambda event, index=vierkanten.index(vierkant): self.handleSquareClick(vierkanten,index, userSequence))  # Bind a click event to each square to handle user responses, TODO: implement the handleSquareClick method to record user responses and check them against the correct sequence
            self.canvas.update()  
            # print("User sequence: " + str(userSequence))  # Print userSquence naar de console voor testdoeleinden, TODO: remove this line later
        return userSequence

    def checkUserResponse(self, userSequence, getoondeReeks):
        if userSequence == getoondeReeks:
            self.statusInfoLabel.config(text="Correct! You repeated the sequence correctly.") 
        else:
            self.statusInfoLabel.config(text="Incorrect. You typed: " + str(userSequence) + ". The correct sequence was: " + str(getoondeReeks))
        
    
    def handleSquareClick(self, vierkanten, nummer, userSequence):
        userSequence.append(nummer)
        self.statusInfoLabel.config(text="You clicked square index: " + str(nummer))  # Update the status label to show which square was clicked, TODO: implement this method to record user responses and check them against the correct sequence
        vierkanten[nummer].hide()  
        self.canvas.update()  
        self.canvas.after(500) 
        vierkanten[nummer].show()
        self.canvas.update()  
        # self.statusInfoLabel.config(text="Current user sequence: " + str(userSequence))  # Update the status label to show the current user sequence, TODO: update this message to be more user-friendly
        return userSequence     
 

class Vierkant:
    def __init__(self, canvas, x1, y1, color, zijdeLengte):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + zijdeLengte
        self.y2 = y1 + zijdeLengte
        self.color = color

    def hide(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white", outline="white")  # rechthoek verwijderen door hem wit te maken
    
    def show(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.color)   


if __name__ == "__main__":
    my_gui = MemoryTestWindow()
