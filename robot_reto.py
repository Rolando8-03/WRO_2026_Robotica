from robot_control import Base
from pybricks.parameters import Color, Direction, Port, Stop

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())


# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================
#SECCION 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.mover_recto(10, 800)
robot.girar(90, 500)
robot.esperar(10)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=82,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
#SECCION 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-87.5, 450) 
robot.esperar(10)
robot.avanzar_con_torque(-11, -165, 1000, 190) 
robot.esperar(10)

#SECCION 1.3 -> DEJAR LA PALA DE ALBAÑILERIA
robot.mover_recto(3,500) 
robot.girar(80)
robot.retroceder_recto(40, 900) 

#===========================SECCION#2 (DEJAR EL CEMENTO)==============================
#SECCION 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.mover_recto(31, 900)
robot.esperar(100)
robot.girar(-20, 500)
robot.mover_recto(9,800)
robot.girar(27, 500)
robot.esperar(120)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=38,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)

# SECCION 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.esperar(10)
robot.girar(90, 500)
robot.avanzar_con_torque(-5, 170, 900, 160) 

# ===================== SECCIÓN #3 (IR POR LOS CEMENTOS BLANCOS) =====================
# SECCION 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.mover_recto(7, 900)
robot.giro_derecha(-90, 450)
robot.esperar(100)

#SECCION 3.2 -> AGARRAR LOS CEMENTOS BLANCOS
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=10,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(-180, 500)
robot.avanzar_con_torque(-20, -176, 850, 200)

# ===================== SECCION #4 (DEJAR LOS CEMENTOS) =====================
#SECCION 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.mover_recto(10, 850)
robot.girar(70, 450)
robot.mover_recto(50.5) 
robot.girar(-70, 500) 
robot.esperar(100)

robot.seguir_linea(
    robot.seguidor,
    velocidad_max=80,
    distancia_cm=38,
    lado="izquierda",
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)

#SECCION 4.2 -> DEJAR LOS CEMENTOS BLANCOS CON GIRO
robot.esperar(100)
robot.mover_recto(24, 700) #entrar en la matriz
robot.retroceder_recto(36, 800)
robot.girar(180, 500) 
robot.retroceder_recto(14, 900)
robot.girar(44, 500)
robot.avanzar_con_torque(-12, 145, 700, 180)
robot.esperar(100)

#==============================SECCION #4 (ESCANEO DE MATRIZ)==========================================
robot.mover_recto(22,900)
robot.girar(-44, 500)

'''
#Condicional del color verde
if Color.GREEN in robot.lista_colores:
    robot.retroceder_recto(2, 700)
    robot.matriz()
    robot.esperar(500)

print(robot.lista_colores)
robot.esperar(500)
'''

#==================================SECCION #5 (IR POR LOS CEMENTOS verdes) ==============================
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=36,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(180, 500) 
robot.avanzar_con_torque(-23, -150, 850, 200)

robot.mover_recto(5, 900)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=38,
    lado="izquierda",
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)

robot.girar(-180, 500)
robot.avanzar_con_torque(-7, 175, 900, 160) 

robot.mover_recto(10, 900)
robot.girar(-40, 500)
robot.mover_recto(33, 900)
robot.girar(39, 500)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=8,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(-180, 400)
robot.avanzar_con_torque(-14, -170, 900, 160) 


robot.mover_recto(10, 900)
robot.girar(-70, 500)
robot.mover_recto(72.5, 900)
robot.girar(71, 500)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=54,
    lado="izquierda",
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(-90, 500)
robot.avanzar_con_torque(-9, 175, 900, 160)
robot.mover_recto(15, 900) 

robot.girar(-90, 500)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=54,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(155, 500)
robot.avanzar_con_torque(-40, -175, 900, 150)


robot.mover_recto(10, 900)
robot.girar(-30, 500)
robot.mover_recto(45, 900)
robot.mover_garra(150, -120)
robot.mover_garra_delantera(300, 250)
robot.mover_garra(150, 130)

robot.retroceder_recto(10, 600)
robot.giro_derecha(28, 450)

robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=140,
    lado="izquierda",
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.mover_garra(150, -120)




'''
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=40,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(180, 500) 
robot.avanzar_con_torque(-12, 145, 700, 180)

robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=45,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.giro_derecha(-90,450)
robot.mover_recto(10,900)
robot.giro_derecha(-89,450)
robot.avanzar_con_torque(-30,120,700,100)
#====================================SECCION #6 (DEJAR LOS CEMENTOS AMARILLOS)==================================
robot.mover_recto(8,900)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=14,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.giro_derecha(-88,450)
robot.mover_recto(54,900)

robot.giro_izquierda(92,450)
robot.mover_recto(60,900)
robot.girar(-90,450)
robot.retroceder_recto(22,700)
robot.mover_torque(-120,150) #AQUI YA DEJO LOS CEMENTOS AMARILLOS EN SU LUGAR

#=================================SECCION #7 (IR POR LOS AZULES) ========================================
robot.mover_recto(16, 800)
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
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=120,
    distancia_cm=130,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
) #seguir la linea hasta el inicio

robot.mover_torque()
robot.mover_garra(500, 110) #AQUI YA DEJO LA PALA EN SU LUGAR
robot.girar(-45)
robot.girar(45)
robot.retroceder_recto(15, 700)
robot.girar(90)
robot.mover_torque(-120, 150) #AQUI DEJA LOS AZULES A UN LADO
'''
