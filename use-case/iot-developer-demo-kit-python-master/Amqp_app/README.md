# IoT Developer Demo Kit: AMQP App

`Amqp_app`
The app accessing the AMQP bus and handling the data from AMQP.

Run `python main.py -h` to get the following help on the parameter settings.


```
AMQP client

optional arguments:
  -h, --help            show this help message and exit 
  -v VHOST, --vhost VHOST  
                        AMQP virtual host name, default: IOTSP_INTERNAL
  -u USER, --user USER  AMQP user name, default: test
  -P PASSWORD, --password PASSWORD
                        AMQP user password, default: test
  -e EXCHANGE, --exchange EXCHANGE
                        AMQP exchange name, default: unknown
  -l LABEL, --label LABEL
                        AMQP label, must be in format a=b, default: None
  -r RMQP_HOST, --rmqphost RMQP_HOST
                        AMQP host ip, default: 127.0.0.1
  -k ROUTING_KEY, --routingkey ROUTING_KEY
                        AMQP routing key, default: dev2app 
```

