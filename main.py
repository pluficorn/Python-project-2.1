import arduino
import connections
import data_transfer
import window
import serial.tools.list_ports
import time

# Haal lijst met porten op waar arduinos aan verbonden zijn
arduino_port = connections.arduino_port
arduinos = {}
for ar in arduino_port:
    # werkelijke sensor moet nog achterhaalt worden van arduino. 
    sensor = data_transfer.get_sensor(ar)
    if isinstance(sensor, arduino.Sensor()):
        arduinos[ar] = arduino.Arduino(ar, "onbekend", sensor)
    else:
        print("deze arduino heeft geen sensor")
    

print(arduinos)

# haal informatie van de schermen
Scherm = window.Window() 