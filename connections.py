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



# vraag om de data van de arduino. Idee is 1 regel per keer
def read_input(arduino, interval):
    
    # https://problemsolvingwithpython.com/11-Python-and-External-Hardware/11.04-Reading-a-Sensor-with-Python/

    # nodig om data op te halen, de 9600 is de baut. Verander dit naar de werkelijke baut die gebruikt wordt wanneer dit niet overeen komt met de code
    arduino_serial = serial.Serial(arduino_port[0][0], 9600)

    b = arduino_serial.readline()           # read a byte string
    string_n = b.decode()                   # decode byte string into Unicode  
    string = string_n.rstrip()              # remove \n and \r
    flt = float(string)                     # convert string to float

    arduino_serial.close()
    return (flt)



# voor het plotten van een lijngrafiek
#import matplotlib.pyplot as plt
# if using a Jupyter notebook include
#%matplotlib inline

#plt.plot(data)
#plt.xlabel('Time (seconds)')
#plt.ylabel('Potentiometer Reading')
#plt.title('Potentiometer Reading vs. Time')
#plt.show()