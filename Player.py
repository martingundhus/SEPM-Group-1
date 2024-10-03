import pygame
from image import Image
class Player:
    def __init__(self, id, stonesLeft):
        self.id = id
        self.stonesLeft = stonesLeft

        if self.id==1:
            self.icon=Image("assets/picture/red_flat_stone.png")
        else:
            self.icon=Image("assets/picture/blue_flat_stone.png")
    def getId(self):
        return self.id
    
    def getStonesLeft(self):
        return self.stonesLeft
    
    def useStone(self):
        if (self.stonesLeft > 0):
            self.stonesLeft -= 1
        else:
            raise TypeError("No stones left")
    
    def getRemaining(self):
        return self.stonesLeft
    
    def draw_player_stats(self,screen, Board):
        center_x = Board.grid_size
        Background = (197, 209, 235)
        Text_color = (45, 45, 42)
        if(self.id == 1):
            center_x = Board.grid_size*8

        center_x=center_x-90
        self.icon.set_position(center_x,20)
        self.icon.draw(screen)

        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 30)
        stones_left = font.render(f"X:{self.stonesLeft}", True, Text_color, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.center = (center_x+120, 100)
        screen.blit(stones_left,stonesRect)

   