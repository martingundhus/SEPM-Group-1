from copy import deepcopy

class Ai_Player:
    def __init__(self, id, stonesLeft, stack):
        self.id = id
        self.stonesLeft = stonesLeft
        self.picked_up_stack = stack


    def pickUpStack(self,stack):
        self.picked_up_stack = stack

    def getId(self):
        return self.id
    
    def getStonesLeft(self):
        return self.stonesLeft
    
    def useStone(self):
        if (self.stonesLeft > 0):
            self.stonesLeft -= 1
        else:
            raise TypeError("No stones left")
    
    def getRemaining(self):
        return self.stonesLeft