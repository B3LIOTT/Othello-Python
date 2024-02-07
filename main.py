"""
OTHELLO GAME 
@Author: Eliott Georges 
"""
from settings import *
from board import Board
from player import Player
from ai_player import AIPlayer
from time import sleep


def is_possible(pm: list, x: int, y: int):
    """
    Vérifie si le coup est possible

    :param pm: liste des coups possibles
    :param x: coordonnée x
    :param y: coordonnée y

    :return: True si le coup est possible, False sinon
    """
    for i in range(len(pm)):
            if (x, y) == (pm[i][0], pm[i][1]):
                return True, i
        
    return False, -1

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
            print("[+] Aucun coup possible")
        return
    
    x, y = Player.add_pion()
    ip, ind = is_possible(pm, x, y)
    while not ip:
        if DEBUG:
            print("[!] Coup invalide : ", x, y, Player.type)
        x, y = Player.add_pion()
        ip, ind = is_possible(pm, x, y)
        
    if DEBUG:
        print("[+] Coup joueur: ", x, y, Player.type)
        print("[+] Details: ", pm[ind])

    board.update_state(pm[ind], Player.type, x, y) 

def process_input_ai(AIPlayer: AIPlayer, board: Board):
    """
    Traite l'entrée de l'IA

    :param Player: joueur ia
    :param Board: Board
    """
    pm = board.possible_moves(AIPlayer.type)
    if len(pm) == 0:
        if DEBUG:
            print("[+] Aucun coup possible")
        return
    
    x, y, ind = AIPlayer.add_pion(ALG_TYPE)

    if DEBUG:
        print("[+] Coup IA: ", x, y, AIPlayer.type)
        print("[+] Details: ", pm[ind])
        
    board.update_state(pm[ind], AIPlayer.type, x, y)

def game_loop(board: Board, Player1: Player | AIPlayer, Player2: Player | AIPlayer):
    """
    Boucle principale du jeu

    :param Board: Board
    :param Player1: joueur 1
    :param Player2: joueur 2
    :param game_type: type d'affrontement
    """
    i = 0
    while True:
        i += 1
        print("Tour: ", i)
        board.display_array()

        if type(Player1) == AIPlayer:
            process_input_ai(Player1, board)
            sleep(SLEEP_TIME)
        else:
            process_input(Player1, board)

        board.display_array()

        if type(Player2) == AIPlayer:
            process_input_ai(Player2, board)
            sleep(SLEEP_TIME)
        else:
            process_input(Player2, board)


def start_game(type: int):
    """
    Démarre le jeu

    :param type: type de jeu (1: joueur vs joueur, 2: joueur vs IA, 3: IA vs IA)
    """
    board = Board(SIZE_X, SIZE_Y)

    if type == 1:
        p1 = Player(1)
        p2 = Player(2)
    elif type == 2:
        p1 = AIPlayer(1, board)
        p2 = Player(2)
    elif type == 3:
        p1 = Player(1)
        p2 = AIPlayer(2, board)
    else:
        p1 = AIPlayer(1, board)
        p2 = AIPlayer(2, board)

    if p1.type == p2.type:
        raise ValueError("Les joueurs ne peuvent pas être du même type")
    
    print("[+] Debug mode activated: ", DEBUG)
    game_loop(board, p1, p2)


if __name__ == '__main__':
    start_game(0)