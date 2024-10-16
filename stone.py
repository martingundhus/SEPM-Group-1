import pygame
import AI_stone
from copy import deepcopy
from image import Image

class Stone:
    #Default is flat stone
    #Player is the ID for player, used to get color of stone here
    def __init__(self, player_index,upright):
        self.player_index = player_index
        self.upright = upright
        
        
        if player_index==0 and self.upright==False:
            self.img_stone=Image("assets/picture/blue_flat_stone.png")
        if player_index==1 and self.upright==False:
            self.img_stone=Image("assets/picture/red_flat_stone.png")
        if player_index==0 and self.upright==True:
            self.img_stone=Image("assets/picture/blue_stand_stone.png")
        if player_index==1 and self.upright==True:
            self.img_stone=Image("assets/picture/red_stand_stone.png")

    def __deepcopy__(self, memo):
        # Create a new Stone instance with the same player_index and upright values
        player_index = deepcopy(self.player_index)
        upright = deepcopy(self.upright)
        new_stone = AI_stone.AI_Stone(player_index, upright)

        # Assign the existing img_stone (no deepcopy, just reference the same image)
        #new_stone.img_stone = self.img_stone  # No need to deep copy the image

        return new_stone
        
    def draw(self,screen,x,y):
        self.img_stone.set_position(x,y)
        self.img_stone.draw(screen)