from robot_control_prueba import Base
from pybricks.parameters import Color, Direction, Port, Stop
from matriz import ejecutar_matriz

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())
matriz_detectada = None


# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================

# SECCIÓN 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_arco_dc(
    radio_cm=9.6,
    angulo_deg=140,
    potencia=100,
    lado="derecha"
)

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
robot.girar(
    -90,
    velocidad=1000,
    velocidad_min=160,
    anticipacion=8,
    perfil="encadenado"
)

robot.avanzar_con_torque(
    distancia_cm=-17.5,
    grados_torque=-169,
    velocidad_robot=1200,
    velocidad_torque=350,
    torque_despues_cm=1,
    esperar_torque=False,
    perfil_entrada="encadenado",
    perfil_salida="encadenado"
)


robot.mover_recto(
    distancia_cm=1,
    velocidad=1000,
    perfil="encadenado"
)


# SECCIÓN 1.3 -> DEJAR LA PALA DE ALBAÑILERÍA
robot.girar(
    69.5,
    velocidad=1000,
    velocidad_min=160,
    anticipacion=8,
    perfil="encadenado"
)

robot.retroceder(
    distancia_cm=42,
    velocidad=870,
    perfil="seguro",
    invertir_correccion=False,
    pausa_gyro=25
)


robot.mover_recto(
    distancia_cm=36,
    velocidad=1200,
    perfil="encadenado"
)

'''
robot.giro_arco_dc(
    radio_cm=13,
    angulo_deg=45,
    potencia=80,
    lado="izquierda"
)
'''
robot.giro_arco_dc(
    radio_cm=13,
    angulo_deg=19,
    potencia=80,
    lado="derecha"
)


# ===================== SECCIÓN 2 (DEJAR EL CEMENTO) =====================

# SECCIÓN 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=39,
    lado="derecha",
    tiempo_acomodo_ms=80,
    kp=1.15,
    kd=2.6,
    k_freno=0.0,
    perfil_salida="encadenado"
)


# SECCIÓN 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.girar(
    90,
    velocidad=950,
    velocidad_min=160,
    anticipacion=8,
    perfil="encadenado"
)

robot.avanzar_con_torque(
    distancia_cm=-9,
    grados_torque=166,
    velocidad_robot=1200,
    velocidad_torque=200,
    esperar_torque=False,
    perfil_entrada="encadenado",
    perfil_salida="encadenado"
)


# ===================== SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.giro_derecha(
    -90,
    velocidad=1200,
    velocidad_min=160,
    anticipacion=10,
    perfil="encadenado"
)

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

robot.girar(
    -160,
    velocidad=1200,
    velocidad_min=160,
    anticipacion=0,
    perfil="encadenado"
)

robot.avanzar_con_torque(
    distancia_cm=-20,
    grados_torque=-168,
    velocidad_robot=1200,
    velocidad_torque=250,
    esperar_torque=False,
    perfil_entrada="encadenado",
    perfil_salida="encadenado"
)
