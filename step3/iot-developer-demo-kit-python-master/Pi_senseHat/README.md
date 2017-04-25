# IoT Developer Demo Kit: Sense Hat Data Web App

Log Sense Hat sensor data and show it in a web app

## Requirements

### Hardware

- Raspberry Pi 
- Sense HAT

### Software

- Flask
- Sense HAT Python library

```bash
    - git clone https://github.com/CiscoDevNet/iot-developer-demo-kit-python.git
    - cd `Pi_SenseHat/www`
    - sudo pip install -r requirements.txt 
```

Make sure the Raspberry Pi has the correct system time before any pip installation is performed.
Wrong system time could cause remote repo certificate authentication problems and connection error.

## Usage

### Simple: LAN

The simple version can be run on a LAN, so you can view the Flask web app on any device on your local network.

1. Find the Pi's local IP address (and keep a note of it):
    - `hostname -I`
1. Run the web app):
    -  cd `Pi_SenseHat/www`
    - `python app.py` or `python app.py -p <port>`
   The port number is by default 5000 if not specified.
1. Navigate to the IP address in a web browser on any device on your network (e.g. `http://192.168.1.3:5000`)
    - You should be able to see the freeboard UI in the browser
1. Available URLs are as the following
    -  `/status`
    -  `/sensehat/<type>`
    - type could be  
     `temperature /               
     humidity /                  
     barometricpressure /      
     magnetometer /         
     accelerometer /       
     gyroscope`         
    -  `/message/<messages>`
      Show messages on the SenseHat screen.
      8 characters at most are allowed one time. Since this operation is not asyncronized, delays up to 10 seconds are expected for the response.
