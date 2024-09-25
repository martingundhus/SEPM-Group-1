from collections import deque
import stone

class Stack:
    def __init__(self):
        self.stack_content = list()  # Store stones in a list
        self.stackable = True
    
    def draw(self, screen, position=(0, 0)):
        if self.height() > 0:
            for i in range(self.height()):
                x, y = position
                self.stack_content[i].draw(screen, x, y - 15 * i)

    # Returns amount of stones in stack (length of stack)
    def height(self):
        return len(self.stack_content)

    def is_stackable(self):
        return self.stackable

    def check_top_stone(self, player_index):
        '''Checks if top stone belongs to player'''
        if self.height() > 0:  # Check if there are stones
            topstone = self.stack_content[-1]  # Get the top stone
            return topstone.player_index == player_index  # Check if it belongs to the player
        return False

    def push_stone(self, player_index, upright_input):
        '''Pushes a stone from a player's hand on the stack in a flat or standing stance'''
        new_stone = stone.Stone(player_index, upright_input)
        self.stack_content.append(new_stone)
        if upright_input:  # If the stone is upright, set stackable to False
            self.stackable = False

    def drop_stone(self, next_stack):
        removed_stone = self.stack_content.pop()  # Use pop() instead of popleft()
        if removed_stone.upright:
            next_stack.stackable = False
        next_stack.stack_content.append(removed_stone)
        return next_stack

    def top_player(self):
        '''Returns the player index of the top stone'''
        if self.height() > 0:
            return self.stack_content[-1].player_index  # Return the player index of the top stone
        return None  # Return None if there are no stones in the stack
