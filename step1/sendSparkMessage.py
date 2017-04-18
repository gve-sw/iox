def sendSparkMessage(self, roomId, message):
    sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": roomId, "text": message})