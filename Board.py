
import stone
import stack
import Player
import pygame
from image import Image

import numpy as np



class tile():
    def __init__(self,grid_path,position=(0,0)) -> None:
        self.img_grid=Image(grid_path,position)
        self.position=position
        self.stack=stack.Stack()
    
    def add_stone(self,player_index, upright_input):
        self.stack.push_stone(player_index, upright_input)
    
    def draw(self,screen):
        self.img_grid.draw(screen)
        self.stack.draw(screen,self.position)

    def empty(self):
        self.stack=stack.Stack()

    def set_stack(self,stack):
        self.stack = stack
    
        

class Board():
    offset_x=31
    offset_y=31
    grid_size=100

       
    def __init__(self, board_size, position=(0,0)) -> None:
        self.board_size = board_size
        self.turn = 0
        self.current_x = -1
        self.current_y = -1
        #square where stack was picked up from
        self.initial_x = -1
        self.initial_y = -1
        self.direction = "none"
        self.players = [Player.Player(0,21),Player.Player(1,21)]
        self.isMove = False
        self.round = 0
        self.img_board=Image("assets/picture/board.png",position)
        self.position=position
        self.error_message = ""
        self.init_grid()

          
    def init_grid(self):
            orig_x,orig_y=self.position
            self.tiles=np.empty((5,5),dtype=tile)
            for y in range(5):
                for x in range(5):
                    index=int((x+y)%2)
                    if index==0:
                        self.tiles[y,x]=tile("assets/picture/white_grid.png",(orig_x+Board.offset_x+x*Board.grid_size,
                                                                                orig_y+Board.offset_y+y*Board.grid_size))
                    elif index==1:
                        self.tiles[y,x]=tile("assets/picture/brown_grid.png",(orig_x+Board.offset_x+x*Board.grid_size,
                                                                                orig_y+Board.offset_y+y*Board.grid_size))
    
    def draw_board(self,screen):
        self.img_board.draw(screen)
        for y in range(5):
            for x in range(5):
                self.tiles[y,x].draw(screen)

        center_x = self.grid_size * (self.board_size + 3.5)
        Background = (197, 209, 235)
        Text_color = (45, 45, 42)
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 40)
        text = font.render('Player ' + str(self.turn+1) +"s turn", True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x // 2, self.grid_size // 2)
        screen.blit(text, textRect)

    def draw(self,screen):
        self.draw_board(screen)
        self.players[0].draw_player_stats(screen,self)
        self.players[1].draw_player_stats(screen,self)
        self.draw_error_message(screen)
    
    def draw_error_message(self,screen):
        Background = (197, 209, 235)
        Text_color = (181, 49, 32)
        center_x = self.grid_size * (self.board_size + 3.5)
        font = pygame.font.Font('assets/fonts/Oswald-VariableFont_wght.ttf', 20)
        text = font.render(self.error_message, True, Text_color, Background)
        textRect = text.get_rect()
        textRect.center = (center_x // 2, self.grid_size - 10)
        screen.blit(text, textRect)

    def hasSelected(self):
        return (self.picked_up_stack.height() > 0)
    
    def changeTurn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
        self.round +=1

    def getStack(self, x, y):
        return self.tiles[x][y].stack
    
    def emptyTile(self,x,y):
        self.tiles[x][y].empty()

    def placeStone(self, x, y, upright_input):
        if self.isMove:
            return False
        player_index = self.turn
        if self.round < 2:
            player_index = (self.turn+1)%2
        if self.getStack(x,y).is_stackable():
            self.getStack(x,y).push_stone(player_index, upright_input) 
            self.changeTurn()
            self.players[player_index].useStone()
            self.error_message = ""
            return True
        else:
            self.error_message = "Invalid tile to place stone"
            return False

    def checkLeft(self, x, y):
        if (x != 0 and self.getStack(x-1,y).stackable):
            return True
        else:
            return False
            
    def checkRight(self, x, y):
        if ( x != 4 and self.getStack(x+1,y).stackable):
            return True
        else:
            return False

    def checkDown(self, x, y):
        if (y != 0 and self.getStack(x, y-1).stackable):
            return True
        else:
            return False

    def checkUp(self, x, y):
        if (y != 4 and self.getStack(x,y+1).stackable):
            return True
        else:
            return False


    # def enoughStones(tileStack):
    #     if (stack.Stack.height(tileStack) >= 2):  # Stack Group have written this!
    #         return True
    #     else:
    #         return False
        

    def isValidMove(self, xFrom, xTo, yFrom, yTo):
        if (self.getStack(yFrom, yTo).stackable):
            if (xFrom > xTo):
                if (self.checkLeft(xFrom, yFrom)):
                     return True
            else:
                if (self.checkRight(xFrom, yFrom)):
                     return True
            if (yFrom > yTo):
                if (self.checkDown(xFrom, yFrom)):
                     return True
            else:
                if (self.checkUp(xFrom, yFrom)):
                     return True

    def pickUpStack(self, x, y):
        if self.getStack(x,y).height() >= 1 and self.getStack(x,y).check_top_stone(self.turn):
            self.players[self.turn].pickUpStack(self.getStack(x,y))
            #reset tile
            self.emptyTile(x,y)
            self.current_x = self.initial_x = x
            self.current_y = self.initial_y = y
            self.isMove = True
            self.direction = "none"
            self.error_message = ""
            return True
        else:
            self.error_message = "Cannot pick up stack"
            return False
        
 

    def moveStack(self, xTo, yTo):
        print("move")
        if (self.isValidMove(self.current_x, self.current_y, xTo, yTo)):
            if (self.direction == "none"): #If first move direction has to be set
                if (self.current_x > xTo and self.current_y == yTo):
                    self.direction = "left"
                elif (self.current_x < xTo and self.current_y == yTo):
                    self.direction = "right"
                elif (self.current_y > yTo and self.current_x == xTo):
                    self.direction = "down"
                elif (self.current_y < yTo and self.current_x == xTo):
                    self.direction = "up"
            if self.current_x == xTo and self.current_y == yTo:  # Allows player to place multiple stones without moving
                self.players[self.turn].picked_up_stack.drop_stone(self.getStack(xTo, yTo))
            elif self.direction == "up" and self.current_y < yTo and self.current_x == xTo or \
            self.direction == "down" and self.current_y > yTo and self.current_x == xTo or \
            self.direction == "left" and self.current_x > xTo and self.current_y == yTo or \
            self.direction == "right" and self.current_x < xTo and self.current_y == yTo:
                self.players[self.turn].picked_up_stack.drop_stone(self.getStack(xTo, yTo))

            # Update position based on direction
                if self.direction in ["up", "down"]:
                    self.current_y = yTo
                elif self.direction in ["left", "right"]:
                    self.current_x = xTo
            else:
                self.error_message = "Have to move in one direction"
                return False
            
            if self.players[self.turn].picked_up_stack.height() == 0:
                self.players[self.turn].picked_up_stack = None
                self.changeTurn()
                self.isMove = False
            self.error_message = ""
            return True
        else:
            self.error_message = "Cannot move this stack"
            return False
    

    def resetMove(self):
       
        if(self.isMove and self.current_x == self.initial_x and self.current_y == self.initial_y):
            self.isMove = False
            self.tiles[self.current_x, self.current_y].set_stack(self.players[self.turn].picked_up_stack)
            self.players[self.turn].picked_up_stack = None

    

    def find_winner(self):
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(x, y, first_player_index, first_upright):
            
            if not (0 <= x < 5 and 0 <= y < 5):
                return False
            if (x, y) in visited:
                return False

            stack = self.getStack(x, y)
            if stack.height() == 0:
                return False

            top_stone = stack.stack_content[-1]
            
            if top_stone.player_index != first_player_index or top_stone.upright != first_upright:
                return False
            
            visited.add((x, y))

            if y == self.board_size - 1 or x == self.board_size - 1:
                print(f"Path found for player {first_player_index} from ({x}, {y})!")
                return True

            #continue dfs
            for dx, dy in directions:
                next_x = x + dx
                next_y = y + dy
                if dfs(next_x, next_y, first_player_index, first_upright):
                    return True

            visited.remove((x, y))
            return False

        
        for player_index in [0, 1]:
            for i in range(self.board_size):
                print(f"Checking player {player_index}'s path from left side and top side...")
                first_stack_left = self.getStack(i, 0)
                if first_stack_left.height() > 0:
                    first_stone_left = first_stack_left.stack_content[-1]
                    if dfs(i, 0, first_stone_left.player_index, first_stone_left.upright):
                        print(f"Player {player_index} wins!")
                        return player_index

                first_stack_top = self.getStack(0, i)
                if first_stack_top.height() > 0:
                    first_stone_top = first_stack_top.stack_content[-1]
                    if dfs(0, i, first_stone_top.player_index, first_stone_top.upright):
                        print(f"Player {player_index} wins!")
                        return player_index

        print("No path found for any player.")
        return None
    

    ###############################################################################
    #                             AI UTILITY FUNCTIONS                            #
    ###############################################################################

    # Returns a list of all the valid moves for a player
    # Example of output : [['move', (1,3), 2, [2,1,1]], ['place', (0, 1), 1]...]
    def get_valid_moves(self, player):
        valid_moves = []
        if player == 0:
            pieces_left = self.players[0][1] #TODO does it update?
        else:
            pieces_left = self.players[1][1]

        for row in range(0, 5): #TODO hard coded 5
            for col in range(0, 5): #TODO hard coded 5
                # if a stack is empty, player can place a stone
                if self.emptyTile(row, col) and pieces_left > 0:
                    valid_moves.append(["place", (row, col), 0])
                    valid_moves.append(["place", (row, col), 1])
                # If the player owns the stack, calculate stack moves
                elif not self.emptyTile(row, col):
                    if self.getStack(row, col).check_top_stone(player):
                        height = self.getStack(row, col).height()
                        travel_paths = self.check_travel_paths(height, row, col)
                        if height > 1:
                            # For each direction and max distance, calculate stone combinations
                            for direction, max_distance in travel_paths:
                                for stones_left_behind in self.generate_stone_combinations(height - 1, max_distance, allow_zero_at_first_step=True): #TODO maybe not "height - 1"
                                    valid_moves.append(["move", (row, col), direction, stones_left_behind])

                        else:
                            for direction, _ in travel_paths:
                                valid_moves.append(["move", (row, col), direction, [0, 1]])

                    if self.getStack(row, col).is_stackable() and pieces_left > 0:
                        valid_moves.append(["place", (row, col), 0])
                        valid_moves.append(["place", (row, col), 1])
                
        if not valid_moves:
            # TODO : end of the game - merge winning conditions ?
            print("No valid moves")

        return valid_moves
    
    def check_travel_paths(self, height, row, col):    
    # Checks how far a stack can travel in each direction and returns a list of tuples
    # where each tuple contains the direction and the maximum distance that can be traveled
    # in that direction.
    
    # Returns:
    #     List of tuples: [(direction, max_distance), ...]
    #     Directions: 0 = down, 1 = up, 2 = left, 3 = right
    
        def get_max_distance_in_direction(row_step, col_step):
            curr_row, curr_col = row + row_step, col + col_step
            remaining_height = height # Since we start with the initial stack
            max_distance = 0

            # Loop to find how far the stack can move in this direction
            while remaining_height > 0 and 0 <= curr_row < 5 and 0 <= curr_col < 5: #TODO hard coded 5 :/
                stackable = self.getStack(curr_row, curr_col).stackable()
                if not stackable:
                    break  # Obstacle encountered, stop moving further in this direction
                max_distance += 1
                curr_row += row_step
                curr_col += col_step
                remaining_height -= 1

            return max_distance

        # Directions: (row_step, col_step) for down, up, left, right
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        travel_paths = []
        for index, (row_step, col_step) in enumerate(directions):
            # for each direction, get the max distance the stack can travel
            distance = get_max_distance_in_direction(row_step, col_step)
            if distance != 0:
                travel_paths.append((index, distance))

        return travel_paths
    
    def generate_stone_combinations(self, stones_to_distribute, max_distance, allow_zero_at_first_step=True):
        """
        Generate all valid combinations of how to distribute stones over a given maximum distance.
        Example: If there are 2 stones and you can move 3 steps, you can leave [1, 1], [0, 1, 1], [0, 2] or [2] stones behind.
        """
        combinations = []

        # Base case: If only one stone, it can only be left behind in one place
        if stones_to_distribute == 1:
            return [[1]]

        start_range = 0 if allow_zero_at_first_step else 1

        # Generate combinations based on the available distance
        for i in range(start_range, stones_to_distribute + 1):
            if max_distance > 1:
                remaining = stones_to_distribute - i
                if remaining > 0:
                    for rest in self.generate_stone_combinations(remaining, max_distance - 1, allow_zero_at_first_step=False):
                        combinations.append([i] + rest)
                else:
                    combinations.append([i])
            else:
                combinations.append([stones_to_distribute])  # If only one step allowed, leave all stones here

        return combinations
    
    def evaluate(self):
        score = 0
    
        if self.find_winner() == 1: # AI wins
            return float('inf') # Best case for AI
        elif self.find_winner() == 0: # Player wins
            return float('-inf') # Worst case for AI

        score += self.evaluate_control(1) - self.evaluate_control(0) # AI controlled stacks - Player controlled stacks
        score += self.evaluate_blocking(1) - self.evaluate_blocking(0)  # AI blocking - Player blocking
        score += self.evaluate_mobility(1) - self.evaluate_mobility(0)  # AI mobility - Player mobility
        score += self.evaluate_proximity_to_win(1) - self.evaluate_proximity_to_win(0)  # AI proximity - Player proximity

        return score

    def evaluate_control(self, player):
        control_score = 0
        for row in range(5): #TODO hardcoded 5 :/
            for col in range(5): #TODO hardcoded 5 :/
                stack = self.getStack(row, col)
                if stack.check_top_stone(player) and stack.is_stackable():
                    control_score += 10
        return control_score
    
    def evaluate_blocking(self, player):
        block_score = 0
        opponent = 1 - player

        for row in range(5): #TODO Hardcoded 5 :/
            for col in range(5):  #TODO Hardcoded 5 :/
                stack = self.getStack(row, col)
                if stack.check_top_stone(player) and stack.is_stackable():
                    # Count how many opponent stones are adjacent that this blocks
                    if row > 0 and self.getStack(row - 1, col).check_top_stone(opponent):
                        block_score += 5  # Example block score
                    if row < 5 - 1 and self.getStack(row + 1, col).check_top_stone(opponent):
                        block_score += 5
                    if col > 0 and self.getStack(row, col - 1).check_top_stone(opponent):
                        block_score += 5
                    if col < 5 - 1 and self.getStack(row + 1, col).check_top_stone(opponent):
                        block_score += 5
        return block_score

    def evaluate_mobility(self, player):
        valid_moves = self.get_valid_moves(player)
        return len(valid_moves) * 2
    
    def evaluate_proximity_to_win(self, player):
        prox_score = 0
        top_stones = []
        for row in range(5): #TODO Hardcoded 5
            for col in range(5): #TODO 5
                stack = self.getStack(row, col)
                if stack.check_top_stone(player) and stack.is_stackable():
                    top_stones.append((row, col))
        for row in range(5):
            rowx = []
            rowx = [x for x in top_stones if x[0]==row]
            if row+1 < 5 and len(rowx)!= 0:
                rowx += [x for x in top_stones if x[0] == row+1 and x[1] not in {x[1] for x in rowx}]
            prox_score += len(rowx)**2

        for col in range(5):
            colx = []
            colx = [x for x in top_stones if x[1]==col]
            if col+1 < 5 and len(colx)!= 0:
                colx += [x for x in top_stones if x[1] == col+1 and x[0] not in {x[0] for x in colx}]
            prox_score += len(colx)**2
        
        return prox_score
    
    # checks if there is a stalemate, returns False if there are possible moves for a player, and else returns true
    def is_stalemate(self, player):
        possible_moves = self.get_valid_moves(player)

        if len(possible_moves) > 0:
            return False
        return True