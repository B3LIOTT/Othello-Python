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
    
    opencv_display(board, pm, AIPlayer.type, interactable = False)
    x, y, ind = AIPlayer.add_pion(ALG_TYPE, pm)

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
    global CAN_MOVE
    CAN_MOVE = [True, True]

    i = 0
    while CAN_MOVE[0] or CAN_MOVE[1]:
        CAN_MOVE[i%2] = True
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
    game_loop(board, p1, p2)



# UI
def mouse_click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cs, board, pm = params
        row = y // cs
        col = x // cs

        if DEBUG:
            print("[+] Click: ", row, col)
            print("[+] Details: ", pm)
        
        play(row, col, board, pm[is_possible(pm, row, col)[1]])


def opencv_display(board: Board, possible_moves: list, type:int, interactable : bool = True) :

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
        cv2.setMouseCallback("Othello", mouse_click_event, [cell_size, board, possible_moves])

    key = cv2.waitKey(10)

    if key == ord("q") :
        cv2.destroyAllWindows()
        exit(0)

    return True


if __name__ == '__main__':
    start_game(0)