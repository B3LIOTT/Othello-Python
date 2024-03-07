

def read_valid_dir(dir: int):
    """
    :param dir: directions valides sous forme de bits
    :return: liste des directions valides sous forme de couples (dx, dy)
    """
    dirs = []
    while dir != 0b0:
        dirs.append(bits_to_dir(dir & 0b111))
        dir >>= 3
    
    return dirs


def dir_to_bits(dir: tuple[int, int]):
    """
        0b010: (1, 0)
        0b001: (0, 1)
        0b100: (-1, 0)
        0b010: (0, -1)
        0b110: (1, 1)
        0b101: (-1, -1)
        0b011: (1, -1)
        0b100: (-1, 1)
    """
    if dir == (1, 0):
        return 0b010
    if dir == (0, 1):
        return 0b001
    if dir == (-1, 0):
        return 0b100
    if dir == (0, -1):
        return 0b010
    if dir == (1, 1):
        return 0b110
    if dir == (-1, -1):
        return 0b101
    if dir == (1, -1):
        return 0b011
    if dir == (-1, 1):
        return 0b100
    

def bits_to_dir(bits: int):
    """
        0b010: (1, 0)
        0b001: (0, 1)
        0b100: (-1, 0)
        0b010: (0, -1)
        0b110: (1, 1)
        0b101: (-1, -1)
        0b011: (1, -1)
        0b100: (-1, 1)
    """
    if bits == 0b010:
        return (1, 0)
    if bits == 0b001:
        return (0, 1)
    if bits == 0b100:
        return (-1, 0)
    if bits == 0b010:
        return (0, -1)
    if bits == 0b110:
        return (1, 1)
    if bits == 0b101:
        return (-1, -1)
    if bits == 0b011:
        return (1, -1)
    if bits == 0b100:
        return (-1, 1)
    