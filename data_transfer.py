import connections
import serial.tools.list_ports
import serial
import time
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
def retreive_data(port):
    with serial.Serial(port) as ser:
        busy = True
        while(busy):
            b = ser.read()
            print (b)
            print(int.from_bytes(b, byteorder='little'))
            time.sleep(60)

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
    ser = serial.Serial(port, CONST_BAUT)
    if(value >= 0 and value < 256):
        byte = value.to_bytes(1, 'little')
        ser.write(byte)
        time.sleep(0.1)
    
    
    

# 0X01 -- OPROLLEN
# 0X02 -- ROLLEN
# 0X03 -- STOP_ROLLEN

# .... NOG ONBEKEND VOOR DATA VAN DE SENSOREN