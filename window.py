import tkinter as tk #importeren GUI package
from tkinter import *
from tkinter import ttk 
from tkinter.ttk import * 
from matplotlib import * #pip install matplotlib
from pandas import DataFrame #pip install pandas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master #main frame
        self.init_window()

#     def lineChart(self, dataset):
#         df = DataFrame(dataset,columns=['Dag','Gemiddelde_temp'])
        
#         figure = plt.Figure(figsize=(4,3), dpi=100)
#         ax = figure.add_subplot(111)
#         line = FigureCanvasTkAgg(figure, tab2)
#         line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
#         df = df[['Dag','Gemiddelde_temp']].groupby('Dag').sum()
#         df.plot(kind='line', legend=True, ax=ax2, color='b',marker='o', fontsize=10)
#         ax.set_title('Gemiddelde temperatuur')    


    def table(self, dataset):
        table = pd.DataFrame(dataset)
        print(table)

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

        #tab2 charts aanroepen
        dataset = {'Dag': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Gemiddelde_temp': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }  
        #lineChart(dataset)

        #tab 3  
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Instellingen')

        #tab 3 table
        dataset = {'Name':['Tom', 'nick', 'krish', 'jack'],
        'Age':[20, 21, 19, 18]}
        table(dataset)

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



