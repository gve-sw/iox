#!/usr/bin/python
# Author stevenyee
#     All rights reserved.
# DESCRIPTION
#     Raspberry Sensorhat sensor operations.
# from sense_hat import SenseHat
from random import randint

class SenseHat(object):
    def get_temperature(self):

        temperatureData = [{"temperature" : 35.35, "ts" : 1476833997042},
            {"temperature" : 35.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 35.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 35.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 85.35, "ts" : 1476833997042},
            {"temperature" : 45.45, "ts" : 1476833997042},
            {"temperature" : 55.55, "ts" : 1476833997042},
            {"temperature" : 65.65, "ts" : 1476833997042},
            {"temperature" : 75.75, "ts" : 1476833997042},
            {"temperature" : 85.85, "ts" : 1476833997042},
            {"temperature" : 95.95, "ts" : 1476833997042},
            {"temperature" : 1050.35, "ts" : 1476833997042},
            {"temperature" : 1150.35, "ts" : 1476833997042},
            {"temperature" : 1250.35, "ts" : 1476833997042},
            {"temperature" : 1350.35, "ts" : 1476833997042},
            {"temperature" : 1450.35, "ts" : 1476833997042},
            {"temperature" : -1050.35, "ts" : 1476833997042},
            {"temperature" : -1150.35, "ts" : 1476833997042},
            {"temperature" : -1250.35, "ts" : 1476833997042},
            {"temperature" : -1350.35, "ts" : 1476833997042},
            {"temperature" : -1450.35, "ts" : 1476833997042}
            ]
        temperature = temperatureData[randint(0, len(temperatureData) - 1)]["temperature"]
        return temperature


sense = SenseHat()

def get_sim_data(type):
    return {
     'temperature':75,       
     'humidity':35,       
     'barometricpressure':25,       
     'magnetometer': 10,       
     'accelerometer': 30,       
     'gyroscope':20       
      }.get(type, 'None')

# Round the data to two digit float    
def get_data_rounded(raw_data):
    if type(raw_data) is dict:
        for key in raw_data:
            raw_data[key] = float("{0:.2f}".format(raw_data[key]))
    else:
        if type(raw_data) is float:
            raw_data = float("{0:.2f}".format(raw_data))
    return raw_data

# Get the sensehat data, return None if the item requested is not available    
def get_data(type):
    return {
     'temperature':         get_data_rounded(sense.get_temperature())
     # 'humidity':            get_data_rounded(sense.get_humidity()),       
     # 'barometricpressure':  get_data_rounded(sense.get_pressure()),     
     # 'magnetometer':        get_data_rounded(sense.get_compass_raw()), 
     # 'accelerometer':       get_data_rounded(sense.get_accelerometer()), 
     # 'gyroscope':           get_data_rounded(sense.get_gyroscope())
      }.get(type, 'None')

