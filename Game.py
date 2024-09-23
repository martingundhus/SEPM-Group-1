import pygame
import sys
import numpy as np
import graphic
class player():
    def __init__(self,id):
        self.id = id
        self.stones_left = 21

    def player_stats(self,screen):
        center_x = graphic.board.grid_size
        if(self.id == 1):
            center_x = graphic.board.grid_size*8


        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Player ' + str(self.id+1), True, Blue, Background)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.top = (graphic.board.grid_size*1.5)
        textRect.centerx = (center_x)
        screen.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 25)
        stones_left = font.render('Stones left:', True, Blue, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.center = (center_x, graphic.board.grid_size*3)
        screen.blit(stones_left,stonesRect)

        text = font.render(str(self.stones_left), True, Blue, Background)
        textRect = text.get_rect()
        textRect.center = (center_x, graphic.board.grid_size*3.5)
        screen.blit(text,textRect)
    
    
COLUMN_COUNT=5
ROW_COUNT=5

EXTRA_WIDTH=2
EXTRA_HEIGHT=1



#colors
Background = (197, 209, 235)
Blue = (146, 175, 215)

class Game():
    def __init__(self):
        #... Initialization ...
        self.running = True
        self.turn = 0
        self.player1 = player(0)
        self.player2 = player(1)

        self.board=graphic.board(position=(int(170),int(100)))
        self.selection=graphic.select()
        
        self.width = (COLUMN_COUNT + EXTRA_WIDTH*2) * graphic.board.grid_size
        self.height = (ROW_COUNT + EXTRA_HEIGHT*2) * graphic.board.grid_size
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
            self.board.grids[self.selection.get_selection()].add_stone(graphic.stone(self.turn,0))
            self.change_turn()
        if event.key==pygame.K_k:
            print("add stand stone")
            self.board.grids[self.selection.get_selection()].add_stone(graphic.stone(self.turn,1))
            self.change_turn()
        if event.key==pygame.K_l:
            print("")

    def draw_player_Information(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render('Player ' + str(self.turn+1) +"s turn", True, Blue, Background)
        textRect = text.get_rect()
    
        # set the center of the rectangular object.
        textRect.center = (self.width // 2, graphic.board.grid_size // 2)
        self.screen.blit(text, textRect)

        self.player1.player_stats(self.screen)
        self.player2.player_stats(self.screen)
        
    def update(self):
        #... Update game state ...
        # send position in board plus player to grid who will handle the new positions of stacks
        return
    
    def render(self):
        # Render game state ...
        #render grid (grid renders stacks?)
        #render sidebars
        self.screen.fill(Background)
        self.board.draw(self.screen)
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