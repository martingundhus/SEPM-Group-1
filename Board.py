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
        if (stack.Stack.height(tileStack) >= 1):  # Stack Group have written this!
            return True
        else:
            return False
        

    def isValidMove(self, playerIndex, xFrom, xTo, yFrom, yTo):
        if (self.enoughStones(Board.getStack(xFrom, yFrom)) and stack.Stack.check_top_stone(playerIndex)):
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
            

    def isWinningCondition(self):
        # Check rows
        for x in range(self.board_size):
            for y in range(self.board_size - 4):  # Ensure at least 5 stones in a row
                if (self.enoughStones(self.grid[x][y]) and
                    self.enoughStones(self.grid[x][y+1]) and
                    self.enoughStones(self.grid[x][y+2]) and
                    self.enoughStones(self.grid[x][y+3]) and
                    self.enoughStones(self.grid[x][y+4])):
                    
                    top_player = self.grid[x][y].stack_content[-1].player_index
                    if (self.grid[x][y+1].check_top_stone(top_player) and
                        self.grid[x][y+2].check_top_stone(top_player) and
                        self.grid[x][y+3].check_top_stone(top_player) and
                        self.grid[x][y+4].check_top_stone(top_player)):
                        return True

        # Check columns
        for y in range(self.board_size):
            for x in range(self.board_size - 4):  # Ensure at least 5 stones in a column
                if (self.enoughStones(self.grid[x][y]) and
                    self.enoughStones(self.grid[x+1][y]) and
                    self.enoughStones(self.grid[x+2][y]) and
                    self.enoughStones(self.grid[x+3][y]) and
                    self.enoughStones(self.grid[x+4][y])):
                    
                    top_player = self.grid[x][y].stack_content[-1].player_index
                    if (self.grid[x+1][y].check_top_stone(top_player) and
                        self.grid[x+2][y].check_top_stone(top_player) and
                        self.grid[x+3][y].check_top_stone(top_player) and
                        self.grid[x+4][y].check_top_stone(top_player)):
                        return True

        # Check zig-zag patterns (flexible version)
        for x in range(self.board_size - 4):  # Ensure at least 5 rows for zig-zag
            for y in range(self.board_size - 4):  # Adjust as needed for zig-zags
                # Check for zig-zag down then up
                if (self.enoughStones(self.grid[x][y]) and
                    self.enoughStones(self.grid[x+1][y+1]) and
                    self.enoughStones(self.grid[x+2][y]) and
                    self.enoughStones(self.grid[x+3][y+1]) and
                    self.enoughStones(self.grid[x+4][y])):
                    
                    top_player = self.grid[x][y].stack_content[-1].player_index
                    if (self.grid[x+1][y+1].check_top_stone(top_player) and
                        self.grid[x+2][y].check_top_stone(top_player) and
                        self.grid[x+3][y+1].check_top_stone(top_player) and
                        self.grid[x+4][y].check_top_stone(top_player)):
                        return True

                # Check for zig-zag up then down
                if (self.enoughStones(self.grid[x][y+4]) and
                    self.enoughStones(self.grid[x+1][y+3]) and
                    self.enoughStones(self.grid[x+2][y+4]) and
                    self.enoughStones(self.grid[x+3][y+3]) and
                    self.enoughStones(self.grid[x+4][y+4])):
                    
                    top_player = self.grid[x][y+4].stack_content[-1].player_index
                    if (self.grid[x+1][y+3].check_top_stone(top_player) and
                        self.grid[x+2][y+4].check_top_stone(top_player) and
                        self.grid[x+3][y+3].check_top_stone(top_player) and
                        self.grid[x+4][y+4].check_top_stone(top_player)):
                        return True

        return False
