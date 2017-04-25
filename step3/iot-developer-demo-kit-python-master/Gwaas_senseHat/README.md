# IoT Developer Demo Kit: IoT Data Connect Sense Hat

`Gwaas_senseHat`
This IOX app gets sensehat data from Raspberry pi and posts them to the Mqtt server in the cloud.

* Iox Package Howto
  To packaging the app into a iox package, use 
```
      ./build_iox_package.sh
```
  The package.tar.gz is the target file under `gwaas_sensehat_pkg`.
  There is a package.tar.gz under `package` ready for use.
  The version information is consistent with the version information in the `package.yaml`.

* App configurations
  When the app is launched, it reads in the data in the configuration file as the input parameters.
  The configuration file is `package_config.ini`. 
  The following are the descriptions of the data fields
  
```
  # All the configs should be automatically set by the Fog Director Portal for Gwaas
  [_cisco_mqtt_attributes]
  mqtt.broker                       - mqtt broker ip and port, eg "127.0.0.1:1883" 
  gw.id                             - gateway id 
  gw.password                       - gateway password 
  device1.id                        - device 1 id
  publish.interval                  - mqtt publishing interval in seconds
  device1.ip                        - Raspberry pi web server ip address. If left as empty, a ip scanning would
                                      happen to find the Raspberry Pi in the specific Gwaas subnet.
                                      <The subnet is specified in the Gwaas network configurations. By default, 
                                       the system scans the next subnet of the IOX app.> 
  device1.port                      - Raspberry pi web server port 
  device2.id                        - device 2 id, multiple devices are supported with the device index
                                      increased sequentially. The programme will stop searching until
                                      the DEV_INDEX_MAX (16) is reached or the device with the searched 
                                      index is missing.
  device2.ip                        - Raspberry pi 2 web server ip address, 
                                      If left as empty, a ip scanning would
                                      happen to find the Raspberry Pi in the specific Gwaas subnet. 
  device2.port                      - Raspberry pi 2 web server port 
  
  [logging]
  # DEBUG:10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50, NOTSET: 0
  log_level: 10
  # Enable/disable logging to stdout
  console: yes 

```
