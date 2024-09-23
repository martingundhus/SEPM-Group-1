import Game
import stone
import stack
import Player

import numpy as np


class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.grid = np.empty([self.board_size, self.board_size],dtype = stack.Stack)
        self.picked_up_stack = stack.Stack()
        self.turn = 0
        self.current_x = -1
        self.current_y = -1
        for r in range(board_size):
            for c in range(board_size):
                self.grid[r][c] = stack.Stack()
                
    # def createBoard(self):
    #     for x in range(self.board_size):
    #         for y in range(self.board_size):
    #             self.grid[x][y] = stack.Stack() #Stack group write this!

    def changeTurn(self):
        self.picked_up_stack = stack.Stack()
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def getStack(self, x, y):
        return self.grid[x][y]

    def placeStone(self, x, y, upright_input, player_index):
        if self.getStack(x,y).stackable:
            self.getStack(x,y).push_stone(player_index, upright_input)  #Stack group write this!
            self.changeTurn()
            #self.Player.Player.useStone()
        else:
            raise TypeError("Not valid move")

    def checkLeft(self, x, y):
        if (x != 0 and self.getStack(x-1,y).stackable):
            return True
        else:
            return False
            
    def checkRight(self, x, y):
        if ( x != 4 and self.getStack(x+1,y).stackable):
            return True
        else:
            return False

    def checkDown(self, x, y):
        if (y != 0 and self.getStack(x, y-1).stackable):
            return True
        else:
            return False

    def checkUp(self, x, y):
        if (y != 4 and self.getStack(x,y+1).stackable):
            return True
        else:
            return False


    # def enoughStones(tileStack):
    #     if (stack.Stack.height(tileStack) >= 2):  # Stack Group have written this!
    #         return True
    #     else:
    #         return False
        

    def isValidMove(self, xFrom, xTo, yFrom, yTo):
        if (self.getStack(yFrom, yTo).stackable):
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

    def pickUpStack(self, x, y):
        if self.getStack(x,y).height() >= 1 and self.getStack(x,y).check_top_stone(self.turn):
            self.picked_up_stack = self.getStack(x,y)
            self.grid[x][y] = stack.Stack()
            self.current_x = x
            self.current_y = y
        else:
            raise TypeError("Cannot pick up this stack")

    def moveStack(self, xFrom, yFrom, xTo, yTo):
        if (self.isValidMove(xFrom, yFrom, xTo, yTo)):
            self.picked_up_stack.drop_stone(self.getStack(xTo, yTo)) #HOW???
            self.current_x = xTo
            self.current_y = yTo
            if self.picked_up_stack.height() == 0:
                self.changeTurn()
        else:
            raise TypeError("Not valid move")
        
    