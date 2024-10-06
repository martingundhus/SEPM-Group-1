
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

    def set_stack(self,stack):
        self.stack = stack
    
        

class Board():
    offset_x=31
    offset_y=31
    grid_size=100

       
    def __init__(self, board_size, position=(0,0)) -> None:
        self.board_size = board_size
        self.turn = 0
        self.current_x = -1
        self.current_y = -1
        #square where stack was picked up from
        self.initial_x = -1
        self.initial_y = -1
        self.players = [Player.Player(0,21),Player.Player(1,21)]
        self.isMove = False
        self.round = 0
        self.img_board=Image("assets/picture/board.png",position)
        self.position=position
        self.error_message = ""
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
        self.players[0].draw_player_stats(screen,self)
        self.players[1].draw_player_stats(screen,self)
        self.draw_error_message(screen)
    
    def draw_error_message(self,screen):
        Background = (197, 209, 235)
        Text_color = (181, 49, 32)
        center_x = self.grid_size * (self.board_size + 3.5)
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render(self.error_message, True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x // 2, (self.board_size + 2 )* self.grid_size)
        screen.blit(text, textRect)

    def hasSelected(self):
        return (self.picked_up_stack.height() > 0)
    

    def changeTurn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
        self.round +=1

    def getStack(self, x, y):
        return self.tiles[x][y].stack
    
    def emptyTile(self,x,y):
        self.tiles[x][y].empty()

    def placeStone(self, x, y, upright_input):
        if self.isMove:
            return False
        player_index = self.turn
        if self.round < 2:
            player_index = (self.turn+1)%2
        if self.getStack(x,y).is_stackable():
            self.getStack(x,y).push_stone(player_index, upright_input) 
            self.changeTurn()
            self.players[player_index].useStone()
            self.error_message = ""
            return True
        else:
            self.error_message = "Invalid tile to place stone"
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
            self.players[self.turn].pickUpStack(self.getStack(x,y))
            #reset tile
            self.emptyTile(x,y)
            self.current_x = self.initial_x = x
            self.current_y = self.initial_y = y
            self.isMove = True
            self.error_message = ""
            return True
        else:
            self.error_message = "Cannot pick up stack"
            return False
        
 

    def moveStack(self, xTo, yTo):
        print("move")
        if (self.isValidMove(self.current_x, self.current_y, xTo, yTo)):
            self.players[self.turn].picked_up_stack.drop_stone(self.getStack(xTo, yTo))
            self.current_x = xTo
            self.current_y = yTo
            if self.players[self.turn].picked_up_stack.height() == 0:
                self.players[self.turn].picked_up_stack = None
                self.changeTurn()
                self.isMove = False
            self.error_message = ""
            return True
        else:
            self.error_message = "Cannot move this stack"
            return False
    

    def resetMove(self):
       
        if(self.isMove and self.current_x == self.initial_x and self.current_y == self.initial_y):
            self.isMove = False
            self.tiles[self.current_x, self.current_y].set_stack(self.players[self.turn].picked_up_stack)
            self.players[self.turn].picked_up_stack = None

    

    def find_winner(self):
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(x, y, first_player_index, first_upright):
            
            if not (0 <= x < 5 and 0 <= y < 5):
                return False
            if (x, y) in visited:
                return False

            stack = self.getStack(x, y)
            if stack.height() == 0:
                return False

            top_stone = stack.stack_content[-1]
            
            if top_stone.player_index != first_player_index or top_stone.upright != first_upright:
                return False
            
            visited.add((x, y))

            if y == self.board_size - 1 or x == self.board_size - 1:
                print(f"Path found for player {first_player_index} from ({x}, {y})!")
                return True

            #continue dfs
            for dx, dy in directions:
                next_x = x + dx
                next_y = y + dy
                if dfs(next_x, next_y, first_player_index, first_upright):
                    return True

            visited.remove((x, y))
            return False

        
        for player_index in [0, 1]:
            for i in range(self.board_size):
                print(f"Checking player {player_index}'s path from left side and top side...")
                first_stack_left = self.getStack(i, 0)
                if first_stack_left.height() > 0:
                    first_stone_left = first_stack_left.stack_content[-1]
                    if dfs(i, 0, first_stone_left.player_index, first_stone_left.upright):
                        print(f"Player {player_index} wins!")
                        return player_index

                first_stack_top = self.getStack(0, i)
                if first_stack_top.height() > 0:
                    first_stone_top = first_stack_top.stack_content[-1]
                    if dfs(0, i, first_stone_top.player_index, first_stone_top.upright):
                        print(f"Player {player_index} wins!")
                        return player_index

        print("No path found for any player.")
        return None
