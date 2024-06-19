class moves:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.pieces = ['king', 'rook']
        
        #maybe this can be a map ['king' : {the moves}, 'rook' : {the moves}]
        #yes you are right

        #the bor
    def possible_moves(self):
        