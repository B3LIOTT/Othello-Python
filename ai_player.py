from plateau import Plateau
from settings import *
import random


class AIPlayer:

    def __init__(self, type:int, plateau:Plateau):
        self.type = type
        self.plateau = plateau
    

    def add_pion(self, alg_type:int):
        """
        Joue un coup en fonction de l'algorithme choisi

        :param alg_type: type d'algorithme

        :return: coordonnées du coup
        """
        if alg_type == 0:
            return self.random_play()
        elif alg_type == 1:
            return self.minimax()
        elif alg_type == 2:
            return self.alpha_beta()
        else:
            raise ValueError("[!] Invalid algorithm type")


    def random_play(self):
        """
        Joue un coup aléatoire
        """
        pm = Plateau.possible_moves(self.plateau, self.type) 
        rand_ind = random.randint(0, len(pm)-1)       
        rand_pm = pm[rand_ind]

        return rand_pm[0], rand_pm[1], rand_ind

    def minimax(self):
        raise NotImplementedError

    def alpha_beta(self):
        raise NotImplementedError