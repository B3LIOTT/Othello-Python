from board import Board
from constants import C, MAX_INT, MAX_ITER, is_win, other_type
import random
import numpy as np


class MonteCarloAgent:

    def __init__(self, board: Board, pm: list, type: int):
        self.board = board 
        self.pm = pm
        self.type = type
        self.boards = [board]
        self.l = len(pm)

        self.values = [(0, 0, None, None, None, None)] + [(0, 0, MAX_INT, 0, m, type) for m in pm]  # (ti, ni, ucb1, parent, coup, type) avec ti = total, ni = nombre de visites, ucb1 = valeur ucb1, parent = indice du parent, coup = coordonnées/paramètres du coup, type = type de pion
        del ot

        self.offset = 1



    def rollout(self, ind: int):
        """
        :param board: plateau
        :return: True si le joueur a gagné, False sinon
        """
        value = self.values[ind]
        type_bis = value[5]
        copy_board = self.boards[value[3]].copy()
        copy_board.update_state(value[4], type_bis)  # on joue le coup pour passer de Si-1 à Si

        while True:  # on "plonge" dans l'arbre aléatoirement
            possible_moves = copy_board.possible_moves(type_bis)
            if len(possible_moves) > 0:
                move = random.choice(possible_moves)  #TODO : utiliser l'heuristique pour choisir le meilleur coup
                copy_board.update_state(move, type_bis)
                type_bis = other_type(type_bis)

            else:
                return is_win(copy_board.game_array, type)


    def expand(self, ind: int, type: int):
        """
        :param ind: indice du coup
        """
        copy_board = self.boards[ind].copy()
        copy_board.update_state(move, type)
        possible_moves = copy_board.possible_moves(type)
        self.boards.append(copy_board)
        for m in possible_moves:  # ajout des nouveaux coups pour le noeud ind
            self.values.append((0, 0, MAX_INT, ind, m)) 


    def contains_unvisited(self, offset: int):
        """
        :param offset: valeur offset à partir de laquelle on commence à chercher, pour éviter de chercher des coups déjà visités
        :param values: liste des valeurs UCB1
        :return: indice du coup non visité "le plus proche" (c'est à dire le premier que l'on trouve), -1 sinon
        """
        for i in range(offset, len(self.values)):
            if self.values[i][1] == 0:
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


    def max_UCB1():
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


    def monte_carlo(self):
        """
        Joue un coup en utilisant l'algorithme de Monte Carlo

        :param board: plateau de jeu
        :param pm: liste des coups possibles
        :param type: type de pion

        :return: coordonnées du coup
        """
        
        for _ in range(MAX_ITER):  # on part de la racine                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            if (uv_ind:=self.contains_unvisited()) != -1:  # si il existe au moins un coup non visité, on rollout le premier trouvé (root exclus)
                r = self.rollout(uv_ind)

                # mise à jour des valeurs du noeud visité
                self.values[uv_ind][0] += r  # mise à jour des valeurs1
                self.values[uv_ind][1] += 1

                # backpropagation
                node = self.values[uv_ind]
                while (parent:=node[3] != -1):                
                    self.values[parent][0] += r  # mise à jour des valeurs du parent
                    self.values[parent][1] += 1
                    node = self.values[parent]
                
                self.offset = uv_ind + 1 

            else:  # si tous les coups ont été visités au moins une fois
                for j in range(1, self.l+1):  # on calcule les valeurs UCB1 pour les coups possibles depuis la racine
                    values[j][2] =self. UCB1(values[j][0], values[j][1], values[0][1])

                ind = self.max_UCB1(values[1:self.l+1])  # meilleur coup depuis la racine

                values = self.expand(ind)

        
        best_move_ind = self.max_UCB1(self.values[1:self.l+1])  # meilleur coup depuis la racine
        return self.values[best_move_ind][4]
