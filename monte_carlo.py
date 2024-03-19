from board import Board
from constants import C, MAX_INT, MAX_ITER, MC_ROLLOUT_METHOD, is_win, other_type, H
import random
import numpy as np


class Node:
        
        def __init__(self, parent: int, move: list, type: int, board: Board):
            self.parent = parent  # indice du parent dans la liste des nodes
            self.move = move
            self.type = type
            self.children = []
            self.wins = 0
            self.visits = 0
            self.ucb1 = MAX_INT
            self.board = board

        def best_child(self, nodes: list):
            """
            :return: meilleur enfant selon le ratio victoires/visites
            """
            return max(self.children, key=lambda x: (nodes[x].wins/nodes[x].visits))
    

        def UCB1(self, N):
            """
            :return: valeur UCB1
            """
            if self.visits == 0:
                return MAX_INT
            
            self.ucb1 = self.wins / self.visits + C * np.sqrt(np.log(N) / self.visits)

        
        def __str__(self):
            return f"Node: parent: {self.parent}, move: {self.move}, type: {self.type}, children: {self.children}, wins: {self.wins}, visits: {self.visits}, ucb1: {self.ucb1}"

class MonteCarlo:

    def __init__(self, board: Board, pm: list, type: int):
        self.board = board 
        self.pm = pm
        self.type = type
        self.l = len(pm)

        root = Node(None, None, None, board)
        root.board = board
        self.nodes = [root] + [Node(0, m, type, None) for m in pm]

        self.offset = 1


    def custom_choice(self, pm: list, type: int):
        """
        :param l: liste
        :return: élément de la liste selon MC_ROLLOUT_METHOD
        """
        if MC_ROLLOUT_METHOD == 0:
            return random.choice(pm)

        elif MC_ROLLOUT_METHOD == 1:
            if type == self.type:
                return random.choice(pm)

            else:
                sh = 0
                for m in pm:
                    sh += H[type-1][m[0], m[1]]+500  # +500 pour rammener les valeurs dans l'intervalle [0, inf[
                
                probas = []
                p = 0
                for m in pm:
                    p += (H[type-1][m[0], m[1]]+500)/sh
                    probas.append(p)

                rand = random.uniform(0, 1)

                for i in range(len(probas)):
                    if rand < probas[i]:
                        return pm[i]
            
        else: # 
            if type == self.type:
                return random.choice(pm)

            else: # Choix du meilleur coup pour l'adversaire
                return max(enumerate(pm), key=lambda x: H[type-1][x[1][0], x[1][1]])[1]
        

    def rollout(self, ind: int):
        """
        :param board: plateau
        :return: True si le joueur a gagné, False sinon
        """
        current_node = self.nodes[ind]
        type_bis = current_node.type
        copy_board = self.nodes[current_node.parent].board.copy()  # récupération de la Board à l'état du noeud parents Si-1
        copy_board.update_state(current_node.move, type_bis)  # on joue le coup pour passer de Si-1 à Si

        while True:  # on "plonge" dans l'arbre aléatoirement
            possible_moves = copy_board.possible_moves(type_bis)
            if len(possible_moves) > 0:
                move = self.custom_choice(possible_moves, type_bis)
                copy_board.update_state(move, type_bis)
                type_bis = other_type(type_bis)

            else:
                return is_win(copy_board.game_array, self.type)


    def expand(self, ind: int):
        """
        :param ind: indice du coup
        """
        current_node = self.nodes[ind]
        copy_board =self.nodes[current_node.parent].board.copy()  # récuperation de la board de l'état Si-1 pour jouer le coup Si, pour pouvoir l'étendre
        copy_board.update_state(current_node.move, current_node.type)
        self.nodes[ind].board = copy_board
        possible_moves = copy_board.possible_moves(current_node.type)
        
        for m in possible_moves:  # ajout des nouveaux coups pour le noeud ind
            self.nodes.append(Node(ind, m, other_type(current_node.type), None))
            self.nodes[ind].children.append(len(self.nodes)-1)
           
        # # TODO: Comme on a étendu l'arbre, on peut supprimer la board du noeud étendu pour libérer de la mémoire


    def contains_unvisited(self):
        """
        :param offset: valeur offset à partir de laquelle on commence à chercher, pour éviter de chercher des coups déjà visités
        :return: indice du coup non visité "le plus proche" (c'est à dire le premier que l'on trouve), -1 sinon
        """
        for i in range(self.offset, len(self.nodes)):
            if self.nodes[i].visits == 0:   
                return i
        
        return None


    def max_UCB1(self):
        """
        :return: indice du coup avec la plus grande valeur UCB1
        """
        return max(enumerate(self.nodes[1:self.l+1]), key=lambda x: x[1].ucb1)[0]+1

    def path_to_best_leaf(self, ind: int):
        """
        :return: indice du noeud le plus bas dans l'arbre depuis le noeud d'indice ind
        """
        while len(self.nodes[ind].children) > 0:
            ind = self.nodes[ind].best_child(self.nodes)
        
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
                while (node.parent != None):                
                    self.nodes[node.parent].wins += r  # mise à jour des valeurs du parent
                    self.nodes[node.parent].visits += 1
                    node = self.nodes[node.parent]
                
                self.offset = uv_ind + 1 

            else:  # si tous les coups ont été visités au moins une fois
                for k in range(1, self.l+1):  # on calcule les valeurs UCB1 pour les coups possibles depuis la racine
                    self.nodes[k].UCB1(self.nodes[0].visits)

                ind = self.max_UCB1()  # meilleur coup depuis la racine

                node_to_expand = self.path_to_best_leaf(ind)
                self.expand(node_to_expand)

        
        best_move_ind = self.max_UCB1()
        # for i in range(1, self.l+1):
        #     print(f"Node {i}: {self.nodes[i]}")
        # print(f"Best move: {self.nodes[best_move_ind]}")
        return self.nodes[best_move_ind].move
