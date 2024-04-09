from board import Board
from constants import *
import random
import numpy as np
import math as m
from monte_carlo import MonteCarlo


class AIPlayer:

    def __init__(self, type:int):
        self.type = type
        self.nb_plays = 0
        self.explored_states = []  # liste des états explorés



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
        
        elif alg_type == 3:
            return self.monte_carlo(board, pm, self.type)
        
        else:
            raise ValueError("[!] Invalid algorithm type")
    

    def mixed_strat(self, board: Board, this_pm: list, other_pm: list, type: int):
        """
        :return: valeur heuristique du plateau selon la stratégie mixte
        """
        if self.nb_plays < 8:
            return [heuristic(board.game_array, type)]
        
        if self.nb_plays < 23:
            return [np.sum(board.game_array == type) - np.sum(board.game_array == other_type(type))]
        
        if this_pm is not None:
            return [len(this_pm) - len(other_pm)]
        else:
            return [len(board.possible_moves(type)) - len(other_pm)]
    
    
    def strat(self, board: Board, this_pm: list, other_pm: list, type: int):
        if STRATS[type-1] == 0:
            return [heuristic(board.game_array, type)]
        
        elif STRATS[type-1] == 1:
                return [np.sum(board.game_array == type) - np.sum(board.game_array == other_type(type))]
        
        elif STRATS[type-1] == 2:
            if this_pm is not None:
                return [len(this_pm) - len(other_pm)]
            else:
                return [len(board.possible_moves(type)) - len(other_pm)]
        
        elif STRATS[type-1] == 3:
            return self.mixed_strat(board, this_pm, other_pm, type)
        
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
        self.nb_plays += 1
 
        if depth == MAX_DEPTH[type-1] or len(board.adjacents) == 0:
            return self.strat(board, None, pm, type)

        if depth != 0:
            moves = board.possible_moves(type)
        else:
            moves = pm

        if len(moves) == 0:
            return self.strat(board, moves, pm, type)
        
        best = -MAX_INT
        best_moves = []
        score = 0

        if AVOID_DUPLICATES:
            if depth != 0 and moves in self.explored_states:
                return [-MAX_INT]
            
            self.explored_states.append(moves)

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
        self.nb_plays += 1
 
        if depth == MAX_DEPTH[type-1] or len(board.adjacents) == 0:
            return self.strat(board, None, pm, type)

        if depth != 0:
            moves = board.possible_moves(type)
        else:
            moves = pm

        if len(moves) == 0:
            return self.strat(board, moves, pm, type)


        # if AVOID_DUPLICATES:
        #     if depth != 0 and self.already_visited(moves):
        #         return [-MAX_INT]
            
        #     self.explored_states.append(moves)

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
        MC = MonteCarlo(board=board, pm=pm, type=type)
        return MC.monte_carlo()
