import serial.tools.list_ports
import time
import threading


# https://en.it1352.com/article/1940209.html
# in cmd: pip3 install pyserial
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]


# als de Arduino Uno in de port zit, toevoegen aan de lijst
arduino_port = [port for port in myports if 'Arduino Uno' in port[1]]

# checks of arduino nog aanwezig is
def check_presence(correct_port, interval=0.1):

    while True:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

        if arduino_port not in myports:
            print ("Arduino has been disconnected!")
            break

        time.sleep(interval)

port_controller = threading.Thread(target=check_presence, args=(arduino_port, 0.1,))
port_controller.setDaemon(True)
port_controller.start()