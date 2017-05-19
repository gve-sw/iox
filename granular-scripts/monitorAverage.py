def monitorAverage(self):
    average = self.averageValues()
    if (average >= self.highValue) or (average <= self.lowValue):
        return True
    return False