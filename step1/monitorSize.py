def monitorSize(self):
    if (len(self.arrayOfValues) >= self.maxSize):
        self.resetValues()
        return True
    return False