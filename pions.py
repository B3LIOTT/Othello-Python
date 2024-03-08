from enum import Enum


class PION(Enum):
    BLACK = 0b01
    WHITE = 0b10
    NONE = 0b00

    def other_type(self):
        """
        Retourne le type opposé

        :param type: type de pion
        :return: type opposé
        """
        return PION.BLACK if self == PION.WHITE else PION.WHITE


    def index(self):
        """
        Retourne la valeur associée

        :param type: type de pion
        :return: valeur associée
        """
        return 0 if self == PION.BLACK else 1