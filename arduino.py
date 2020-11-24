import data_transfer
import datetime
import string
import serial
import time
import threading
from datetime import timedelta

#####################################################################################################################################

class Sensor:

    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=200, min=10):
        self.min = min
        self.max = max
        self.data = {}
    
    # verander het bovenste limiet
    def change_max(self, value):
        # Can't be equal or lower than the min
        # Useless if value == max
        try:
            if value <= self.min:
                raise ValueError("the value needs to be higher than", self.min)
            if value == self.max:
                raise ValueError("the higher limit is already set on", value)
            data_transfer.change_higher_limiet(self, value)
        except ValueError as ve:
            print(ve)

    # verander het onderste limiet
    def change_min(self, value):
        # Can't be equal or higher than the max
        # Useless if value == min
        try:
            if value >= self.max:
                raise ValueError("the value needs to be lower than", self.max)
            if value == self.min:
                raise ValueError("the lower limit is already set on ", value)
            data_transfer.change_lower_limiet(self, value)
        except ValueError as ve:
            print(ve)

    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self, value):
        datum = datetime.datetime.now()
        jaar = datum.year
        maand = datum.month
        dag = datum.month
        uur = datum.hour

        if jaar in self.data:
            if maand in self.data[jaar]:
                if dag in self.data[jaar][maand]:
                    if uur in self.data[jaar][maand][dag]:
                        self.data[jaar][maand][dag][uur].append(value)
                    else:
                         self.data[jaar][maand][dag][uur] = [value]
                else:
                    self.data[jaar][maand][dag][uur] = [value]
            else:
                self.data[jaar][maand][dag][uur] = [value]
        else:
            self.data[jaar][maand][dag][uur] = [value]

    # returnd lijst van gemiddelden gebasseerd op de periode tussen begin en eind datum (het is tot en met, dus laatste dag wordt ook gegeven)
    def return_data(self, begindatum, einddatum):
        b_datum = begindatum
        e_datum = einddatum

        verschil = e_datum - b_datum
            # gemiddelde data per uur over 1 dag
        if verschil.days == 0:
            # bereken per uur het gemiddelde en voeg het toe aan een lijst
            l = {}
            l["uur"] = []
            l["gemiddelde"] = []
            datum = self.data[b_datum.year][b_datum.month][b_datum.day]
            for uur in datum:
                tijdstip =datum[uur]
                l["uur"].append(uur)
                l["gemiddelde"].append((round((sum(tijdstip)/len(tijdstip))*10))/10)

        else:
            # stuurt een lege lijst terug als 
            l = {}

        return l
    
    #retourneerd de laatste lezing 
    def laatste_lezing(self):
        datum = datetime.datetime.now()
        return self.data[datum.year][datum.month][datum.day][datum.hour][-1]  

#####################################################################################################################################

class Lichtsensor(Sensor):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=200, min=10):
        super().__init__(min, max)
                
#####################################################################################################################################

class Temperatuursensor(Sensor):
    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=25, min=15):
        super().__init__(min, max)

#####################################################################################################################################

class Arduino:
    # arduino is 1 item uit de lijst arduino_port uit connections
    def __init__(self, arduino, sensor, rolmin=2, rolmax=100):
        self.port = str(arduino[0])
        self.naam = arduino[1].split(" (COM")[0]
        self.sensor = sensor
        self.serial = serial.Serial(self.port,  data_transfer.CONST_BAUT)
        self.status = "omhoog"
        self.rolmin = rolmin
        self.rolmax = rolmax
        time.sleep(5)
        
        # retreive_data(self)
    
    # verander de status van de arduino (of hij ingerold op uitgerold is)
    def status_omhoog(self):
        data_transfer.command_omhoog(self)
        self.status = "omhoog"
    
    def status_omlaag(self):
        data_transfer.command_omlaag(self)
        self.status = "omlaag"
    
    # verander de naam
    def set_naam(self, naam):
        self.naam = naam

    def change_min_rol_limit(self, value):
        # Can't be equal or higher than the max
        # Useless if value == min
        try:
            if value >= self.rolmax:
                raise ValueError("the value needs to be lower than", self.rolmax)
            if value == self.rolmin:
                raise ValueError("the lower limit is already set on ", value)
            data_transfer.change_lower_rollout(self, value)
        except ValueError as ve:
            print(ve)
    
    def change_max_rol_limit(self, value):
        # Can't be equal or lower than the min
        # Useless if value == max
        try:
            if value <= self.rolmin:
                raise ValueError("the value needs to be higher than", self.rolmin)
            if value == self.rolmax:
                raise ValueError("the higher limit is already set on ", value)
            data_transfer.change_higher_rollout(self, value)
        except ValueError as ve:
            print(ve)

#####################################################################################################################################
