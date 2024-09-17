import Game

class Board:
    def __init__(self, board_size, grid):
        self.board_size = 5
        self.grid = grid

    def createBoard(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.grid[x][y] = CreateStack() #Stack group write this!

    def getStack(self, x, y):
        return self.grid[x][y]

    def placeStone(self, x, y):
        self.grid[x][y] = addStone() #Stack group write this!

    def checkLeft(self, x, y):
        if x == 0:
            return False
        else: 
            if (self.grid[x-1][y] != isTopStoneStanding):
                return True
            else:
                return False
            
    def checkRight(self, x, y):
        if x == 4:
            return False
        else:
            if (self.grid[x+1][y] != isTopStoneStanding):
                return True
            else:
                return False

    def checkDown(self, x, y):
        if y == 0:
            return False
        else:
            if (self.grid[x][y-1] != isTopStoneStanding):
                return True
            else:
                return False

    def checkUp(self, x, y):
        if y == 4:
            return False
        else:
            if (self.grid[x][y+1] != isTopStoneStanding):
                return True
            else:
                return False


    def enoughStones(self, stack):
        if (height(stack) >= 2):  # Stack Group have written this!
            return True
        

    def isValidMove(self, playerIndex, xFrom, xTo, yFrom, yTo):
        if (Board.enoughStones(self, Board.getStack(xFrom, yFrom)) and check_top_stone(playerIndex)):
            if (xFrom > xTo):
                if (Board.checkLeft(self, xFrom, yFrom)):
                     return True
            else:
                if (Board.checkRight(self, xFrom, yFrom)):
                     return True
            if (yFrom > yTo):
                if (Board.checkDown(self, xFrom, yFrom)):
                     return True
            else:
                if (Board.checkUp(self, xFrom, yFrom)):
                     return True

    def moveStack(self, xFrom, yFrom, xTo, yTo):
        if (Board.isValidMove(self, xFrom, yFrom, xTo, yTo)):
            moveAndLeaveBottomStone() #HOW???