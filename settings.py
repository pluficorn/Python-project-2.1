import data_transfer

# This file is meant for setting the settings. So max


arduino_dict = data_transfer.arduino_dict

# sets the value voor het uitrollen
def set_max_out(arduino, value):
    arduino_dict[arduino]["max. uitrol"] = value

def set_sensortype(arduino, sensor):
    arduino_dict[arduino]["sensor"] = sensor

def set_signal_out(arduino, value):
    arduino_dict[arduino]["signaalwaarde"] = value

def set_status(arduino):
    arduino_dict[arduino]["status"] = data_transfer.get_position(arduino)


