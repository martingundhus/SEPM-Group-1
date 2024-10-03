import pygame
import sys
import numpy as np
import graphic
import Board
import Player
import time

 
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
        self.player1 = Player.Player(0,21)
        self.player2 = Player.Player(1,21)


        self.winner_found = False

        
        self.round = 0

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
    
    def show_winner_popup(self, message):
        font = pygame.font.Font(None, 74)
        text = font.render(message, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))

        self.screen.fill(Background)  # Re-draw background
        self.screen.blit(text, text_rect)
        pygame.display.update()
        
        # Keep the pop-up on the screen for 3 seconds
        time.sleep(3)

    def check_winner(self):
        winner = self.Board.find_winner()
        if winner == 0:
            print("Player 1 Wins!")
            self.winner_found = True
            self.show_winner_popup("Player 1 Wins!")
            pygame.quit()
            sys.exit()
        elif winner == 1:
            print("Player 2 Wins!")
            self.winner_found = True
            self.show_winner_popup("Player 2 Wins!")
            pygame.quit()
            sys.exit()

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
             if event.key == pygame.K_j:
                x, y = self.selection.get_selection_pos()
                if self.Board.placeStone(x, y, False):
                    self.Board.find_winner()
                else:
                    self.selection.set_invalid_color()
                    print("Invalid move")

        if event.key==pygame.K_k:
            x, y = self.selection.get_selection_pos()
            if self.Board.placeStone(x, y, True):
                self.Board.find_winner()   
                self.round += 1
            else:
                self.selection.set_invalid_color()
                print("Invalid move")
                
        if event.key==pygame.K_l:
            x,y = self.selection.get_selection_pos()
            if (not self.Board.isMove):
                if (self.Board.getStack(x,y).height()) > 0:
                    if(self.Board.pickUpStack(x,y)):
                        print("select grid")
                    else:
                        self.selection.set_invalid_color()
                        print("invalid move")
                        #self.Board.draw_error_message(self.screen)
            else:
                if(self.Board.moveStack(x,y)):
                    print("move stack")
                else:
                    print("invalid move")         
        ##cancel select
        if event.key==pygame.K_o:
            self.Board.resetMove()
        ##change turn
        if event.key==pygame.K_p:
            self.Board.changeTurn()

    def update(self):
        # Update game state
        pass

    def render(self):
        # Render game state
        self.screen.fill(Background)
        self.Board.draw(self.screen)
        self.selection.draw(self.screen)
        self.draw_instructions()

        pygame.display.update()

    def draw_instructions(self):
        i=0
        xPos=10
        yPos=130
        if self.Board.turn==1:
            xPos=xPos+self.Board.grid_size*7+30
        
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render('W,A,S,D: move', True, Text_color, Background)
        textRect = text.get_rect()
        textRect.topleft = (xPos, yPos+i)
        self.screen.blit(text, textRect)
        i=i+30

        if self.Board.players[self.Board.turn].hasSelected():
            
            text=font.render("L: place stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("O: cancel select stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("P: turn over", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            # draw stack
            pygame.draw.rect(self.screen, (0,0,0), (xPos,yPos+270,155,250), 1)
            self.Board.players[self.Board.turn].picked_up_stack.draw(self.screen,(xPos+30,500))
        else:
            text = font.render('J: place flat', True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text = font.render('K: place standing', True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("L: select stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

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

        self.selection.draw(self.screen,self.Board.turn)
        self.draw_instructions()
        
        pygame.display.update()
       

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            if not self.winner_found:
                self.check_winner()
       
    
game = Game()
game.run()

