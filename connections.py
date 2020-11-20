import serial.tools.list_ports
import time
import threading

CONST_COM1 = "COM1"
CONST_COM2 = "COM2"
CONST_COM3 = "COM3"
CONST_COM4 = "COM4"
CONST_COM5 = "COM5"
CONST_COM6 = "COM6"

# Zet in deze lijst alle coms met een arduino verbonden
arduino_ports = [CONST_COM4]

# https://en.it1352.com/article/1940209.html
# in cmd: pip3 install pyserial
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

# als de Arduino Uno in de port zit, toevoegen aan de lijst
arduino_port = [port for port in myports if port[0] in arduino_ports]

