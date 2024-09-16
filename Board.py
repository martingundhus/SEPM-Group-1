class Board:
    def __init__(self, board_size, grid):
        self.board_size = 5
        self.grid = grid

    def createBoard(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.grid[x][y] = CreateStack() #Stack group write this!

    def placeStone(self, x, y):
        self.grid[x][y] = addStone() #Stack group write this!

    def moveStone(self, xFrom, yFrom, xTo, yTo):
        if (xFrom > xTo):
            checkLeft()
        else:
            checkRight()
        if (yFrom > yTo):
            checkDown()
        else:
            checkUp()

        self.grid[xFrom][yFrom] = removeStone() #Stack group write this!
        self.grid[xTo][yTo] = addStone()