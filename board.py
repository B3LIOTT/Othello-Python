import numpy as np
from constants import *


class Board:
    """
    Plateau de jeu du jeu Othello, de taille x*y.
    0 = case vide
    1 = pion noir
    2 = pion blanc
    """
    def __init__(self):
        self.range_size = range(SIZE)
        self.game_array = np.zeros((SIZE, SIZE))

        if SIZE%2 != 0:
            raise ValueError("Les dimensions du plateau doivent être pairs")

        self.game_array[SIZE//2-1, SIZE//2-1] = 2
        self.game_array[SIZE//2, SIZE//2] = 2
        self.game_array[SIZE//2-1, SIZE//2] = 1
        self.game_array[SIZE//2, SIZE//2-1] = 1

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
                if self.game_array[x+dx, y+dy] == 0 and (x+dx, y+dy) not in self.adjacents:
                    self.adjacents.append((x+dx, y+dy))

    def update_state(self, data: list, type: int):
        """
        Met à jour l'état du plateau

        :param data: données du coup
        :param type: type de pion
        :param x: coordonnée x
        :param y: coordonnée y
        """
        x, y = data[0], data[1]

        if DEBUG:
            print("[+] updating state")
        
        self.game_array[x, y] = type
        self.update_adjacents(x, y)
        
        for i in range(len(data[2])):
            pm = data[2][i]
            current_x = x
            current_y = y

            dx, dy = pm[0]
            end_x, end_y = pm[1]
            current_x += dx
            current_y += dy

            while (current_x, current_y) != (end_x, end_y):
                self.game_array[current_x, current_y] = type
                current_x += dx
                current_y += dy
  
    def possible_moves(self, type:int):
        """
        Retourne la liste des coups possibles pour un joueur

        :param type: type de pion
        """
        moves = []
        for adj in self.adjacents:
            x, y = adj
            check = self.check_directions(x, y, type)
            if check != []: 
                moves.append((x, y, check))

        return moves

    def check_directions(self, x:int, y:int, type:int):
        """
        Vérifie si placer un pion de type 'type' en (x, y) permet d'encadrer au moins un pion adverse
        dans la direction spécifiée. Retourne True si c'est le cas, False sinon.

        :param x: coordonnée x
        :param y: coordonnée y
        :param type: type de pion

        :return: liste des coups possibles avec leurs caractéristiques (comme la direction par exemple)
        """

        res_l = []
    
        for k in range(8):
            dx, dy = self.directions[k] 
            current_x, current_y = x + dx, y + dy

            if not (0 <= current_x < SIZE and 0 <= current_y < SIZE) or self.game_array[current_x, current_y] != other_type(type):
                continue
            
            while 0 <= current_x < SIZE and 0 <= current_y < SIZE:
                if self.game_array[current_x, current_y] == 0:
                    break
                if self.game_array[current_x, current_y] == type:
                    res_l.append([(dx, dy), (current_x, current_y)])
                    break
                
                current_x += dx
                current_y += dy

        return res_l
    

    def display_array(self):
        print(self.game_array)
        print("---------------------")
        print("Adjacents: ", self.adjacents)

    
    def copy(self):
        """
        Retourne une copie du plateau
        """
        copy = Board()
        copy.game_array = self.game_array.copy()
        copy.adjacents = self.adjacents.copy()

        return copy
            
