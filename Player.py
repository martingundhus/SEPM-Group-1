class Player:
    def __init__(self, color, stonesLeft):
        self.color = color
        self.stonesLeft = stonesLeft

    def getColor(self):
        return self.color
    
    def getStonesLeft(self):
        return self.stonesLeft
    
    def useStone(self):
        if (self.stonesLeft > 0):
            self.stonesLeft -= 1
        else:
            raise TypeError("No stones left")
    
    def getRemaining(self):
        return self.stonesLeft