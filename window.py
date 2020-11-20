import tkinter as tk
from tkinter.ttk import * 
import tkinter.font as TkFont
from tkinter import * #pip install tk
from matplotlib import * #pip install matplotlib
from pandas import DataFrame #pip install pandas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from arduino import *
import connections
import data_transfer

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master 

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        tree = Treeview(statusoverzicht)

        #adding menus
        overzicht = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Overzicht", menu=overzicht)
        overzicht.add_command(label="Statusoverzicht", command=self.openStatusoverzicht)
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
        self.dropdown(arduinos, temperatuur)
        self.dropdown(arduinos, lichtintensiteit)
        self.dropdown(arduinos, rolluiken)

        omhoogButton = Button(rolluiken, text="Omhoog", command = omhoog_command) #function placeholder
        omhoogButton.place(x=460, y=200)
        omlaagButton = Button(rolluiken, text="Omlaag", command = omlaag_command) #function placeholder
        omlaagButton.place(x=460, y=250)

        #statusoverzicht page
        tree['columns'] = ("Rolluik", "Status", "Temperatuur", "Lichtintensiteit")
        tree.column("#0", width=0, minwidth=25)
        tree.column("Rolluik", anchor=W, width=120)
        tree.column("Status", anchor=W, width=60)
        tree.column("Temperatuur", anchor=W, width=120)
        tree.column("Lichtintensiteit", anchor=W, width=160)

        tree.heading("#0", text="", anchor=W)
        tree.heading("Rolluik", text="Rolluik", anchor=W)
        tree.heading("Status", text="Status", anchor=W)
        tree.heading("Temperatuur", text="Huidige temperatuur", anchor=W)
        tree.heading("Lichtintensiteit", text="Huidige lichtintensiteit", anchor=W)

        tree.insert(parent='', index='end', iid=0, text="", values=("Woonkamer", "Open", 20, 42))
        tree.insert(parent='', index='end', iid=1, text="", values=("Slaapkamer", "Dicht", 46, 12))
        tree.pack(pady=20)

        #page temperatuur en lichtintensiteit
        self.lineChartTemperatuur(dataset, temperatuur)
        dropdown = StringVar(temperatuur)
        dropdown.set("Dag") #default value
        self.lineChartLicht(dataset2, lichtintensiteit)
        dropdown = StringVar(lichtintensiteit)
        dropdown.set("Dag") #default value

        dropdownMenu = OptionMenu(temperatuur, dropdown,"Dag", "Week", "Maand", "Jaar")
        dropdownMenu.pack()
        dropdownMenu.place(x=350, y=0)
        dropdownMenu = OptionMenu(lichtintensiteit, dropdown,"Dag", "Week", "Maand", "Jaar")
        dropdownMenu.pack()
        dropdownMenu.place(x=350, y=0)
        
        #font
        myFont = TkFont.Font(family="helvetica", size=10)
        helpmijTekst.configure(font=myFont, state="disabled")

        #openen startpagina(help)
        self.openHelpmij()

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
        statusoverzicht.pack_forget()
        temperatuur.pack_forget()
        lichtintensiteit.pack_forget()
        rolluiken.pack_forget()
        helpmij.pack_forget()
    
    def exitProgram(self):
        exit()

    def openTemperatuur(self):
        self.hide_frames()
        temperatuur.pack(fill="both", expand=1)

    def openStatusoverzicht(self):
        self.hide_frames()
        statusoverzicht.pack(fill="both", expand=1)

    def openLichtintensiteit(self):
        self.hide_frames()
        lichtintensiteit.pack(fill="both", expand=1)

    def openRolluiken(self):
        self.hide_frames()
        rolluiken.pack(fill="both", expand=1)
    
    def openHelpmij(self):
        self.hide_frames()
        helpmij.pack(fill="both", expand=1)

    def dropdown(self, lijst, locatie):
        dropdown.set(lijst[0]) # default value, eerste index
        widget = OptionMenu(locatie, dropdown, *lijst)
        widget.pack()

    def doNothing(self):
        pass

    def table(self):
        tree= Treeview(statusoverzicht)

#create a main window
root=tk.Tk() 
root.title("Centrale")
root.configure(background='red')
root.geometry('600x500')

#variabele
temperatuur=tk.Frame(root, width=600, height=500)
lichtintensiteit=tk.Frame(root, width=600, height=500)
rolluiken=tk.Frame(root, width=600, height=500)
helpmij=tk.Frame(root, width=600, height=500)
statusoverzicht=tk.Frame(root, width=600, height=500)

#Help
exittekst = "   - Exit: sluit de centrale \n"
helptekst = "   - Help: informatie hoe de centrale werkt \n"
rolluikenuitleg = "   - Rolluiken: wijzig de instellingen van de verschillende rolluiken \n"
statusoverzichtuitleg = "   - Statusoverzicht: een overzicht van alle rolluiken en de huidige temperatuur en lichtintensiteit\n"
temperatuuruitleg = "   - Temperatuur: informatie over de gemiddelde temperatuur \n"
lichtuitleg = "   - Lichtintensiteit: informatie over de gemiddelde lichtintensiteit \n"
meerinfo = "\nVoor meer informatie kunt u contact opnemen met 06-12345678 of mailen naar centrale@hanze.nl"
helpmijtekst = ("Welkom! \n\n" + "In deze centrale kunt u alles inzien omtrent de rolluiken, hieronder volgt een korte uitleg van alle \nonderdelen binnen deze centrale: \n" 
                + exittekst + helptekst + rolluikenuitleg + statusoverzichtuitleg + temperatuuruitleg + lichtuitleg + meerinfo)


# haal de arduino in de porten op van Connections
arduino_port = connections.arduino_port
# lege list om de arduinos in op te slaan
arduinos = []
# voor elke arduino...
for ar in arduino_port:
    # Kijk welke sensor wordt meegegeven
    sensor = data_transfer.get_sensor(ar[0])
    # Voeg een arduino klasse Arduino toe aan de list
    arduinos.append(Arduino(ar, sensor))

# arduinos.append(Arduino(('COM4', 'Arduino Uno (COM4)', 'USB VID:PID=2341:0043 SER=75834303638351E03130 LOCATION=1-2'), Sensor()))

# geef wel nog de geselecteerde arduino voor het command. Dus {arduino}.status...
omlaag_command = arduinos[0].status_omlaag()
omhoog_command = arduinos[0].status_omhoog()

#placeholders
dataset = {'Dag': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010], #placeholder voor linechart temperatuur
         'Gemiddelde_temp': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}  
dataset2 = {'Dag': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010], #placeholder voor linechart lichtintensiteit
         'Gemiddelde_licht': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}  
dropdown = StringVar(rolluiken)

#class aanroepen/instellen + start window
GUI=Window(root)
root.mainloop()