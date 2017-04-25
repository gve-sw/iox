#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#     Raspberry Sensorhat web server URLs' implementations in flask.
from flask import Flask, jsonify
from uuid import getnode as get_mac
import sensor 
import time
import sys
import argparse
import urllib2
import json

app = Flask(__name__, static_url_path='', static_folder="static")
roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vMjIyYTE3MjAtMjMwMi0xMWU3LWE1ZDMtYmQ4ODU5YjY3ODc4"
bearer = "YzY2ZTMzNWEtOWVkYy00NDlhLThkZmYtZTNiZDQ3NTkyYTdjMDFkNjkzNTEtY2Y3"

@app.route('/status')
def status():
    deviceId = hex(get_mac())
    return jsonify({'deviceId':deviceId})

@app.route('/sensehat/<type>')
def get_data(type):
    try:
        t = sensor.get_data(type)
    except Exception as e:
        # handle sensor data error
        t = {}
        t[type] = '-1'
    return jsonify({'ts': int(time.time() *1000), type:t})

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

def sendSparkMessage(roomId, message):
    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": roomId, "text": message})

@app.route('/test')
def test_messages():
    sendSparkMessage("my temporary room ID", "Hello")


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
    parser.add_argument('-p', '--port', help='Web server port, default: 5000', type=int, default=5000, dest='port')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    args = parser.parse_args()
    try:
        app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as e:
        print 'Flask Launch Error! Check port number'
        sys.exit(2)
