import requests
import json

class IOTWrapper():

    def __init__(self, maxSize, highValue, lowValue, roomId, bearer):
        self.maxSize = maxSize
        self.highValue = highValue
        self.lowValue = lowValue
        self.roomId = roomId
        self.bearer = bearer
        self.arrayOfValues = []


## Monitor methods

    def addValue(self, value):
        self.arrayOfValues.append(value)
        return len(self.arrayOfValues)

    def averageValues(self):
        return (sum(self.arrayOfValues)/len(self.arrayOfValues))

    def monitorAverage(self):
        average = self.averageValues()
        self.resetValues()
        if (average >= self.highValue) or (average <= self.lowValue):
            return True
        return False

    def getHigh(self):
        return self.highValue

    def getLow(self):
        return self.lowValue

    def getMaxSize(self):
        return self.maxSize

    def monitorSize(self):
        if (len(self.arrayOfValues) >= self.maxSize):
            return True
        return False

    def resetValues(self):
        self.arrayOfValues = []


## Setter Methods

    def setHighValue(self, highValue):
        self.highValue = highValue

    def setLowValue(self, lowValue):
        self.lowValue = lowValue

    def setMaxSize(self, maxSize):
        self.maxSize = maxSize


## Spark Methods

    def sendSparkMessage(self, message):
        self.sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": self.roomId, "text": message})

    def sendSparkPOST(self, message, data):
        url = "https://api.ciscospark.com/v1/messages"
        header = {'Content-type': 'application/json; charset=utf-8',
                  'Authorization': 'Bearer ' + self.bearer}
        requests.post(url, headers=header, data=json.dumps(data))

    def test_messages(self):
        self.sendSparkMessage("Test Message")
