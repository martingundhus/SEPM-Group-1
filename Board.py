
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
    
    def add_stone(self,player_index, upright_input):
        self.stack.push_stone(player_index, upright_input)
    
    def draw(self,screen):
        self.img_grid.draw(screen)
        self.stack.draw(screen,self.position)

    def empty(self):
        self.stack=stack.Stack()
    
        

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
        self.player1 = Player.Player(0,21)
        self.player2 = Player.Player(1,21)
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

        center_x = self.grid_size * (self.board_size + 3.5)
        Background = (197, 209, 235)
        Text_color = (45, 45, 42)
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 40)
        text = font.render('Player ' + str(self.turn+1) +"s turn", True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x // 2, self.grid_size // 2)
        screen.blit(text, textRect)

    def draw(self,screen):
        self.draw_board(screen)
        self.player1.draw_player_stats(screen,self)
        self.player2.draw_player_stats(screen,self)



    def hasSelected(self):
        return (self.picked_up_stack.height() > 0)
    

    def changeTurn(self):
        self.picked_up_stack = stack.Stack()
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def getStack(self, x, y):
        return self.tiles[x][y].stack
    
    def emptyTile(self,x,y):
        self.tiles[x][y] = stack.Stack()

    def placeStone(self, x, y, upright_input,round):
        player_index = self.turn
        if round < 2:
            player_index = (self.turn+1)%2
        if self.getStack(x,y).is_stackable():
            self.getStack(x,y).push_stone(player_index, upright_input)  #Stack group write this!
            self.changeTurn()
            if(player_index == 0):
                self.player1.useStone()
            else:
                self.player2.useStone()
            return True
        else:
            return False

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
            #self.getStack(x,y)
            self.current_x = x
            self.current_y = y
            return True
        else:
            return False

    def moveStack(self, xTo, yTo):
        print("move")
        if (self.isValidMove(self.current_x, self.current_y, xTo, yTo)):
            self.picked_up_stack.drop_stone(self.getStack(xTo, yTo))
            self.current_x = xTo
            self.current_y = yTo
            if self.picked_up_stack.height() == 0:
                self.changeTurn()
                self.current_x = -1
                self.current_y = -1
        else:
            raise TypeError("Not valid move")
    
    def possible_moves_left(self):
         #check stones left
        self.stones_left = True
        if self.turn == 0:
           if self.player1.getStonesLeft() == 0:
               self.stones_left = False
        else:
            if self.player2.getStonesLeft() == 0:
               self.stones_left = False
        
        #check playable tiles left
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.getStack(x,y).height() == 0 or self.getStack(x,y).is_stackable():
                    if self.stones_left:
                        return True
                    else:
                        #check if there are movable stacks in proximity to playable tile
                        if (y > 0 and self.getStack(x, y - 1).check_top_stone(self.turn)) or \
                            (y < self.board_size - 1 and self.getStack(x, y + 1).check_top_stone(self.turn)) or \
                            (x > 0 and self.getStack(x - 1, y).check_top_stone(self.turn)) or \
                            (x < self.board_size - 1 and self.getStack(x + 1, y).check_top_stone(self.turn)) or \
                            (x > 0 and y > 0 and self.getStack(x - 1, y - 1).check_top_stone(self.turn)) or \
                            (x < self.board_size - 1 and y < self.board_size - 1 and self.getStack(x + 1, y + 1).check_top_stone(self.turn)):
                            return True
                        else:
                            continue
        return False
    
    def majority_tiles(self):
        self.first_player = 0
        self.second_player = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.getStack(x,y).height() > 0: 
                    if self.getStack(x,y).check_top_stone(0):
                        self.first_player += 1
                    else:
                        self.second_player += 1
        if self.first_player > self.second_player:
            return self.player1
        #what do we do if they have equal amount of top stones? can happen in for example 4x4 board
        #elif self.first_player == self.second_player:
        else:
            return self.player2
                

