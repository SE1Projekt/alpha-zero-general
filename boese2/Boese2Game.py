import sys
sys.path.append('..')
from Game import Game
from .Boese2Logic import Board
import numpy as np

class Boese2Game(Game):

    def __init__(self, n):
        self.n = n
        self.move = 1
        self.result = 0
    
    def getInitBoard(self):
        self.move = 1
        self.result = 0
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (19, 19)
    
    def getActionSize(self):
        # return number of actions
        return 361 # 19*19
    
    def getNextState(self, board, player, action):
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/19), action%19)
        self.result = b.execute_move(move, player)
        self.move += 1
        if self.move == 3:
            b.seccond_move(-player)
            self.move += 1
            return (b.pieces, player)
        return (b.pieces, -player)
    
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
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
        if self.result*self.result == 1:
            print("Moves played: " + str(self.move))
            return player*self.result
        return self.result
    
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
                rotB = np.copy(board)
                rotB[:self.n,:self.n] = np.rot90(board[:self.n,:self.n], i)
                rotPi = np.copy(pi_board)
                rotPi[:self.n,:self.n] = np.rot90(pi_board[:self.n,:self.n], i)

                flipB = np.copy(rotB)
                flipB[:self.n,:self.n] = np.fliplr(rotB[:self.n,:self.n])
                flipPi = np.copy(rotPi)
                flipPi[:self.n,:self.n] = np.fliplr(rotPi[:self.n,:self.n])

                l += [(rotB, list(rotPi.ravel()))]
                l += [(flipB, list(flipPi.ravel()))]
        return l
    
    def stringRepresentation(self, board):
        return board.tostring()