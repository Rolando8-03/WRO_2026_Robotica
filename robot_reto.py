from robot_control import Base
from pybricks.parameters import Color, Direction, Port, Stop

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())

# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================
#SECCION 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.mover_recto(10, 850)
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
robot.mover_recto(9,850)
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
robot.giro_derecha(-90, 550)
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
robot.avanzar_con_torque(-20, -176, 900, 200)

# ===================== SECCION #4 (DEJAR LOS CEMENTOS) =====================
#SECCION 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.mover_recto(10, 850)
robot.girar(70, 450)
robot.mover_recto(50.5) 
robot.girar(-70, 500) 
robot.esperar(100)

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

#SECCION 4.2 -> DEJAR LOS CEMENTOS BLANCOS CON GIRO
robot.esperar(100)
robot.mover_recto(24.5, 700) #entrar en la matriz
robot.retroceder_recto(38, 800)
robot.girar(180, 500) 
robot.retroceder_recto(14, 900)
robot.girar(48, 500)
robot.avanzar_con_torque(-10, 145, 850, 180) #DEJAR LOS CEMENTOS BLANCOS
robot.esperar(100)

#==============================SECCION #5 (ESCANEO DE MATRIZ)==========================================
robot.mover_recto(18,900)
robot.girar(-44, 550)

'''
#Condicional del color verde
if Color.GREEN in robot.lista_colores:
    robot.retroceder_recto(2, 700)
    robot.matriz()
    robot.esperar(500)

print(robot.lista_colores)
robot.esperar(500)
'''

#==================================SECCION #6 (IR POR LOS CEMENTOS AMARILLOS) ==============================

#SECCION 6.1 -> AVANZA PARA IR A BUSCAR LOS CEMENTOS VERDES Y HACE GIRO PARA AGARRARLOS 
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
robot.avanzar_con_torque(-23, -150, 900, 200)

#SECCION 6.2 -> AVANZA PARA IR A DEJAR LOS CEMENTOS VERDES Y HACE GIRO PARA DEJARLO
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
robot.avanzar_con_torque(-8, 175, 900, 160) #AQUI DEJA LOS VERDES

#==================================SECCION #7 (IR POR LOS CEMENTOS AMARILLOS) ==============================
#SECCION 7.1 -> SEGUIR LA LINEA PARA IR A TOMA LOS CEMENTOS AMARILLOS (EN ESPERA DE MEJOR PRECISION)
robot.mover_recto(10, 900)
robot.girar(-43, 500)
robot.mover_recto(34, 900)
robot.girar(44, 500)
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
robot.avanzar_con_torque(-14, -170, 900, 160) #TOMAR LOS CEMENTOS AMARILLOS

#SECCION 7.2 -> AVANCES MECANICOS PARA IR A ACOMODARSE A UN LINEA PARA IR A DEJAR LOS CEMENTOS AMARILLOS
robot.mover_recto(10, 900)
robot.girar(-75, 500)
robot.mover_recto(70, 900) #IR PARA SEGUIR LA LINEA AL LUGAR DE LOS AMARILLOS
robot.girar(76, 500)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=57,
    lado="izquierda",
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)

#SECCION 7.3 -> POSICIONAMIENTO PARA DEJAR EN SU LUGAR LOS CEMENTOS AMARILLOS
robot.girar(-90, 500)
robot.avanzar_con_torque(-9, 175, 900, 160)
robot.mover_recto(15, 900) 

#==================================SECCION #8 (IR POR LOS CEMENTOS AZULES) ==============================
#SECCION 8.1 -> GIRO PARA ACOMODARSE EN LA LINEA PARA BUSCAR LOS CEMENTOS AZULES + GIRO PARA IR DIRECTO A LOS CEMENTOS Y RECOGERLOS
robot.girar(-90, 500)
robot.seguir_linea(
    robot.seguidor,
    velocidad_max=100,
    distancia_cm=55,
    kp=0.48,
    kd=1.70,
    k_freno=0.52,
    tiempo_acomodo_ms=400
)
robot.girar(149, 500)
robot.avanzar_con_torque(-40, -175, 900, 150) #TOMAR LOS CEMENTOS AZULES

#SECCION 8.2 -> AVANCES MECANICOS PARA IR A AGARRAR LA PALA Y PODER LLEVARLA AL INICIO JUNTO LOS AZULES 
robot.mover_recto(10, 900)
robot.girar(-29, 500)
robot.mover_recto(44.5, 900)
robot.mover_garra(150, -61) #abrir la garra
robot.mover_garra_delantera(400, 270) #velocidad, grados
robot.mover_garra(150, 61)

#SECCION 8.3 -> ACOMODACION PARA SEGUIR LINEA Y IR A DEJAR LOS CEMENTOS JUNTO CON LA PALA 
robot.retroceder_recto(8.5, 600)
robot.giro_derecha(25, 500)
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

#SECCION 8.4 -> POSICIONAMIENTO DE LA PALA CON LIGERO GIRO Y DESPUES APERTURA DE LA CELDA PARA DEJAR LOS CEMENTOS AZULES
robot.giro_derecha(90, 500)
robot.mover_garra(150, -120)
robot.giro_derecha(-90, 500)
robot.girar(90, 500)
robot.mover_torque(-176, 500)





