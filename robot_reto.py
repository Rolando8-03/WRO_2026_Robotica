from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from robot_control import Base

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()


#Seccion 1 --------------------------------------------------------------------------------------------------
print(robot.Hub.battery.voltage()) #imprimir el voltaje

#Giro inicial para acomodarse al seguidor de línea
robot.esperar(200) #pausa
robot.avanzar(84) #primer avance
robot.reset_imu_y_base() #reseteo de imu
robot.giro_izquierda(500 ,87) #giro para que swe acomode
robot.esperar(100) #pausa

# Seccion 2: Ir por el cemento -----------------------------------------------------------------------------
robot.seguir_linea_con_giroscopio(distancia_cm=74, velocidad=1000, ref=30)
robot.girar_giroscopio(850, -80) #giro para tomar el cementoa
robot.mover_torque(400, 30) #bajar la celda
robot.avanzar(-130) #retroceso
robot.mover_torque(400, 20) #bajar la celda
robot.avanzar(-60) #retroceso para asegurar
robot.avanzar(80) #avanzar

#Seccion 3: dejar la pala----------------------------------------------------------------------------------
robot.reset_imu_y_base() #reseteo
robot.giro_derecha(900, -90) #giro para estar en direccion al logo
robot.avanzar(-320) #empujar la pala a su lugar

#Seccion 4: ir hacia el lugar del cemento----------------------------------------------------------------
robot.avanzar(290) #avance hacia atras para volver al camino
robot.reset_imu_y_base() #reseteo
robot.giro_derecha(800, 52) #giro de acomodo
robot.reset_imu_y_base() #reseteo
robot.giro_izquierda(800, 49) #giro de acomodo
robot.esperar(100)#pausa
robot.reset_imu_y_base() #reseteo
robot.seguir_linea_con_giroscopio(distancia_cm=44, velocidad=1000, ref=30) #movimiento para ir recto hacia el lugar del cemento

#seccion 5: Dejar el cemento ----------------------------------------------------------------------------
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(500, 90) #giro para ubic ar el cemento
robot.mover_torque(400, -80) #subir la celda
robot.esperar(90) #pausa
robot.avanzar(-115) #retroceso para meter un poco mas el cemento en su lugar


#seccion 6: Camino a los cementos blancos-----------------------------------------------------------------
robot.reset_imu_y_base() #reseteo
robot.movimiento_giroscopio(850, 5.65) #movimeinto hacia delante despues de dejar el cemento
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(500, -89.5) #giro en direccion a los cementos
robot.esperar(100) #pausa
robot.drive_base.straight(50)
robot.reset_imu_y_base() #reseteo
robot.seguir_linea_con_giroscopio(distancia_cm=19.5, velocidad=1000, ref=30)
robot.reset_imu_y_base() #reseteo
robot.girar_giroscopio(450,-180) #giro para poner la celda sobre los cementos
robot.avanzar(-120) #avance de seguridad
robot.mover_torque(400, 85)#agarrar los cementos blancos
robot.avanzar(-50) #avance de seguridad


#Seccion 7: camino a dejar los cementos blancos------------------------------------------------------
robot.reset_imu_y_base()
robot.giro_izquierda(500, 53) #Gira para avanzar
robot.movimiento_giroscopio_hasta_linea_n(velocidad=600, umbral=20, lineas_a_saltar=1)
robot.drive_base.straight(65)
robot.reset_imu_y_base()
robot.drive_base.stop()
robot.girar_giroscopio(500, -53.5) #giro para quedar recto sobre la linea
robot.esperar(100)
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=16.5, velocidad=1000, ref=30) #seguidor para ajustarse
robot.girar_giroscopio(450, 180) #Giro de 180 para poner la celda viendo a la matriz
robot.esperar(100)
robot.giro_derecha(500, -38) # giro para entrar en el espacio indicado 27.5
robot.avanzar(-250) #avance para dejar los cementos
robot.reset_imu_y_base()
robot.drive_base.stop()
robot.girar_giroscopio(500, -30) #este y el de abajo para acomodar los cementos
robot.reset_imu_y_base()
robot.drive_base.stop()
robot.girar_giroscopio(500, 30)
robot.mover_torque(400, -80) #abrir la celda
robot.reset_imu_y_base()
robot.giro_derecha(500, -2) #Pequeño giro de salida para que no se lleve la columna
robot.reset_imu_y_base()
robot.movimiento_giroscopio(850, 22) #retroceso de salida
robot.reset_imu_y_base()
robot.giro_derecha(500, 38) #Giro para acomodarse
robot.reset_imu_y_base() 


#Seccion 8: DETECTAR LA MATRIZ
robot.reset_imu_y_base()
robot.drive_base.straight(-160) #Movimiento de retroceso para clasificar la matriz
robot.mover_torque(400, 80) #Movimiento del torque para bajar el sensor
robot.esperar(100)
robot.iden_matriz()
print(robot.lista_L)

