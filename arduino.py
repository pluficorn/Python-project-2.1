import data_transfer
import datetime
import string
import serial
import time
import threading
from datetime import timedelta

year = datetime.datetime(2020, 11, 1).year
month = datetime.datetime(2020, 11, 1).month
day1 = datetime.datetime(2020, 11, 1).day 
day2 = datetime.datetime(2020, 11, 2).day
day3 = datetime.datetime(2020, 11, 3).day
day4 = datetime.datetime(2020, 11, 4).day
day5 = datetime.datetime(2020, 11, 5).day
day6 = datetime.datetime(2020, 11, 6).day
day7 = datetime.datetime(2020, 11, 7).day
day8 = datetime.datetime(2020, 11, 8).day
day9 = datetime.datetime(2020, 11, 9).day
day10 = datetime.datetime(2020, 11, 10).day
day11 = datetime.datetime(2020, 11, 11).day
day12 = datetime.datetime(2020, 11, 12).day
day13 = datetime.datetime(2020, 11, 13).day
day14 = datetime.datetime(2020, 11, 14).day
day15 = datetime.datetime(2020, 11, 15).day
day16 = datetime.datetime(2020, 11, 16).day
day17 = datetime.datetime(2020, 11, 17).day
day18 = datetime.datetime(2020, 11, 18).day
day19 = datetime.datetime(2020, 11, 19).day
day20 = datetime.datetime(2020, 11, 20).day
day21 = datetime.datetime(2020, 11, 21).day
day22 = datetime.datetime(2020, 11, 22).day
day23 = datetime.datetime(2020, 11, 23).day
day24 = datetime.datetime(2020, 11, 24).day
day25 = datetime.datetime(2020, 11, 25).day
hour1 = datetime.datetime(2020, 11, 1, 0).hour
hour2 = datetime.datetime(2020, 11, 1, 1).hour
hour3 = datetime.datetime(2020, 11, 1, 2).hour

testdata = {
    year: {
        month: {
            day1: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day2: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day3: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day4: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day5: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day6 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day7 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day8 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day9: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day10 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day11: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day12: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day13: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day14: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day15: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day16 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day17 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day18 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day19: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day20 : {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day21: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day22: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day23: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day24: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            },
            day25: {
                hour1: [25, 12,7, 27, 20, 0, 24, 21, 3, 30],
                hour2: [31, 34, 32, 5, 14, 10, 6, 2, 33, 23],
                hour3: [8, 15, 17, 19, 26, 9, 22, 35, 28, 16]
            }
        }
    }
}

#pprint(testdata[2020][11])
#####################################################################################################################################

class Sensor:

    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, max=200, min=10):
        self.min = min
        self.max = max
        self.data = testdata
    
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
                         self.data[jaar][maand][dag] = { 
                            uur: [value]
                        }
                else:
                    self.data[jaar][maand] = { 
                        dag : {
                            uur: [value]
                        }
                    }
            else:
                self.data[jaar] = { 
                    maand: {
                        dag : {
                            uur: [value]
                        }
                    }
                }
        else:
            self.data[jaar] = { 
                maand: {
                    dag : {
                        uur: [value]
                    }
                }
            }

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

# s = Sensor()
