import connections
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

# vraag om de data van de arduino. Idee is 1 regel per keer. 
# Dit moet elke 60 seconden voor alle sensors worden uitgevoerd
def get_data(port):
    
    # https://problemsolvingwithpython.com/11-Python-and-External-Hardware/11.04-Reading-a-Sensor-with-Python/

    # nodig om data op te halen, de 9600 is de baut. 
    # Verander dit naar de werkelijke baut die gebruikt wordt wanneer dit niet overeen komt met de code
    # 
    arduino_serial = serial.Serial(port, CONST_BAUT)

    b = arduino_serial.readline()           # read a byte string
    string_n = b.decode()                   # decode byte string into Unicode  
    string = string_n.rstrip()              # remove \n and \r
    flt = float(string)                     # convert string to float

    arduino_serial.close()
    return (flt)


# methode voor het verkrijgen van de status van de rolluik / scherm (of hij ingerold is, uitgerold, of gedeeltelijk)
# de code blijft nu constant running
def retreive_data(ar):
    port = ar.return_port()
    sensor = ar.return_sensor()
    ser = serial.Serial(port, CONST_BAUT)
    temp = 0
    
    past = 0    # tijd voorbij sinds laatste keer opslaan van gem
    m = 60      # tijd in sec om gem op te slaan

    # zet te tijd in seconden tussen metingen
    if isinstance(sensor, arduino.Temperatuursensor()):
        s = 40
    elif isinstance(sensor, arduino.Lichtsensor()):
        s = 30
    # als we de sensor niet weten, lezen we elke minuut
    else:
        s = 60
    
    while(1):
        b = ser.read()
        value = int.from_bytes(b, byteorder='little')
        past += s
        # als er 1 minuut of meer voorbij is
        if past >= m:
            # overlap = overlap over de minuut
            overlap = past - m
            # aantal sec - overlap
            x = s - overlap
            temp += (value * x)
            gem = value / m
            ar.sensor.collect_data(port, gem)

            # zet waardes gebasseerd op overlap
            # met overlap worden er alvast waardes ingezet die meetellen tot het gem.
            # bij overlap = 0 wordt alles op 0 gezet
            past = overlap
            temp = (value * overlap)

        else:
            # gewoon toevoegen aan temp als nog geen minuut verlopen zal zijn
            temp += (value * s)
        time.sleep(s)

# methode gebruiken om uit te vinden welke arduino het is
def get_sensor(ar):
    # ar is nog geen Arduino klasse!!!
    # lees [0] voor port
    # lees regel om sensor te achterhalen
    return 0



# methode om de positie van de rolluik te veranderen
def command_omhoog(port):
    ser = serial.Serial(port, CONST_BAUT)
    time.sleep(0.1)
    ser.write(chr(0x01))

def command_omlaag(port):
    ser = serial.Serial(port, CONST_BAUT)
    time.sleep(0.1)
    ser.write(chr(0x02))
    

def change_limiet(port, value):
    # alle data lezen en zelf gemmiddelde per minuut
    # moet nog toegevoegd worden
    ser = serial.Serial(port, CONST_BAUT)
    if(value >= 0 and value < 256):
        byte = value.to_bytes(1, 'little')
        ser.write(byte)
        time.sleep(0.1)
    
    
    

# 0X01 -- OPROLLEN
# 0X02 -- ROLLEN
# 0X03 -- STOP_ROLLEN

# .... NOG ONBEKEND VOOR DATA VAN DE SENSOREN