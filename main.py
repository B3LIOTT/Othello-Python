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
    
    if ANALYSE:
        delta = time.time() - start_time
    else:
        delta = None
    
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
def mouse_event_checker(img: np.ndarray):
    x = -1
    y = -1
    def mouse_callback(event, x_, y_, flags, param):
        cell_size, board, pm = param
        nonlocal x, y
        if event == cv2.EVENT_LBUTTONDOWN:
            y = x_//100
            x = y_//100
            play(x, y, board, pm[is_possible(pm, x, y)[1]])

    cv2.setMouseCallback("Othello", mouse_callback)

    while True:
        cv2.imshow("Othello", img)
        if x != -1 and y != -1:
            break
        cv2.waitKey(1)


def opencv_display(board: Board, possible_moves: list, type:int, interactable : bool = True):

    img = np.zeros((SIZE, SIZE, 3), dtype = np.uint8)

    for i in range(SIZE) :
        for j in range(SIZE) :
            if board.game_array[i, j] == 0 :
                img[i, j] = bg_color
            elif  board.game_array[i, j] == 1 :
                img[i, j] = black_color
            else :
                img[i, j] = white_color

    for i in range(len(possible_moves)):
        if type == 1:
            img[possible_moves[i][0], possible_moves[i][1]] = valid_move_color_black
        elif type == 2:
            img[possible_moves[i][0], possible_moves[i][1]] = valid_move_color_white
        else:
            raise ValueError("[!] Invalid type")

    img = cv2.resize(img, (SIZE * cell_size, SIZE* cell_size), interpolation = cv2.INTER_NEAREST)

    # add lines
    for i in range(1, SIZE) :
        img = cv2.line(img, (0, i * cell_size), (SIZE * cell_size, i * cell_size), (0, 0, 0), 2)
        img = cv2.line(img, (i * cell_size, 0), (i * cell_size, SIZE * cell_size), (0, 0, 0), 2)

    #convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            

    #display the board
    cv2.imshow("Othello", img)

    #add mouse click event to play
    if interactable :
        cv2.setMouseCallback("Othello", mouse_event_checker, [cell_size, board, possible_moves])

    key = cv2.waitKey(10)

    if key == ord("q") :
        cv2.destroyAllWindows()
        exit(0)
    


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
        GAME_TYPE = int(input("Type de jeu (1: joueur vs joueur, 2: joueur vs IA (IA=Noirs), 2: joueur vs IA (IA=Blancs), 0: IA vs IA): "))
        start_game(GAME_TYPE)