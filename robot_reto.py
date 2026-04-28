from robot_control import Base
from pybricks.parameters import Color, Direction, Port, Stop

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())

# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================
#SECCION 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_izquierda(45, 620) 
robot.mover_recto(12.25, 900) 
robot.giro_izquierda(45, 620) 
robot.esperar(10)
robot.seguir_linea(robot.seguidor, 100, 65) 

#SECCION 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-87.5, 450) 
robot.esperar(10)
robot.avanzar_con_torque(-13, 155, 900, 140) 
robot.esperar(10)

#SECCION 1.3 -> DEJAR LA PALA DE ALBAÑILERIA
robot.mover_recto(1,500) 
robot.girar(80)
robot.retroceder_recto(40, 900) 

#===========================SECCION#2 (DEJAR EL CEMENTO)==============================
#SECCION 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.mover_recto(31, 900)
robot.esperar(100)
robot.girar(-18, 500)
robot.mover_recto(12,800)
robot.girar(24, 500)
robot.esperar(120)
robot.seguir_linea(robot.seguidor, 100, 34)

# SECCION 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.esperar(10)
robot.girar(91, 500)
robot.mover_torque(-100, 1000)
robot.retroceder_recto(9, 650) 

# ===================== SECCIÓN #3 (IR POR LOS CEMENTOS BLANCOS) =====================
# SECCION 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.mover_recto(8, 900)
robot.giro_derecha(-85, 450)
robot.esperar(100)

#SECCION 3.2 -> AGARRAR LOS CEMENTOS BLANCOS
robot.mover_recto(4, 800)
robot.seguir_linea(robot.seguidor, 80, 10) 
robot.girar(-175, 500)
robot.avanzar_con_torque(-21, 170, 850, 200)

# ===================== SECCION #4 (DEJAR LOS CEMENTOS) =====================
#SECCION 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.mover_recto(10, 850)
robot.girar(77, 450)
robot.mover_recto(47) 
robot.girar(-70, 500) 
robot.esperar(100)

#SECCION 4.2 -> DEJAR LOS CEMENTOS BLANCOS CON GIRO
robot.mover_recto(5,900)
robot.seguir_linea(robot.seguidor, 65, 22) 
robot.esperar(100)
robot.girar(-181, 500) 
robot.retroceder_recto(11, 900)
robot.girar(42, 500)
robot.avanzar_con_torque(-12, -150, 700, 180)
robot.esperar(100)

#==============================SECCION #4 (ESCANEO DE MATRIZ)==========================================
#SECCION 4.1 -> SE POSICIONA PARA ESCANEAR LA MATRIZ
robot.mover_recto(45, 900) 
robot.girar(-43, 450)
''' 
robot.esperar(100)
robot.seguir_linea(robot.seguidor, 60, 7)

#SECCION 4.2 -> ESCANEA LA MATRIZ CON RETROCESO
robot.retroceder_recto(23, 600) 
robot.mover_torque(100, 100) 
robot.matriz()
robot.esperar(500)
robot.mover_recto(-2,900)

#Condicional del color verde
if Color.GREEN in robot.lista_colores:
    robot.retroceder_recto(2, 700)
    robot.matriz()
    robot.esperar(500)

print(robot.lista_colores)
robot.mover_torque(-70,100) 
robot.esperar(500)
#==================================SECCION #5 (IR POR LOS CEMENTOS AMARILLOS) ==============================
robot.mover_torque(-70,150)
robot.mover_recto(8,900)
robot.seguir_linea(robot.seguidor, 100, 45)
robot.giro_derecha(-90,450)
robot.mover_recto(10,900)
robot.giro_derecha(-89,450)
robot.avanzar_con_torque(-30,120,700,100) #AQUI AGARRA LOS CEMENTOS AMARILLOS

#====================================SECCION #6 (DEJAR LOS CEMENTOS AMARILLOS)==================================
robot.mover_recto(8,900)
robot.seguir_linea(robot.seguidor, 100, 14)
robot.giro_derecha(-88,450)
robot.mover_recto(54,900)

robot.giro_izquierda(92,450)
robot.mover_recto(60,900)
robot.girar(-90,450)
robot.retroceder_recto(22,700)
robot.mover_torque(-120,150) #AQUI YA DEJO LOS CEMENTOS AMARILLOS EN SU LUGAR

#=================================SECCION #7 (IR POR LOS AZULES) ========================================
robot.mover_recto(20, 800)
robot.girar(-89, 450) #GIRO PARA TOMAR LA PALA
robot.mover_recto(40, 800)
robot.girar(-90, 450)
robot.retroceder_recto(5,700)
robot.mover_torque(70, 150) #AQUI TOMA LA PALA
robot.girar(45, 450)
robot.mover_recto(32.5, 800)
robot.mover_torque(-120, 150) #aqui deja la pala en el camino
robot.girar(44, 500)

robot.seguir_linea(robot.seguidor, 100, 9)
robot.girar(-175, 450)
robot.retroceder_recto(10,700)
robot.mover_torque(120, 150) #Aqui toma los cementos azules

#========================SECCION #8 (DEJAR LOS CEMENTOS AZULES) ==========================
robot.retroceder_recto(10,700)
robot.mover_recto(25, 800)
robot.mover_garra(500, 110) #abrir la garra para llevar la pala

robot.girar(-45)
robot.mover_garra(500, -20)
robot.mover_recto(20, 700)
robot.girar(45)
robot.seguir_linea(robot.seguidor, 100, 140) #seguir la linea hasta el inicio

robot.mover_garra(500, 110) #AQUI YA DEJO LA PALA EN SU LUGAR
robot.girar(-45)
robot.girar(45)
robot.retroceder_recto(15, 700)
robot.girar(90)
robot.mover_torque(-120, 150) #AQUI DEJA LOS AZULES A UN LADO
'''