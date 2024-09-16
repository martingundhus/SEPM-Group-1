class Stone:
    #Default is flat stone
    #Player is the ID for player, used to get color of stone here
    def __init__(self, player):
        self.player = player
        self.upright = False

    def set_upright(self):
        # sets stone upright
        self.upright = True

    

