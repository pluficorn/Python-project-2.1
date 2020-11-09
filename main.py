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
    arduinos[ar]=(arduino.Arduino(ar, "onbekend", arduino.Lichtsensor(), arduino.Temperatuur()))
print(arduinos)

# haal informatie van de schermen
Scherm = window.Window()


# toon gewenste informatie op scherm




# dict of rolluiken / schermen + status

# buttons

# dictionary van sensortype + data
    # lichtsensor per x seconden
        # dict per uur
    # temperatuur per x seconden
        # dict per uur met lijst van elke temp
    # lichtintensiteit per 30 sec

# status

# instellen hoe ver hij in- en uitrolt
# instellen wanneer hij automatisch in- en uitrolt
# toon alleen info voor verbonden apparaten

# zelf uitrollen