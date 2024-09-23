import pygame
import numpy as np
import board

class select():
    def __init__(self,):
        self.y=0
        self.x=0
        self.select_grid=None
    def input(self,y,x):

        self.y=self.y+y

        self.x=self.x+x

        if self.y>4:
            self.y=4
        if self.y<0:
            self.y=0
        
        if self.x>4:
            self.x=4
        if self.x<0:
            self.x=0

        print(f"y={self.y} x={self.x}")
    def draw(self,screen):
        pygame.draw.rect(screen, (0, 255, 0), (170+board.Board.offset_x+self.x*board.Board.grid_size
                                                 ,100+board.Board.offset_y+self.y*board.Board.grid_size
                                                 , 100, 100)
                                                 , 3)
    
    def get_selection(self):
        return (self.y,self.x)
    def __str__(self) -> str:
        return f"y={self.y} x={self.x}"
        

