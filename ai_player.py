from board import Board
from settings import *
import random


class AIPlayer:

    def __init__(self, type:int):
        self.type = type
    

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


    def random_play(self, pm: list):
        """
        Joue un coup aléatoire
        """ 
        rand_ind = random.randint(0, len(pm)-1)       
        rand_pm = pm[rand_ind]

        return rand_pm[0], rand_pm[1], rand_ind

    def minimax(self):
        raise NotImplementedError

    def alpha_beta(self):
        raise NotImplementedError