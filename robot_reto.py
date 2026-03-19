from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot_control import Base

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()

# FASE 1 - SECUENCIA COMPLETA DEL CÓDIGO 2

# Seccion1
# Inicio de camino
# Ligero avance del robot y levantamiento de la celda y giro para pegar en la pared y acomodarse e ir temprano
#SALIDA

#Seccion 1 --------------------------------------------------------------------------------------------------
print(robot.Hub.battery.voltage()) #imprimir el voltaje

robot.esperar(200) #pausa
robot.avanzar(84) #primer avance
robot.reset_imu_y_base() #reseteo de imu
robot.giro_izquierda(500 ,87) #giro para que swe acomode
robot.esperar(100) #pausa

# Seccion 2: Ir por el cemento -----------------------------------------------------------------------------
robot.seguir_linea_con_giroscopio(distancia_cm=75, velocidad=1000, ref=30)
robot.girar_giroscopio(800, -83) #giro para tomar el cementoa
robot.mover_torque(300, 75) #bajar la celda
robot.avanzar(-120) #retorceso
robot.mover_torque(300, 75) #bajar la celda
robot.avanzar(-60) #avanzar para asegurar
robot.avanzar(70) #retorceso

#Seccion 3: dejar la pala----------------------------------------------------------------------------------
robot.reset_imu_y_base() #reseteo
robot.giro_derecha(900, -70) #giro para estar en direccion al logo
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, -33) #empujar la pala a su lugar

#Seccion 4: ir hacia el lugar del cemento----------------------------------------------------------------
robot.avanzar(290) #avance hacia atras para volver al camino
robot.reset_imu_y_base() #reseteo
robot.giro_derecha(800, 50) #giro de acomodo
robot.reset_imu_y_base() #reseteo
robot.giro_izquierda(800, 47) #giro de acomodo
robot.esperar(100)#pausa
robot.reset_imu_y_base() #reseteo
robot.seguir_linea_con_giroscopio(distancia_cm=46, velocidad=1000, ref=30) #movimiento para ir recto hacia el lugar del cemento


#seccion 5: dejar el cemento ----------------------------------------------------------------------------
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(500, 90) #giro para ubic ar el cemento
robot.mover_torque(200, -143) #subir la celda
robot.esperar(90) #pausa
robot.avanzar(-140) #retroceso para meter un poco mas el cemento en su lugar


#seccion 6: Camino a los cementos blancos-----------------------------------------------------------------
robot.reset_imu_y_base() #reseteo

robot.movimiento_giroscopio(800, 15) #movimeinto hacia delante despues de dejar el cemento
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(500, -90) #giro en direccion a los cementos
robot.esperar(100) #pausa
robot.reset_imu_y_base() #reseteo
robot.seguir_linea_con_giroscopio(distancia_cm=22, velocidad=1000, ref=30)
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(450,-181) #giro para poner la celda sobre los cementos
robot.avanzar(-95) #avance de seguridad
robot.mover_torque(300, 150) #agarrar los cementos blancos
robot.avanzar(-80) #avance de seguridad


#Seccion 7: camino a dejar los cementos blancos------------------------------------------------------
robot.reset_imu_y_base()
robot.giro_izquierda(500, 53) #Gira para avanzar
robot.movimiento_giroscopio(800, 51) #Movimiento recto para llegar hasta la linea
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
robot.movimiento_giroscopio(500, 29) #retroceso de salida
robot.reset_imu_y_base()
robot.giro_derecha(500, 35) #Giro para acomodarse
robot.reset_imu_y_base() 


#Seccion 8: DETECTAR LA MATRIZ

robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, -17) #Movimiento de retroceso para clasificar la matriz
robot.mover_torque(250, 140) #Movimiento del torque para bajar el sensor
robot.esperar(1000)
# -------- DETECCIÓN DE MATRIZ --------
robot.lista_L = []  # limpiar lista antes de leer

# Leer primer cuadro
robot.avanzar(-200)  # ajusta distancia real
robot.iden_matriz()

robot.esperar(200)

# Leer segundo cuadro
robot.avanzar(-200)  # ajusta distancia real
robot.iden_matriz()

# Convertir a clave
clave = tuple(robot.lista_L)

# Buscar en diccionario
matriz_id = robot.claves_matrices.get(clave)

if matriz_id is not None:
    print(f"Matriz detectada: {matriz_id} | firma={clave}")
else:
    print(f"Matriz no identificada | firma leída={clave}")

#seccion 9: Ir por los cementos amarillos
robot.mover_torque(250, -140)
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=35, velocidad=1000, ref=30) #seguir linea para avanzar
robot.esperar(100)
robot.reset_imu_y_base()
robot.giro_derecha(500, 85) #giro en direccion a la derecha
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, 12) 
robot.reset_imu_y_base()
robot.giro_derecha(500, 86)
robot.reset_imu_y_base()
robot.movimiento_giroscopio(350, -33)
robot.mover_torque(250, 140) 
robot.avanzar(-100)


#Seccion 9
robot.avanzar(100)
robot.reset_imu_y_base() 
robot.girar_giroscopio(500, -85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.movimiento_giroscopio(700, 65) #Movimiento recto para llegar hasta la linea
robot.reset_imu_y_base()
robot.giro_izquierda(500, 80) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.movimiento_giroscopio(800, 71.5)
robot.reset_imu_y_base()
robot.girar_giroscopio(500, -85)
robot.reset_imu_y_base()
robot.movimiento_giroscopio(800, -20)
robot.mover_torque(200, -140) #abrir la celda


#Seccion 10
robot.avanzar(90)
robot.reset_imu_y_base()
robot.giro_derecha(800, 85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=33, velocidad=1000, ref=30)
robot.reset_imu_y_base()
robot.giro_izquierda(800, -85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(15)
robot.mover_torque(200, 140)
robot.avanzar(-30)
robot.reset_imu_y_base()
robot.giro_izquierda(800, 85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(240)
robot.mover_torque(200, -140)
robot.reset_imu_y_base()
robot.giro_derecha(800, 85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(20)
robot.reset_imu_y_base()
robot.giro_derecha(800, 90) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()

#Seccion 11 
robot.avanzar(-300)
robot.mover_torque(200, 142)
robot.avanzar(220)
robot.reset_imu_y_base() 
robot.girar_giroscopio(500, -85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(160)
robot.reset_imu_y_base()
robot.giro_izquierda(800, 110) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(90)
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=140, velocidad=1000, ref=30)
robot.reset_imu_y_base()

#Realizar giro para acomodar la paleta en el inicio
#Falta eso
#Seccion 12
robot.giro_derecha(800,-75)
robot.esperar(100)
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600,10)
robot.seguir_linea_con_giroscopio(distancia_cm=33, velocidad=1000, ref=30) #seguir linea para avanzar