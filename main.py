"""
OTHELLO GAME 
@Author: Eliott Georges 
"""
from constants import *
from board import Board
from player import Player
from ai_player import AIPlayer
from time import sleep
import cv2
import numpy as np
import time
from bitwise_op import *
from pions import PION

"""
---------------------------BIT VERSION--------------------------------
"""

def play(board: Board, move, pion: PION):
    """
    Joue un coup

    :param x: coordonnée x
    :param y: coordonnée y
    """
    board.update_state(move, pion) 

def is_possible(pm: list, x: int, y: int):
    """
    Vérifie si le coup est possible

    :param pm: liste des coups possibles
    :param x: coordonnée x
    :param y: coordonnée y

    :return: True si le coup est possible, False sinon et l'indice du coup dans la liste des coups possibles
    """
    for i in range(len(pm)):
            if (x, y) == x_y_from_move(pm[i]):
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
    pm = board.possible_moves(Player.pion)  
    if len(pm) == 0:
        if DEBUG:
            print("[!] Aucun coup possible")

        CAN_MOVE[Player.pion.index()] = False
        return
    
    if not ANALYSE and DISPLAY:
        opencv_display(board, pm, Player.pion, interactable = True)
    

def process_input_ai(AIPlayer: AIPlayer, board: Board):
    """
    Traite l'entrée de l'IA

    :param Player: joueur ia
    :param Board: Board
    """
    pm = board.possible_moves(AIPlayer.pion)
    if len(pm) == 0:
        if DEBUG:
            print("[!] Aucun coup possible")
            
        CAN_MOVE[AIPlayer.pion.index()] = False
        return
    
    if not ANALYSE and DISPLAY:
        opencv_display(board, pm, AIPlayer.pion, interactable = False)

    move = AIPlayer.play(board, ALGS[AIPlayer.pion.index()], pm)

    if DEBUG:
        print("[+] Coup IA: ", x_y_from_move(move), AIPlayer.pion.index())
        print("[+] Details: {:02b}".format(move))
        
    board.update_state(move, AIPlayer.pion)


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
        start_time = time.perf_counter()
    
    play_times_black = 0
    play_times_white = 0
    delta = None    
    i = 0
    while CAN_MOVE[0] or CAN_MOVE[1]:
        CAN_MOVE[i%2] = True
        if DEBUG:
            print("Tour: ", i+1)
        
        if ANALYSE_EACH_PLAY:
                start_time_i = time.perf_counter()

        if i%2 == 0:                
            if type(Player1) == AIPlayer:
                process_input_ai(Player1, board)
            else:
                process_input(Player1, board)
            
            if ANALYSE_EACH_PLAY:
                play_times_black += time.perf_counter() - start_time_i

        else:
            if type(Player2) == AIPlayer:
                process_input_ai(Player2, board)
            else:
                process_input(Player2, board)

            if ANALYSE_EACH_PLAY:
                play_times_white += time.perf_counter() - start_time_i
    

        i += 1
    
    if ANALYSE:
        delta = time.perf_counter() - start_time

    if ANALYSE_EACH_PLAY:
        play_times_black /= (i+1)/2
        play_times_white /= (i+1)/2
    
    return game_over(board, delta, play_times_black, play_times_white)

def start_game(TYPE: int = GAME_TYPE):
    """
    Démarre le jeu

    :param type: type de jeu (1: joueur vs joueur, 2: joueur vs IA, 3: IA vs IA)
    """
    board = Board()
    board.init_board()

    if TYPE == 1:
        p1 = Player(PION.BLACK)
        p2 = Player(PION.WHITE)
    elif TYPE == 2:
        p1 = AIPlayer(PION.BLACK)
        p2 = Player(PION.WHITE)
    elif TYPE == 3:
        p1 = Player(PION.BLACK)
        p2 = AIPlayer(PION.WHITE)
    else:
        p1 = AIPlayer(PION.BLACK)
        p2 = AIPlayer(PION.WHITE)
    
    print("[+] Debug mode activated: ", DEBUG)
    print("[+] Analyse mode activated: ", ANALYSE)
    print("[+] Display mode activated: ", DISPLAY)

    return game_loop(board, p1, p2)

