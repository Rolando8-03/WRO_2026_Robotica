from base import BaseRobot as BaseConfig
from giros import Giros
from movimiento import Movimiento
from linea import Linea
from manipuladores import Manipuladores


def copiar_metodos(destino, origen):
    """
    Copia métodos de una clase origen hacia una clase destino.
    Evita herencia múltiple, que Pybricks/MicroPython no soporta en el Hub.
    """
    for nombre in dir(origen):
        if nombre.startswith("__"):
            continue

        atributo = getattr(origen, nombre)

        if callable(atributo):
            setattr(destino, nombre, atributo)


class Robot(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)

        print("=" * 30)
        print("Voltaje:", self.Hub.battery.voltage(), "mV")
        print("=" * 30)


# Copiamos los métodos al final, fuera de la clase.
copiar_metodos(Robot, Giros)
copiar_metodos(Robot, Movimiento)
copiar_metodos(Robot, Linea)
copiar_metodos(Robot, Manipuladores)