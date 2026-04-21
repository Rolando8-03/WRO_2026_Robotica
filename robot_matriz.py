from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot_control import Base

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()

print(robot.Hub.battery.voltage())

#----------------- Combinación #4 -----------------------

#----- Primera Fase: Dejar los primeros 4 bloques -------
robot.seguir_linea(distancia_cm = 61.2, velocidad=1100, ref=30)
robot.mover_garra(1000, 120)
robot.girar(-89, 500)
robot.mover_recto(14, 900)
robot.mover_garra(1000, -100)
robot.retroceder_recto(20, 650)
robot.girar(-90, 500)
robot.mover_recto(8, 900)
robot.girar(-89, 500)
#robot.seguir_linea(distancia_cm = 10, velocidad=1100, ref=30)
robot.mover_recto(23, 900)
robot.mover_torque(80, 300)
robot.mover_recto(10,900)
robot.mover_torque(-80, 150)
robot.mover_garra(1000, 60)

#------ En este punto ya está en frente de la matriz ----