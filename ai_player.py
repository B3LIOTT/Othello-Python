from board import Board
from settings import *
import random
import numpy as np
import math as m


class AIPlayer:

    def __init__(self, type:int):
        self.type = type
    

    def play(self, board: Board, alg_type:int, pm: list):
        """
        Joue un coup en fonction de l'algorithme choisi

        :param alg_type: type d'algorithme

        :return: coordonnées du coup
        """
        if alg_type == 0:
            return self.random_play(pm)
        elif alg_type == 1:
            copy = board.copy()
            nm = self.negamax(copy, 0)
            return nm[1][0], nm[1][1]
        elif alg_type == 2:
            return self.alpha_beta()
        else:
            raise ValueError("[!] Invalid algorithm type")


    def random_play(self, pm: list):
        """
        Joue un coup aléatoire
        """ 
        rand_ind = random.randint(0, len(pm)-1)       
        rand_pm = pm[rand_ind]

        return rand_pm

    def minimax(self):
        raise NotImplementedError
    
    def negamax(self, board: Board, depth: int):
        """
        Joue un coup en utilisant l'algorithme negamax

        :param board: plateau de jeu
        """

        if depth == MAX_DEPTH or len(board.adjacents) == 0:
            return [heuristic(board.game_array, self.type)]
        
        moves = board.possible_moves(self.type)

        if len(moves) == 0:
            return [heuristic(board.game_array, self.type)]
        
        best = -m.inf
        best_move = None
        for move in moves:
            board_copy = board.copy()
            board.update_state(move, self.type, move[0], move[1]) 
            score = -self.negamax(board_copy, depth+1)[0]

            if score == best and random.choice([True, False]):  
                best_move = move

            if score > best:
                best = score
                best_move = move
        
        return best, best_move
        

    def alpha_beta(self):
        raise NotImplementedError
    

    def other_type(self, type:int):
        """
        Retourne le conjugué du type de pion
        """
        if type == 1:
            return 2
        else:
            return 1