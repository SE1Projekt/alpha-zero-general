import sys
sys.path.append('..')
from Game import Game
from .Boese2Logic import Board
import numpy as np

class Boese2Game(Game):

    def __init__(self, n):
        self.n = n
        self.Es = {}
    
    def getInitBoard(self):
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)
    
    def getActionSize(self):
        # return number of actions
        return self.n*self.n
    
    def getNextState(self, board, player, action):
        b = Board(self.n, True)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        result = b.execute_move(move, player)
        self.Es[self.stringRepresentation(b.pieces)] = result
        # if self.move == 3:
        #     b.seccond_move(-player)
        #     self.move += 1
        #     return (b.pieces, player)
        return (b.pieces, -player)
    
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n, True)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves()
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)
    
    #White Won: 1
    #Black Won: -1
    #Draw: 1e-4
    #No Result: 0
    def getGameEnded(self, board, player):
        r = self.Es[self.stringRepresentation(board)]
        if r*r == 1:
            #print("Moves played: " + str(self.move))
            return player*r
        return r
    
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == 1:
            return board
        with np.nditer(board, op_flags=['readwrite']) as it:
            for x in it:
                if x*x == 1:
                    x[...] = -x
        return board
    
    def getSymmetries(self, board, pi):
        # mirror, rotational
        pi_board = np.reshape(pi, (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()))]
        return l
    
    def stringRepresentation(self, board):
        return board.tostring()