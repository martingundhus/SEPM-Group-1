class Stone:
    #Default is flat stone
    #Player is the ID for player, used to get color of stone here
    def __init__(self, player_index):
        self.player_index = player_index
        self.upright = False
