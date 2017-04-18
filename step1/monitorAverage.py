def monitorAverage():
    average = self.averageValues()
    if (average >= self.high) or (average <= low):
        return True
    return False