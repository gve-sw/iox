import urllib2
import json

def sendSparkPOST(self, url, data):
    request = urllib2.Request(url, json.dumps(data),
        headers={"Accept" : "application/json",
                 "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+ bearer)
    contents = urllib2.urlopen(request).read()
    return contents