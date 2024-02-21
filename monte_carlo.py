from board import Board
from constants import C, MAX_INT, MAX_ITER, heuristic
import random
import numpy as np


def rollout(board: Board, type: int):
    while len(pm:=board.possible_moves(type)) != 0:
        move = random.choice(pm)
        board.update_state(move, type)

    return heuristic(board.game_array, type) # TODO: ajouter les strats


def UCB1(wi, N: int, ni: int):
    if ni == 0:
        return MAX_INT
    
    v = wi / ni
    return v + C * np.sqrt(np.log(N) / ni)


def max_UCB1(values: list):
    max = values[0]
    max_index = 0
    for i in range(len(values)):
        if values[1] > max:
            max = values[1]
            max_index = i
    
    return max_index


def monte_carlo(board: Board, pm: list, type: int, is_leaf: bool):
    """
    Joue un coup en utilisant l'algorithme de Monte Carlo

    :param board: plateau de jeu
    :param pm: liste des coups possibles
    :param type: type de pion

    :return: coordonnées du coup
    """
    l = len(pm)
    root = (0, 0)
    values = [(0, 0)] * l
    
    for k in range(l):
        if values[k][1] == 0:
            r = rollout(board, type, pm[k])
            values[k][0] += r
            values[k][1] += 1
            root[0] += r
            root[1] += 1

            continue

        UCB1

        

        


        