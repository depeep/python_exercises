# # empty window 13-2

# import tkinter

# def main():
#     mainWindow = tkinter.Tk()
#     mainWindow.mainloop() 

# if __name__ == "__main__":
#     main()

# ###########################################################################

# # OO version 13-3
# import tkinter

# class MyGui:
#     def __init__(self):

#         self.mainWindow = tkinter.Tk()
#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGui()

# ###########################################################################

# # 13-3 window with title
# import tkinter

# class MyGui:
#     def __init__(self):

#         self.mainWindow = tkinter.Tk()
#         self.mainWindow.title("My First GUI")
#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGui()

# ###########################################################################    

# # 13-4  text with labelwidgets met extra

# import tkinter
# class MyGui:
#     def __init__(self, tekst2):

#         self.mainWindow = tkinter.Tk()
#         self.mainWindow.title("My First GUI")

#         self.label1 = tkinter.Label(self.mainWindow, text="Hello World")
#         self.label2 = tkinter.Label(self.mainWindow, text=tekst2)

#         self.label1.pack(side = 'left')
#         self.label2.pack(side = 'left')

#         tkinter.mainloop()  

# if __name__ == "__main__":
#     my_gui = MyGui("Welcome to Python Programming!")

# ###########################################################################    

# # 13-5 two labels with text
# import tkinter
# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.label1 = tkinter.Label(self.mainWindow, text = "Hello world!")
#         self.label2 = tkinter.Label(self.mainWindow, text = 'this is my gui-program')

#         self.label1.pack()
#         self.label2.pack()

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()

# ###########################################################################    

# 13.6 layout veranderen met pack, side = 'left' of 'right', left laat ze achter elkaar doorlopen, 
# right laat ze achter elkaar lopen maar dan van rechts naar links (andere volgorde). Left is standaard volgorde, right is omgekeerde volgorde.
# import tkinter
# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.label1 = tkinter.Label(self.mainWindow, text = "Hello world!")
#         self.label2 = tkinter.Label(self.mainWindow, text = 'this is my gui-program')

#         self.label1.pack(side = 'left')
#         self.label2.pack(side = 'left')

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()


# ###########################################################################    

# borders toevoegen aan labels, met borderwidth en relief, borderwidth geeft de dikte van de border aan, relief geeft het type border aan, bijvoorbeeld 'sunken' of 'raised'

# import tkinter
# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.label1 = tkinter.Label(self.mainWindow, text = "Hello world!", borderwidth = 1, relief = 'solid')
#         self.label2 = tkinter.Label(self.mainWindow, text = 'this is my gui-program', borderwidth = 2, relief = 'sunken')
#         # opties voor relief zijn: 'flat', 'raised', 'sunken', 'groove', 'ridge', 'solid'
#         self.label1.pack()
#         self.label2.pack()

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()


# ###########################################################################    
# 13-7 padding (internal)

# import tkinter
# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.label1 = tkinter.Label(self.mainWindow, text = "Hello world!", borderwidth = 1, relief = 'solid')
#         self.label2 = tkinter.Label(self.mainWindow, text = 'this is my gui-program', borderwidth = 2, relief = 'sunken')
        
#         self.label1.pack(ipadx=20, ipady=20)
#         self.label2.pack(ipadx=20, ipady=20)
   

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()
# ###########################################################################    

# # 13-8 padding external toevoegen
# import tkinter
# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.label1 = tkinter.Label(self.mainWindow, text = "Hello world!", borderwidth = 1, relief = 'solid')
#         self.label2 = tkinter.Label(self.mainWindow, text = 'this is my gui-program', borderwidth = 2, relief = 'sunken')
        
#         self.label1.pack(ipadx=20, ipady=20, padx=10, pady=10)
#         self.label2.pack(ipadx=20, ipady=20, padx=(10, 20), pady=(20,5)) 
#         # padx en pady kunnen ook een tuple zijn, waarbij de eerste waarde de padding aan de linkerkant is 
#         # en de tweede waarde de padding aan de rechterkant, hetzelfde geldt voor pady, 
#         # waarbij de eerste waarde de padding aan de bovenkant is en de tweede waarde de padding aan de onderkant.
   

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()

