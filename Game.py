import pygame
import sys
import numpy as np
import graphic
import Board
import Player


COLUMN_COUNT = 5
ROW_COUNT = 5

EXTRA_WIDTH = 2
EXTRA_HEIGHT = 1.7

# Colors
Background = (197, 209, 235)
Blue = (146, 175, 215)
Text_color = (45, 45, 42)


class Game():
    def __init__(self):
        self.running = True
        self.winner = None  # Initialize winner as None
        self.player1 = Player.Player(0, 21)
        self.player2 = Player.Player(1, 21)
        self.round = 0

        self.Board = Board.Board(5, position=(int(170), int(100)))
        self.selection = graphic.select()

        self.width = (COLUMN_COUNT + EXTRA_WIDTH * 2) * self.Board.grid_size
        self.height = (ROW_COUNT + EXTRA_HEIGHT * 2) * self.Board.grid_size
        size = (self.width, self.height)

        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('The UU game')

    def processInput(self):
        for event in pygame.event.get():
            if self.winner and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to restart
                    self.restart_game()  # Restart the game
            if event.type == pygame.KEYDOWN:
                self.key_control(event)
            if event.type == pygame.QUIT:
                self.running = False
        return

    def key_control(self, event):
        if self.winner:  # If there's a winner, ignore inputs
            return

        if event.key == pygame.K_w:
            print("w is pressed")
            self.selection.input(-1, 0)
        if event.key == pygame.K_s:
            print("s is pressed")
            self.selection.input(1, 0)
        if event.key == pygame.K_a:
            print("a is pressed")
            self.selection.input(0, -1)
        if event.key == pygame.K_d:
            print("d is pressed")
            self.selection.input(0, 1)
        if event.key == pygame.K_j:
            print("add flat stone")
            x, y = self.selection.get_selection()
            self.Board.placeStone(x, y, False, self.round)
            self.round += 1

            # Check for a winner
            if self.Board.check_winning_condition():  # Check if there's a winner
                self.winner = self.Board.turn  # Set the winner (0 or 1)

        if event.key == pygame.K_k:
            print("add stand stone")
            x, y = self.selection.get_selection()
            self.Board.placeStone(x, y, True, self.round)
            self.round += 1

            # Check for a winner
            if self.Board.check_winning_condition():  # Check if there's a winner
                self.winner = self.Board.turn  # Set the winner (0 or 1)

    def draw_player_Information(self):
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 40)
        text = font.render('Player ' + str(self.Board.turn + 1) + "s turn", True, Text_color, Background)
        textRect = text.get_rect()

        # Set the center of the rectangular object.
        textRect.center = (self.width // 2, self.Board.grid_size // 2)
        self.screen.blit(text, textRect)

        self.player1.draw_player_stats(self.screen, self.Board)
        self.player2.draw_player_stats(self.screen, self.Board)

    def draw_instructions(self):
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render('W,A,S,D to move', True, Text_color, Background)
        textRect = text.get_rect()

        # Set the center of the rectangular object.
        textRect.center = (self.width // 2, (self.Board.board_size + 2.3) * self.Board.grid_size)
        self.screen.blit(text, textRect)

        text = font.render('J: place flat', True, Text_color, Background)
        textRect = text.get_rect()

        # Set the center of the rectangular object.
        textRect.center = (self.width // 3, (self.Board.board_size + 2.7) * self.Board.grid_size)
        self.screen.blit(text, textRect)

        text = font.render('K: place standing', True, Text_color, Background)
        textRect = text.get_rect()

        # Set the center of the rectangular object.
        textRect.center = (self.width // 3 * 2, (self.Board.board_size + 2.7) * self.Board.grid_size)
        self.screen.blit(text, textRect)

    def update(self):
        # Update game state ...
        return

    def render(self):
        self.screen.fill(Background)
        self.Board.draw(self.screen)
        self.selection.draw(self.screen)
        self.draw_player_Information()
        self.draw_instructions()

        if self.winner is not None:
            self.display_winner()  # Call the display_winner method

        pygame.display.update()

    def display_winner(self):
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 50)
        winner_text = f"Player {self.winner + 1} wins!"
        text = font.render(winner_text, True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 2)  # Center of the screen
        self.screen.blit(text, textRect)

    def restart_game(self):
        self.winner = None  # Reset winner
        self.round = 0  # Reset round
        self.Board = Board.Board(5, position=(int(170), int(100)))  # Re-initialize the board
        self.player1 = Player.Player(0, 21)  # Re-initialize players
        self.player2 = Player.Player(1, 21)

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
        return


game = Game()
game.run()
