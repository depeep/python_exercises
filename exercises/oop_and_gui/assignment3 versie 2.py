import tkinter
import time
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
        # self.StartButton = tkinter.Button(self.mainWindow, text="Start", command=self.startTest)
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
        self.countDown(2)  #tijd meegeven voor de countdown, nu 5 seconden
        self.vierkanten = self.prepareObservationPhase() # prepareObservationPhase() returnt de vierkanten zodat ze kunnen worden gebruikt in runObservationPhase() om ze te verbergen/tonen
        self.runObservationPhase(self.vierkanten) 
        self.userResponsePhase()  


    def countDown(self, time):  
        message = "Counting down:" 
        for i in range (time+1, 0, -1):
            message = "Counting down: " + "." * (i-1) #("." * time)  # Add dots to indicate the countdown
            self.statusInfoLabel.config(text=message)# self.updateStatus(message)
            self.statusInfoLabel.update()  # Update the GUI to show the new message
            self.statusInfoLabel.after(1000)  # Wait for 1 second

    def fillCanvas(self):
        self.canvas.delete("all")  # Clear the canvas for the new phase
        self.roodVierkant =  Vierkant(self.canvas, 300, 25, "red", 300)  # kan nog verder worden geparametriseerd zodat het makkelijker is om de grootte en positie van de vakken aan te passen
        self.blauwVierkant = Vierkant(self.canvas, 625, 25, "blue", 300)
        self.groenVierkant = Vierkant(self.canvas, 300, 375, "green", 300)
        self.geelVierkant = Vierkant(self.canvas, 625, 375, "yellow", 300)
        self.roodVierkant.show() 
        self.blauwVierkant.show()
        self.groenVierkant.show()
        self.geelVierkant.show()
        self.canvas.update()  # Update the canvas to show the new rectangles
        return [self.roodVierkant, self.blauwVierkant, self.groenVierkant, self.geelVierkant]

    def prepareObservationPhase(self):
        self.statusInfoLabel.config(text="Watch the sequence!") 
        self.vierkanten= self.fillCanvas() 
        return self.vierkanten
       

    def runObservationPhase(self, vierkanten):
        getoondeReeks =[]
        for i in range(6):
            nummer = random.randint(0, 3)  # Get a random index for the rectangles  
            getoondeReeks.append(nummer)
            self.canvas.after(500)  # Wait for 500 milliseconds before hiding the rectangles, nu 500ms
            vierkanten[nummer].hide()
            self.canvas.update()  # Update the canvas to show the changes
            self.canvas.after(500)  # Wait for 500   milliseconds before hiding the rectangles,
            vierkanten[nummer].show()
            self.canvas.update()  # Update the canvas to show the changes
        # tijdelijk getoonde reeks tonen, later verwijderen
        self.statusInfoLabel.config(text="The sequence was: " + str(getoondeReeks))  # Update the status label to show the sequence that was displayed, TODO: remove this line later, nu alleen voor testdoeleinden

    def userResponsePhase(self):
        # TODO: draw squares, record clicks on square, hide/show squares on click, return userResponse
        self.statusInfoLabel.config(text="repeat the sequence by clicking the squares in the correct order!")  # Update the status label to prompt the user to repeat the sequence, TODO: update this message to be more user-friendly
        self.roodVierkant.bind("<Button-1>", lambda event: self.handleSquareClick(0))  # Set the command for the red square to handle clicks, TODO: implement handleSquareClick() to record user responses
        self.blauwVierkant.bind("<Button-1>", lambda event: self.handleSquareClick(1))  # Set the command for the blue square to handle clicks
        self.groenVierkant.bind("<Button-1>", lambda event: self.handleSquareClick(2))  # Set the command for the green square to handle clicks
        self.geelVierkant.bind("<Button-1>", lambda event: self.handleSquareClick(3))  # Set the command for the yellow square to handle clicks   
          # Example of how to handle a click on the red square, this should be implemented for all squares and should record the user's response    

        
        return
    
    def handleSquareClick(self, squareIndex):
        self.statusInfoLabel.config(text="You clicked square index: " + str(squareIndex))  # Update the status label to show which square was clicked, TODO: remove this line later, nu alleen voor testdoeleinden
        self.vierkanten[squareIndex].hide()  # Hide the clicked square


    def checkUserResponse(self, userResponse, correctSequence):
        # TODO: compare userResponse with correctSequence, update statusInfoLabel with result
        return

        

        # hardcoded zonder objecten
        # self.canvas.create_rectangle(300, 25, 600, 350, fill="blue")   # >>>>naar een aparte class/object? en parametriseren zodat het makkelijker is om de grootte en positie van de vakken aan te passen 
        # self.canvas.create_rectangle(625, 25, 925, 350, fill="red")
        # self.canvas.create_rectangle(300, 375, 600, 675, fill="green")
        # self.canvas.create_rectangle(625, 375, 925, 675, fill="yellow")
        # self.statusInfoLabel.update()  # Update the GUI to show the new message # wordt toch weergegeven dus niet nodig

class Vierkant:
    def __init__(self, canvas, x1, y1, color, zijdeLengte):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + zijdeLengte
        self.y2 = y1 + zijdeLengte
        self.color = color

    def hide(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white", outline="white")  # Clear the rectangle by filling it with white
    
    def show(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.color)  # Draw the rectangle with the specified color
    

if __name__ == "__main__":
    my_gui = MemoryTestWindow()
