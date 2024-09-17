import Game

class Board:
    def __init__(self, board_size, grid):
        self.board_size = 5
        self.grid = grid

    def createBoard(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.grid[x][y] = CreateStack() #Stack group write this!

    def getTile(self, x, y):
        return self.grid[x][y]

    def placeStone(self, x, y):
        self.grid[x][y] = addStone() #Stack group write this!

    def moveStack(self, xFrom, yFrom, xTo, yTo):
        self.grid[xFrom][yFrom] = removeStone() #Stack group write this!
        self.grid[xTo][yTo] = addStone()



    