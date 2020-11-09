import tkinter as tk
from tkinter.ttk import * 
import tkinter.font as TkFont
from tkinter import *
from matplotlib import * #pip install matplotlib
from pandas import DataFrame #pip install pandas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master 

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        #adding menus
        overzicht = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Overzicht", menu=overzicht)
        overzicht.add_command(label="Statusoverzicht", command=self.openRoot)
        overzicht.add_command(label="Temperatuur", command=self.openTemperatuur)
        overzicht.add_command(label="Lichtintensiteit", command=self.openLichtintensiteit)

        instellingen = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Instellingen", menu=instellingen)
        instellingen.add_command(label="Rolluiken", command=self.openRolluiken)

        menu.add_command(label="Help", command=self.openHelpmij)
        menu.add_command(label="Exit", command=self.exitProgram)
        
        #helpmij page
        helpmijTekst = tk.Text(helpmij, bg="whitesmoke")
        helpmijTekst.pack(fill="both", expand=1)
        helpmijTekst.insert(tk.END, helpmijtekst)

        #rolluiken page
        #dropdown(tijdelijkeLijst)

        #gem temp & licht
        self.lineChartTemperatuur(dataset, temperatuur)
        dropdown = StringVar(temperatuur)
        dropdown.set("Dag") #default value
        self.lineChartLicht(dataset2, lichtintensiteit)
        dropdown = StringVar(lichtintensiteit)
        dropdown.set("Dag") #default value

        dropdownMenu = OptionMenu(temperatuur, dropdown,"Dag", "Week", "Maand", "Jaar")
        dropdownMenu.pack()
        dropdownMenu.place(x=470, y=0)
        dropdownMenu = OptionMenu(lichtintensiteit, dropdown,"Dag", "Week", "Maand", "Jaar")
        dropdownMenu.pack()
        dropdownMenu.place(x=470, y=0)
        
        #font
        myFont = TkFont.Font(family="helvetica", size=10)
        helpmijTekst.configure(font=myFont, state="disabled")

        #table



    def lineChartTemperatuur(self, dataset, locatie):
        df = DataFrame(dataset,columns=['Dag','Gemiddelde_temp'])
        figure = plt.Figure(figsize=(4,3), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, locatie)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df = df[['Dag','Gemiddelde_temp']].groupby('Dag').sum()
        df.plot(kind='line', legend=True, ax=ax, color='b',marker='o', fontsize=10)
        ax.set_title('Gemiddelde temperatuur')   

    def lineChartLicht(self, dataset, locatie):
        df = DataFrame(dataset,columns=['Dag','Gemiddelde_licht'])
        figure = plt.Figure(figsize=(4,3), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, locatie)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df = df[['Dag','Gemiddelde_licht']].groupby('Dag').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
        ax.set_title('Gemiddelde lichtintensiteit')  
        
    def hide_frames(self):
        temperatuur.pack_forget()
        lichtintensiteit.pack_forget()
        rolluiken.pack_forget()
        helpmij.pack_forget()
    
    def exitProgram(self):
        exit()

    def openTemperatuur(self):
        self.hide_frames()
        temperatuur.pack(fill="both", expand=1)

    def openRoot(self):
        self.hide_frames()
        root.mainloop()

    def openLichtintensiteit(self):
        self.hide_frames()
        lichtintensiteit.pack(fill="both", expand=1)

    def openRolluiken(self):
        self.hide_frames()
        rolluiken.pack(fill="both", expand=1)
    
    def openHelpmij(self):
        self.hide_frames()
        helpmij.pack(fill="both", expand=1)

    #def dropdown(self, lijst):
        #dropdown = StringVar(rolluiken)
        #dropdown.set(lijst[0]) # default value, eerste index

        #widget = OptionMenu(master, dropdown, *lijst)
        #widget.pack()
        #return dropdown

    def overzichtTable(self, locatie, dataset):
        total_rows = len(dataset) 
        total_columns = len(dataset[0]) 
        for i in range(total_rows): 
            for j in range(total_columns):     
                self.e = Entry(root, width=20, fg='blue', 
                               font=('Arial',16,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, dataset[i][j])
        
        
#create a main window
root=tk.Tk() 
root.title("Centrale")
root.configure(background='red')
root.geometry('600x500')

#variabele
temperatuur=tk.Frame(root, width=600, height=500)
lichtintensiteit=tk.Frame(root, width=600, height=500)
rolluiken=tk.Frame(root, width=600, height=500, bg="black")
helpmij=tk.Frame(root, width=600, height=500)
helpmijtekst = "help mij nu!" #uitschrijven

#placeholders
#tijdelijkeLijst=["egg", "bunny", "chicken"]
dataset = {'Dag': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010], #placeholder
         'Gemiddelde_temp': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}  
dataset2 = {'Dag': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010], #placeholder
         'Gemiddelde_licht': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}  

#class aanroepen/instellen + start window
GUI=Window(root)
root.mainloop()