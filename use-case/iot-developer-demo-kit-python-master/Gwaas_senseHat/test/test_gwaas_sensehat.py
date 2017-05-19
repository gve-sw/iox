#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#     Python based Gwaas senseHat test 
import sys 
from types import *
import unittest  
import logging
sys.path.append("..")
import sensor_data 

logging.basicConfig(level=logging.DEBUG)
  
class mytest(unittest.TestCase):  
    def setUp(self):  
        logging.info(' Test Set Up \n')

    def tearDown(self):  
        logging.info(' Test Cleaned Up \n')
    
    def test_001_sd(self):
        gwdev = '0x123456'
        sd = sensor_data.SensorDataSenseHat()
        sd.set_device_info(gwdev, '127.0.0.1')
        logging.info(' Test None existing URL \n')
        data = sd.sensehat_data(gwdev+'_x')
        self.assertEqual(data, -1)
        logging.info(' Test None existing URL PASS\n')
        logging.info(' Test System status URL\n')
        data = sd.sensehat_data(gwdev+'_s')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test System status URL PASS\n')
        logging.info(' Test temperature URL \n')
        data = sd.sensehat_data(gwdev+'_t')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test temperature URL PASS\n')
        data = sd.sensehat_data(gwdev+'_g')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test gyroscope URL PASS\n')
    
    def test_002_sd(self):
        gwdev = '0x234567'
        sd = sensor_data.SensorDataSenseHat()
        sd.set_device_info(gwdev, '127.0.0.2', 5100)
        logging.info(' Test None existing URL \n')
        data = sd.sensehat_data(gwdev+'_x')
        self.assertEqual(data, -1)
        logging.info(' Test None existing URL PASS\n')
        logging.info(' Test System status URL\n')
        data = sd.sensehat_data(gwdev+'_s')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test System status URL PASS\n')
        logging.info(' Test temperature URL \n')
        data = sd.sensehat_data(gwdev+'_t')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test temperature URL PASS\n')
        data = sd.sensehat_data(gwdev+'_g')
        logging.debug(data)
        self.assertIs(type(data), DictType)
        logging.info(' Test gyroscope URL PASS\n')
          
          
if __name__ =='__main__':  
    logging.info('#### Test Started ####\n')
    unittest.main()  
