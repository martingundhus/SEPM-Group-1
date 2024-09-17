import pygame
import sys
import numpy as np
import random
import GUI

class stone():
    def __init__(self,player_tag,stone_tag=0):
        #tag=0 flat, 
        #tag=1 stand 
        self.stone_tag=stone_tag
        if player_tag==0:
            self.color=Red
        if player_tag==1:
            self.color=Blue
        
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

Black=(0,0,0)
Brown=(88,57,39)
Red=(255,0,0)
Blue=(0,0,255)

player_tag=0

COLUMN_COUNT=5
ROW_COUNT=5

board=init_board()

SQUARESIZE=100
width=COLUMN_COUNT*SQUARESIZE+100
height=(ROW_COUNT+1)*SQUARESIZE

size=(width,height)
pygame.init()
screen=pygame.display.set_mode(size)

def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,Brown,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.rect(screen,Black,(c*SQUARESIZE+5,r*SQUARESIZE+SQUARESIZE+5,SQUARESIZE-10,SQUARESIZE-10))

def draw_stone():

    for r in range(5):
        for c in range(5):
            
            if board[r,c].stones.shape[0]>0:
                for i in range(board[r,c].stones.shape[0]):
                    

                    if board[r,c].stones[i].stone_tag==0:
                        x= c*SQUARESIZE+SQUARESIZE/2
                        y= (r+1)*SQUARESIZE+SQUARESIZE/2
                        pygame.draw.circle(screen,board[r,c].stones[i].color,(x,y),40-5*i)
                    if board[r,c].stones[i].stone_tag==1:
                        x= c*SQUARESIZE+10
                        y= r*SQUARESIZE+SQUARESIZE+10
                        pygame.draw.rect(screen,board[r,c].stones[i].color,(x,y,80,80))

def print_board():
    stones_count=np.empty([5,5])
    for r in range(5):
        for c in range(5):

            stones_count[r,c]=board[r,c].stones.shape[0]

    print(stones_count)

flat_button=GUI.Button("flat stone")
stand_button=GUI.Button("stand stone")
def draw_GUI():
    global player_tag
    if flat_button.draw(screen):

        c=int(flat_button.x/SQUARESIZE)
        r=int(flat_button.y/SQUARESIZE)-1
        newStone=stone(player_tag)
        board[r,c].AddStone(newStone)
        player_tag=(player_tag+1)%2

    if stand_button.draw(screen):
        c=int(stand_button.x/SQUARESIZE)
        r=int(stand_button.y/SQUARESIZE)-1
        newStone=stone(player_tag,1)
        board[r,c].AddStone(newStone)
        player_tag=(player_tag+1)%2

game_over=False
while not game_over:
    screen.fill((0,0,0))
    draw_board()
    draw_stone()
    draw_GUI()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            flat_button.set_pos(x+10,y+10,True)
            stand_button.set_pos(x+10,y+30,True)
            print_board()
            
    
    pygame.display.update()