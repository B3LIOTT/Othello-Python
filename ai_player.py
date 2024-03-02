from board import Board
from constants import *
import random
import numpy as np
import math as m
from monte_carlo import MonteCarloAgent as MCAgent


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
            if MAX_DEPTH %2 != 0:
                raise ValueError("[!] MAX_DEPTH doit être pair")
            nm = self.negamax(board, 0, pm, self.type)
            return nm[1]
        elif alg_type == 2:
            if MAX_DEPTH %2 != 0:   
                raise ValueError("[!] MAX_DEPTH doit être pair")
            return self.nega_alpha_beta(board, 0, pm, -MAX_INT, MAX_INT, self.type)[1]
        else:
            raise ValueError("[!] Invalid algorithm type")
    

    def strat(self, board: Board, pm: list, type: int):
        if STRATS[type-1] == 0:
            return [heuristic(board, type)]
        
        elif STRATS[type-1] == 1:
                return [np.sum(board == type) - np.sum(board == other_type(type))]
        
        elif STRATS[type-1] == 2:
            return [len(pm) - len(board.possible_moves(other_type(type)))]
        
        elif STRATS[type-1] == 3:
            raise NotImplementedError
        else:
            raise ValueError("[!] Invalid strategy type")
        

    def random_play(self, pm: list):
        """
        Joue un coup aléatoire
        """ 
        rand_ind = random.randint(0, len(pm)-1)       
        rand_pm = pm[rand_ind]

        return rand_pm
    
    def nega_alpha_beta(self, board: Board, depth: int, pm: list, alpha: int, beta: int, type: int):
        """
        Joue un coup en utilisant l'algorithme negamax

        :param board: plateau de jeu
        """
        if depth == MAX_DEPTH or len(board.adjacents) == 0:
            return self.strat(board.game_array, pm, type)

        if depth != 0:
            moves = board.possible_moves(type)
        else:
            moves = pm

        if len(moves) == 0:
            return self.strat(board.game_array, pm, type)
        
        best = -MAX_INT
        best_moves = []
        score = 0
        for move in moves:
            board_copy = board.copy()
            board_copy.update_state(move, type) 
            score = -self.nega_alpha_beta(board_copy, depth+1, moves, -beta, -alpha, other_type(type))[0]

            if score == best:  
                best_moves.append(move)

            if score > best:
                best = score
                best_moves = [move]
                if best > alpha:
                    alpha = best
                    if alpha > beta:
                        break

        best_move = random.choice(best_moves)
        return best, best_move
        
        

    def negamax(self, board: Board, depth: int, pm: list, type: int):
        """
        Joue un coup en utilisant l'algorithme negamax

        :param board: plateau de jeu
        """
        if depth == MAX_DEPTH or len(board.adjacents) == 0:
            return self.strat(board.game_array, pm, type)

        if depth != 0:
            moves = board.possible_moves(type)
        else:
            moves = pm

        if len(moves) == 0:
            return self.strat(board.game_array, pm, type)

        best = -MAX_INT
        best_moves = []
        score = 0
        for move in moves:
            board_copy = board.copy()
            board_copy.update_state(move, type) 
            score = -self.negamax(board_copy, depth+1, moves, other_type(type))[0]

            if score == best:  
                best_moves.append(move)

            if score > best:
                best = score
                best_moves = [move]

        best_move = random.choice(best_moves)
        return best, best_move
    

    def monte_carlo(self, board: Board, pm: list, type: int):
        """
        Joue un coup en utilisant l'algorithme monte carlo
        """
        MCA = MCAgent(board=board, pm=pm, type=type)
        return MCA.monte_carlo()
    