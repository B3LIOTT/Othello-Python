import numpy as np
from settings import *


class Board:
    """
    Plateau de jeu du jeu Othello, de taille x*y.
    0 = case vide
    1 = pion noir
    2 = pion blanc
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range_x = range(x)
        self.range_y = range(y)
        self.value_range = [0,1,2]
        self.game_array = np.zeros((x, y))

        if x%2!=0 and y%2!=0:
            raise ValueError("x et y doivent être pairs")

        self.game_array[x//2-1, y//2-1] = 2
        self.game_array[x//2, y//2] = 2
        self.game_array[x//2-1, y//2] = 1
        self.game_array[x//2, y//2-1] = 1

        self.adjacents = [
            (x//2-1,y//2-2), (x//2-2, y//2-1), (x//2-2,x//2-2),
            (x//2-1,y//2), (x//2-2, y//2+1), (x//2-2,y//2),
            (x//2,y//2-1), (x//2+1, y//2-2), (x//2,y//2-2),
            (x//2,y//2+1), (x//2+1, y//2), (x//2+1,y//2+1)
        ]
    


    def update_adjacents(self, x, y):
        """
        Met à jour les cases adjacentes à (x, y) après un coup
        """
        l = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
        self.adjacents.remove((x, y))
        for dx, dy in l:
            if self.game_array[dx, dy] == 0 and (x+dx, y+dy) not in self.adjacents and 0 <= x+dx < self.x and 0 <= y+dy < self.y:
                self.adjacents.append((x+dx, y+dy))

    def update_state(self, data, type, x, y):
        """
        Met à jour l'état du plateau
        """
        if DEBUG:
            print("[+] updating state")
        
        self.game_array[x, y] = type
        self.update_adjacents(x, y)
        
        for i in range(self.x):
            pm = data[2][i]

            if pm[0]:
                end_x, end_y = pm[3]
                current_x, current_y = pm[1]
                dx, dy = pm[2]

                while current_x != end_x or current_y != end_y:
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
            check = self.check_lines(x, y, type)
            successes = [check[i][0] for i in range(8)]
            if successes.__contains__(True):
                moves.append((x, y, check))

        return moves

    def check_lines(self, x:int, y:int, type:int):
        """
        Vérifie si placer un pion de type 'type' en (x, y) permet d'encadrer au moins un pion adverse
        dans la direction spécifiée. Retourne True si c'est le cas, False sinon.

        :param x: coordonnée x
        :param y: coordonnée y
        :param type: type de pion

        :return: liste des coups possibles avec leurs caractéristiques (comme la direction par exemple)
        """

        if (x, y) not in self.adjacents:
            return [[False, None, None, None]]*SIZE_X
    
        res_l = [[False, None, None, None]]*SIZE_X
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        for k in range(8):
            dx, dy = directions[k]

            current_x, current_y = x + dx, y + dy
            opposite = (-1, -1)

            while 0 <= current_x < self.x and 0 <= current_y < self.y:
                if self.game_array[current_x, current_y] == self.other_type(type):
                    opposite = (current_x, current_y)
                elif self.game_array[current_x, current_y] == type and opposite != (-1, -1):
                    res_l[k] = [True, opposite, (dx, dy), (current_x, current_y)]
                    break
                else:
                    break

                current_x += dx
                current_y += dy

        return res_l
    
    
    def other_type(self, type:int):
        """
        Retourne le conjugué du type de pion
        """
        if type == 1:
            return 2
        else:
            return 1
    

    def display_array(self):
        T = np.zeros((self.x, self.y))
        for x in self.range_x:
            for y in self.range_y:
                T[x, y] = self.game_array[x, y]
        
        print(T)
        print("---------------------")
        print("Adjacents: ", self.adjacents)
            
