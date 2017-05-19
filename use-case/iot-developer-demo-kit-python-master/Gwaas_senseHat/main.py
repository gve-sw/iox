#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#     This sample app does mqtt posts for sensor data collected from
#     Raspberry Sensorhat web server.

import time
import json
import signal
import threading
import paho.mqtt.client as mqtt
import socket
import os 
import sys 
import logging
import random
import sensor_data 
import ConfigParser
from   ConfigParser     import SafeConfigParser
from   logging.handlers import RotatingFileHandler

client        = mqtt.Client()
sd            = sensor_data.SensorDataSenseHat()
device_list   = []
DEV_INDEX_MAX = 16

logger        = logging.getLogger("Sensehat_client")
envlist       = ["CAF_APP_PERSISTENT_DIR", "CAF_APP_LOG_DIR", "CAF_APP_CONFIG_FILE", "CAF_APP_CONFIG_DIR",
                "CAF_APP_USERNAME", "CAF_HOME", "CAF_HOME_ABS_PATH", "CAF_APP_PATH", "CAF_MODULES_PATH",
                "CAF_APP_DIR", "CAF_MODULES_DIR", "CAF_APP_ID", "HOST_DEV1"]

def _sleep_handler(signum, frame):
    logger.debug("SIGINT Received. Stopping CAF")
    raise KeyboardInterrupt

def _stop_handler(signum, frame):
    logger.debug("SIGTERM Received. Stopping CAF")
    raise KeyboardInterrupt

# The MQTT callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.debug("Connected - " + str(rc))
    else:
        logger.debug("Connection Error! - " + str(rc))
    

# The MQTT callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info("%s> %s" %(msg.topic, msg.payload))

       
# logger.debug out the environment dictionary 
def dump_caf_env():
    logger.info("Printing CAF ENV VARIABLES")
    for l in envlist:
        logger.info("%s: %s" % (l, os.getenv(l)))

def setup_logging(cfg):
    """
        Setup logging for the current module and dependent libraries based on
        values available in config.
    """
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    # Set log level based on what is defined in package_config.ini file
    loglevel = cfg.getint("logging", "log_level")
    logger.setLevel(loglevel)

        # Create a console handler only if console logging is enabled
    ce = cfg.getboolean("logging", "console")
    if ce:
        console = logging.StreamHandler()
        console.setLevel(loglevel)
        console.setFormatter(formatter)
        # add the handler to the root logger
        logger.addHandler(console)

        # The default is to use a Rotating File Handler
        log_file_dir = os.getenv("CAF_APP_LOG_DIR", "/tmp")
        log_file_path = os.path.join(log_file_dir, "Sensehat_client.log")

        # Lets cap the file at 1MB and keep 3 backups
        rfh = RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=3)
        rfh.setLevel(loglevel)
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)

def setup_sensehat(devId, ip=None, port=5000):
    # if ip is not specified, use scan instead
    sd.set_device_info(devId, ip, port)
    
def prep_message(gwdev, keep_alive=False):
    messages ={"messages": []}   
    #'_s'    #status
    #'_t'    #temperature
    #'_h'    #humidity.
    #'_p'    #pressure.
    #'_v'    #accelerometer
    #'_m'    #magnetometer
    #'_g'    #gyroscope
    if keep_alive:
        message =  {"format":"json", "data": sd.sensehat_data(gwdev+'_s')}
    else:
        message =  { "format":"json", "data": { 
                     "temperature":sd.sensehat_data(gwdev+'_t'),
                     "humidity":sd.sensehat_data(gwdev+'_h'), 
                     "gyroscope": sd.sensehat_data(gwdev+'_g')
                   }}
    message["ts"] = int(time.time() *1000)
    messages["messages"].append(message)
    return json.dumps(messages).encode('utf8')


