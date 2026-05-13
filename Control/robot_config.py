from .base import BaseConfig
from .utilidades import Utilidades
from .giros import Giros
from .movimiento import Movimiento
from .linea import Linea
from .manipuladores import Manipuladores

class Robot(BaseConfig, Utilidades, Giros, Movimiento, Linea, Manipuladores):
    def __init__(self):
        BaseConfig.__init__(self)
        print("="*30)
        print(f"Voltaje: {self.Hub.battery.voltage()} mV")
        print("="*30)