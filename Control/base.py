from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction

class BaseConfig:
    def __init__(self):
        self.Hub = PrimeHub()
        self.motor_derecho = Motor(Port.A, Direction.CLOCKWISE)
        self.motor_izquierdo = Motor(Port.E, Direction.COUNTERCLOCKWISE)
        self.motor_torque = Motor(Port.D)
        self.motor_garra = Motor(Port.F)
        self.motor_garra_delantera = Motor(Port.B)
        self.seguidor = ColorSensor(Port.C)

        self.diametro_rueda = 56
        self.circunferencia = self.diametro_rueda * 3.14159
        self.grados_por_mm = 360 / self.circunferencia
