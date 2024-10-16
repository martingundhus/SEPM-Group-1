import pygame
from image import Image

class AI_Stone:
    #Default is flat stone
    #Player is the ID for player, used to get color of stone here
    def __init__(self, player_index,upright):
        self.player_index = player_index
        self.upright = upright