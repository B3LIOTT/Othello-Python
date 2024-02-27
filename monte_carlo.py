from board import Board
from constants import C, MAX_INT, MAX_ITER, is_win, other_type
import random
import numpy as np


def rollout(board: Board, type: int, move: tuple):
    """
    :param board: plateau
    :param type: type de pion
    :return: True si le joueur a gagné, False sinon
    """
    type_bis = type
    copy_board = board.copy()
    copy_board.update_state(move, type_bis)

    while True:
        possible_moves = copy_board.possible_moves(type_bis)
        if len(possible_moves) != 0:
            move = random.choice(possible_moves)
            copy_board.update_state(move, type_bis)
            type_bis = other_type(type_bis)

        else:
            return is_win(copy_board.game_array, type)


def expand(board: Board, move: tuple, values: list, ind: int, type: int):
    """
    :param board: plateau
    :param pm: liste des coups possibles
    :param values: liste des valeurs UCB1
    :param ind: indice du coup
    :param type: type de pion
    :return: None
    """
    copy_board = board.copy()
    copy_board.update_state(move, type)
    possible_moves = copy_board.possible_moves(type)
    l = len(possible_moves)
    for _ in range(l):  # ajout des nouveaux coups pour le noeud ind
        values.append((0, 0, MAX_INT, ind)) 
    
    return values


def contains_unvisited(values: list, offset: int):
    """
    :param offset: valeur offset à partir de laquelle on commence à chercher, pour éviter de chercher des coups déjà visités
    :param values: liste des valeurs UCB1
    :return: indice du coup non visité "le plus proche" (c'est à dire le premier que l'on trouve), -1 sinon
    """
    for i in range(offset, len(values)):
        if values[i][1] == 0:
            return i
    
    return -1


def UCB1(wi, ni: int, N: int):
    """
    :param wi: somme des récompenses
    :param ni: nombre de simulations pour le coup i
    :param N: nombre total de simulations
    :return: valeur UCB1
    """
    if ni == 0:
        return MAX_INT
    
    return  wi / ni + C * np.sqrt(np.log(N) / ni)


def max_UCB1(values: list):
    """
    :param values: liste des valeurs UCB1
    :return: indice du coup avec la plus grande valeur UCB1
    """
    max = values[0]
    max_index = 0
    for i in range(len(values)):
        if values[1] > max:
            max = values[1]
            max_index = i
    
    return max_index


def monte_carlo(board: Board, pm: list, type: int):
    """
    Joue un coup en utilisant l'algorithme de Monte Carlo

    :param board: plateau de jeu
    :param pm: liste des coups possibles
    :param type: type de pion

    :return: coordonnées du coup
    """
    possible_moves = [pm]
    l = len(pm)
    values = [(0, 0, -1, -1)] + [(0, 0, MAX_INT, 0)] * l  # (ti, ni, ucb1, parent) avec ti = total, ni = nombre de visites, ucb1 = valeur ucb1, parent = indice du parent
    offset = 0
    for _ in range(MAX_ITER):  # on part de la racine                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        if (uv_ind:=contains_unvisited(values[1:], offset)) != -1:  # si il existe au moins un coup non visité, on rollout le premier trouvé (root exclus)
            move = (pm[uv_ind][0], pm[uv_ind][1])
            r = rollout(board, type, move)

            # mise à jour des valeurs du noeud visité
            values[uv_ind][0] += r  # mise à jour des valeurs1
            values[uv_ind][1] += 1

            # backpropagation
            node = values[uv_ind]
            while (parent:=node[3] != -1):                
                values[parent][0] += r  # mise à jour des valeurs du parent
                values[parent][1] += 1
                node = values[parent]
            
            offset = uv_ind + 1 

        else:  # si tous les coups ont été visités au moins une fois
            for j in range(len(values)):  # on calcule les valeurs UCB1 pour tous les noeuds
                values[j][2] = UCB1(values[j][0], values[j][1], values[0][1])

            ind = max_UCB1(values[1:l+1])  # meilleur coup depuis la racine

            move = (pm[ind][0], pm[ind][1])
            values = expand(board, move, values, ind, type)

    
    best_move_ind = max_UCB1(values[1:l+1])  # meilleur coup depuis la racine
    return pm[best_move_ind]
