class Game:
    def __init__(self, board):
        self.board = board

    def isValidMove(board, xFrom, xTo, yFrom, yTo):
            if (xFrom > xTo):
                if (checkLeft(board, xFrom, xTo, yFrom, yTo)):
                     return True
            else:
                if (checkRight(board, xFrom, xTo, yFrom, yTo)):
                     return True
            if (yFrom > yTo):
                if (checkDown(board, xFrom, xTo, yFrom, yTo)):
                     return True
            else:
                if (checkUp(board, xFrom, xTo, yFrom, yTo)):
                     return True
