import pygame


class Player:
    def __init__(self, id, stonesLeft):
        self.id = id
        self.stonesLeft = stonesLeft
        self.picked_up_stack = None
    
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
        if(self.id == 1):
            center_x = Board.grid_size*8

        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 32)
        text = font.render('Player ' + str(self.id+1), True, Text_color, Background)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.top = (Board.grid_size*1.5)
        textRect.centerx = (center_x)
        screen.blit(text, textRect)

        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 25)
        stones_left = font.render('Stones left:', True, Text_color, Background)
        stonesRect = stones_left.get_rect()
        stonesRect.center = (center_x, Board.grid_size*3)
        screen.blit(stones_left,stonesRect)

        text = font.render(str(self.stonesLeft), True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x, Board.grid_size*3.5)
        screen.blit(text,textRect)

        if(self.picked_up_stack != None):
            text = font.render("Picked up stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.center = (center_x, Board.grid_size*4.3)
            screen.blit(text,textRect)
            self.picked_up_stack.draw(screen,(center_x - Board.grid_size/2, Board.grid_size*5))

    
   