import data_transfer
import datetime
import string
import serial
import time
import threading

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
    
    def set_status(self, position):
        
        data_transfer.send_command(self.port, position)
        self.status = position
    
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

    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value
        
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

class Temperatuur(Arduino):
    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=22, min=18):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = {}
    
    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value

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

    def change_max(self, value):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(self.port, 'max', value)
            self.max = value
    
    def change_min(self, value):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(self.port, 'min', value)
            self.min = value
    
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