# ###########################################################################    
# 
#  13-9 widgets in frames
# import tkinter
# class MyGUI:    
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.topframe = tkinter.Frame(self.mainWindow, border=1 , relief='sunken')
#         self.bottomframe = tkinter.Frame(self.mainWindow)

#         self.label1 = tkinter.Label(self.topframe, text = "Hello world!", borderwidth = 1, relief = 'solid')
#         self.label2 = tkinter.Label(self.topframe, text = 'this is my gui-program', borderwidth = 2, relief = 'sunken')

#         self.label3 = tkinter.Label(self.bottomframe, text = 'This is another frame', borderwidth = 3, relief = 'raised')
#         self.label4 = tkinter.Label(self.bottomframe, text = 'with more widgets', borderwidth = 4, relief = 'groove')

#         self.label1.pack(side= 'top',padx=20, pady=20)
#         self.label2.pack(side= 'top', padx=20, pady=20)
#         self.label3.pack(side = 'left', padx=10, pady=10)
#         self.label4.pack(side= 'left')
    

#         self.topframe.pack(padx=20, pady=20,ipadx=10, ipady=10)
#         self.bottomframe.pack(padx=10, pady=10,ipadx=10, ipady=10   )

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_gui = MyGUI()

##############################################################################################

# button en dialogvenster toevoegen, met een button en een messagebox, de button heeft een command die een functie aanroept die een messagebox laat zien

# import tkinter
# from tkinter import messagebox  

# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.myButton = tkinter.Button(self.mainWindow, text="Click me!", command=self.show_message)
#         self.myButton.pack()
#         tkinter.mainloop()

#     def show_message(self):
#         messagebox.showinfo("Information", "You clicked the button!")


# if __name__ == "__main__":
#     my_gui = MyGUI()

##############################################################################################
# quit button toevoegen, met een button die de mainloop stopt en het venster sluit
# import tkinter
# import tkinter.messagebox #andere manier om messagebox te importeren

# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.myButton = tkinter.Button(self.mainWindow, text="Click me!", command=self.show_message)
#         self.quitButton = tkinter.Button(self.mainWindow, text="Quit", command=self.mainWindow.destroy) 
#         #destroy had ook kunnen zijn quit, maar destroy sluit het venster en quit stopt de mainloop, beide werken hier
#         self.myButton.pack()
#         self.quitButton.pack()
#         tkinter.mainloop()

#     def show_message(self):
#         tkinter.messagebox.showinfo("Information", "You clicked the button!")   

# if __name__ == "__main__":
#     my_gui = MyGUI()

##############################################################################################

# Entry widget
# import tkinter
# import tkinter.messagebox


# class MyGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.topFrame = tkinter.Frame(self.mainWindow)
#         self.bottomFrame = tkinter.Frame(self.mainWindow)
#         self.promptLabel = tkinter.Label(self.topFrame, text="Enter distance in kilometers:")
#         self.kiloEntry = tkinter.Entry(self.topFrame, width=10)
#         self.calcButton = tkinter.Button(self.bottomFrame, text="Convert", command=self.convert)
#         self.quitButton= tkinter.Button(self.bottomFrame, text="Quit", command=self.mainWindow.destroy)

#         self.calcButton.pack(side="left")
#         self.quitButton.pack(side="left")
#         self.promptLabel.pack(side="left")
#         self.kiloEntry.pack(side="left")
       
#         self.topFrame.pack(ipadx=10, ipady=10, padx=10, pady=10)
#         self.bottomFrame.pack(  ipadx=10, ipady=10, padx=10, pady=10) 
#         tkinter.mainloop()

#     def convert(self):
#         kilo = float(self.kiloEntry.get())
#         miles = kilo * 0.6214
#         tkinter.messagebox.showinfo("Result", str(kilo) + " kilometers is equal to " + str(miles) + " miles.")

# if __name__ == "__main__":
#     my_gui = MyGUI()

# ##############################################################################################
#  omrekekenen en resutlat in label zetten, in plaats van een messagebox, met een StringVar en een label die de waarde van de StringVar weergeeft, de StringVar wordt geupdate in de convert functie
# import tkinter
# import tkinter.messagebox


