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

# # 13-4 =5 text with labelwidgets met extra

import tkinter
class MyGui:
    def __init__(self, tekst2):

        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("My First GUI")

        self.label1 = tkinter.Label(self.mainWindow, text="Hello World")
        self.label2 = tkinter.Label(self.mainWindow, text=tekst2)

        self.label1.pack(side = 'left')
        self.label2.pack(side = 'left')

        tkinter.mainloop()  

if __name__ == "__main__":
    my_gui = MyGui("Welcome to Python Programming!")

# ###########################################################################    

