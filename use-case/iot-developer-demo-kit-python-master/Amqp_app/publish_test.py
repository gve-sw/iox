#!/usr/bin/python
# COPYRIGHT
#     Copyright (c) 2016 by Cisco Systems, Inc.
#     All rights reserved.
# 
# DESCRIPTION
#    This is a AMQP client side message consumer programme.

import pika
import time
import sys
import argparse
import datetime
import logging

def callback(ch, method, properties, body):
    print(" [x] rk: {}, headers: {}, msg: {}, ts: {}".
          format(method.routing_key, properties.headers, body,
                 datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))

def main():
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="AMQP client")
    parser.add_argument("-v", "--vhost", help='AMQP virtual host name, default: IOTSP_INTERNAL', default='IOTSP_INTERNAL', dest='vhost')
    parser.add_argument("-u", "--user", help='AMQP user name, default: test', default='test', dest='user')
    parser.add_argument("-P", "--password", help='AMQP user password, default: test', default='test', dest='password')
    parser.add_argument("-e", "--exchange", help='AMQP exchange name, default: unknown', default='unknown', dest='exchange')
    parser.add_argument("-l", "--label", help='AMQP label,  must be in format a=b, default: None', default=None, dest='label')
    parser.add_argument("-r", "--rmqphost", help='AMQP host ip, default: 127.0.0.1', default='127.0.0.1', dest='rmqp_host')
    parser.add_argument("-k", "--routingkey", help='AMQP routing key, default: dev2app', default='dev2app', dest='routing_key')
    args = parser.parse_args()
    
    queue_name = args.user + ':' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    credentials = pika.PlainCredentials(args.user, args.password)
    parameters = pika.ConnectionParameters(
    host=args.rmqp_host, virtual_host=args.vhost, credentials = credentials)    # port = 5672,
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except Exception as e:
        logging.error(args.rmqp_host + " Connection error!")
        logging.error(type(e))
        sys.exit()

    i = 0
    while True:
        i = i + 1
        message = "Hello world! %d" %i
        channel.basic_publish(exchange=args.exchange, routing_key=args.routing_key, body=message)
        logging.info('published: ' + message)
        time.sleep(2)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   main()