# class MyKiloConverterGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()
#         self.topFrame = tkinter.Frame()
#         self.midFrame = tkinter.Frame()  
#         self.bottomFrame = tkinter.Frame()
#         self.promptLabel = tkinter.Label(self.topFrame, text="Enter distance in kilometers:")
#         self.kiloEntry = tkinter.Entry(self.topFrame, width=10)
#         self.calcButton = tkinter.Button(self.bottomFrame, text="Convert", command=self.convert)
#         self.quitButton= tkinter.Button(self.bottomFrame, text="Quit", command=self.mainWindow.destroy)

#         self.value= tkinter.StringVar() 

#         self.descriptionLabel = tkinter.Label(self.midFrame, text="Distance in miles:")
#         self.milesLabel = tkinter.Label(self.midFrame, textvariable=self.value)
        
#         self.descriptionLabel.pack(side="left")
#         self.milesLabel.pack(side="left")  
#         self.calcButton.pack(side="left")
#         self.quitButton.pack(side="left")
#         self.promptLabel.pack(side="left")
#         self.kiloEntry.pack(side="left")
       
#         self.topFrame.pack(ipadx=10, ipady=10, padx=10, pady=10)
#         self.midFrame.pack(ipadx=10, ipady=10, padx=10, pady=10)
#         self.bottomFrame.pack(  ipadx=10, ipady=10, padx=10, pady=10) 

#         tkinter.mainloop()

#     def convert(self):
#         kilo = float(self.kiloEntry.get())
#         miles = kilo * 0.6214
#         self.value.set(miles) # je kunt set en get gebruiken om de waarde van een StringVar te veranderen en op te halen, in dit geval zetten we de waarde van miles in de StringVar value, die vervolgens wordt weergegeven in de milesLabel

# if __name__ == "__main__":
#     kiloconv = MyKiloConverterGUI()

##############################################################################################
# 13-15 radiobuttons

# import tkinter
# import tkinter.messagebox

# class myGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.topFrame = tkinter.Frame()
#         self.bottomFrame = tkinter.Frame()

#         self.radioVar =tkinter.IntVar() # IntVar is een variabele die een integer waarde kan opslaan, in dit geval gebruiken we het om de waarde van de radiobuttons op te slaan

#         self.rb1 = tkinter.Radiobutton(self.topFrame, text="Option 1", variable=self.radioVar, value=1)
#         self.rb2 = tkinter.Radiobutton(self.topFrame, text="Option 2", variable=self.radioVar, value=2)
#         self.rb3 = tkinter.Radiobutton(self.topFrame, text="Option 3", variable=self.radioVar, value=3, command=self.showChoice)

#         self.rb1.pack()
#         self.rb2.pack()
#         self.rb3.pack()

#         self.okButton= tkinter.Button(self.bottomFrame, text="OK", command=self.showChoice)
#         self.quitButton= tkinter.Button(self.bottomFrame, text="Quit", command=self.mainWindow.destroy)

#         self.okButton.pack(side="left")
#         self.quitButton.pack(side="left")

#         self.topFrame.pack()
#         self.bottomFrame.pack()
#         tkinter.mainloop()

#     def showChoice(self):
#         tkinter.messagebox.showinfo("Selection", "You selected option " + str(self.radioVar.get())) # met get kun je de waarde van de IntVar ophalen, in dit geval de waarde van de geselecteerde radiobutton

# if __name__ == "__main__":
#     my_gui = myGUI()

##############################################################################################

# #13-16 checkbuttons, met een IntVar voor elke checkbox, en een functie die de geselecteerde opties laat zien in een messagebox
# import tkinter
# import tkinter.messagebox

# class myGUI:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.topFrame = tkinter.Frame()
#         self.bottomFrame = tkinter.Frame()

#         self.cbVar1 =tkinter.IntVar() 
#         self.cbVar2 =tkinter.IntVar() 
#         self.cbVar3 =tkinter.IntVar() # IntVar is een variabele die een integer waarde kan opslaan, in dit geval gebruiken we het om de waarde van de checkboxes op te slaan

#         self.cbVar1.set(0) # 0 betekent dat de checkbox niet is geselecteerd, 1 betekent dat de checkbox is geselecteerd
#         self.cbVar2.set(0)
#         self.cbVar3.set(0)  

#         self.cb1 = tkinter.Checkbutton(self.topFrame, text="Option 1", variable=self.cbVar1 )
#         self.cb2 = tkinter.Checkbutton(self.topFrame, text="Option 2", variable=self.cbVar2 )
#         self.cb3 = tkinter.Checkbutton(self.topFrame, text="Option 3", variable=self.cbVar3)

