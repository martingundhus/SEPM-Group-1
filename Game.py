class Game:
    def __init__(self, board):
        self.board = board

    def isValidMove(self, board, xFrom, xTo, yFrom, yTo):
            if (xFrom > xTo):
                checkLeft(board, xFrom, xTo, yFrom, yTo)
            else:
                checkRight(board, xFrom, xTo, yFrom, yTo)
            if (yFrom > yTo):
                checkDown(board, xFrom, xTo, yFrom, yTo)
            else:
                checkUp(board, xFrom, xTo, yFrom, yTo)