import pygame
class Game():
    def __init__(self):
        #... Initialization ...
        pygame.init()
        self.players = [] # change to initiate 2 players
        self.turn = "white"
        self.board = "board" #change to an instance of the grid class. The grid should check for winning conditions and keep track of all stack positions


        return

    def processInput(self):
        #... Handle user input ...
        #
        return

    def update(self):
        #... Update game state ...
        # 
        return

    def render(self):
        # Render game state ...
        #render grid (grid renders stacks?)
        #render sidebars
        return

    def run(self):    
       # ... Main loop ...
       return