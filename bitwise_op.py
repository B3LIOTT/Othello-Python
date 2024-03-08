

# TODO: génrerer les masques dans init_board en fonction de la taille du plateau
def N(x):
    return (x & 0x00ffffffffffffff) << 8


def S(x):
    return (x & 0xffffffffffffff00) >> 8


def E(x):
    return (x & 0x7f7f7f7f7f7f7f7f) << 1


def W(x):
    return (x & 0xfefefefefefefefe) >> 1


def NW(x):
    return N(W(x))


def NE(x):
    return N(E(x))


def SW(x):
    return S(W(x))


def SE(x):
    return S(E(x))
