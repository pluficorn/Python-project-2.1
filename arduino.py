import data_transfer
import datetime
import string
import serial
import time
import threading
from datetime import timedelta

# This file is meant for setting the settings. So max

str = string

#####################################################################################################################################

class Sensor():

    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=999999, min=0):
        self.min = min
        self.max = max
        self.data = {}
    
    # verander het bovenste limiet
    def change_max(self, value, port):
        if value != self.max and value > self.min:
            data_transfer.change_limiet(port, 'max', value)
            self.max = value
    
    # verander het onderste limiet
    def change_min(self, value, port):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(port, 'min', value)
            self.min = value

    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self, port):
        datum = datetime.datetime.now()
        jaar = datum.year
        maand = datum.month
        dag = datum.month

        data = data_transfer.get_data(port)

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

    def return_data(self, begindatum, einddatum):

        b_datum = datetime.datetime(*begindatum)
        e_datum = datetime.datetime(*einddatum)

        verschil = e_datum - b_datum

        if verschil <= 0:
            pass

            # gemiddelde data per uur over 1 dag
        if verschil.days is 1:

            # bereken per uur het gemiddelde en voeg het toe aan een lijst
            l = []
            datum = self.data[b_datum.year][b_datum.month][b_datum.day]
            for uur in datum:
                tijdstip =datum[uur]
                l.append(sum(tijdstip)/len(tijdstip))

        elif verschil.days is 7:
            l = []
            # gem per dag over 1 week
            for i in range(verschil.days + 1):
                datum = b_datum + timedelta(days=i)
                dagdata = self.data[datum.year][datum.month][datum.day]
                totaal = 0
                lengte = 0

                # tel alles van de dag op
                for uur in dagdata:
                    totaal = sum(dagdata[uur])
                    lengte += len(dagdata[uur])

                # voeg het gemiddelde per dag toe aan de lijst
                l.append(totaal/lengte)

        elif b_datum.month is (e_datum.month - 1) and b_datum.day is e_datum.day:
            l = []
            # gem per dag over 1 week
            for i in range(verschil.days + 1):
                datum = b_datum + timedelta(days=i)
                dagdata = self.data[datum.year][datum.month][datum.day]
                totaal = 0
                lengte = 0

                # tel alles van de dag op
                for uur in dagdata:
                    totaal += sum(dagdata[uur])
                    lengte += len(dagdata[uur])

                # voeg het gemiddelde per dag toe aan de lijst
                l.append(totaal/lengte)
        # over een volledig jaar of periodes gebasseerd op gemiddelde per maand
        elif verschil is 365 or b_datum.day is e_datum.day and b_datum.month is not e_datum.month - 1:
            for i in range(verschil.days + 1):
                datum = b_datum + timedelta(days=i)
                maanddata = self.data[datum.year][datum.month]
                totaal = 0
                lengte = 0
                
                # tel alles van de maand op
                for dag in maanddata:
                    dagdata = maanddata[dag]
                    for uur in dagdata:
                        totaal += sum(dagdata[uur])
                        lengte += len(dagdata[uur])
                
                l.append(totaal/lengte)
        else:
            # stuurt een lege lijst terug als 
            l = []

        return l

    def laatste_lezing(self):
        datum = datetime.datetime.now()
        return self.data[datum.year][datum.month][datum.day][datum.hour][-1]

#####################################################################################################################################

class Lichtsensor(Sensor):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=80000, min=10000):
        super().__init__(min, max)
                
#####################################################################################################################################

class Temperatuursensor(Sensor):
    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=22, min=18):
        super().__init__(min, max)

#####################################################################################################################################

class Luchtvochtigheid(Sensor):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=80000, min=10000):
        super().__init__(min, max)

#####################################################################################################################################

class Arduino():

    # arduino is 1 item uit de lijst arduino_port uit connections
    def __init__(self, arduino, status, *sensor):
        self.port = arduino[0]
        self.naam = arduino[1].split(" (COM")[0]
        self.sensor = sensor
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

    def return_port(self):
        return self.port

#####################################################################################################################################
