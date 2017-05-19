#!/usr/bin/python
# Author steveyee
#     All rights reserved.
# 
# DESCRIPTION
#     Raspberry Sensorhat web server URLs' implementations in flask.
from flask import Flask, jsonify
from uuid import getnode as get_mac
import sensor 
import time
from IOTWrapper import IOTWrapper
import sys
import argparse
import json
import time

app = Flask(__name__, static_url_path='', static_folder="static")

global myWrapper

@app.route('/status')
def status():
    deviceId = hex(get_mac())
    return jsonify({'deviceId':deviceId})

@app.route('/sensehat/<type>')
def get_data(type):
    try:
        t = sensor.get_data(type)
    except Exception as e:
        t = {}
        t[type] = '-1'
    return jsonify({'ts': int(time.time() *1000), type:t})

def pull_temperature():
    global myWrapper
    temperature = sensor.get_data('temperature')
    myWrapper.addValue(temperature)
    average = myWrapper.averageValues()
    if myWrapper.monitorSize():
        if myWrapper.monitorAverage():
            if average >= myWrapper.getHigh():
                myWrapper.sendSparkMessage("\n\nHOT DAMN HOT DAMN HOT DAMN HOT DAMN")
                myWrapper.sendSparkMessage("It's steamy in here.")
            else:
                myWrapper.sendSparkMessage("\n\nBRRRRRRR BRRRRRRR BRRRRRRR BRRRRRRR")
                myWrapper.sendSparkMessage("It's freezing in here")
            myWrapper.sendSparkMessage("There is an extreme average temperature of " + str(average) + " degrees Fahrenheit over the past " + str(myWrapper.getMaxSize() * 3) + " seconds!!!")
        else:
            myWrapper.sendSparkMessage("\n\nIt's all good in the hood")


@app.route('/initialize')
def initializeSensor(maxSize = 5, highValue = 120.0, lowValue = 60.0, roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vMjIyYTE3MjAtMjMwMi0xMWU3LWE1ZDMtYmQ4ODU5YjY3ODc4", bearer = "YzY2ZTMzNWEtOWVkYy00NDlhLThkZmYtZTNiZDQ3NTkyYTdjMDFkNjkzNTEtY2Y3"):
    global myWrapper
    myWrapper = IOTWrapper(maxSize, highValue, lowValue, roomId, bearer)
    myWrapper.sendSparkMessage("\n\nI am initialized with an interval of " + str(maxSize * 3) + " seconds\n,"
        "a high temperature of " + str(highValue) + " degrees Fahrenheit\n,"
        "and a low temperature of " + str(lowValue) + " degrees Fahrenheit\n\n"
        )
    degrassi_thread()

def degrassi_thread():
    while True:
        pull_temperature()
        time.sleep(3)

@app.route('/message/<messages>')
def show_messages(messages):
    try:
        t = sensor.set_data('messages', messages)
    except Exception as e:
        return jsonify({'Status':'Error!'})

@app.route('/')
def index():
    return app.send_static_file('index.html') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Raspberry Pi Sensehat web server")
    parser.add_argument('-p', '--port', help='Web server port, default: 8000', type=int, default=8000, dest='port')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    args = parser.parse_args()
    try:
        print("Hello")
        app.run(host='0.0.0.0', port=args.port, debug=True)

    except Exception as e:
        sys.exit(2)

