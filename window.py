from tkinter import * #importeren GUI package
from tkinter import ttk 
from tkinter.ttk import *

class Window(Frame):

    def __init__(self, master=None):
            Frame.__init__(self, master)                 
            self.master = master #main frame
            self.init_window()

    #create a main window
    def init_window(self):
        
        #verander naam main window
        self.master.title("Centrale")
        self.pack(fill=BOTH)

        #create tabcontrol
        tabControl = ttk.Notebook(mainWindow)
        tabControl.pack(expand = 1, fill =BOTH)
        
        #tab1
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Rolluiken')

        #tab 1 buttons
        openRolluik = Button(tab1, text="Omhoog")
        openRolluik.place(x=400, y=50) 

        sluitRolluik = Button(tab1, text="Omlaag")
        sluitRolluik.place(x=400, y=100)

        selectAll = Button(tab1, text="Selecteer alles")
        selectAll.place(x=400, y=150) 

        helpButton1 = Button(tab1, text="?")
        helpButton1.place(x=400, y=430)


        #tab 2
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Data')

        #tab 2 button
        helpButton2 = Button(tab2, text="?")
        helpButton2.place(x=400, y=430)

        #tab 2 dropdown
        dropdown = StringVar(tab2)
        dropdown.set("dag") # default value

        dropdownMenu = OptionMenu(tab2, dropdown,"dag", "week", "maand", "jaar")
        dropdownMenu.pack()
        dropdownMenu.place(x=400, y=0) #3 dropdowns
 
        #tab 3
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Instellingen')

        #tap 3 buttons
        helpButton3 = Button(tab3, text="?")
        helpButton3.place(x=400, y=430)

        save = Button(tab3, text="Wijzigingen opslaan")
        save.place(x=300, y=200)

#create a main window
mainWindow = Tk() 

# size window
mainWindow.geometry('500x500')

#class aanroepen/instellen
GUI = Window(mainWindow)

#start de window
mainWindow.mainloop()