#         self.cb1.pack()
#         self.cb2.pack()
#         self.cb3.pack()

#         self.okButton= tkinter.Button(self.bottomFrame, text="OK", command=self.showChoice)
#         self.quitButton= tkinter.Button(self.bottomFrame, text="Quit", command=self.mainWindow.destroy)

#         self.okButton.pack(side="left")
#         self.quitButton.pack(side="left")

#         self.topFrame.pack()
#         self.bottomFrame.pack()
#         tkinter.mainloop()

#     def showChoice(self):
#         self.message = 'You selected: \n'
#         if self.cbVar1.get() == 1:
#             self.message += "Option 1\n"    # met get kun je de waarde van de IntVar ophalen, in dit geval de waarde van de geselecteerde checkboxes
#         if self.cbVar2.get() == 1:
#             self.message += "Option 2\n"
#         if self.cbVar3.get() == 1:
#             self.message += "Option 3\n"
#         tkinter.messagebox.showinfo("Selection", self.message) 

# if __name__ == "__main__":
#     my_gui = myGUI()

########################################################################################################################################################################

# # listbox 13-17

# import tkinter

# class listBox:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.label = tkinter.Label(self.mainWindow, text="Select a programming language:")
#         self.label.pack(padx = 10, pady = 10)

#         self.bottomframe = tkinter.Frame(self.mainWindow)

#         self.listbox = tkinter.Listbox(self.bottomframe)
#         self.listbox.pack(padx = 10, pady = 10 )
#         self.listbox.insert(1, "Python")
#         self.listbox.insert(2, "Java")
#         self.listbox.insert(3, "C++")
#         self.listbox.insert(4, "JavaScript")
#         self.listbox.pack()

#         self.bottomframe.pack(padx=10, pady=10, ipadx=10, ipady=10)

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_listbox = listBox()

########################################################################################################################################################################

# # listbox vullen met een loop 13-18

# import tkinter

# class listBox:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.listbox= tkinter.Listbox(self.mainWindow, height=0, width=20, selectmode=tkinter.BROWSE) # height=0 betekent dat de listbox automatisch de hoogte aanpast aan het aantal items, width geeft de breedte van de listbox aan in aantal tekens
#         self.listbox.pack(padx=10, pady=10)

#         days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         for day in days:
#             self.listbox.insert(tkinter.END, day) # met END voeg je een item toe aan het einde van de lijst, je kunt ook een index gebruiken om een item op een specifieke positie toe te voegen

#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_listbox = listBox()


########################################################################################################################################################################

# # geselecteerde idems in listbox ophalen 13-19

# import tkinter
# import tkinter.messagebox

# class listBoxSelection:
#     def __init__(self):
#         self. mainWindow = tkinter.Tk()
#         self.dogListbox = tkinter.Listbox(self.mainWindow, width= 0 , height=0, selectmode=tkinter.MULTIPLE) # met MULTIPLE kun je meerdere items selecteren, met BROWSE kun je maar één item selecteren

#         dogs = ["Labrador", "Poodle", "Bulldog", "Beagle", "Chihuahua", "Dachshund", "Boxer"]

#         for dog in dogs:
#             self.dogListbox.insert(tkinter.END, dog)

#         self.getButton = tkinter.Button (self.mainWindow, text="Get Selection", command=self.retrieveDog)
#         self.dogListbox.pack(padx=10, pady=10)
#         self.getButton.pack(padx=10, pady=10)
#         tkinter.mainloop()

#     def retrieveDog(self):
#         indexes=self.dogListbox.curselection() # met curselection krijg je een tuple met de indexen van de geselecteerde items
#         if len(indexes) == 0:
#             tkinter.messagebox.showinfo("Selection", "No dog selected.")
#         else:
#             #meer selecteren tegelijk
#             selectedDogs = [self.dogListbox.get(index) for index in indexes] # met get kun je de waarde van een item op een specifieke index ophalen, in dit geval de geselecteerde items
#             tkinter.messagebox.showinfo("Selection", "You selected: " + ", ".join(selectedDogs)) # met join kun je een lijst van strings samenvoegen tot één string, in dit geval de geselecteerde items gescheiden door een komma
#             # tkinter.messagebox.showinfo(message = self.dogListbox.get(indexes[0])) # als je maar één item wilt ophalen, kun je de eerste index gebruiken, in dit geval de eerste geselecteerde item omdat de selectmode MULTIPLE is, kunnen er meerdere items geselecteerd zijn, maar we laten hier alleen de eerste geselecteerde item zien

