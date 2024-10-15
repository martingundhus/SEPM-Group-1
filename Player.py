import pygame
from image import Image
from copy import deepcopy

class Player:
    def __init__(self, id, stonesLeft):
        self.id = id
        self.stonesLeft = stonesLeft
        self.picked_up_stack = None

        if self.id==1:
            self.icon=Image("assets/picture/red_flat_stone.png")
        else:
            self.icon=Image("assets/picture/blue_flat_stone.png")

    def __deepcopy__(self, memo):
        # Create a new Player instance with the same id and stonesLeft
        new_player = Player(self.id, self.stonesLeft)

        # Assign the existing icon (no deepcopy, just reference the same image)
        new_player.icon = self.icon  # No need to deep copy the icon

        # Copy any other attributes if necessary
        new_player.picked_up_stack = deepcopy(self.picked_up_stack, memo)

        return new_player
    
    def pickUpStack(self,stack):
        self.picked_up_stack = stack

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
        #if(self.id == 1):
        #    center_x = Board.grid_size*8
        xPos=10
        yPos=130
        if self.id ==1:
            xPos=xPos+Board.grid_size*7+30

        self.icon.set_position(xPos,20)
        self.icon.draw(screen)

        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 30)
        stones_left = font.render(f"X:{self.stonesLeft}", True, Text_color, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.topleft = (xPos+100, 70)
        screen.blit(stones_left,stonesRect)


        if(self.picked_up_stack != None):
            # draw stack
            pygame.draw.rect(screen, (0,0,0), (xPos,yPos+270,155,250), 1)
            self.picked_up_stack.draw(screen,(xPos+30,500))

            
            font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 25)
            text = font.render("Picked up stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, Board.grid_size*3.6)
            screen.blit(text,textRect)

    
   