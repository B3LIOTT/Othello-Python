
import numpy as np

DEBUG=False
ANALYSE=True
NB_ITERATIONS=1000
DISPLAY=False

# GAME
SIZE = 8
SLEEP_TIME = 0
ALG_TYPE = 0

# IA
MAX_DEPTH = 3
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

H = H1

def heuristic(board: np.ndarray, type: int):
    """
    Calcule la valeur heuristique du plateau

    :param board: plateau
    :param type: type de pion

    :return: valeur heuristique
    """
    return np.sum(H[np.where(board == 2)]) if type == 2 else np.sum(H[np.where(board == 1)])

# UI
bg_color = (53, 132, 186)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
valid_move_color_black = (0, 0, 255)
valid_move_color_white = (0, 255, 0)
adjacent_color = (0, 255, 0)
cell_size = 100