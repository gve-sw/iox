import urllib2
import json

class IOTWrapper():

    def IOTWrapper(self, maxSize, highValue, lowValue, roomId, bearer):
        self.maxSize = maxSize
        self.highValue = highValue
        self.lowValue = lowValue
        self.roomId = roomId
        self.bearer = bearer
        self.arrayOfValues = []

    def addValue(self, value):
        self.arrayOfValues.append(value)
        return len(self.arrayOfValues)

    def averageValues(self):
        return (sum(self.arrayOfValues)/len(self.arrayOfValues))

    def monitorAverage(self):
        average = self.averageValues()
        if (average >= self.highValue) or (average <= self.lowValue):
            return True
        return False

    def resetValues(self):
        self.arrayOfValues = []

    def sendSparkMessage(self, message):
        self.sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": self.roomId, "text": message})

    def sendSparkPOST(self, url, data):
        request = urllib2.Request(url, json.dumps(data),
            headers={"Accept" : "application/json",
                     "Content-Type":"application/json"})
        request.add_header("Authorization", "Bearer "+ self.bearer)
        contents = urllib2.urlopen(request).read()
        return contents

    def setHighValue(self, highValue):
        self.highValue = highValue

    def setLowValue(self, lowValue):
        self.lowValue = lowValue

    def setMaxSize(self, maxSize):
        self.maxSize = maxSize

    def test_messages(self):
        self.sendSparkMessage("Test Message")