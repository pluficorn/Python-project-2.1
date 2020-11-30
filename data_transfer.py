# import connections
import serial.tools.list_ports
import serial
import time
import arduino
import struct
from string import ascii_lowercase

# set const
CONST_BAUT = 19200
CONST_INROLLEN = b'\x01'
CONST_UITROLLEN = b'\x02'
CONST_STOPROLLEN = b'\x03'
CONST_TEMP_SENSOR = b'\x04'
CONST_LICHT_SENSOR = b'\x05'
CONST_MAX_TEMP_CHANGE = b'\x07'
CONST_MAX_LICHT_CHANGE = b'\x08'
CONST_MAX_ROLLOUT_CHANGE = b'\x09'
CONST_MIN_TEMP_CHANGE = b'\x0A'
CONST_MIN_LICHT_CHANGE = b'\x0B'
CONST_MIN_ROLLOUT_CHANGE = b'\x0C'
CONST_MANUAL = (b'\x0E')
CONST_AUTOMATIC = (b'\x0D')

CONST_SLEEP = 0.01

# weet zo niet waar deze voor is
CONST_SWITCH = 50

# # Data ophalen en opslaan
def retreive_data(ar):
    ser = ar.serial
    sensor = ar.sensor
    # tijd tussen lezingen
    s = 6
    if isinstance(sensor, type(arduino.Lichtsensor())):
        sign = False
    else:
        sign = True
    # print("one")
    while(1):
        incoming_bytes = ser.read(4)
        number_array = struct.unpack('<BBBB', incoming_bytes)
        print(incoming_bytes, number_array)
        if number_array[2] == 31:
            sensor.collect_data(number_array[3])
        time.sleep(s)

def send_sensor(ar):
    sensor = ar.sensor
    ser = ar.serial
    print("hello")
    if isinstance(sensor, type(arduino.Temperatuursensor())):
        ser.write(CONST_TEMP_SENSOR)
        # ser.write(1)
    else:
        ser.write(CONST_LICHT_SENSOR)

# Command om op te rollen
def command_omhoog(ar):
    ser = ar.serial
    print("sending",b'\x01', "moet 01 zijn")
    ser.write(b'\x01')

# Command om uit te rollen
def command_omlaag(ar):
    ser = ar.serial
    print("omlaag")
    print("sending",b'\x02', "moet 02 zijn")
    ser.write(b'\x02')

def command_autonomy(ar):
    ser = ar.serial
    print("sending",b'\x0D', "moet 0D zijn")
    ser.write(b'\x0D')

def command_manual(ar):
    ser = ar.serial
    print("sending",b'\x0E', "moet 0E zijn")
    ser.write(b'\x0E')

# Command to change lower limit for temp & light sensors 
def change_lower_limiet(ar, value):
    ser = ar.serial
    sensor = ar.sensor
    # print("higher")
    try:
        if isinstance(sensor, type(arduino.Temperatuursensor())):
            # 0x0A, opgevolgd met een nummer van -128-127 (signed byte): minimumtemperatuur
            # check if value is between values for arduino code
            if value < -128 or value > 127:
                raise ValueError("The value has to be between -128 and 127.")

            b = value.to_bytes(1, 'little', signed=True)
            ser.write(CONST_MIN_TEMP_CHANGE)
            while ser.out_waiting > 0 :
                pass
            ser.write(b)

        elif isinstance(sensor, type(arduino.Lichtsensor())):
            # 0x0B, opgevolgd met een nummer van 0-255 (unsigned byte): minimumlichteenheid
            # check waarde voor adruino
            if value < 0 or value > 255:
                raise ValueError("The value has to be between 0 and 255.")

            b = value.to_bytes(1, 'little', signed=False)
            ser.write(CONST_MIN_LICHT_CHANGE)
            while ser.out_waiting > 0 :
                pass
            ser.write(b)
    except ValueError as ve:
            print(ve)

# Command to change higher limit for temp & light sensors 
def change_higher_limiet(ar, value):
    ser = ar.serial
    sensor = ar.sensor
    # print("lower")
    try:
        if isinstance(sensor, type(arduino.Temperatuursensor())):
            # 0x07, opgevolgd met een nummer van -128-127 (signed byte): maximumtemperatuur
            # check if value is between values for arduino code
            if value < -128 or value > 127:
                raise ValueError("The value has to be between -128 and 127.")

            b = value.to_bytes(1, 'little', signed=True)
            ser.write(CONST_MAX_TEMP_CHANGE)
            while ser.out_waiting > 0 :
                pass
            ser.write(b)

        elif isinstance(sensor, type(arduino.Lichtsensor())):
            # 0x08, opgevolgd met een nummer van 0-255 (unsigned byte): maximumlichteenheid
            # check value for arduino
            if value < 0 or value > 255:
                raise ValueError("The value has to be between 0 and 255.")

            b = value.to_bytes(1, 'little', signed=False)
            ser.write(CONST_MAX_LICHT_CHANGE)
            while ser.out_waiting > 0 :
                pass
            ser.write(b)
    except ValueError as ve:
            print(ve)  

def change_lower_rollout(ar, value):
    ser = ar.serial
    # print("lower rollout")
    try:
        # 0x0C, opgevolgd met een nummer van 2-255 (unsigned byte): minimumuitrolafstand
        # check waarde voor adruino
        if value < 0 or value > 255:
            raise ValueError("The value has to be between 0 and 255.")

        b = value.to_bytes(1, 'little', signed=False)
        ser.write(CONST_MIN_ROLLOUT_CHANGE)
        while ser.out_waiting > 0 :
            pass
        ser.write(b)
    except ValueError as ve:
            print(ve)

def change_higher_rollout(ar, value):
    ser = ar.serial
    # print("higher rollout")
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
