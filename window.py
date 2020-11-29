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

        omhoogButton = Button(rolluiken, text="Omhoog", command=omhoog_command)
        omhoogButton.place(x=460, y=200)
        omlaagButton = Button(rolluiken, text="Omlaag", command=omlaag_command)
        omlaagButton.place(x=460, y=250)

        #Buttons voor veranderen waardes
        # maxTempButton = Button(rolluiken, text="Verander Max Temperatuur", )

        #statusoverzicht page
        self.tree = Treeview(statusoverzicht)
        self.tree['columns'] = ("Rolluik", "Status", "Laatste meting")
        self.tree.column("#0", width=0, minwidth=25)
        self.tree.column("Rolluik", anchor=W, width=120)
        self.tree.column("Status", anchor=W, width=60)
        self.tree.column("Laatste meting", anchor=W, width=120)

        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("Rolluik", text="Rolluik", anchor=W)
        self.tree.heading("Status", text="Status", anchor=W)
        self.tree.heading("Laatste meting", text="Laatste meting", anchor=W)

        for i in arduinos:
            t = i.tuple_info()
            self.tree.insert(parent='', index='end', iid=0, text="Text", values= t)
        self.tree.pack(pady=20)
        insert_tree(self.tree)

        #linechart
        self.lineChartSensorData(getDatalist(selected), sensordata)

        #font
        myFont = TkFont.Font(family="helvetica", size=10)
        helpmijTekst.configure(font=myFont, state="disabled")

        #openen startpagina(help)
        self.openHelpmij()

    def lineChartSensorData(self, tempdata, locatie):
        df = DataFrame(tempdata, columns=['uur','gemiddelde'])
        figure = plt.Figure(figsize=(4,3), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, locatie)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df = df[['uur','gemiddelde']].groupby('uur').sum()
        df.plot(kind='line', legend=True, ax=ax, color='b',marker='o', fontsize=10)
        ax.set_title('Gemiddelde waardes') 

    def hide_frames(self):
        statusoverzicht.pack_forget()
        rolluiken.pack_forget()
        helpmij.pack_forget()
        sensordata.pack_forget()
    
    def exitProgram(self):
        exit()

    def openData(self):
        self.hide_frames()
        sensordata.pack(fill="both", expand=1)

    def openStatusoverzicht(self):
        self.hide_frames()
        insert_tree(self.tree)
        statusoverzicht.pack(fill="both", expand=1)

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

###############################################################################

#create a main window
root=tk.Tk() 
root.title("Centrale")
root.configure()
root.geometry('600x500')

#variabele
rolluiken=tk.Frame(root, width=600, height=500)
helpmij=tk.Frame(root, width=600, height=500)
statusoverzicht=tk.Frame(root, width=600, height=500)
sensordata = tk.Frame(root, width=600, height=500)

#Help
exittekst = "   - Exit: sluit de centrale \n"
helptekst = "   - Help: informatie hoe de centrale werkt \n"
rolluikenuitleg = "   - Rolluiken: wijzig de instellingen van de verschillende rolluiken \n"
statusoverzichtuitleg = "   - Statusoverzicht: een overzicht van alle rolluiken en de huidige temperatuur en lichtintensiteit\n"
sensordatauitleg = "   - Sensordata: informatie over de gemiddelde waardes van de Sensors over tijd \n"
meerinfo = "\nVoor meer informatie kunt u contact opnemen met 06-12345678 of mailen naar centrale@hanze.nl"

helpmijtekst = ("Welkom! \n\n" + "In deze centrale kunt u alles inzien omtrent de rolluiken, hieronder volgt een korte uitleg van alle \nonderdelen binnen deze centrale: \n" 
                + exittekst + helptekst + rolluikenuitleg + statusoverzichtuitleg + sensordatauitleg + meerinfo)

#Lijst arduinos
arduinos = connections.arduinos

# De methodes hieronder t/m grafiek vervangen de hierboven gecommente ifthen()
# methode om juiste arduino te krijgen
def get_arduino(ar):
    for ard in arduinos:
        if ard.naam == selected.get():
            return ard

# Moet ervoor zorgen dat de grafiekdata meest recent is
# en dus dat de grafiek elke keer bij het openen van de grafiektab
# opnieuw wordt opgehaald en getoond
def getDatalist(ar):
    # Haalt de arduino op die bij de naam zit
    ard = get_arduino(ar)
    l = ard.sensor.return_data(datetime.datetime.now(), datetime.datetime.now())
    return l

# volgens mij waren deze en de volgende onbedoeld weggehaald
def omlaag_command():
    ar = get_arduino(selected)
    ar.status_omlaag()

def omhoog_command():
    ar = get_arduino(selected)
    ar.status_omhoog()

def insert_tree(tree):
    # Verwijder bestaande data
    for record in tree.get_children():
        tree.delete(record)

    # Zet data in de tabel (tree)
    i = 0
    for a in arduinos:
        t = a.tuple_info()
        tree.insert(parent='', index='end', iid=i, text="", values= t)
        i += 1
        tree.pack(pady=20)

# selected was dropdown
selected = StringVar(rolluiken)

#class aanroepen/instellen + start window
GUI=Window(root)
root.mainloop()         