
# Black: -1
# White: 1
# Empty: 1/3
# Blocked -1/3
class Board():

    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n):
        self.n = n
        self.pieces = [[0 for x in range(19)] for y in range(19)]
    
    def get_legal_moves(self):
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 1/3:
                    newmove = (x,y)
                    moves.add(newmove)
        return list(moves)
    
    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 1/3:
                    return 0
        return 1e-4

    def eval(self, move):
        (x,y) = move
        color = color = self.pieces[x][y]
        for (xoff,yoff) in self.__directions[:4]:  
            for i in range(5):
                try:
                    if self.pieces[x - (4-i)*xoff][y - (4-i)*yoff] == color and self.pieces[x - (3-i)*xoff][y - (3-i)*yoff] == color and self.pieces[x - (2-i)*xoff][y - (2-i)*yoff] == color and self.pieces[x - (1-i)*xoff][y - (1-i)*yoff] == color and self.pieces[x - (0-i)*xoff][y - (0-i)*yoff] == color:
                        return True
                except:
                    continue

    def remove(self, move):
        (x,y) = move
        color = self.pieces[x][y]
        for (xoff,yoff) in self.__directions:
            x3 = x + 3*xoff
            y3 = y + 3*yoff
            if x3 < 0 or x3 > self.n or y3 < 0 or y3 > self.n or self.pieces[x3][y3] != color:
                continue
            if self.pieces[x + xoff][y + yoff] == -color and self.pieces[x + 2*xoff][y + 2*yoff] == -color:
                self.pieces[x + xoff][y + yoff] = 1/3
                self.pieces[x + 2*xoff][y + 2*yoff] = 1/3

    #White Won: 1
    #Black Won: -1
    #Draw: 1e-4
    #No Result: 0
    def execute_move(self, move, color):
        (x,y) = move
        self.pieces[x][y] = color

        if self.eval(move):
            return color
        self.remove(self,move)
        return self.has_legal_moves()
            