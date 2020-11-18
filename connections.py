import serial.tools.list_ports
import time
import threading


# https://en.it1352.com/article/1940209.html
# in cmd: pip3 install pyserial
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]


# als de Arduino Uno in de port zit, toevoegen aan de lijst
arduino_port = [port for port in myports if 'Arduino Uno' in port[1]]
