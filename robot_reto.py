from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot_control import Base

robot = Base()

#Seccion 1 --------------------------------------------------------------------------------------------------
print(robot.Hub.battery.voltage()) #imprimir el voltaje
robot.esperar(100) #pausa
robot.mover(5.7, velocidad=1000) #primer avance
robot.giro_derecho_llanta(1000 , 81) #giro para que se acomode

# Seccion 2: Ir por el cemento -----------------------------------------------------------------------------
robot.seguir_linea(1000,distancia_cm=77)
robot.giro_izquierdo_llanta(1000,87) #giro para tomar el cemento
robot.mover_torque(900, 75) #bajar la celda
robot.mover(-14, velocidad=800)
robot.mover_torque(900, 35)
robot.mover(4.5, velocidad=1000)

#Seccion 3: dejar la pala----------------------------------------------------------------------------------
robot.esperar(10) #pausa
robot.giro_izquierdo_llanta(1000, -80) #giro para estar en direccion al logo
robot.mover(-32, velocidad=1000) #empujar la pala a su lugar
robot.mover(8, velocidad=1000)

#Seccion 4: ir hacia el lugar del cemento----------------------------------------------------------------
robot.giro_izquierdo_llanta(1000, 40)
robot.mover(5, velocidad=1000)
robot.giro_derecho_llanta(1000, 40)
robot.seguir_linea(1000, distancia_cm=65) #movimiento para ir recto hacia el lugar del cemento

#seccion 5: dejar el cemento ----------------------------------------------------------------------------
robot.esperar(100)
robot.girar(1000, -97) #giro para ubicar el cemento
robot.mover(-5, velocidad=1000)
robot.mover_torque(900, -115) #subir la celda

#seccion 6: Camino a los cementos blancos-----------------------------------------------------------------
robot.giro_izquierdo_llanta(1000, 80)
robot.mover(5, velocidad=1000)
robot.seguir_linea(1000, distancia_cm=10)
robot.giro_derecho_llanta(1000,-91)
robot.giro_izquierdo_llanta(1000,82)
robot.mover(5, velocidad=1000)
robot.mover_torque(900, 115)
'''
#Seccion 7: camino a dejar los cementos blancos------------------------------------------------------
robot.reset_imu_y_base()
robot.giro_izquierda(500, 53) #Gira para avanzar
robot.movimiento_giroscopio(800, 49) #Movimiento recto para llegar hasta la linea
robot.girar_giroscopio(500, -53) #giro para quedar recto sobre la linea
robot.esperar(100)
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=16, velocidad=1000, ref=30) #seguidor para ajustarse
robot.girar_giroscopio(450, 180) #Giro de 180 para poner la celda viendo a la matriz
robot.giro_derecha(500, -27) # giro para entrar en el espacio indicado 27.5
robot.avanzar(-300) #avance para dejar los cementos
robot.mover_torque(200, -140) #abrir la celda
robot.reset_imu_y_base()
robot.giro_derecha(500, -2) #Pequeño giro de salida para que no se lleve la columna
robot.reset_imu_y_base()
robot.movimiento_giroscopio(500, 30) #retroceso de salida
robot.giro_derecha(500, 10) #Giro para acomodarse
robot.reset_imu_y_base() 


#Seccion 8: DETECTAR LA MATRIZ
robot.seguir_linea_con_giroscopio(distancia_cm=14, velocidad=1000, ref=30) #seguidor de linea para enderesarse
robot.reset_imu_y_base()
robot.movimiento_giroscopio(500, -20) #Movimiento de retroceso para clasificar la matriz
robot.mover_torque(200, 120) #Movimiento del torque para bajar el sensor
#Aqui va a ir la funcion de detectar


#seccion 9: Ir por los cementos amarillos
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=35, velocidad=1000, ref=30) #seguir linea para avanzar
robot.esperar(100)
robot.reset_imu_y_base()
robot.giro_derecha(500, 85) #giro en direccion a la derecha
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=10, velocidad=1000, ref=30)
robot.reset_imu_y_base()
robot.giro_derecha(500, 84)
robot.mover_torque(200, -25)
robot.avanzar(-330)
robot.mover_torque(200, -25)
robot.avanzar(-100)
robot.mover_torque(200, 70)
'''