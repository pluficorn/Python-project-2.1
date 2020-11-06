import connections
import serial.tools.list_ports
import serial
import time

arduino_port = connections.arduino_port
# vraag om de data van de arduino. Idee is 1 regel per keer. 
# Dit moet elke 60 seconden voor alle sensors worden uitgevoerd
def get_data(arduino):
    
    # https://problemsolvingwithpython.com/11-Python-and-External-Hardware/11.04-Reading-a-Sensor-with-Python/

    # nodig om data op te halen, de 9600 is de baut. Verander dit naar de werkelijke baut die gebruikt wordt wanneer dit niet overeen komt met de code
    arduino_serial = serial.Serial(arduino_port[0][0], 9600)

    b = arduino_serial.readline()           # read a byte string
    string_n = b.decode()                   # decode byte string into Unicode  
    string = string_n.rstrip()              # remove \n and \r
    flt = float(string)                     # convert string to float

    arduino_serial.close()
    return (flt)

# methode voor het verkrijgen van de status van de rolluik / scherm (of hij ingerold is, uitgerold, of gedeeltelijk)
def get_position(arduino):
    # check which lamp is on on the arduino

    return "onbekend"

# methode om de positie van de rolluik te veranderen
def change_position(arduino, positie):
    # tell arduino to turn on other light
    return "onbekend"

arduino_dict = {}
for port in arduino_port:
    arduino_dict[port] = {}
    arduino_dict[port]["com"] = port[0]
