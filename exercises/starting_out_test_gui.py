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

import tkinter
import tkinter.messagebox


class MyKiloConverterGUI:
    def __init__(self):
        self.mainWindow = tkinter.Tk()
        self.topFrame = tkinter.Frame()
        self.midFrame = tkinter.Frame()  
        self.bottomFrame = tkinter.Frame()
        self.promptLabel = tkinter.Label(self.topFrame, text="Enter distance in kilometers:")
        self.kiloEntry = tkinter.Entry(self.topFrame, width=10)
        self.calcButton = tkinter.Button(self.bottomFrame, text="Convert", command=self.convert)
        self.quitButton= tkinter.Button(self.bottomFrame, text="Quit", command=self.mainWindow.destroy)

        self.value= tkinter.StringVar() 

        self.descriptionLabel = tkinter.Label(self.midFrame, text="Distance in miles:")
        self.milesLabel = tkinter.Label(self.midFrame, textvariable=self.value)
        
        self.descriptionLabel.pack(side="left")
        self.milesLabel.pack(side="left")  
        self.calcButton.pack(side="left")
        self.quitButton.pack(side="left")
        self.promptLabel.pack(side="left")
        self.kiloEntry.pack(side="left")
       
        self.topFrame.pack(ipadx=10, ipady=10, padx=10, pady=10)
        self.midFrame.pack(ipadx=10, ipady=10, padx=10, pady=10)
        self.bottomFrame.pack(  ipadx=10, ipady=10, padx=10, pady=10) 

        tkinter.mainloop()

    def convert(self):
        kilo = float(self.kiloEntry.get())
        miles = kilo * 0.6214
        self.value.set(miles) # je kunt set en get gebruiken om de waarde van een StringVar te veranderen en op te halen, in dit geval zetten we de waarde van miles in de StringVar value, die vervolgens wordt weergegeven in de milesLabel

if __name__ == "__main__":
    kiloconv = MyKiloConverterGUI()

##############################################################################################
