"""
OTHELLO GAME 
@Author: Eliott Georges 
"""
from settings import *
from board import Board
from player import Player
from ai_player import AIPlayer
from time import sleep
import cv2
import numpy as np
import time


def play(x: int, y: int, board: Board, move):
    """
    Joue un coup

    :param x: coordonnée x
    :param y: coordonnée y
    """
    board.update_state(move, Player.type, x, y) 

def is_possible(pm: list, x: int, y: int):
    """
    Vérifie si le coup est possible

    :param pm: liste des coups possibles
    :param x: coordonnée x
    :param y: coordonnée y

    :return: True si le coup est possible, False sinon et l'indice du coup dans la liste des coups possibles
    """
    for i in range(len(pm)):
            if (x, y) == (pm[i][0], pm[i][1]):
                return True, i
        
    return False, -1

# TODO: fix
def process_input(Player: Player, board: Board):
    """
    Traite l'entrée du joueur

    :param Player: joueur
    :param board: Plateau
    :param type: type de pion
    :param x: coordonnée x
    :param y: coordonnée y
    """
    pm = board.possible_moves(Player.type)  
    if len(pm) == 0:
        if DEBUG:
            print("[!] Aucun coup possible")

        CAN_MOVE[Player.type-1] = False
        return
    
    if DISPLAY:
        opencv_display(board, pm, Player.type, interactable = True)

def process_input_ai(AIPlayer: AIPlayer, board: Board):
    """
    Traite l'entrée de l'IA

    :param Player: joueur ia
    :param Board: Board
    """
    pm = board.possible_moves(AIPlayer.type)
    if len(pm) == 0:
        if DEBUG:
            print("[!] Aucun coup possible")
        CAN_MOVE[AIPlayer.type-1] = False
        return
    
    if DISPLAY:
        opencv_display(board, pm, AIPlayer.type, interactable = False)

    rand_move = AIPlayer.play(board, ALG_TYPE, pm)

    if DEBUG:
        print("[+] Coup IA: ", rand_move[0],  rand_move[1], AIPlayer.type)
        print("[+] Details: ", rand_move)
        
    board.update_state(rand_move, AIPlayer.type, rand_move[0], rand_move[1])

def game_loop(board: Board, Player1: Player | AIPlayer, Player2: Player | AIPlayer):
    """
    Boucle principale du jeu

    :param Board: Board
    :param Player1: joueur 1
    :param Player2: joueur 2
    :param game_type: type d'affrontement
    """
    global CAN_MOVE
    CAN_MOVE = [True, True]

    if ANALYSE:
        start_time = time.time()

    i = 0
    while CAN_MOVE[0] or CAN_MOVE[1]:
        CAN_MOVE[i%2] = True
        if DEBUG:
            print("Tour: ", i+1)

        if i%2 == 0:
            if type(Player1) == AIPlayer:
                process_input_ai(Player1, board)
                sleep(SLEEP_TIME)
            else:
                process_input(Player1, board)

        else:
            if type(Player2) == AIPlayer:
                process_input_ai(Player2, board)
                sleep(SLEEP_TIME)
            else:
                process_input(Player2, board)
        
        i += 1
    

    delta = time.time() - start_time
    return game_over(board, delta)

def start_game(type: int):
    """
    Démarre le jeu

    :param type: type de jeu (1: joueur vs joueur, 2: joueur vs IA, 3: IA vs IA)
    """
    board = Board()

    if type == 1:
        p1 = Player(1)
        p2 = Player(2)
    elif type == 2:
        p1 = AIPlayer(1)
        p2 = Player(2)
    elif type == 3:
        p1 = Player(1)
        p2 = AIPlayer(2)
    else:
        p1 = AIPlayer(1)
        p2 = AIPlayer(2)
    
    print("[+] Debug mode activated: ", DEBUG)
    print("[+] Analyse mode activated: ", ANALYSE)
    print("[+] Display mode activated: ", DISPLAY)

    return game_loop(board, p1, p2)

def game_over(board: Board, delta: float):
    """
    Affiche le vainqueur

    :param board: plateau
    """
    print("[+]---- Fin de la partie ---- ")
    nb_discs_p1 = np.sum(board.game_array == 1)
    nb_discs_p2 = np.sum(board.game_array == 2)

    print("[+] Score: ", nb_discs_p1, " - ", nb_discs_p2)

    black = 0
    white = 0
    if nb_discs_p1 > nb_discs_p2:
        print("[+] Les noirs gagnent")
        black = 1

    elif nb_discs_p1 < nb_discs_p2:
        print("[+] Les blancs gagnent")
        white = 1

    else:
        print("[+] Match nul")
    
    if ANALYSE:
        print("[+] Temps de jeu: ", delta, "s")
    
    return delta, black, white



# UI
def mouse_click_event(event, x, y, flags, params):
    raise NotImplementedError


def opencv_display(board: Board, possible_moves: list, type:int, interactable : bool = True) :

    img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    moves_x_y_only = [(move[0], move[1]) for move in list(moves)]
    
    # Set the background color
    img[:] = background
    # Change the background color for the adjacent cells
    if adj_cells is not None:
        for cell in adj_cells:
            cv2.rectangle(img, (cell[1]*100, cell[0]*100), (cell[1]*100+100, cell[0]*100+100), (0, 160, 0), -1)
    
    # Add pieces (circles)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 1:
                cv2.circle(img, (j*100+50, i*100+50), 40, (255, 255, 255), -1)
            elif board[i][j] == -1:
                cv2.circle(img, (j*100+50, i*100+50), 40, (0, 0, 0), -1)
    # Add possible moves in grey (circles)
    for move in moves_x_y_only:
        cv2.circle(img, (move[1]*100+50, move[0]*100+50), 40, (128, 128, 128), -1)
    # Add grid lines
    for i in range(0, size):
        cv2.line(img, (0, i*100), (height, i*100), (0, 0, 0), 1)
        cv2.line(img, (i*100, 0), (i*100, width), (0, 0, 0), 1)     
    
    cv2.imshow("Othello", img)
    key = cv2.waitKey(1) &  0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit()
        
    if display_only:
        if last_display:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return
    # Wait for the user to click on a cell
    x, y = cv2_setMouseCallback(size, img)
    while (x, y) not in moves_x_y_only:
        x, y = cv2_setMouseCallback(size, img)
    cv2.destroyAllWindows()
    for move in moves:
        if move[0] == x and move[1] == y:
            return move
    return None


if __name__ == '__main__':
    if ANALYSE:
        mean = 0
        black = 0
        white = 0
        for i in range(NB_ITERATIONS):
            res = start_game(0)
            mean += res[0]/NB_ITERATIONS
            black += res[1]/NB_ITERATIONS
            white += res[2]/NB_ITERATIONS
        
        print("-----------------------------")
        print("[+] Moyenne: ", mean, "s")
        print("[+] Victoires des noirs: ", round(black*100), "%")
        print("[+] Victoires des blancs: ", round(white*100), "%")
        print("[+] Matchs nuls: ", 100 - round(black*100) - round(white*100), "%")
        
    else:
        start_game(0)