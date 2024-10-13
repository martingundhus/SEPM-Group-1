import pygame
import sys
import numpy as np
import graphic
import Board
import Player
import time

 
COLUMN_COUNT=5
ROW_COUNT=5

EXTRA_WIDTH=2
EXTRA_HEIGHT=1



#colors
Background = (197, 209, 235)
Blue = (146, 175, 215)
Text_color = (45, 45, 42)

###############################################################################
#                                Game Modes                                   #
###############################################################################
class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()
    
class MenuGameMode(GameMode):
    def __init__(self,ui):
        self.ui = ui
        
        # Font
        self.titleFont = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 70)
        self.itemFont = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 45)

        # Menu items
        self.menuItems = [
            {
                'title': '2 players',
                'action': lambda: self.ui.setGameMode('1v1')
            },
            {
                'title': '1 player vs AI',
                'action': lambda: self.ui.setGameMode('AI')
            },
            {
                'title': 'Quit',
                'action': lambda: self.ui.quitGame()
            }
        ]
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("assets/picture/blue_flat_stone.png") ##change

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def difficultySelection(self):
        # Menu items
        self.menuItems = [
            {
                'title': 'easy',
                'action': lambda: self.ui.setGameMode('easy')
            },
            {
                'title': 'med',
                'action': lambda: self.ui.setGameMode('med')
            },
            {
                'title': 'hard',
                'action': lambda: self.ui.setGameMode('hard')
            },
            {
                'title': 'Quit',
                'action': lambda: self.ui.quitGame()
            }
        ]

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ui.quitGame()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem['action']()
                    except Exception as ex:
                        print(ex)
    
    def render(self,window):
        window.fill(Background)

        # Initial y
        y = 50

        # Title
        surface = self.titleFont.render("The UU game", True, Text_color)
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100


        # Compute menu width
        menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item['title'], True, Text_color)
            menuWidth = max(menuWidth, surface.get_width())
            item['surface'] = surface

        # Draw menu items
        x = (window.get_width() - menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item['surface']
            window.blit(surface, (x, y))

            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                window.blit(self.menuCursor, (cursorX, cursorY))

            y += (120 * surface.get_height()) // 100

        pygame.display.update() 

class PlayGameMode(GameMode):
    def __init__(self,ui,dificulty):
        self.ui = ui
        self.running = True
        self.player1 = Player.Player(0,21)
        self.player2 = Player.Player(1,21)
        self.winner_found = False
        
        self.Board=Board.Board(5,dificulty,(int(170),int(100)))
        self.selection=graphic.select()
        
        self.width = int((COLUMN_COUNT + EXTRA_WIDTH*2) * self.Board.grid_size)
        self.height = int((ROW_COUNT + EXTRA_HEIGHT*2) * self.Board.grid_size+100)
        size=(self.width,self.height)

        pygame.init()
        self.screen=pygame.display.set_mode(size)
        pygame.display.set_caption('The UU game')

        return
    
    def processInput(self):
        #... Handle user input ...
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                self.key_control(event)
            if event.type==pygame.QUIT:
                self.ui.quitGame()
        return

    
    def show_winner_popup(self, message):
        font = pygame.font.Font(None, 74)
        text = font.render(message, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))

        self.screen.fill(Background)  # Re-draw background
        self.screen.blit(text, text_rect)
        pygame.display.update()
        
        # Keep the pop-up on the screen for 3 seconds
        time.sleep(3)

    def check_winner(self):
        winner = self.Board.find_winner()
        if winner == 0:
            print("Player 1 Wins!")
            self.winner_found = True
            self.show_winner_popup("Player 1 Wins!")
            pygame.quit()
            sys.exit()
        elif winner == 1:
            print("Player 2 Wins!")
            self.winner_found = True
            self.show_winner_popup("Player 2 Wins!")
            pygame.quit()
            sys.exit()


    def key_control(self,event):
        if event.key== pygame.K_w or event.key == pygame.K_UP:
            print("w is pressed")
            self.selection.input(-1,0)
        if event.key==pygame.K_s or event.key == pygame.K_DOWN:
            print("s is pressed")
            self.selection.input(1,0)
        if event.key==pygame.K_a or event.key == pygame.K_LEFT:
            print("a is pressed")
            self.selection.input(0,-1)
        if event.key==pygame.K_d or event.key == pygame.K_RIGHT:
            print("d is pressed")
            self.selection.input(0,1)

        if event.key==pygame.K_j:
             if event.key == pygame.K_j:
                x, y = self.selection.get_selection_pos()
                if self.Board.placeStone(x, y, False):
                    self.Board.find_winner()
                else:
                    self.selection.set_invalid_color()
                    print("Invalid move")

        if event.key==pygame.K_k:
            x, y = self.selection.get_selection_pos()
            if self.Board.placeStone(x, y, True):
                self.Board.find_winner()   
                
            else:
                self.selection.set_invalid_color()
                print("Invalid move")
                
        if event.key==pygame.K_l:
            x,y = self.selection.get_selection_pos()
            if (not self.Board.isMove):
                if (self.Board.getStack(x,y).height()) > 0:
                    if(self.Board.pickUpStack(x,y)):
                        print("select grid")
                    else:
                        self.selection.set_invalid_color()
                        print("invalid move")
            else:
                if(self.Board.moveStack(x,y)):
                    print("move stack")
                else:
                    print("invalid move")         
        ##cancel select
        if event.key==pygame.K_o:
            self.Board.resetMove()
        ##change turn
        if event.key==pygame.K_p:
            self.Board.changeTurn()


    def render(self,screen):
        # Render game state
        self.screen.fill(Background)
        self.Board.draw(self.screen)
        self.selection.draw(self.screen)
        self.draw_instructions()

        pygame.display.update()
    
    def draw_instructions(self):
        i=0
        xPos=10
        yPos=130
        if self.Board.turn==1:
            xPos=xPos+self.Board.grid_size*7+30
        
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render('W,A,S,D: move', True, Text_color, Background)
        textRect = text.get_rect()
        textRect.topleft = (xPos, yPos+i)
        self.screen.blit(text, textRect)
        i=i+30

        if self.Board.players[self.Board.turn].picked_up_stack!=None:
            
            text=font.render("L: place stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("O: cancel select stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("P: turn over", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

        else:
            text = font.render('J: place flat', True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text = font.render('K: place standing', True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30

            text=font.render("L: select stack", True, Text_color, Background)
            textRect = text.get_rect()
            textRect.topleft = (xPos, yPos+i)
            self.screen.blit(text, textRect)
            i=i+30
 
    def run(self):
        while self.running:
            self.processInput()
            self.render()
            if not self.winner_found:
                self.check_winner()



###############################################################################
#                             User Interface                                  #
###############################################################################
class UserInterface():
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((1000, 720))
        pygame.display.set_caption("The UU game")
        

        # Modes
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode(self)
        self.currentActiveMode = 'Overlay'

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True 

        return
    
    def setGameMode(self, gameMode):
        if self.playGameMode is None:
            if(gameMode == '1v1'):
                self.playGameMode = PlayGameMode(self,0)
                self.currentActiveMode = 'Play'
            if(gameMode == 'AI'):
                self.overlayGameMode.difficultySelection()
            if(gameMode == 'easy'):
                self.playGameMode = PlayGameMode(self,1)
                self.currentActiveMode = 'Play'
                #change to set AIGameModeEasy
            if(gameMode == 'med'):
                self.playGameMode = PlayGameMode(self,2)
                self.currentActiveMode = 'Play'
            if(gameMode == 'hard'):
                self.playGameMode = PlayGameMode(self,3)
                self.currentActiveMode = 'Play'
            
            
    
    
    def showGame(self):
        if self.playGameMode is not None:
            self.currentActiveMode = 'Play'

    def showMenu(self):
        self.overlayGameMode = MenuGameMode(self)
        self.currentActiveMode = 'Overlay'
        
    def quitGame(self):
        self.running = False
       
    def run(self):
        while self.running:
            if self.currentActiveMode == 'Overlay':
                self.overlayGameMode.processInput()
            elif self.playGameMode is not None:
                self.playGameMode.processInput()
                    
            # Render game (if any), and then the overlay (if active)
            if self.playGameMode is not None:
                self.playGameMode.render(self.window)
            else:
                self.window.fill((0,0,0))
            if self.currentActiveMode == 'Overlay':
                darkSurface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0,0))
                self.overlayGameMode.render(self.window)
                
            # Update display
            pygame.display.update()    
            self.clock.tick(60)
       
    
ui = UserInterface()
ui.run()

