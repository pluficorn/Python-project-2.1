# import connections
import serial.tools.list_ports
import serial
import time
import arduino
from string import ascii_lowercase

# set Baut als constant
CONST_BAUT = 19200
CONST_INROLLEN = "0x01"
CONST_UITROLLEN = "0x02"
CONST_STOPROLLEN = "0x03"
# 0x10
# zet waarden voor bepalen sensor
CONST_SWITCH = 50

# methode voor het verkrijgen van de status van de rolluik / scherm (of hij ingerold is, uitgerold, of gedeeltelijk)
# de code blijft nu constant running
# redo code tomorrow
def retreive_data(ar):
    port = ar.return_port()
    sensor = ar.return_sensor()
    ser = ar.serial
    temp = 0
    
    past = 0    # tijd voorbij sinds laatste keer opslaan van gem
    m = 60      # tijd in sec om gem op te slaan
    s = 60

    # # zet te tijd in seconden tussen metingen
    # if isinstance(type(sensor), arduino.Temperatuursensor()):
    #     s = 40
    # elif isinstance(type(sensor), arduino.Lichtsensor()):
    #     s = 30
    # # als we de sensor niet weten, lezen we elke minuut
    # else:
    #     s = 60
    
    while(1):
        b = ser.read()
        value = int.from_bytes(b, byteorder='little')
        
        # past += s
        # # als er 1 minuut of meer voorbij is
        # if past >= m:
        #     # overlap = overlap over de minuut
        #     overlap = past - m
        #     # aantal sec - overlap
        #     x = s - overlap
        #     temp += (value * x)
        #     gem = value / m
        #     ar.sensor.collect_data(port, gem)

        #     # zet waardes gebasseerd op overlap
        #     # met overlap worden er alvast waardes ingezet die meetellen tot het gem.
        #     # bij overlap = 0 wordt alles op 0 gezet
        #     past = overlap
        #     temp = (value * overlap)

        # else:
        #     # gewoon toevoegen aan temp als nog geen minuut verlopen zal zijn
        #     temp += (value * s)

        ar.sensor.collect_data(port, gem)
        time.sleep(s)
        
# methode gebruiken om uit te vinden welke arduino het is
def get_sensor(port,  minimum = 0, maximum = 0):
    ser = serial.Serial(port, CONST_BAUT)
    x = 1
    while(x):
        b = ser.read()
        value = int.from_bytes(b, byteorder='little')

        if value < CONST_SWITCH:
            if minimum and maximum:
                result = arduino.Temperatuursensor(maximum, minimum) 
            else:
                result = arduino.Temperatuursensor() 
        elif value > CONST_SWITCH:
            if minimum and maximum:
                result = arduino.Lichtsensor(maximum, minimum)
            else:
                result = arduino.Lichtsensor()
        else:
            if minimum and maximum:
                result = arduino.Sensor(maximum, minimum)
            else:
                result = arduino.Sensor()
        x = 0
    return result

# methode om de positie van de rolluik te veranderen
def command_omhoog(ar):
    ser = ar.serial
    v = 1
    time.sleep(0.1)
    b = v.to_bytes(1, 'little')
    ser.write(b)

def command_omlaag(ar):
    ser = ar.serial
    v = 2
    time.sleep(0.1)
    b = v.to_bytes(1, 'little')
    ser.write(v)
    
def change_limiet(ar, value):
    # alle data lezen en zelf gemmiddelde per minuut
    # moet nog toegevoegd worden
    ser = ar.serial
    if(value >= 0 and value < 256):
        byte = value.to_bytes(1, 'little')
        ser.write(byte)
        time.sleep(0.1)

    