def game_over(board: Board, delta: float, play_times_black: float, play_times_white: float):
    """
    Affiche le vainqueur

    :param board: plateau
    """
    print("[-]---- Fin de la partie ---- ")
    area_p1, area_p2 = board.score()

    print("[+] Score: ", area_p1, " - ", area_p2)

    black = 0
    white = 0
    if area_p1 > area_p2:
        print("[+] Les noirs gagnent")
        black = 1

    elif area_p1 < area_p2:
        print("[+] Les blancs gagnent")
        white = 1

    else:
        print("[+] Match nul")
    
    if ANALYSE:
        print("[+] Temps de jeu: ", delta, "s")
    if ANALYSE_EACH_PLAY:
        print("[+] Temps moyen par coup du joueur noir: ", play_times_black, "s")
        print("[+] Temps moyen par coup du joueur blanc: ", play_times_white, "s")
    
    return delta, black, white, play_times_black, play_times_white



# UI
def mouse_callback_process(possible_moves: list[int]):

    x = None
    y = None
    def mouse_callback(event, _x, _y, flags, param):
        nonlocal x, y
        if event == cv2.EVENT_LBUTTONDOWN:
            y = _x // cell_size
            x = _y // cell_size

    
    cv2.setMouseCallback("Othello", mouse_callback)
    
    while not (m:=is_possible(possible_moves, x, y))[0]:
        cv2.waitKey(10)
    
    #cv2.destroyAllWindows()
        
    if DEBUG:
        print("[+] Click: ", x, y)          
        print("[+] Details: {:03b}".format(possible_moves[m[1]]))

    return possible_moves[m[1]]

def opencv_display(board: Board, possible_moves: list, pion: PION, interactable : bool = True):

    img = np.zeros((SIZE, SIZE, 3), dtype = np.uint8)

    for i in range(SIZE):
        for j in range(SIZE):
            if board.GET_VAL(i, j) == 0b10:
                img[i, j] = white_color

            elif  board.GET_VAL(i, j) == 0b01:
                img[i, j] = black_color

            else :
                img[i, j] = bg_color

    for i in range(len(possible_moves)):
        x, y = x_y_from_move(possible_moves[i])
        if pion == PION.BLACK:
            img[x, y] = valid_move_color_black

        elif pion == PION.WHITE:
            img[x, y] = valid_move_color_white

        else:
            raise ValueError("[!] Invalid type")

    img = cv2.resize(img, (SIZE * cell_size, SIZE* cell_size), interpolation = cv2.INTER_NEAREST)

    # add lines
    for i in range(1, SIZE):
        img = cv2.line(img, (0, i * cell_size), (SIZE * cell_size, i * cell_size), (0, 0, 0), 2)
        img = cv2.line(img, (i * cell_size, 0), (i * cell_size, SIZE * cell_size), (0, 0, 0), 2)

    #convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            

    #display the board
    cv2.imshow("Othello", img)

    if interactable:
        move = mouse_callback_process(possible_moves)
        play(board, move, pion)
    
    else:
        cv2.waitKey(10) # pour ralentir l'affichage, sinon c'est trop rapide et rien ne s'affiche
        

def run():
    if ANALYSE:
        mean = 0
        black = 0
        white = 0
        each_mean_black = 0
        each_mean_white = 0
        accumulated_params = []
        for _ in range(NB_ITERATIONS):
            res = start_game(0)
            accumulated_params.append(res)
            mean += res[0]/NB_ITERATIONS
            each_mean_black += res[3]/NB_ITERATIONS
            each_mean_white += res[4]/NB_ITERATIONS
            black += res[1]/NB_ITERATIONS
            white += res[2]/NB_ITERATIONS

        
        print("[-]--------------------------------------------------------")
        print("[+] Nombre d'itérations: ", NB_ITERATIONS)
        print("[+] Moyenne: ", mean, "s")
        print("[+] Moyenne des coup du joueur noir: ", each_mean_black, "s")
        print("[+] Moyenne des coup du joueur blanc: ", each_mean_white, "s")
        print("[+] Victoires des noirs: ", round(black*100), "%")
        print("[+] Victoires des blancs: ", round(white*100), "%")
        print("[+] Matchs nuls: ", 100 - round(black*100) - round(white*100), "%")
        
        with open("res.txt", "a") as f:
            f.write(f"{MAX_DEPTH}:{mean}:{black}:{white}:{each_mean_black}:{each_mean_white}\n")


        return [mean, black, white, each_mean_black, each_mean_white], accumulated_params
    
    else:
        print("[+] Type de jeu: ", GAME_TYPE)
        start_game()


if __name__ == "__main__":
    run()