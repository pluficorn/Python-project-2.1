import data_transfer

# This file is meant for setting the settings. So max

class Arduino():

    # arduino is 1 item uit de lijst arduino_port uit connections
    def __init__(self, arduino, status="onbekend"):
        self.port = arduino[0]
        self.naam = arduino[1].split(" (COM")[0]
        self.status = status
    
    def set_status(self, position):
        data_transfer.set_position(self.port, position)
    
    def set_naam(self, naam):
        self.naam = naam



#####################################################################################################################################

class Lichtsensor(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=80000, min=10000):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = str()

    def change_max(self, value):
        data_transfer.set_max(self.port, value)
    
    def change_min(self, value):
        data_transfer.set_min(self.port, value)

#####################################################################################################################################

class Temperatuur(Arduino):
    # Bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=22, min=18):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = []
    
    def change_max(self, value):
        data_transfer.set_max(self.port, value)
    
    def change_min(self, value):
        data_transfer.set_min(self.port, value)

#####################################################################################################################################

class Luchtvochtigheid(Arduino):
    #bij max gaan ze naar beneden, bij min gaan ze omhoog
    def __init__(self, arduino, status="onbekend", max=80000, min=10000):
        super().__init__(arduino, status)
        self.min = min
        self.max = max
        self.data = str()

    def change_max(self, value):
        data_transfer.set_max(self.port, value)
    
    def change_min(self, value):
        data_transfer.set_min(self.port, value)

#####################################################################################################################################

