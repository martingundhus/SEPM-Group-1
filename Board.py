import game
import stone
import stack
import player

class Board:
    def __init__(self, board_size, grid):
        self.board_size = 5
        self.grid = grid

    def createBoard(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.grid[x][y] = stack.Stack() #Stack group write this!

    def getStack(self, x, y):
        return self.grid[x][y]

    def placeStone(self, x, y, upright_input, player_index):
        self.grid[x][y] = stack.Stack.push_stone(player_index, upright_input)  #Stack group write this!

    def checkLeft(self, x, y):
        if (x != 0 and self.grid[x-1][y].stack.Stack.stackable):
            return True
        else:
            return False
            
    def checkRight(self, x, y):
        if ( x != 4 and self.grid[x+1][y].stack.Stack.stackable):
            return True
        else:
            return False

    def checkDown(self, x, y):
        if (y != 0 and self.grid[x][y-1].stack.Stack.stackable):
            return True
        else:
            return False

    def checkUp(self, x, y):
        if (y != 4 and self.grid[x][y+1].stack.Stack.stackable):
            return True
        else:
            return False


    def enoughStones(tileStack):
        if (stack.Stack.height(tileStack) >= 2):  # Stack Group have written this!
            return True
        else:
            return False
        

    def isValidMove(self, playerIndex, xFrom, xTo, yFrom, yTo):
        if (self.enoughStones(Board.getStack(xFrom, yFrom)) and check_top_stone(playerIndex)):
            if (xFrom > xTo):
                if (self.checkLeft(xFrom, yFrom)):
                     return True
            else:
                if (self.checkRight(xFrom, yFrom)):
                     return True
            if (yFrom > yTo):
                if (self.checkDown(xFrom, yFrom)):
                     return True
            else:
                if (self.checkUp(xFrom, yFrom)):
                     return True

    def moveStack(self, xFrom, yFrom, xTo, yTo):
        if (self.isValidMove(xFrom, yFrom, xTo, yTo)):
            moveAndLeaveBottomStone() #HOW???
        else:
            raise TypeError("Not valid move")