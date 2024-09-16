from collections import deque
import stone

class Stack:
    def __init__(self):
        self.stack_content = deque()
        self.stackable = True

    # returns amount of stones in stack (length of queue)
    def height(self):
        return len(self.stack_content)

    def check_top_stone(self, player):
        '''Checks if top stone belongs to player'''
        topstone = self.stack_content[-1]
        if topstone.player == player:
            return True
        return False

    # '''Checks if topstone is standing or flat'''
    # def check_push_stone(self,):
    #     topstone = self.stack_content[-1]
    #     if topstone.upright == False:
    #         return True
    #     return False

    '''Pushes a stone from a players hand on the stack in a flat or standing stance'''
    def push_stone(self, player, upright_input):
        new_stone = stone.Stone(player)
        if upright_input == True:
            new_stone.upright = True
            self.stackable = False
            self.stack_content.append(new_stone)
        else:
            self.stack_content.append(new_stone)

    '''Drops a stone from the stack to the next stack'''
    def drop_stone(self, next_stack):
        removed_stone = self.stack_content.popleft()
        if removed_stone.upright:
            next_stack.stackable = False
        next_stack.stack_content.append(removed_stone)
        return next_stack
