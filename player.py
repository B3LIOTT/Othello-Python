from plateau import Plateau
from settings import *

class Player:

    def __init__(self, type:int):
        self.type = type

    
    def add_pion(self):
        print("Joueur: ", self.type)
        x = int(input("x: "))
        y = int(input("y: "))

        return x, y