# if __name__ == "__main__":
#     my_listbox_selection = listBoxSelection()

# ###############################################################################################################################

# # 13-21 Vertical scrollbar toevoegen aan listbox

# import tkinter

# class VerticalScrollbar:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.listboxFrame = tkinter.Frame(self.mainWindow)
#         self.listboxFrame.pack(padx=20, pady=20)

#         self.listbox = tkinter.Listbox(self.listboxFrame, height=6, width=0)
#         self.listbox.pack(side="left", padx=10, pady=10)

#         self.scrollbar = tkinter.Scrollbar(self.listboxFrame, orient=tkinter.VERTICAL)
#         self.scrollbar.pack(side='right', fill=tkinter.Y)

#         # verbind de scrollbar met de listbox
#         self.scrollbar.config(command=self.listbox.yview) # met config kun je de eigenschappen van een widget aanpassen, in dit geval de command van de scrollbar, zodat de scrollbar de yview van de listbox aanpast, waardoor de listbox scrollt als je aan de scrollbar trekt
#         self.listbox.config(yscrollcommand=self.scrollbar.set) # met config kun je de eigenschappen van een widget aanpassen, in dit geval de yscrollcommand van de listbox, zodat de listbox de set van de scrollbar aanpast, waardoor de scrollbar de positie van de listbox bijhoudt als je aan de scrollbar trekt

#         months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#         for month in months:
#             self.listbox.insert(tkinter.END, month) 
        
#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_vertical_scrollbar = VerticalScrollbar()


# ###############################################################################################################################

# 13-22 Horizontal scrollbar toevoegen aan listbox

# import tkinter

# class HorizontalScrollbar:
#     def __init__(self):
#         self.mainWindow = tkinter.Tk()

#         self.listboxFrame = tkinter.Frame(self.mainWindow)
#         self.listboxFrame.pack(padx=20, pady=20)

#         self.listbox = tkinter.Listbox(self.listboxFrame, height=5, width=30)
#         self.listbox.pack(side="top", padx=10, pady=10)

#         self.scrollbar = tkinter.Scrollbar(self.listboxFrame, orient=tkinter.HORIZONTAL)
#         self.scrollbar.pack(side='bottom', fill=tkinter.X)

#         # verbind de scrollbar met de listbox
#         self.scrollbar.config(command=self.listbox.xview) # met config kun je de eigenschappen van een widget aanpassen, in dit geval de command van de scrollbar, zodat de scrollbar de xview van de listbox aanpast, waardoor de listbox horizontaal scrollt als je aan de scrollbar trekt
#         self.listbox.config(xscrollcommand=self.scrollbar.set) # met config kun je de eigenschappen van een widget aanpassen, in dit geval de xscrollcommand van de listbox, zodat de listbox de set van de scrollbar aanpast, waardoor de scrollbar de positie van de listbox bijhoudt als je aan de scrollbar trekt

#         long_items = ["This is a long item that will require horizontal scrolling", "Another long item that will require horizontal scrolling", "Yet another long item that will require horizontal scrolling"]
#         for item in long_items:
#             self.listbox.insert(tkinter.END, item) 
        
#         tkinter.mainloop()

# if __name__ == "__main__":
#     my_horizontal_scrollbar = HorizontalScrollbar()

# ########################################################################################################################################################

#   draw line 13-24 draw multiple lines13-25

import tkinter

class MyGUI:
    def __init__(self):
        self.mainWindow = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.mainWindow, width = 200, height = 200)
        self.canvas.create_line(0,0, 199,199) # met create_line kun je een lijn tekenen op het canvas, de eerste twee parameters zijn de x en y coördinaten van het beginpunt van de lijn, de laatste twee parameters zijn de x en y coördinaten van het eindpunt van de lijn
        self.canvas.create_line(199,0, 0, 199)
        self.canvas.create_line(0,100, 199,100)
        self.canvas.create_line(100,0,100,199)
        self.canvas.pack()
        tkinter.mainloop()
if __name__ == "__main__":
    my_gui = MyGUI()

    