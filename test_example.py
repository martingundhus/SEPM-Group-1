import pygame
import sys
import numpy as np
import random

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

Black=(0,0,0)
Brown=(88,57,39)
Red=(255,0,0)

COLUMN_COUNT=5
ROW_COUNT=5

board=init_board()

SQUARESIZE=100
width=COLUMN_COUNT*SQUARESIZE
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
                    x= c*SQUARESIZE+SQUARESIZE/2
                    y= (r+1)*SQUARESIZE+SQUARESIZE/2
                    pygame.draw.circle(screen,board[r,c].stones[i].color,(x,y),40-5*i)

def print_board():
    stones_count=np.empty([5,5])
    for r in range(5):
        for c in range(5):

            stones_count[r,c]=board[r,c].stones.shape[0]

    print(stones_count)

game_over=False
while not game_over:
    screen.fill((0,0,0))
    draw_board()
    draw_stone()


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            c=int(x/SQUARESIZE)
            r=int(y/SQUARESIZE)-1
            newStone=stone((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            board[r,c].AddStone(newStone)
            print_board()
    
    pygame.display.update()