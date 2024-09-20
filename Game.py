import pygame
import sys
import numpy as np


class stone():
    def __init__(self,color):
        self.color=color
        
class grid():
    def __init__(self) :
        self.stones=np.empty([0],dtype=stone)

    def AddStone(self,stone):
        self.stones=np.append(self.stones,stone)   

def init_board():
    board=np.empty([5,5],dtype=grid)

    for r in range(5):
        for c in range(5):
            board[r,c]=grid()

    return board

SQUARESIZE=100
COLUMN_COUNT=5
ROW_COUNT=5


#colors
Background = (197, 209, 235)
Grid = (90, 118, 132)
Black=(0,0,0)
White=(255,255,255)
Brown=(88,57,39)
Red=(255,0,0)
Blue = (146, 175, 215)

class Game():
    def __init__(self):
        #... Initialization ...
        
        self.running = True
        self.turn = 1

        self.x = 0
        self.y = 0


        self.board=init_board()

        
        self.width = (COLUMN_COUNT + 2) * SQUARESIZE
        self.height = (ROW_COUNT + 2) * SQUARESIZE

        size=(self.width,self.height)
        pygame.init()
        self.screen=pygame.display.set_mode(size)
        pygame.display.set_caption('The UU game')

        return

    
    def processInput(self):
        #... Handle user input ...
        #
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                c=int(x/SQUARESIZE)
                r=int(y/SQUARESIZE)
                color = Black
                if (self.turn == 1):
                    color = White

                ##Change to board.update(player, x , y) also need to know if turn should change
                #might want to have gameState containing board, players, sidebar etc who will do all of this
                # check board.check_winner()
                newStone=stone(color)
                self.board[r,c].AddStone(newStone)
                self.turn = not self.turn
                
        return

    def update(self):
        #... Update game state ...
        # send position in board plus player to grid who will handle the new positions of stacks
        return


#add in board, should call render_stack   
    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen,Grid,(c*SQUARESIZE+SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
                pygame.draw.rect(self.screen,Background,(c*SQUARESIZE+5+SQUARESIZE,r*SQUARESIZE+SQUARESIZE+5,SQUARESIZE-10,SQUARESIZE-10))

#add in stack as render_stack
    def draw_stone(self):
        for r in range(5):
            for c in range(5):   
                if self.board[r,c].stones.shape[0]>0:
                    for i in range(self.board[r,c].stones.shape[0]):
                        x= c*SQUARESIZE+SQUARESIZE/2
                        y= (r+1)*SQUARESIZE+SQUARESIZE/2
                        pygame.draw.circle(self.screen,self.board[r,c].stones[i].color,(x,y),40-5*i)


    def render(self):
        # Render game state ...
        #render grid (grid renders stacks?)
        #render sidebars
        self.screen.fill(Background)
        self.draw_board()
        self.draw_stone()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GeeksForGeeks', True, Red, Blue)
        textRect = text.get_rect()
        textRect.center = (self.width // 2, SQUARESIZE // 2)
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