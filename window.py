import tkinter as tk
from tkinter.ttk import * 
import tkinter.font as TkFont
from tkinter import * #pip install tk
from matplotlib import * #pip install matplotlib
from pandas import DataFrame #pip install pandas
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import arduino
import connections
import data_transfer
import datetime
from pprint import pprint

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
        automaticButton = Button(rolluiken, text="Autonoom", command=autonomy_command)
        automaticButton.place(x=460, y=275)
        manualButton = Button(rolluiken, text="Handmatig", command=manual_command)
        manualButton.place(x=460, y=300)
        
        #Buttons voor veranderen waardes
        maxWaardeButton = Button(rolluiken, text="Verander max waarde", command=verander_max)
        maxWaardeButton.place(x=300, y=100)
        minWaardeButton = Button(rolluiken, text="Verander min waarde", command=verander_min)
        minWaardeButton.place(x=300, y=150)
        maxUitrolButton = Button(rolluiken, text="Verander max uitrol", command=verander_max_uitrol)
        maxUitrolButton.place(x=150, y=100)
        minUitrolButton = Button(rolluiken, text="Verander min uitrol", command=verander_min_uitrol)
        minUitrolButton.place(x=150, y=150)

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

        #font
        myFont = TkFont.Font(family="helvetica", size=10)
        helpmijTekst.configure(font=myFont, state="disabled")

        #openen startpagina(help)
        self.openHelpmij()
    
    def lineChartSensorData(self, tempdata, locatie):
        pprint(tempdata)
        plt.plot(tempdata, linestyle='--', marker='o', color='b')
        plt.ylabel('gemiddelde lezing')
        plt.xlabel('tijd in uren')
        plt.grid(True)
        plt.show()

    def hide_frames(self):
        statusoverzicht.pack_forget()
        rolluiken.pack_forget()
        helpmij.pack_forget()
        sensordata.pack_forget()
    
    def exitProgram(self):
        exit()

    def openData(self):
        self.hide_frames()
        self.lineChartSensorData(getDatalist(selected), sensordata)
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
    
    def minimal(self):
        pass

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

waarde = Entry(rolluiken)
waarde.place(x=450, y=130)

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
    #l = ard.sensor.return_data(datetime.datetime.now(), datetime.datetime.now())
    l = ard.sensor.return_alle_data()
    return l

# volgens mij waren deze en de volgende onbedoeld weggehaald
def omlaag_command():
    ar = get_arduino(selected)
    ar.status_omlaag()

def omhoog_command():
    ar = get_arduino(selected)
    ar.status_omhoog()

def manual_command():
    ar = get_arduino(selected)
    ar.status_manual()

def autonomy_command():
    ar = get_arduino(selected)
    ar.status_autonomy()

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

# Methodes voor veranderen van waarden
def verander_min():
    ar = get_arduino(selected)
    value = getint(waarde.get())
    data_transfer.change_lower_limiet(ar, value)

def verander_max():
    ar = get_arduino(selected)
    value = getint(waarde.get())
    data_transfer.change_higher_limiet(ar, value)

def verander_max_uitrol():
    ar = get_arduino(selected)
    value = getint(waarde.get())
    data_transfer.change_higher_rollout(ar, value)

def verander_min_uitrol():
    ar = get_arduino(selected)
    value = getint(waarde.get())
    data_transfer.change_lower_rollout(ar, value)

# selected was dropdown
selected = StringVar(rolluiken)

#class aanroepen/instellen + start window
window=Window(root)
root.mainloop()         