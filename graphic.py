import pygame
import numpy as np

class Image():
    def __init__(self,path,position=(0,0)) -> None:
        self.img=pygame.image.load(path)

        self.rect=self.img.get_rect()
        self.rect.topleft=position
    
    def set_position(self,x,y):
        self.rect.topleft=x,y
    
    def draw(self,screen):
        screen.blit(self.img,self.rect)

class board():
    offset_x=31
    offset_y=31
    grid_size=100

    def __init__(self,position=(0,0)) -> None:
        self.img_board=Image("assets/picture/board.png",position)
        self.position=position
        self.init_grid()
    
    def init_grid(self):
        orig_x,orig_y=self.position
        self.grids=np.empty((5,5),dtype=grid)
        for y in range(5):
            for x in range(5):
                index=int((x+y)%2)
                if index==0:
                    self.grids[y,x]=grid("assets/picture/white_grid.png",(orig_x+board.offset_x+x*board.grid_size,
                                                                            orig_y+board.offset_y+y*board.grid_size))
                elif index==1:
                    self.grids[y,x]=grid("assets/picture/brown_grid.png",(orig_x+board.offset_x+x*board.grid_size,
                                                                            orig_y+board.offset_y+y*board.grid_size))

    def draw_board(self,screen):
        self.img_board.draw(screen)
        for y in range(5):
            for x in range(5):
                self.grids[y,x].draw(screen)

    def draw(self,screen):
        self.draw_board(screen)
        

class grid():
    def __init__(self,grid_path,position=(0,0)) -> None:
        self.img_grid=Image(grid_path,position)
        self.position=position
        self.stones=np.empty([0],dtype=stone)
    
    ## for prototype
    def add_stone(self,stone):
        self.stones=np.append(self.stones,stone)
    def draw(self,screen):
        self.img_grid.draw(screen)

        if self.stones.shape[0]>0:
            for i in range(self.stones.shape[0]):
                x,y=self.position
                self.stones[i].draw(screen,x,y-15*i)

class stone():
    def __init__(self,player_tag,stone_tag) -> None:
        
        if player_tag==0 and stone_tag==0:
            self.img_stone=Image("assets/picture/blue_flat_stone.png")
        if player_tag==1 and stone_tag==0:
            self.img_stone=Image("assets/picture/red_flat_stone.png")
        if player_tag==0 and stone_tag==1:
            self.img_stone=Image("assets/picture/blue_stand_stone.png")
        if player_tag==1 and stone_tag==1:
            self.img_stone=Image("assets/picture/red_stand_stone.png")
        
    def draw(self,screen,x,y):
        self.img_stone.set_position(x,y)
        self.img_stone.draw(screen)

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
        pygame.draw.rect(screen, (0, 255, 0), (170+board.offset_x+self.x*board.grid_size
                                                 ,100+board.offset_y+self.y*board.grid_size
                                                 , 100, 100)
                                                 , 3)
    
    def get_selection(self):
        return (self.y,self.x)
    def __str__(self) -> str:
        return f"y={self.y} x={self.x}"
        

