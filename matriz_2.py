"""Recorrido adaptado para la matriz 2.

Todas las llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait


def ejecutar_matriz_2(robot):
    """Ejecuta el recorrido activo de la matriz 2."""

    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 2")

    # PRIMERA PARTE DE LA MATRIZ
    # Tomar los azules

    robot.avanzar_cruzando_lineas(cruces_objetivo=2, velocidad=900, escape_inicial_cm=8, retraso_freno_ms=90)
    robot.avanzar_recto(distancia_cm=0.5, velocidad_max=900, perfil="encadenado")
    wait(400)
    robot.girar(-90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.mover_garra_principal(300, 90, esperar=False)

    robot.avanzar_recto(distancia_cm=10, velocidad_max=900, perfil="encadenado")
    robot.mover_garra_delantera(600, 290)

    # Salir del azul
    robot.avanzar_recto(distancia_cm=-20.8, velocidad_max=700, perfil="seguro")
    wait(200)
    robot.girar(-90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=9, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    wait(200)

    # Tomar los amarillos
    robot.girar(90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.mover_garra_delantera(600, -25)
    robot.mover_garra_principal(300, -50, esperar=False, apretar=False)
    wait(200)
    robot.avanzar_recto(distancia_cm=13, velocidad_max=750, perfil="encadenado")
    robot.mover_garra_delantera(600, 15)

    # En el recorrido anterior aparecía apretar=80.
    # Se interpreta como potencia de apriete de 80%.
    robot.mover_garra_principal(300, -31, esperar=False, potencia_apriete=80, apretar=True)
    robot.avanzar_recto(distancia_cm=-14, velocidad_max=550, perfil="seguro")
    wait(200)
    robot.girar(90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=14, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    wait(200)

    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=12, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    robot.mover_garra_principal(300, 80, esperar=False)
    robot.mover_garra_delantera(600, -90)

    robot.avanzar_recto(distancia_cm=-13, velocidad_max=400, perfil="seguro")
    robot.mover_garra_delantera(600, 93)
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=15, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    robot.mover_garra_principal(500, -50, esperar=False, potencia_apriete=130)
    robot.mover_garra_delantera(600, -150)

    robot.seguir_linea_hasta_color(color_objetivo=Color.BLUE, velocidad_max=100, lado="derecha")

    wait(20)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-10)

    robot.avanzar_recto(distancia_cm=13, velocidad_max=650, perfil="encadenado")

    robot.mover_garra_delantera(400, 99)

    robot.mover_garra_rapida(potencia=100, grados=50, abrir=True)

    robot.mover_garra_delantera(400, 65)

    robot.avanzar_recto(distancia_cm=0.5, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(5):
        robot.girar_corto(8, potencia_max=55, potencia_min=45)
        robot.girar_corto(-8, potencia_max=55, potencia_min=45)

    robot.avanzar_recto(distancia_cm=-1, velocidad_max=400, zona_rampa_cm=0.5, perfil="seguro")

    robot.mover_garra_delantera(400, -150)

    robot.avanzar_recto(distancia_cm=-18, velocidad_max=400, perfil="seguro")

    robot.girar(180, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # SEGUNDA PARTE DE LA MATRIZ

    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=80, distancia_cm=24, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    robot.girar(-90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.avanzar_recto(distancia_cm=4.65, velocidad_max=400, perfil="seguro")

    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=80, distancia_cm=9, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    robot.avanzar_recto(distancia_cm=22, velocidad_max=350, perfil="seguro")

    robot.mover_garra_delantera(400, 150)

    robot.avanzar_recto(distancia_cm=-28, velocidad_max=400, perfil="seguro")

    robot.girar(-90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=13, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    wait(200)

    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.mover_garra_delantera(600, -25)

    robot.mover_garra_principal(300, 50, esperar=False)

    wait(300)

    robot.avanzar_recto(distancia_cm=13, velocidad_max=750, perfil="encadenado")

    robot.mover_garra_delantera(600, 18)

    robot.mover_garra_principal(300, -50, esperar=False, potencia_apriete=80, apretar=True)

    robot.mover_garra_delantera(600, -80)

    robot.avanzar_recto(distancia_cm=14.9, velocidad_max=450, perfil="seguro")

    robot.mover_garra_delantera(600, 80)

    robot.avanzar_recto(distancia_cm=-40.9, velocidad_max=550, perfil="seguro")

    robot.girar(89, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.avanzar_recto(distancia_cm=-15, velocidad_max=550, perfil="seguro")

    robot.mover_torque(grados_torque=-169.5, velocidad_torque=600, esperar=False)

    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=900, escape_inicial_cm=8, retraso_freno_ms=90)

    robot.avanzar_recto(distancia_cm=1, velocidad_max=400, perfil="seguro")

    robot.girar(96, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=6, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    robot.mover_garra_principal(300, 90, esperar=False)

    robot.mover_garra_delantera(600, -90)
    robot.avanzar_recto(distancia_cm=-16, velocidad_max=400, perfil="seguro")

    robot.mover_garra_delantera(600, 94)

    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=16, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    robot.mover_garra_principal(500, -50, esperar=False, potencia_apriete=150)
    robot.mover_garra_delantera(600, -150)
    robot.seguir_linea_hasta_color(color_objetivo=Color.BLUE, velocidad_max=100, lado="derecha")

    wait(200)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-10)

    robot.avanzar_recto(distancia_cm=5, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")
    robot.mover_garra_delantera(400, 99)
    robot.mover_garra_rapida(potencia=100, grados=50, abrir=True)
    robot.mover_garra_delantera(400, 65)
    robot.avanzar_recto(distancia_cm=0.4, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(4):
        robot.girar_corto(8, potencia_max=50, potencia_min=45)
        robot.girar_corto(-8, potencia_max=50, potencia_min=45)

    robot.avanzar_recto(distancia_cm=-30, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")
    robot.girar(180, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.avanzar_recto(distancia_cm=-21, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")


if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_2(robot)
