import pygame
import sys
import numpy as np

class player():
    def __init__(self,id):
        self.id = id
        self.stones_left = 21

    def player_stats(self,screen):
        center_x = SQUARESIZE
        if(self.id == 2):
            center_x = SQUARESIZE*8


        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Player ' + str(self.id), True, Blue, Background)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.top = (SQUARESIZE*1.5)
        textRect.centerx = (center_x)
        screen.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 25)
        stones_left = font.render('Stones left:', True, Blue, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.center = (center_x, SQUARESIZE*3)
        screen.blit(stones_left,stonesRect)

        text = font.render(str(self.stones_left), True, Blue, Background)
        textRect = text.get_rect()
        textRect.center = (center_x, SQUARESIZE*3.5)
        screen.blit(text,textRect)
    
    

class stone():
    def __init__(self,color):
        self.color=color

class tile():
    def __init__(self):
        self.stones=np.empty([0],dtype=stone)

    def add_stone(self,stone):
        self.stones=np.append(self.stones,stone)   
        
class board():
    def __init__(self,columns,rows) :
       # self.stones=np.empty([0],dtype=stone)
        self.colums = columns
        self.rows = rows
        self.grid=np.empty([self.colums,self.rows],dtype=tile)

        for r in range(5):
            for c in range(5):
                self.grid[r,c]=tile()

    def add_stone(self,stone, r,c):
        self.grid[r,c].add_stone(stone)

    def get_tile(self,r,c):
        return self.grid[r,c]

"""
def init_board(columns,rows):
    board=np.empty([columns,rows],dtype=board)

    for r in range(5):
        for c in range(5):
            board[r,c]=grid()

    return board
"""

SQUARESIZE=100
COLUMN_COUNT=5
ROW_COUNT=5

EXTRA_WIDTH=2
EXTRA_HEIGHT=1



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
        self.player1 = player(1)
        self.player2 = player(2)

        self.x = 0
        self.y = 0
        self.board=board(5,5)

        
        self.width = (COLUMN_COUNT + EXTRA_WIDTH*2) * SQUARESIZE
        self.height = (ROW_COUNT + EXTRA_HEIGHT*2) * SQUARESIZE
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
               
                #get column and row of matrix
                c=int((x)/SQUARESIZE)-EXTRA_WIDTH
                r=int((y)/SQUARESIZE)-EXTRA_HEIGHT
                if(x >= 0 & x <= 5 & y >= 0 & y <= 5):
                    color = Black
                    if (self.turn == 1):
                        color = White
                        self.player1.stones_left -=1
                        self.turn = 2
                    else:
                        self.turn = 1
                        self.player2.stones_left -=1

                    ##Change to board.update(player, x , y) also need to know if turn should change
                    #might want to have gameState containing board, players, sidebar etc who will do all of this
                    # check board.check_winner()
                    newStone=stone(color)
                    self.board.add_stone(newStone,r,c)
                    
                    
        return

    def update(self):
        #... Update game state ...
        # send position in board plus player to grid who will handle the new positions of stacks
        return


#add in board, should call render_stack   
    def draw_board(self):
        shape = pygame.Rect(EXTRA_WIDTH*SQUARESIZE -2.5 ,EXTRA_HEIGHT*SQUARESIZE -2.5 ,5*SQUARESIZE+5,5*SQUARESIZE+5)
        pygame.draw.rect(self.screen,Grid,shape)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                #pygame.draw.rect(self.screen,Grid,((c+EXTRA_WIDTH)*SQUARESIZE,(r+EXTRA_HEIGHT)*SQUARESIZE,SQUARESIZE,SQUARESIZE))
                pygame.draw.rect(self.screen,Background,((c+EXTRA_WIDTH)*SQUARESIZE+5,(r+EXTRA_HEIGHT)*SQUARESIZE+5,SQUARESIZE-10,SQUARESIZE-10))

#add in stack as render_stack
    def draw_stone(self):
        for r in range(5):
            for c in range(5):   
                if self.board.grid[r,c].stones.shape[0]>0:
                    for i in range(self.board.get_tile(r,c).stones.shape[0]):
                        x= (c+EXTRA_WIDTH)*SQUARESIZE+SQUARESIZE/2
                        y= (r+EXTRA_HEIGHT)*SQUARESIZE+SQUARESIZE/2
                        pygame.draw.circle(self.screen,self.board.get_tile(r,c).stones[i].color,(x,y),40-5*i)

    def draw_turn(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render('Player ' + str(self.turn) +"s turn", True, Blue, Background)
        textRect = text.get_rect()
    
        # set the center of the rectangular object.
        textRect.center = (self.width // 2, SQUARESIZE // 2)
        self.screen.blit(text, textRect)

    def render(self):
        # Render game state ...
        #render grid (grid renders stacks?)
        #render sidebars
        self.screen.fill(Background)
        self.draw_board()
        self.draw_stone()
        self.draw_turn()
        self.player1.player_stats(self.screen)
        self.player2.player_stats(self.screen)


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