#seccion 9: Ir por los cementos amarillos
robot.mover_torque(400, -80) #subir celda
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=35, velocidad=1000, ref=30) #seguir linea para avanzar
robot.esperar(100)
robot.reset_imu_y_base()
robot.giro_derecha(500, 85) #primer giro para ir al amarillo
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, 10)  #movimiento para avanzar
robot.reset_imu_y_base()
robot.giro_derecha(500, 82) #segundo giro para ir al amarillo
robot.reset_imu_y_base()
robot.drive_base.straight(-375) #movimiento para ir hacia los cementos amarillos
robot.mover_torque(400, 90)  #agarrar los cementos amarillos
robot.drive_base.straight(-50) #avance de seguridad

'''
#Seccion 10: dejar los cementos amarillos
robot.avanzar(150) #avance para dar bien el giro
robot.reset_imu_y_base() 
robot.girar_giroscopio(500, -85) #giro de regreso a la direccion de los blancos
robot.reset_imu_y_base()
robot.movimiento_giroscopio(700, 59) #movimiento para ir hacia la dereccion de los blancos
robot.reset_imu_y_base()
robot.giro_izquierda(500, 80) #giro para ir hacia el lugar de los amarillos
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(71, 1000, 30)
robot.reset_imu_y_base()
robot.girar_giroscopio(500, -83) #giro para ubicar la celda sobre los amarillos
robot.mover_torque(400, -90) #abrir la celda para dejar los cementos
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, -21) #movimiento para dejar los cementos

#Seccion 10: IR POR LOS CEMENTOS AZULES
robot.movimiento_giroscopio(500, 9.7) #movimiento de retroceso para salir de la seccion de los amarillos
robot.reset_imu_y_base()
robot.giro_derecha(600, 81) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(distancia_cm=40, velocidad=1000, ref=30) #seguir linea
robot.giro_izquierda(500, -85) #giro para agarrar la pala
robot.avanzar(30) #pequeño retorceso
robot.mover_torque(400, 80)#agarrar la pala
robot.reset_imu_y_base()
robot.giro_izquierda(500, 85) #giro para voler a la linea
robot.reset_imu_y_base()
robot.movimiento_giroscopio(500, 10) #leve anvance
robot.mover_torque(400, -90)  #Dejar la pala en el camino para pasarla llevando despues
robot.reset_imu_y_base()

robot.giro_derecha(500, 85) #Primer giro para ir al azul
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, 16)#movimeinto de avance
robot.reset_imu_y_base()
robot.giro_izquierda(500, -93) #Segundo giro para ir a los azules
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, -20) #movimiento para ir hacia los cementos azules
robot.mover_torque(400, 90)  #agarrar los cementos azules
robot.avanzar(-100) #avance de seguridad

robot.avanzar(150) #avance de seguridad
robot.reset_imu_y_base()


robot.girar_giroscopio(500, -30)
robot.reset_imu_y_base()
robot.movimiento_giroscopio(500, 16)
robot.reset_imu_y_base()
robot.giro_izquierda(500, 35)
robot.reset_imu_y_base()
robot.seguir_linea_con_giroscopio(155, 1000, 30)



robot.giro_izquierda(800, -85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(15)
robot.mover_torque(200, 140)
robot.avanzar(-30)
robot.reset_imu_y_base()

robot.giro_izquierda(600, -85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(240)
robot.mover_torque(200, -140) #bajar ls celda para agarrar los azules
robot.reset_imu_y_base()
robot.giro_derecha(800, 85) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()
robot.avanzar(20)
robot.reset_imu_y_base()
robot.giro_derecha(800, 90) #giro para quedar recto sobre la linea
robot.reset_imu_y_base()

#Llevar los cementos azules
robot.avanzar(-300)
robot.mover_torque(200, 150) #agarrar los azules

robot.avanzar(220) 
robot.reset_imu_y_base() 
robot.girar_giroscopio(500, -85) #giro para salir de la zona azul
robot.reset_imu_y_base()

robot.avanzar(130) 
robot.reset_imu_y_base()
robot.giro_izquierda(800, 83) #giro en direccion al logo
robot.reset_imu_y_base()
robot.movimiento_giroscopio(600, 150) #movimiento largo hasta el inicio
robot.reset_imu_y_base()
robot.giro_derecha(800,45)
robot.avanzar(-250) #retroceso despues de dejar la pala

#Realizar giro para acomodar la paleta en el inicio
#Falta eso
#Seccion 12
robot.reset_imu_y_base() 
robot.girar_giroscopio(500, 130) #giro para salir de la zona azul
robot.reset_imu_y_base()
robot.mover_torque(200, -150) #dejar los cementos azules en espera
robot.reset_imu_y_base()

robot.mover_torque(400, 80)
'''