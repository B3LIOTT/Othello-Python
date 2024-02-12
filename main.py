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
    raise NotImplementedError


if __name__ == '__main__':
    if ANALYSE:
        mean = 0
        black = 0
        white = 0
        for i in range(NB_ITERATIONS):
            res = start_game(0, display=False)
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