
import numpy as np

DEBUG=False
ANALYSE=True              # ANALYSE_* = True passe automatiquement DISPLAY à False pour éviter les problèmes de performance
ANALYSE_EACH_PLAY=True     # Uniquement pour le joueur 1
NB_ITERATIONS=1000
DISPLAY=True

# GAME
SIZE = 8
SLEEP_TIME = 0
ALGS = [0, 0]              # 0: random, 1: negamax, 2: nega_alpha_beta
STRATS = [0, 0]            # 0: positionnel, 1: absolu, 2: mobilité, 3: mixte
GAME_TYPE = 0              # 1: joueur vs joueur, 2: IA vs joueur, 3: joueur vs IA, IA vs IA sinon
MAX_INT = np.iinfo(np.int16).max

# IA
MAX_DEPTH = 4
MAX_ITER = 100
C = 2
H1 = np.array(
    [
        [500, -150, 30, 10, 10, 30, -150, 500],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [30, 0, 1, 2, 2, 1, 0, 30],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [30, 0, 1, 2, 2, 1, 0, 30],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [500, -150, 30, 10, 10, 30, -150, 500]
    ]
)

H2 = np.array(
    [
        [100, -20, 10, 5, 5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [-20, -50, -2, 2, -2, -2, -50, -20],
        [100, -20, 10, 5, 5, 10, -20, 100]
    ]
)

H = [H1, H1]

def heuristic(board: np.ndarray, type: int):
    """
    Calcule la valeur heuristique du plateau

    :param board: plateau
    :param type: type de pion

    :return: valeur heuristique
    """
    return np.sum(H[type-1][np.where(board == 2)]) if type == 2 else np.sum(H[type-1][np.where(board == 1)])


# UI
bg_color = (53, 132, 186)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
valid_move_color_black = (0, 0, 255)
valid_move_color_white = (0, 255, 0)
adjacent_color = (0, 255, 0)
cell_size = 100