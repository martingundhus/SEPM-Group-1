import pygame
import sys
import numpy as np
import graphic
import Board
import Player

 
COLUMN_COUNT=5
ROW_COUNT=5

EXTRA_WIDTH=2
EXTRA_HEIGHT=1.7



#colors
Background = (197, 209, 235)
Blue = (146, 175, 215)
Text_color = (45, 45, 42)


class Game():
    def __init__(self):
        #... Initialization ...
        self.running = True
       # self.turn = 0  #board keeps track of turn??
        self.player1 = Player.Player(0,21)
        self.player2 = Player.Player(1,21)
        self.round = 0

        self.Board=Board.Board(5,position=(int(170),int(100)))
        self.selection=graphic.select()
        
        self.width = (COLUMN_COUNT + EXTRA_WIDTH*2) * self.Board.grid_size
        self.height = (ROW_COUNT + EXTRA_HEIGHT*2) * self.Board.grid_size+100
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
            self.player1.useStone()
        else:
            self.player2.useStone()
        
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
            x,y = self.selection.get_selection_pos()
            if(self.Board.placeStone(x,y,False,self.round)):
                self.round += 1
            else:
                print("invalid move")
        if event.key==pygame.K_k:
            print("add stand stone")
            x,y = self.selection.get_selection_pos()
            if(self.Board.placeStone(x,y,True,self.round)):
                self.round += 1
            else:
                print("invalid move")
        if event.key==pygame.K_l:
            x,y = self.selection.get_selection_pos()
            print(self.Board.picked_up_stack==None)
            if (not self.Board.hasSelected()):
                if (self.Board.getStack(x,y).height()) > 0:
                    #self.selection.select_grid=self.Board.tiles[self.selection.get_selection_pos()]
                    if(self.Board.pickUpStack(x,y)):
                        print("select grid")
                    else:
                        print("invalid move")
            else:
                #self.selection.select_grid.stack.drop_stone(self.Board.tiles[self.selection.get_selection_pos()].stack)
                #pickedUpStack= self.selection.select_grid
                if(self.Board.moveStack(x,y)):
                    print("move stack")
                else:
                    print("invalid move")
                    
        ##cancel select
        if event.key==pygame.K_o:
            self.selection.select_grid==None
        ##change turn
        if event.key==pygame.K_p:
            self.change_turn()


    def draw_instructions(self):
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render('W,A,S,D to move', True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3*2, (self.Board.board_size + 2.7 )* self.Board.grid_size)
        self.screen.blit(text, textRect)

        
        text = font.render('J: place flat', True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3, (self.Board.board_size + 2.7 )* self.Board.grid_size)
        self.screen.blit(text, textRect)

        text = font.render('K: place standing', True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3 * 2, (self.Board.board_size + 3.1 )* self.Board.grid_size)
        self.screen.blit(text, textRect)

        text=font.render("L: select stack and place", True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3, (self.Board.board_size + 3.1 )* self.Board.grid_size)
        self.screen.blit(text, textRect)

        text=font.render("O: cancel select stack", True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3 * 2, (self.Board.board_size + 3.5 )* self.Board.grid_size)
        self.screen.blit(text, textRect)

        text=font.render("P: turn over", True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 3, (self.Board.board_size + 3.5 )* self.Board.grid_size)
        self.screen.blit(text, textRect)
        
        
        
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
        self.draw_instructions()
        
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