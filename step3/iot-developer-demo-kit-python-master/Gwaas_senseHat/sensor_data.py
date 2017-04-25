#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#     This program collects data from Raspberry Sensorhat web server.
import requests 
import logging 
import socket
from collections import deque
import netifaces
from netaddr import *
import json

logger  = logging.getLogger("Sensehat_client")
class Simplemovingaverage():
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer > 0"
        self.period = period
        self.stream = deque()
 
    def __call__(self, n):
        stream = self.stream
        stream.append(n)    # appends on the right
        streamlength = len(stream)
        if streamlength > self.period:
            stream.popleft()
            streamlength -= 1
        if streamlength == 0:
            average = 0
        else:
            average = sum( stream ) / streamlength
 
        return average


class SensorDataSenseHat():

    sensor_sensehats = {}
    
    def __init__(self, period = 5, port=5000):
        self.period = period 
        # 5000 is the default port of flask
        self.default_port = port 
    
    def set_sliding_window(self, period):
        self.period = period 
    
    def set_device_info(self, devId, ip, port=5000):
        if  not devId:
            return
        if  devId not in self.sensor_sensehats:
            self.init_sensehat_sensor(devId) 
        self.sensor_sensehats[devId]['port'] = port 
        if ip:
	    self.sensor_sensehats[devId]['addr'] = ip + ':%d' %self.sensor_sensehats[devId]['port'] 
    
    # This function is specific to the Gwaas networking setup, assuming 
    # that Pi is connected to a port in the next available subnet of a IOX app.
    def get_next_subnet(self):
        try:
            ipv4s = netifaces.ifaddresses('eth0').get(netifaces.AF_INET, [])
            logger.debug(ipv4s) 
            ip = ipv4s[0]['addr']
            mask = ipv4s[0]['netmask']
            net = IPNetwork(ip + '/' + mask)
            net_size = 1 << (32 - net.prefixlen + 1)
            next_subnet = str(IPAddress(int(net_size) + int(IPAddress(net.network))))
            logger.debug('next_subnet %s,  size 0x%x' %(next_subnet, net_size))
            return (next_subnet, net_size)
        except Exception as e:
            logger.error('Could not get ip address & size!')
            return (None, None)

    # Check the status of a Raspberry PI. 
    # A working one should be accessible over the URL '/status'
    def get_sensehat_status(self, ip):
        logger.debug("testing %s" %ip)
        url = 'http://' + ip + '/status'
        h = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            r = requests.get(url, headers = h, timeout = 1)
        except Exception as e:
            return None 
        if (r.status_code == requests.codes.ok):
            rs = r.json()
            logger.debug(rs)
            try:
                #if rs['deviceId'].encode('utf-8') == devId.split(':')[1][:-2]:
                #    # show the connection info
                #    url = 'http://' + ip + '/message/Gwaas'
                #    requests.get(url, headers = h)
                logger.debug(ip) 
                return ip
            except KeyError:
                return None
        return None

    # Scannning the subnet where the Raspberry PI belongs to. 
    # Return the first IP that responds. 
    def find_sensehat(self, devId):
        next_subnet, net_size = self.get_next_subnet()
        if next_subnet:
            start_ip = int(IPAddress(next_subnet))
        else:
	    logger.error("Network is not ready!")
            return None
	logger.info("Starting scanning netowrk ...")
	for i in range(1, net_size):
            ip = str(IPAddress((start_ip + i))) + ':' + '%s' %self.sensor_sensehats[devId]['port'] 
            logger.debug("testing %s" %ip)
            res = self.get_sensehat_status(ip)
            if res:
	        logger.info("End scanning netowrk!")
                return res
	logger.error(devId + " not found!")
        return None
       

    def discover_device(self, devId):
	# discover_device will only be performed when the server address is founded.
        if not self.sensor_sensehats[devId]['addr']:
            self.sensor_sensehats[devId]['addr'] = self.find_sensehat(devId)

    def init_sensehat_sensor(self, devId):
        self.sensor_sensehats[devId] = {} 
        self.sensor_sensehats[devId]['value'] = 0
        self.sensor_sensehats[devId]['addr'] = None 
        self.sensor_sensehats[devId]['port'] = self.default_port 
        self.sensor_sensehats[devId]['min'] = 0
        self.sensor_sensehats[devId]['max'] = 0
        self.sensor_sensehats[devId]['sma'] = Simplemovingaverage(self.period)
    
    def get_sensehat_sensor(self, devItem):
        try:
            devId = devItem[:-2]
            if  not devId:
                logger.error('Device ID could not be null!')
                return None
        except Exception as e:
            return None

        if  devId not in self.sensor_sensehats:
            self.init_sensehat_sensor(devId) 
	self.discover_device(devId)

        index = devItem[-2:]
	# keep alive messages handling
	if index == '_s':
	    status = {}
	    if self.sensor_sensehats[devId]['addr']:
                # Check the device status to make sure it is still alive
	        # Return the discovered devices ip, or None
                res = self.get_sensehat_status(self.sensor_sensehats[devId]['addr'])
                if res:
                    status['device'] = self.sensor_sensehats[devId]['addr'] 
                else:
                    # If the device is not alive, it is removed from the 
                    # known server address
                    status['device'] = 'None'
                    self.sensor_sensehats[devId]['addr'] = None
	    else:
		status['device'] = 'None'
	    return status
        
        # for queries other than keep alive, return None if no device found
        if not self.sensor_sensehats[devId]['addr']:
	    return None	

        sub_url =  {
            '_t': 'temperature',
            '_h': 'humidity',
            '_g': 'gyroscope',
            '_m': 'magnetometer',
            '_v': 'accelerometer',
            '_p': 'barometricpressure'
        }
        try:	
	    url = 'http://' + self.sensor_sensehats[devId]['addr'] + '/sensehat/' + sub_url[index]
        except KeyError:
            logger.error("Message type not supported!")
            return None
        params = {}
        h = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            r = requests.get(url, headers = h, params = params)
        except requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout:
            logger.error('Connection Error or timeout!')
            return None
        except Exception as e:
            logger.error('Failed to get data from Raspberry PI!')
            return None
        if (r.status_code == requests.codes.ok):
            rs = r.json()
            #self.sensor_sensehats[devId]['value'] = self.sensor_sensehats[devId]['sma'](int(rs['value']))
            self.sensor_sensehats[devId]['value'] = rs
        else: 
            logger.error(url + ' failed!')
        return self.sensor_sensehats[devId]['value']
    
    def sensehat_data(self, devItem):
	res = self.get_sensehat_sensor(devItem)
	if res: 
	    return res
	else:
	    return -1 
