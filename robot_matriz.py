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
'''
#----- Primera Fase: Dejar los primeros 4 bloques -------
robot.seguir_linea(robot.seguidor,100,52.5)
robot.mover_garra(1000, 110)
robot.girar(-89.5, 500)
robot.mover_recto(15, 900)
robot.mover_garra(1000, -85)
robot.retroceder_recto(14, 650)
robot.girar(-90, 500)
robot.mover_recto(13,900)
robot.girar(-89, 500)
robot.mover_recto(5,900)
robot.seguir_linea(robot.seguidor,100,11)
robot.girar(-45,500)
robot.mover_recto(1,800)
robot.girar(45,500)
robot.mover_recto(2,900)
robot.mover_torque(80, 300)
robot.mover_recto(5,900)
robot.mover_torque(-80, 150)
robot.mover_garra(1000, 110)
for i in range (2):
    robot.girar(5,900)
    robot.girar(-5,900)
robot.retroceder_recto(42,500)
robot.girar(92,500)
robot.seguir_linea(robot.seguidor,100,19)
robot.girar(90,500)
robot.mover_recto(12,900)
'''
#CODIGO PARA LA PRIMERA MATRIZ
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=31.5,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(-89, 500)
robot.mover_recto(15.5, 850)
robot.mover_garra(150, -130) #abrir la garra
robot.mover_garra_delantera(300, 286) #velocidad, grados

robot.retroceder_recto(25, 600)
robot.girar(90, 500)
robot.retroceder_recto(14.5, 600)
robot.girar(-89, 500)

robot.mover_garra_delantera(300, -286) #velocidad, grados
robot.mover_recto(24.5, 850)
robot.mover_garra_delantera(300, 279) #velocidad, grados
robot.retroceder_recto(14.5, 600)
robot.girar(89, 500)
robot.mover_recto(8.75, 800)
robot.girar(-88, 500)
robot.mover_garra(150, 105)
robot.mover_garra_delantera(300, -60) #velocidad, grados
robot.mover_recto(16.5, 900)
robot.mover_garra_delantera(300, 63) #velocidad, grados
robot.mover_garra(150, 25) 
robot.retroceder_recto(30,600)
robot.girar(90,500)
robot.mover_garra(150,-130)
robot.mover_garra_delantera(300, -286) #velocidad, grados
robot.retroceder_recto(20,600)
robot.mover_garra_delantera(300, 286) #velocidad, grados
robot.mover_recto(22,900)
robot.mover_garra(150,115)
robot.esperar(10)
robot.mover_garra(150,-115)
robot.retroceder_recto(13,600)
robot.mover_garra_delantera(300, -286) #velocidad, grados


#Segunda matriz
robot.girar(-91,500)
robot.mover_garra(150,130)
robot.mover_recto(40,900)
robot.mover_garra_delantera(300, 286) #velocidad, grados
