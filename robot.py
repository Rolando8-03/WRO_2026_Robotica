from Control.base import BaseRobot
from Control.movimiento import Movimiento
from Control.giros import Giros
from Control.linea import Linea
from Control.manipuladores import Manipuladores


class Robot(Movimiento,Giros,Linea,Manipuladores,BaseRobot):
    def __init__(self):
        super().__init__()