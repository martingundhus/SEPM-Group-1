import pygame

class Button():
    def __init__(self,text,x=0,y=0):
        green = (0, 255, 0)
        blue = (0, 0, 128)
        font = pygame.font.Font('freesansbold.ttf', 20)
        
        self.text = font.render(text, True, green, blue)
        self.x=x
        self.y=y

        self.textRect = self.text.get_rect()
        self.show=False
        self.clicked=False
        
    
    def set_pos(self,x,y,show=False):

        pos=pygame.mouse.get_pos()
        if not self.textRect.collidepoint(pos):
            self.x=x
            self.y=y
            self.show=show

    def draw(self,screen):
        action=False
        if self.show:
            self.textRect.topleft=(self.x,self.y)
            screen.blit(self.text,self.textRect)
            pos=pygame.mouse.get_pos()

            if(self.textRect.collidepoint(pos)):
                if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                    self.clicked=True
                    action=True
                    print("clicked")
                
                if pygame.mouse.get_pressed()[0]==0:
                    self.clicked=False
        
        return action
        