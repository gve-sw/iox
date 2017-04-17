#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#     Sensorhat web server URLs' stub implementations in flask.
import time
import sys
import argparse
from flask import Flask,jsonify

app = Flask(__name__)
deviceId = '0x123456' 

@app.route('/status')
def status():
    return jsonify({'deviceId':deviceId})

@app.route('/sensehat/<type>')
def get_data(type):
    t = {}
    try:
         t[type] = {
         'temperature':75,       
         'humidity':35,       
         'barometricpressure':25,       
         'magnetometer': 10,       
         'accelerometer': 30,       
         'gyroscope':{'y':10,'m':20,'k':30}       
          }.get(type, 'None')
    
    except Exception as e:
        # handle sensor data error
        t[type] = '-1'
    return jsonify({'ts': int(time.time() *1000), type:t})

@app.route('/message/<messages>')
def show_messages(messages):
    if len(messages) > 8: 
        return jsonify({'Status':'Error!'})
    else:
        return jsonify({'Status':'Done!' + messages})

@app.route('/')
def index():
    return "This is sensehat test stub!" 

def ws_run(flask_port=5000):
    app.run(host='0.0.0.0', port=flask_port, debug=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Raspberry Pi Sensehat web server stub functions")
    parser.add_argument("-p", "--port", help='Web server port, default: 5000', type=int, default=5000, dest='port')
    parser.add_argument("-i", "--id", help='Device id, default: %s' %deviceId, default=deviceId, dest='id')
    args = parser.parse_args()
    flask_port = args.port 
    deviceId = args.id
    try:
       ws_run(flask_port) 
    except Exception as e:
        print 'Flask Launch Error! Check port number'
        sys.exit(2)