def main():
    # Get hold of the configuration file (package_config.ini)
    moduledir   = os.path.abspath(os.path.dirname(__file__))
    BASEDIR     = os.getenv("CAF_APP_PATH", moduledir)
    # If we are not running with CAF, use the BASEDIR to get cfg file
    tcfg        = os.path.join(BASEDIR, "package_config.ini")
    CONFIG_FILE = os.getenv("CAF_APP_CONFIG_FILE", tcfg)
    
    mqtt_section = "_cisco_mqtt_attributes"
    
    if CONFIG_FILE:
        cfg = SafeConfigParser()
        cfg.read(CONFIG_FILE)
        setup_logging(cfg)
        # Log env variables
        dump_caf_env()
    
        try:
            mqtt_broker   = cfg.get(mqtt_section, "mqtt.broker")
            mqtt_server   = mqtt_broker.split(':', 2)[0] 
            mqtt_port     = int(mqtt_broker.split(':', 2)[1])
            mqtt_name     = cfg.get(mqtt_section, "gw.id")
            mqtt_password = cfg.get(mqtt_section, "gw.password")
            interval      = int(cfg.get(mqtt_section, "publish.interval"))
            window_size   = int(cfg.get(mqtt_section, "sliding.window"))
            
            logger.info("Server config      :   %s:%d" %(mqtt_server,mqtt_port))
            logger.info("Mqtt Gateway ID    :   %s" %mqtt_name)
            logger.info("Interval           :   %d" %interval)
            logger.info("Sliding Window Size:   %d" %window_size)
        except ConfigParser.NoOptionError:
            logger.error("Config missing!")
            sys.exit(1)
        except IndexError:
            logger.error("Mqtt port missing!")
            sys.exit(1)
        except Exception as e:
            logger.error("Config parsing error!")
            sys.exit(1)
       
    # Loop to find all the devices specified
    for index in range(1, DEV_INDEX_MAX):
        try:
             device = {}
             device['index'] = index
             device['name']  = cfg.get(mqtt_section, "device%d.id" %index)
             device['ip']    = cfg.get(mqtt_section, "device%d.ip" %index)
             device['port']  = int(cfg.get(mqtt_section, "device%d.port" %index))
             logger.info("Device%d ID          :   %s" %(index, device['name']))
             logger.info("Device%d IP          :   %s" %(index, device['ip']))
             logger.info("Device%d port        :   %d" %(index, device['port']))
             if device['name']:
                 device_list.append(device)
        except ConfigParser.NoOptionError:
             logger.info("End looking for device!")
             break
        except Exception as e:
             logger.error("Device Config parsing error!")
             sys.exit(1) 

    # Signal handling
    signal.signal(signal.SIGTERM, _stop_handler)
    signal.signal(signal.SIGINT, _sleep_handler)
    
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(mqtt_name, mqtt_password)
        try: 
            if mqtt_port == 8883:
		allow_invalid_cert = True    
                dc_cert = os.path.join(os.getenv('CAF_APP_PATH', ''),
                                   "STAR_iotspdev_io.crt")
                logger.info("Mqtt Cert          :   %s" %dc_cert)
                logger.info("Allow Invalid Cert :   %r" %allow_invalid_cert)
                try:
                    client.tls_set(dc_cert)
                except IOError as e:
                    logger.error('Unable to load DC certificate "%s"',
                                  dc_cert)
                    raise
                client.tls_insecure_set(allow_invalid_cert)
            client.connect(mqtt_server, mqtt_port, 60)
        except socket.error:
            logger.debug("MqttReconnect 1")
        except ValueError:
            logger.debug("Mqtt Host Connection Error!")
            sys.exit(1)
        
        client.loop_start()
        
        keep_alive_interval = 0

        while True:
            for device in device_list:
                gwdev = ('%s:%s' %(mqtt_name, device['name']))
                topic = '/v1/' + gwdev + '/json/dev2app'
                logger.info("Mqtt Topic         :   %s" %topic)
                setup_sensehat(gwdev, device['ip'], device['port'])
                # When the counting is less than 0, it's time to send keep alive message
                if keep_alive_interval <= 0:
                    payload = prep_message(gwdev, keep_alive = True)
                else:
                    payload = prep_message(gwdev)
                logger.info(payload)
                
                try:
                    client.publish(topic, payload)
                except socket.error:
                    logger.debug("MqttReconnect 2")
            time.sleep(interval)
            keep_alive_interval = keep_alive_interval - interval
            if keep_alive_interval <= 0:
                keep_alive_interval = 60
    
    except KeyboardInterrupt:
        #p.stop()
        sys.exit(0)
    except Exception as e:
        logger.error("System error!")
        sys.exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
