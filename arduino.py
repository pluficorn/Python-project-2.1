import data_transfer
import datetime
import string
import serial
import time
import threading
from datetime import timedelta

# This file is meant for setting the settings. So max

str = string


class Arduino():

    # arduino is 1 item uit de lijst arduino_port uit connections
    def __init__(self, arduino, status="onbekend"):
        self.port = arduino[0]
        self.naam = arduino[1].split(" (COM")[0]
        self.serial = serial.Serial(self.port, data_transfer.CONST_BAUT)
        self.status = status
        time.sleep(5)
    
    # verander de status van de arduino (of hij ingerold op uitgerold is)
    def set_status(self, position):
        
        data_transfer.send_command(self.port, position)
        self.status = position
    
    # verander de naam
    def set_naam(self, naam):
        self.naam = naam

#####################################################################################################################################

class Lichtsensor(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=80000, min=10000):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = {}

    # verander het bovenste limiet
    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    # verander het onderste limiet
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value
    
    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self):
        datum = datetime.datetime.now()
        jaar = datum.year
        maand = datum.month
        dag = datum.month
        uur = datum.hour

        data = data_transfer.get_data(self.port)

        data_added = False

        if jaar in self.data:
            if maand in self.data[jaar]:
                if dag in self.data[jaar][maand]:
                    if uur in self.data[jaar][maand][dag]:
                        self.data[jaar][maand][dag][uur].append(data)
                        data_added = True

        # als het geen nieuwe sleutel heeft gecreëerd en dus geen data heeft tegevoegd,
        # wordt de data nu toegevoegd aan een al bestaande lijst
        if not data_added:
            self.data[jaar][maand][dag][uur] = [data]
            data_added = True

    def return_data(self, begindatum, einddatum):
        pass


#####################################################################################################################################

class Temperatuur(Arduino):
    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=22, min=18):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = {}
    
    # verander het bovenste limiet
    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    # verander het onderste limiet
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value

    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self):
        datum = datetime.datetime.now()
        jaar = datum.year
        maand = datum.month
        dag = datum.month

        data = data_transfer.get_data(self.port)

        if jaar in self.data:
            if maand in self.data[jaar]:
                if dag in self.data[jaar][maand]:
                    self.data[jaar][maand][dag].append(data)
                else:
                    self.data[jaar][maand][dag] = [data]
            else:
                self.data[jaar][maand][dag] = [data]
        else:
            self.data[jaar][maand][dag] = [data]

#####################################################################################################################################

class Luchtvochtigheid(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=80000, min=10000):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = {}

    # verander het bovenste limiet
    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    # verander het onderste limiet
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value
    
    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self):
        datum = datetime.datetime.now()
        jaar = datum.year
        maand = datum.month
        dag = datum.month

        data = data_transfer.get_data(self.port)

        if jaar in self.data:
            if maand in self.data[jaar]:
                if dag in self.data[jaar][maand]:
                    self.data[jaar][maand][dag].append(data)
                else:
                    self.data[jaar][maand][dag] = [data]
            else:
                self.data[jaar][maand][dag] = [data]
        else:
            self.data[jaar][maand][dag] = [data]

#####################################################################################################################################

