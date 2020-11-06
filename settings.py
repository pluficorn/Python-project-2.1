import data_transfer

# This file is meant for setting the settings. So max

class Arduino():

    def __init__(self, naam, status="onbekend"):
        self.naam = naam
        self.status = status



#####################################################################################################################################

class Lichtsensor(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, naam, status="onbekend", max=80000, min=10000):
        super().__init__(naam, status)
        self.min = min
        self.max = max
        self.data = str()

#####################################################################################################################################

class Temperatuur(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, naam, status="onbekend", max=22, min=18):
        super().__init__(naam, status)
        self.min = min
        self.max = max
        self.data = []

#####################################################################################################################################

class Luchtvochtigheid(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, naam, status="onbekend", max=80000, min=10000):
        super().__init__(naam, status)
        self.min = min
        self.max = max
        self.data = str()