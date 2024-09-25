import pygame
import sys
import numpy as np
import graphic
import Board


class player():
    def __init__(self,id):
        self.id = id
        self.stones_left = 21

    #feels wrong
    def player_stats(self,screen):
        center_x = Board.Board.grid_size
        if(self.id == 1):
            center_x = Board.Board.grid_size*8


        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 32)
        text = font.render('Player ' + str(self.id+1), True, Text_color, Background)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.top = (Board.Board.grid_size*1.5)
        textRect.centerx = (center_x)
        screen.blit(text, textRect)

        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 25)
        stones_left = font.render('Stones left:', True, Text_color, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.center = (center_x, Board.Board.grid_size*3)
        screen.blit(stones_left,stonesRect)

        text = font.render(str(self.stones_left), True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x, Board.Board.grid_size*3.5)
        screen.blit(text,textRect)
    
    
COLUMN_COUNT=5
ROW_COUNT=5

EXTRA_WIDTH=2
EXTRA_HEIGHT=1



#colors
Background = (197, 209, 235)
Blue = (146, 175, 215)
Text_color = (45, 45, 42)


class Game():
    def __init__(self):
        #... Initialization ...
        self.running = True
        self.turn = 0
        self.player1 = player(0)
        self.player2 = player(1)

        self.Board=Board.Board(5,position=(int(170),int(100)))
        self.selection=graphic.select()
        
        self.width = (COLUMN_COUNT + EXTRA_WIDTH*2) * self.Board.grid_size
        self.height = (ROW_COUNT + EXTRA_HEIGHT*2) * self.Board.grid_size
        size=(self.width,self.height)

        pygame.init()
        self.screen=pygame.display.set_mode(size)
        pygame.display.set_caption('The UU game')

        return
    
    def processInput(self):
        #... Handle user input ...
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                self.key_control(event)
            if event.type==pygame.QUIT:
                self.running=False
        return

   
    def change_turn(self):
        if self.turn == 0:
            self.player1.stones_left -=1
        else:
            self.player2.stones_left -=1
        
        self.turn=(self.turn+1)%2
        self.selection.select_grid=None

    def key_control(self,event):
        if event.key== pygame.K_w:
            print("w is pressed")
            self.selection.input(-1,0)
        if event.key==pygame.K_s:
            print("s is pressed")
            self.selection.input(1,0)
        if event.key==pygame.K_a:
            print("a is pressed")
            self.selection.input(0,-1)
        if event.key==pygame.K_d:
            print("d is pressed")
            self.selection.input(0,1)
        if event.key==pygame.K_j:
            print("add flat stone")
            self.Board.tiles[self.selection.get_selection_pos()].add_stone(self.turn,False)
            self.change_turn()
        if event.key==pygame.K_k:
            print("add stand stone")
            self.Board.tiles[self.selection.get_selection_pos()].add_stone(self.turn,True)
            self.change_turn()
        if event.key==pygame.K_l:
            if self.selection.select_grid==None:
                if len(self.Board.tiles[self.selection.get_selection_pos()].stack.stack_content)>0:
                    self.selection.select_grid=self.Board.tiles[self.selection.get_selection_pos()]
                    print("select grid")
            else:
                self.selection.select_grid.stack.drop_stone(self.Board.tiles[self.selection.get_selection_pos()].stack)
        ##cancel select
        if event.key==pygame.K_o:
            self.selection.select_grid==None
        ##change turn
        if event.key==pygame.K_p:
            self.change_turn()



    def draw_player_Information(self):
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 40)
        text = font.render('Player ' + str(self.turn+1) +"s turn", True, Text_color, Background)
        textRect = text.get_rect()
    
        # set the center of the rectangular object.
        textRect.center = (self.width // 2, self.Board.grid_size // 2)
        self.screen.blit(text, textRect)

        self.player1.player_stats(self.screen)
        self.player2.player_stats(self.screen)
        
    def update(self):
        #... Update game state ...
        # send position in Board.Board plus player to grid who will handle the new positions of stacks
        return
    
    def render(self):
        # Render game state ...
        #render grid (grid renders stacks?)
        #render sidebars
        self.screen.fill(Background)
        self.Board.draw(self.screen)
        self.selection.draw(self.screen)
        self.draw_player_Information()
        
        pygame.display.update()
       

    def run(self):
       while self.running:
           self.processInput()
           self.update()
           self.render()
           #self.clock.tick(60) 
       return
    
game = Game()
game.run()