import stone
import stack
import Player
import pygame
from image import Image

import numpy as np



class tile():
    def __init__(self,grid_path,position=(0,0)) -> None:
        self.img_grid=Image(grid_path,position)
        self.position=position
        self.stack=stack.Stack()
    
    ## for prototype
    def add_stone(self,player_index, upright_input):
        self.stack.push_stone(player_index, upright_input)
    
    def draw(self,screen):
        self.img_grid.draw(screen)

        #might not work! TODO
    
        self.stack.draw(screen,self.position)
        

class Board():
    offset_x=31
    offset_y=31
    grid_size=100

       
    def __init__(self, board_size, position=(0,0)) -> None:
        self.board_size = board_size
        self.picked_up_stack = stack.Stack()
        self.turn = 0
        self.current_x = -1
        self.current_y = -1
        #new
        self.img_board=Image("assets/picture/board.png",position)
        self.position=position
        self.init_grid()

 
    def init_grid(self):
            orig_x,orig_y=self.position
            self.tiles=np.empty((5,5),dtype=tile)
            for y in range(5):
                for x in range(5):
                    index=int((x+y)%2)
                    if index==0:
                        self.tiles[y,x]=tile("assets/picture/white_grid.png",(orig_x+Board.offset_x+x*Board.grid_size,
                                                                                orig_y+Board.offset_y+y*Board.grid_size))
                    elif index==1:
                        self.tiles[y,x]=tile("assets/picture/brown_grid.png",(orig_x+Board.offset_x+x*Board.grid_size,
                                                                                orig_y+Board.offset_y+y*Board.grid_size))
    
    def draw_board(self,screen):
        self.img_board.draw(screen)
        for y in range(5):
            for x in range(5):
                self.tiles[y,x].draw(screen)

    def draw(self,screen):
        self.draw_board(screen)
        

    def changeTurn(self):
        self.picked_up_stack = stack.Stack()
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def getStack(self, x, y):
        return self.tiles[x][y].stack

    def placeStone(self, x, y, upright_input,round):
        player_index = self.turn
        if round < 2:
            player_index = (self.turn+1)%2
        if self.getStack(x,y).is_stackable():
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

    def placeStone(self, x, y, upright_input, round):
        player_index = self.turn
        if round < 2:
            player_index = (self.turn + 1) % 2
        if self.getStack(x, y).is_stackable():
            self.getStack(x, y).push_stone(player_index, upright_input)
            if self.check_winning_condition():  # Check for a win after placing a stone
                print(f"Player {player_index + 1} wins!")  # Example win announcement
            self.changeTurn()
        else:
            raise TypeError("Not valid move")

    def check_winning_condition(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.getStack(x, y).height() > 0:  # Only check stacks with stones
                    if (self.check_line_winner(x, y, 1, 0) or  # Check horizontally
                        self.check_line_winner(x, y, 0, 1) or  # Check vertically
                        self.check_line_winner(x, y, 1, 1) or  # Check diagonally \
                        self.check_line_winner(x, y, 1, -1)):  # Check diagonally /
                        return True
        return False

    def check_line_winner(self, start_x, start_y, delta_x, delta_y):
        player_index = self.getStack(start_x, start_y).top_player()  # Get the player of the top stone
        if player_index is None:  # No stones in this stack
            return False

        count = 1  # Start counting with the first stone

        # Check in one direction
        for step in range(1, 5):  # Check the next 4 positions
            x = start_x + step * delta_x
            y = start_y + step * delta_y
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                if self.getStack(x, y).top_player() == player_index:
                    count += 1
                else:
                    break

        # Check in the opposite direction
        for step in range(1, 5):
            x = start_x - step * delta_x
            y = start_y - step * delta_y
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                if self.getStack(x, y).top_player() == player_index:
                    count += 1
                else:
                    break

        return count >= 5  # Check if there are 5 in a row
