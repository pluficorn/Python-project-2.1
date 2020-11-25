import serial.tools.list_ports
import time
import threading
import data_transfer
import arduino

CONST_COM1 = "COM1"
CONST_COM2 = "COM2"
CONST_COM3 = "COM3"
CONST_COM4 = "COM4"
CONST_COM5 = "COM5"
CONST_COM6 = "COM6"

# Zet in deze lijst alle coms met een arduino verbonden
ports = input("Give the COMs with ',' between the different COMs: ")
ports_list = ports.split(",")
arduino_ports = [i.upper() for i in ports_list]

# # hardcoded
# arduino_ports = [CONST_COM4]


# https://en.it1352.com/article/1940209.html
# in cmd: pip3 install pyserial
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

# als de Arduino Uno in de port zit, toevoegen aan de lijst
arduino_port = [port for port in myports if port[0] in arduino_ports]

# lege list om de arduinos in op te slaan
arduinos = []
threads = []
# voor elke arduino...
for ar in arduino_port:
    # Kijk welke sensor wordt meegegeven
    #sensor = data_transfer.get_sensor(ar[0])
    i = input("give 'T' for temperaturesensor, give 'L' for lightsensor: ")
    try:
        if i.upper() == 'T':
            sensor = arduino.Temperatuursensor()

        elif i.upper() == 'L':
            sensor = arduino.Lichtsensor()
        else:
            raise ValueError("we don't have that sensor, use 'T' or 'L' to appoint a sensor")
    except ValueError as ve:
        print (ve)
        
    # Voeg een arduino klasse Arduino toe aan de list
    arduinos.append(arduino.Arduino(ar, sensor))
    current = arduinos[-1]
    data_transfer.send_sensor(current)
    # Add data reading method to threading (so it runs in the background)
    t = threading.Thread(target=data_transfer.retreive_data, args= [current])
    t.start()
    threads.append(t)