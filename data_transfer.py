# import connections
import serial.tools.list_ports
import serial
import time
import arduino
from string import ascii_lowercase

# set const
CONST_BAUT = 19200
CONST_INROLLEN = 0x01
CONST_UITROLLEN = 0x02
CONST_STOPROLLEN = 0x03
CONST_TEMP_SENSOR = 0x04
CONST_LICHT_SENSOR = 0x05
CONST_MAX_TEMP_CHANGE = 0x07
CONST_MAX_LICHT_CHANGE = 0x08
CONST_MAX_ROLLOUT_CHANGE = 0x09
CONST_MIN_TEMP_CHANGE = 0x0A
CONST_MIN_LICHT_CHANGE = 0x0B
CONST_MIN_ROLLOUT_CHANGE = 0x0C
CONST_SLEEP = 3

# weet zo niet waar deze voor is
CONST_SWITCH = 50

# # Data ophalen en opslaan
def retreive_data(ar):
    port = ar.port
    ser = ar.serial
    sensor = ar.sensor
    s = 60
    if isinstance(sensor, type(arduino.Lichtsensor())):
        sign = False
    else:
        sign = True

    while(1):
        b = ser.read()
        value = int.from_bytes(b, byteorder='little', signed=sign)
        ar.sensor.collect_data(value)
        time.sleep(s)

def send_sensor(ar):
    sensor = ar.sensor
    ser = ar.serial
    # ser.write(CONST_TEMP_SENSOR)

    if isinstance(sensor, type(arduino.Temperatuursensor())):
        ser.write(CONST_TEMP_SENSOR)
    else:
        ser.write(CONST_LICHT_SENSOR)


# Command om op te rollen
def command_omhoog(ar):
    ser = ar.serial
    ser.write(CONST_STOPROLLEN)

# Command om uit te rollen
def command_omlaag(ar):
    ser = ar.serial
    ser.write(CONST_UITROLLEN)

# Command to change lower limit for temp & light sensors 
def change_lower_limiet(ar, value):
    ser = ar.serial
    sensor = ar.sensor()
    try:
        if isinstance(sensor, type(arduino.Temperatuursensor())):
            # 0x0A, opgevolgd met een nummer van -128-127 (signed byte): minimumtemperatuur
            # check if value is between values for arduino code
            if value < -128 or value > 127:
                raise ValueError("The value has to be between -128 and 127.")

            b = value.to_bytes(1, 'little', signed=True)
            ser.write(CONST_MIN_TEMP_CHANGE)
            time.sleep(CONST_SLEEP)
            ser.write(b)

        elif isinstance(sensor, type(arduino.Lichtsensor())):
            # 0x0B, opgevolgd met een nummer van 0-255 (unsigned byte): minimumlichteenheid
            # check waarde voor adruino
            if value < 0 or value > 255:
                raise ValueError("The value has to be between 0 and 255.")

            b = value.to_bytes(1, 'little', signed=False)
            ser.write(CONST_MIN_LICHT_CHANGE)
            time.sleep(CONST_SLEEP)
            ser.write(b)
    except ValueError as ve:
            print(ve)

# Command to change higher limit for temp & light sensors 
def change_higher_limiet(ar, value):
    ser = ar.serial
    sensor = ar.sensor()
    try:
        if isinstance(sensor, type(arduino.Temperatuursensor())):
            # 0x07, opgevolgd met een nummer van -128-127 (signed byte): maximumtemperatuur
            # check if value is between values for arduino code
            if value < -128 or value > 127:
                raise ValueError("The value has to be between -128 and 127.")

            b = value.to_bytes(1, 'little', signed=True)
            ser.write(CONST_MAX_TEMP_CHANGE)
            time.sleep(CONST_SLEEP)
            ser.write(b)

        elif isinstance(sensor, type(arduino.Lichtsensor())):
            # 0x08, opgevolgd met een nummer van 0-255 (unsigned byte): maximumlichteenheid
            # check value for arduino
            if value < 0 or value > 255:
                raise ValueError("The value has to be between 0 and 255.")

            b = value.to_bytes(1, 'little', signed=False)
            ser.write(CONST_MAX_LICHT_CHANGE)
            time.sleep(CONST_SLEEP)
            ser.write(b)
    except ValueError as ve:
            print(ve)  

def change_lower_rollout(ar, value):
    ser = ar.serial
    try:
        # 0x0C, opgevolgd met een nummer van 2-255 (unsigned byte): minimumuitrolafstand
        # check waarde voor adruino
        if value < 0 or value > 255:
            raise ValueError("The value has to be between 0 and 255.")

        b = value.to_bytes(1, 'little', signed=False)
        ser.write(CONST_MIN_ROLLOUT_CHANGE)
        time.sleep(CONST_SLEEP)
        ser.write(b)
    except ValueError as ve:
            print(ve)

def change_higher_rollout(ar, value):
    ser = ar.serial
    try:
        # 0x09, opgevolgd met een nummer van 2-255 (unsigned byte): maximumuitrolafstand
        # check waarde voor adruino
        if value < 0 or value > 255:
            raise ValueError("The value has to be between 0 and 255.")

        b = value.to_bytes(1, 'little', signed=False)
        ser.write(CONST_MAX_ROLLOUT_CHANGE)
        time.sleep(CONST_SLEEP)
        ser.write(b)
    except ValueError as ve:
            print(ve)
