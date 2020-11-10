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
    arduinos[ar]=(arduino.Arduino(ar, "onbekend", arduino.Lichtsensor(), arduino.Temperatuursensor()))
print(arduinos)

# haal informatie van de schermen
Scherm = window.Window() 