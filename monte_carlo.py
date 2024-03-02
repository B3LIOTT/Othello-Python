from board import Board
from constants import C, MAX_INT, MAX_ITER, is_win, other_type
import random
import numpy as np


class Node:
        
        def __init__(self, parent: int, move: list, type: int):
            self.parent = parent  # indice du parent dans la liste des nodes
            self.move = move
            self.type = type
            self.children = []
            self.wins = 0
            self.visits = 0
            self.ucb1 = MAX_INT
            self.board = None

        def best_child(self):
            """
            :return: meilleur enfant selon le ratio victoires/visites
            """
            max = self.children[0].wins / self.children[0].visits
            best = self.children[0]
            for child in self.children:
                if child.wins / child.visits > max:
                    max = child.wins / child.visits
                    best = child
            
            return best
    
        def UCB1(self):
            """
            :return: valeur UCB1
            """
            if self.visits == 0:
                return MAX_INT
            
            self.ucb1 = self.wins / self.visits + C * np.sqrt(np.log(self.parent.visits) / self.visits)

class MonteCarloAgent:

    def __init__(self, board: Board, pm: list, type: int):
        self.board = board 
        self.pm = pm
        self.type = type
        self.l = len(pm)

        root = Node(None, None, None)
        root.board = board
        self.nodes = [root] + [Node(0, m, type) for m in pm]

        self.offset = 1



    def rollout(self, ind: int):
        """
        :param board: plateau
        :return: True si le joueur a gagné, False sinon
        """
        current_node = self.nodes[ind]
        type_bis = current_node.type
        copy_board = current_node.parent.board.copy()  # récupération de la Board à l'état du noeud parents Si-1
        copy_board.update_state(current_node.move, type_bis)  # on joue le coup pour passer de Si-1 à Si

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
        current_node = self.nodes[ind]
        copy_board =self.nodes[current_node.parent].board.copy()  # récuperation de la board de l'état Si-1 pour jouer le coup Si, pour pouvoir l'étendre
        copy_board.update_state(current_node.move, type)
        possible_moves = copy_board.possible_moves(type)

        for m in possible_moves:  # ajout des nouveaux coups pour le noeud ind
            self.nodes.append(Node(ind, m, other_type(type)))
            self.nodes[ind].children.append(len(self.nodes)-1)
        
        # Comme on a étendu l'arbre, on peut supprimer la board du noeud étendu pour libérer de la mémoire
        self.nodes[current_node.parent].board = None


    def contains_unvisited(self, offset: int):
        """
        :param offset: valeur offset à partir de laquelle on commence à chercher, pour éviter de chercher des coups déjà visités
        :return: indice du coup non visité "le plus proche" (c'est à dire le premier que l'on trouve), -1 sinon
        """
        for i in range(offset, len(self.nodes)):
            if self.nodes[i].visits == 0:
                return i
        
        return None


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


    def max_UCB1(self):
        """
        :return: indice du coup avec la plus grande valeur UCB1
        """
        max = self.nodes[0].ucb1
        max_index = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].ucb1 > max:
                max = self.nodes[i].ucb1
                max_index = i
        
        return max_index

    def path_to_best_leaf(self, ind: int):
        """
        :return: indice du noeud le plus bas dans l'arbre depuis le noeud d'indice ind
        """
        while len(self.nodes[ind].children) > 0:
            ind = self.nodes[ind].best_child()
        
        return ind

    def monte_carlo(self):
        """
        Joue un coup en utilisant l'algorithme de Monte Carlo

        :return: coordonnées du meilleur coup d'après la recherche Monte Carlo
        """
        
        for _ in range(MAX_ITER):  # on part de la racine                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            if (uv_ind:=self.contains_unvisited()) != None:  # si il existe au moins un coup non visité, on rollout le premier trouvé (root exclus)
                r = self.rollout(uv_ind)

                # mise à jour des valeurs du noeud visité
                self.nodes[uv_ind].wins += r  # mise à jour des valeurs1
                self.nodes[uv_ind].visits += 1

                # backpropagation
                node = self.nodes[uv_ind]
                while (self.nodes[node.parent] != None):                
                    self.nodes[node.parent].wins += r  # mise à jour des valeurs du parent
                    self.nodes[node.parent].visits += 1
                    node = self.nodes[node.parent]
                
                self.offset = uv_ind + 1 

            else:  # si tous les coups ont été visités au moins une fois
                for k in range(1, self.l+1):  # on calcule les valeurs UCB1 pour les coups possibles depuis la racine
                    self.nodes[k].UCB1()

                ind = self.max_UCB1(self.nodes[1:self.l+1])  # meilleur coup depuis la racine

                node_to_expand = self.path_to_best_leaf(ind)

                self.expand(node_to_expand)

        
        best_move_ind = self.max_UCB1(self.values[1:self.l+1])  # meilleur coup depuis la racine
        return self.values[best_move_ind][4]
