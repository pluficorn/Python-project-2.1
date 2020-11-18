import data_transfer
import datetime
import string
import serial
import time
import threading
from datetime import timedelta

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
            data_transfer.change_limiet(port, value)
            self.max = value
    
    # verander het onderste limiet
    def change_min(self, value, port):
        if value != self.min and value < self.max:
            data_transfer.change_limiet(port, value)
            self.min = value

    # verzamel de data van de arduino gebasseerd op datum
    def collect_data(self, port, value):
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
        b_datum = datetime.datetime(*begindatum)
        e_datum = datetime.datetime(*einddatum)

        verschil = e_datum - b_datum
            # gemiddelde data per uur over 1 dag
        if verschil.days == 0:
            # bereken per uur het gemiddelde en voeg het toe aan een lijst
            l = []
            datum = self.data[b_datum.year][b_datum.month][b_datum.day]
            for uur in datum:
                tijdstip =datum[uur]
                l.append((round((sum(tijdstip)/len(tijdstip))*10))/10)

        elif verschil.days == 6:
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
                l.append((round((totaal/lengte*10)))/10)

        elif (b_datum.month == (e_datum.month - 1) and (b_datum.day == e_datum.day + 1)) or b_datum.month == e_datum.month and ((e_datum + datetime.timedelta(days=1)).month) == (b_datum.month + 1):
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
                l.append((round((totaal/lengte*10)))/10)


        # over een volledig jaar 
        elif verschil.days == 365:
            l = []
            maand = b_datum.month
            totaal = 0
            lengte = 0
            # gem per dag over 1 week
            for i in range(verschil.days + 1):
                datum = b_datum + timedelta(days=i)
                dagdata = self.data[datum.year][datum.month][datum.day]
                    
                #print(maand, datum.month)

                if maand == datum.month:
                    # tel alles van de dag op
                    for uur in dagdata:
                        totaal += sum(dagdata[uur])
                        lengte += len(dagdata[uur])
                else:
                    print("1 maand voorbij")
                    l.append((round((totaal/lengte*10)))/10)
                    totaal = 0
                    lengte = 0
                    maand = datum.month
                    for uur in dagdata:
                        totaal += sum(dagdata[uur])
                        lengte += len(dagdata[uur])

            l.append((round((totaal/lengte*10)))/10)

        else:
            # stuurt een lege lijst terug als 
            l = []

        return l
    
    #retourneerd de laatste lezing 
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

class Arduino():

    # arduino is 1 item uit de lijst arduino_port uit connections
    def __init__(self, arduino, status, sensor):
        self.port = arduino[0]
        self.naam = arduino[1].split(" (COM")[0]
        self.sensor = sensor
        self.serial = serial.Serial(self.port, data_transfer.CONST_BAUT)
        self.status = status
        time.sleep(5)
    
    # verander de status van de arduino (of hij ingerold op uitgerold is)
    def set_status(self, position):
        
        #data_transfer.send_command(self.port, position)
        self.status = position
    
    # verander de naam
    def set_naam(self, naam):
        self.naam = naam
    def return_port(self):
        return self.port

    def return_sensor(self):
        return self.sensor

    def tuple_info(self):
        return tuple(self.naam, self.status, self.sensor.laatste_lezing())

#####################################################################################################################################
