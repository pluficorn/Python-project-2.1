# Dit Bestand verwijderen voor gebruik.

import tkinter as tk
from tkinter.ttk import * 
import tkinter.font as TkFont
from tkinter import * #pip install tk
from matplotlib import * #pip install matplotlib
from pandas import DataFrame #pip install pandas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import arduino
import connections
import data_transfer
import datetime

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
        overzicht.add_command(label="Sensordata", command=self.openData)

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
        namenlijst = [ar.naam for ar in arduinos]
        self.dropdown(namenlijst, sensordata)
        self.dropdown(namenlijst, rolluiken)

        omhoogButton = Button(rolluiken, text="Omhoog", command=omlaag_command)
        omhoogButton.place(x=460, y=200)
        omlaagButton = Button(rolluiken, text="Omlaag", command=omhoog_command)
        omlaagButton.place(x=460, y=250)

        #statusoverzicht page
        tree['columns'] = ("Rolluik", "Status", "Laatste meting")
        tree.column("#0", width=0, minwidth=25)
        tree.column("Rolluik", anchor=W, width=120)
        tree.column("Status", anchor=W, width=60)
        tree.column("Laatste meting", anchor=W, width=120)

        tree.heading("#0", text="", anchor=W)
        tree.heading("Rolluik", text="Rolluik", anchor=W)
        tree.heading("Status", text="Status", anchor=W)
        tree.heading("Laatste meting", text="Laatste meting", anchor=W)
        
        #linechart
        self.lineChartSensorData(getDatalist(selected), sensordata)
     
        #font
        myFont = TkFont.Font(family="helvetica", size=10)
        helpmijTekst.configure(font=myFont, state="disabled")

        #openen startpagina(help)
        self.openHelpmij()

    def lineChartSensorData(self, tempdata, locatie):
        df = DataFrame(tempdata,columns=['uur','gemiddelde'])
        figure = plt.Figure(figsize=(4,3), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, locatie)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df = df[['uur','gemiddelde']].groupby('uur').sum()
        df.plot(kind='line', legend=True, ax=ax, color='b',marker='o', fontsize=10)
        ax.set_title('Gemiddelde waardes') 

    def hide_frames(self):
        statusoverzicht.pack_forget()

        sensordata.pack_forget()
        rolluiken.pack_forget()
        helpmij.pack_forget()
    
    def exitProgram(self):
        exit()

    def openData(self):
        self.hide_frames()
        sensordata.pack(fill="both", expand=1)
        # get_data()

    def openStatusoverzicht(self):
        self.hide_frames()
        statusoverzicht.pack(fill="both", expand=1)
        get_data()

    def openRolluiken(self):
        self.hide_frames()
        rolluiken.pack(fill="both", expand=1)

    def openHelpmij(self):
        self.hide_frames()
        helpmij.pack(fill="both", expand=1)

    def dropdown(self, lijst, locatie):
        selected.set(lijst[0])
        widget = OptionMenu(locatie, selected, *lijst)
        widget.pack()

    def table(self):
        tree=Treeview(statusoverzicht)

##################################################################################################################

#create a main window
root=tk.Tk() 
root.title("Centrale")
root.configure()
root.geometry('600x500')

#variabele
sensordata = tk.Frame(root, width = 600, height = 500)
rolluiken=tk.Frame(root, width=600, height=500)
helpmij=tk.Frame(root, width=600, height=500)
statusoverzicht=tk.Frame(root, width=600, height=500)

#Help
exittekst = "   - Exit: sluit de centrale \n"
helptekst = "   - Help: informatie hoe de centrale werkt \n"
rolluikenuitleg = "   - Rolluiken: wijzig de instellingen van de verschillende rolluiken \n"
statusoverzichtuitleg = "   - Statusoverzicht: een overzicht van alle rolluiken en de huidige temperatuur en lichtintensiteit\n"
# temperatuuruitleg = "   - Temperatuur: informatie over de gemiddelde temperatuur \n"
# lichtuitleg = "   - Lichtintensiteit: informatie over de gemiddelde lichtintensiteit \n"
sensordatauitleg = "   - Sensordata: informatie over de gemiddelde waardes van de Sensors over tijd \n"
meerinfo = "\nVoor meer informatie kunt u contact opnemen met 06-12345678 of mailen naar centrale@hanze.nl"
# helpmijtekst = ("Welkom! \n\n" + "In deze centrale kunt u alles inzien omtrent de rolluiken, hieronder volgt een korte uitleg van alle \nonderdelen binnen deze centrale: \n" 
#                 + exittekst + helptekst + rolluikenuitleg + statusoverzichtuitleg + temperatuuruitleg + lichtuitleg + meerinfo)

helpmijtekst = ("Welkom! \n\n" + "In deze centrale kunt u alles inzien omtrent de rolluiken, hieronder volgt een korte uitleg van alle \nonderdelen binnen deze centrale: \n" 
                + exittekst + helptekst + rolluikenuitleg + statusoverzichtuitleg + sensordatauitleg + meerinfo)

#Lijst arduinos
arduinos = connections.arduinos

# methode om juiste arduino te krijgen
def get_arduino(ar):
    for ard in arduinos:
        if ard.naam == selected.get():
            return ard

def getDatalist(ar):
    ard = get_arduino(ar)
    return (ard.sensor.return_data(datetime.datetime.now(), datetime.datetime.now()))

def omlaag_command():
    ar = get_arduino(selected)
    ar.status_omlaag()

def omhoog_command():
    ar = get_arduino(selected)
    ar.status_omhoog()

# more
def grafiek():
    ar = get_arduino(selected)
    dataset = ar.sensor.return_data(datetime.datetime.now(), datetime.datetime.now())

def get_data():
    for i in arduinos:
        t = i.tuple_info()
        tree.insert(parent='', index='end', iid=0, text="Text", values= t) 
    tree.pack(pady=20)

#variabele
#dataset = arduinos[0].sensor.return_data(datetime.datetime.now(), datetime.datetime.now())
selected = StringVar(rolluiken)
# selected = arduino.Arduino()

#class aanroepen/instellen + start window
GUI=Window(root)