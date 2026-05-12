from robot_control_prueba import Base
from pybricks.parameters import Color, Direction, Port, Stop
from matriz import ejecutar_matriz

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())
matriz_detectada = None


# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================

# SECCIÓN 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_arco_dc(radio_cm=9.6, angulo_deg=140, potencia=100, lado="derecha")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=65,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)


# SECCIÓN 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-90, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.avanzar_con_torque(distancia_cm=-17.5, grados_torque=-170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.mover_recto( distancia_cm=1, velocidad=1000, perfil="encadenado")

# SECCIÓN 1.3 -> DEJAR LA PALA DE ALBAÑILERÍA
robot.girar( 68.5, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado"
)

robot.esperar(80)

robot.retroceder(distancia_cm=42, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)

robot.mover_recto( distancia_cm=42, velocidad=1000, perfil="encadenado")

robot.giro_arco_dc( radio_cm=13, angulo_deg=19, potencia=80, lado="derecha")

# ===================== SECCIÓN 2 (DEJAR EL CEMENTO) =====================

# SECCIÓN 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=34,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

# SECCIÓN 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.esperar(300)

robot.avanzar_con_torque(distancia_cm=-8, grados_torque=166, velocidad_robot=1200, velocidad_torque=300,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# ===================== SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.giro_derecha( -90, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=9,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.esperar(300)

robot.girar( -170, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=-170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.giro_izquierda( 70, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")

robot.mover_recto( distancia_cm=39, velocidad=1000, perfil="encadenado")

robot.girar( -60, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=20,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.mover_recto( distancia_cm=40, velocidad=1000, perfil="encadenado")

# SECCIÓN 4.2 -> ENTRAR EN LA MATRIZ Y ESCANEAR
robot.mover_recto( distancia_cm=19.5, velocidad=700, perfil="seguro")

robot.esperar(500)

matriz_detectada = robot.escanear_matriz()
print("Matriz guardada:", matriz_detectada)

'''
robot.retroceder( distancia_cm=38, velocidad=800, perfil="seguro", invertir_correccion=False, pausa_gyro=30)

robot.girar( 180, velocidad=800, velocidad_min=180, anticipacion=10, perfil="encadenado")

robot.retroceder( distancia_cm=14, velocidad=850, perfil="seguro", invertir_correccion=False, pausa_gyro=30)

robot.girar( 49, velocidad=800, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=145, velocidad_robot=900, velocidad_torque=200, 
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.esperar(100)


# ===================== SECCIÓN 5 (BUSCAR LÍNEA) =====================

robot.mover_recto( distancia_cm=17, velocidad=900, perfil="encadenado")

robot.girar( -44, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

# ===================== SECCIÓN 6 (IR POR LOS CEMENTOS VERDES) =====================

# SECCIÓN 6.1 -> IR A BUSCAR LOS CEMENTOS VERDES
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=34,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.girar( 180, velocidad=850, velocidad_min=180, anticipacion=10, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-29, grados_torque=-150, velocidad_robot=900, velocidad_torque=400,  torque_despues_cm=1,
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# SECCIÓN 6.2 -> DEJAR LOS CEMENTOS VERDES
robot.mover_recto( distancia_cm=5, velocidad=900, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=38,
    lado="izquierda",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.girar( -180, velocidad=850, velocidad_min=180, anticipacion=10, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-16, grados_torque=175, velocidad_robot=900, velocidad_torque=400, 
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# ===================== SECCIÓN 7 (IR POR LOS CEMENTOS AMARILLOS) =====================

# SECCIÓN 7.1 -> TOMAR LOS CEMENTOS AMARILLOS
robot.mover_recto( distancia_cm=9, velocidad=900, perfil="encadenado")

robot.girar( -43, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.mover_recto( distancia_cm=34, velocidad=900, perfil="encadenado")

robot.girar( 44, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=9,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.girar( -180, velocidad=750, velocidad_min=160, anticipacion=10, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-18, grados_torque=-170, velocidad_robot=1000, velocidad_torque=400, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# SECCIÓN 7.2 -> IR A DEJAR LOS CEMENTOS AMARILLOS
robot.mover_recto( distancia_cm=10, velocidad=900, perfil="encadenado")

robot.girar( -75, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.mover_recto( distancia_cm=69, velocidad=900, perfil="seguro")

robot.girar( 76, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=56,
    lado="izquierda",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

# SECCIÓN 7.3 -> DEJAR LOS CEMENTOS AMARILLOS
robot.girar(-90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-17, grados_torque=175, velocidad_robot=900, velocidad_torque=160,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.mover_recto( distancia_cm=14, velocidad=900, perfil="encadenado")

# ===================== SECCIÓN 8 (IR POR LOS CEMENTOS AZULES) =====================

# SECCIÓN 8.1 -> TOMAR LOS CEMENTOS AZULES
robot.girar( -90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=55,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

robot.girar( 140, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.retroceder( distancia_cm=27, velocidad=900, perfil="seguro", invertir_correccion=False, pausa_gyro=30)

robot.girar( 40, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=-175, velocidad_robot=900, velocidad_torque=400, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

# SECCIÓN 8.2 -> AGARRAR LA PALA
robot.mover_recto( distancia_cm=10,velocidad=900,perfil="encadenado"
)

robot.girar(-29, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.mover_recto( distancia_cm=44.5, velocidad=900, perfil="seguro")

robot.mover_garra( velocidad=400, grados=-61)

robot.mover_garra_delantera( velocidad=1000, grados=265)

robot.mover_garra( velocidad=400, grados=61)

# SECCIÓN 8.3 -> SEGUIR LÍNEA PARA REGRESAR
robot.retroceder( distancia_cm=8.5, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=30)

robot.giro_derecha( 25, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=140,
    lado="izquierda",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)

# SECCIÓN 8.4 -> DEJAR PALA Y CEMENTOS AZULES
robot.mover_garra( velocidad=400, grados=-120)

robot.retroceder( distancia_cm=12.5, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=30)

robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")

robot.mover_torque( grados_torque=176, velocidad_torque=500)

robot.mover_garra_delantera( velocidad=500, grados=-265)

robot.mover_garra( velocidad=400, grados=130)

# ===================== EJECUTAR MATRIZ =====================
ejecutar_matriz(robot, matriz_detectada)

'''
