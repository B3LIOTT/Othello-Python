import numpy as np
from constants import *
from pions import *
from bitwise_op import *

"""
---------------------------BIT VERSION--------------------------------
"""

class Board:
    """
    Plateau de jeu du jeu Othello, de taille x*y.
    0b00 = case vide
    0b01 = pion noir
    0b10 = pion blanc
    """
    def __init__(self):
        if SIZE%2 != 0:
            raise ValueError("Les dimensions du plateau doivent être pairs")

        self.range_size = range(SIZE)
        self.game_array = 0
        self.adjacents = []
        self.directions = []


    def SET_VAL(self, x: int, y: int, pion: PION):
        """
        Modifie la valeur de la case (x, y), ne marche que si la case est vide

        :param x: coordonnée x
        :param y: coordonnée y
        """
        self.game_array |= (pion.value << (x * SIZE + y) * 2)
    

    def GET_VAL(self, x: int, y: int):
        """
        Retourne la valeur de la case (x, y)

        :param x: coordonnée xs
        :param y: coordonnée y
        """
        return (self.game_array >> (x * SIZE + y) * 2) & 0b11
    
    def SWAP_PION(self, x: int, y: int):
        """
        Inverse la valeur de la case (x, y)

        :param x: coordonnée x
        :param y: coordonnée y
        """
        self.game_array ^= (0b11 << (x * SIZE + y) * 2)


    def init_board(self):
        self.SET_VAL(SIZE//2-1, SIZE//2-1, PION.WHITE)
        self.SET_VAL(SIZE//2, SIZE//2, PION.WHITE)
        self.SET_VAL(SIZE//2-1, SIZE//2, PION.BLACK)
        self.SET_VAL(SIZE//2, SIZE//2-1, PION.BLACK)

        self.adjacents = [
            (SIZE // 2 - 2, SIZE // 2 - 2),
            (SIZE // 2 - 2, SIZE // 2 - 1),
            (SIZE // 2 - 2, SIZE // 2),
            (SIZE // 2 - 2, SIZE // 2 + 1),
            (SIZE // 2 - 1, SIZE // 2 - 2),
            (SIZE // 2 - 1, SIZE // 2 + 1),
            (SIZE // 2, SIZE // 2 - 2),
            (SIZE // 2, SIZE // 2 + 1),
            (SIZE // 2 + 1, SIZE // 2 - 2),
            (SIZE // 2 + 1, SIZE // 2 - 1),
            (SIZE // 2 + 1, SIZE // 2),
            (SIZE // 2 + 1, SIZE // 2 + 1)
        ]

        self.directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]


    def update_adjacents(self, x: int, y: int):
        """
        Met à jour les cases adjacentes à (x, y) après un coup
        """

        self.adjacents.remove((x, y))
        for dx, dy in self.directions:
            if 0 <= x+dx < SIZE and 0 <= y+dy < SIZE:
                if self.GET_VAL(x+dx, y+dy) == PION.NONE.value and (x+dx, y+dy) not in self.adjacents:
                    self.adjacents.append((x+dx, y+dy))


    def update_state(self, move: list, pion: PION):
        """
        Met à jour l'état du plateau

        :param data: données du coup
        :param type: type de pion
        :param x: coordonnée x
        :param y: coordonnée y
        """
        if DEBUG:
            print("[+] updating state")
        

        x, y = move[0]
        self.SET_VAL(x, y, pion)
        self.update_adjacents(x, y)

        directions = move[1]
        
        if DEBUG:
            print("[+] Valid directions: ", directions)
        
        for dir in directions:
            dx, dy = dir[0]
            end_x, end_y = dir[1]
            current_x = x + dx
            current_y = y + dy

            while (current_x, current_y) != (end_x, end_y):
                self.SWAP_PION(current_x, current_y)
                current_x += dx
                current_y += dy


    def check_directions(self, x:int, y:int, pion: PION) -> list:
        """
        Vérifie si placer un pion de type 'type' en (x, y) permet d'encadrer au moins un pion adverse
        dans la direction spécifiée. Retourne True si c'est le cas, False sinon.

        :param x: coordonnée x
        :param y: coordonnée y
        :param pion: type de pion

        :return: liste des coups possibles avec leurs caractéristiques (comme la direction par exemple)
        """

        valid_directions = []

        for k in range(8):
            dx, dy = self.directions[k]
            current_x, current_y = x + dx, y + dy

            if not (0 <= current_x < SIZE and 0 <= current_y < SIZE) or self.GET_VAL(current_x, current_y) != pion.other_type().value:
                continue
            
            while 0 <= current_x < SIZE and 0 <= current_y < SIZE:
                if self.GET_VAL(current_x, current_y) == PION.NONE.value:
                    break
                if self.GET_VAL(current_x, current_y) == pion.value:
                    valid_directions.append([(dx, dy), (current_x, current_y)])
                    break
                
                current_x += dx
                current_y += dy

        return valid_directions
    
      
    def possible_moves(self, pion: PION) -> list:
        """
        Retourne l'ensemble des coups possibles pour un joueur

        :param type: type de pion
        """
        moves = []
        for adj in self.adjacents:
            x, y = adj
            valid_directions = self.check_directions(x, y, pion)
            if valid_directions != []:  
                moves.append([(x,y), dir])

        return moves
    

    def score(self):
        """
        :return: score noirs, score blancs
        """
        b_score = 0
        w_score = 0

        for i in range(0, pow(SIZE, 2)*2, 2):
            if (self.game_array >> i) & 0b11 == PION.BLACK.value:
                b_score += 1
            elif (self.game_array >> i) & 0b11 == PION.WHITE.value:
                w_score += 1

        return b_score, w_score
    

    def __str__(self):
        raise NotImplementedError

    
    def copy(self):
        """
        Retourne une copie du plateau
        """
        copy = Board()
        copy.game_array = self.game_array
        copy.adjacents = self.adjacents.copy()

        return copy
            
