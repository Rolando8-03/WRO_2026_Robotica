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


#Tomar los azules
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=30,
        lado="derecha",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    wait(300)

    robot.girar(
        -90,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_principal(
        300,
        90,
        esperar=False
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=60,
        distancia_cm=7,
        lado="derecha",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.avanzar_recto(
        distancia_cm=11,
        velocidad_max=900,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(600, 290)
    wait(200)

#Salir del azul
    robot.avanzar_recto(
        distancia_cm=-20,
        velocidad_max=700,
        perfil="seguro"
    )

    wait(200)

    robot.girar(
        -90,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=60,
        distancia_cm=11,
        lado="izquierda",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    wait(200)

#Tomar los amarillos
    robot.girar(
        90,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(600, -25)
    wait(300)

    robot.mover_garra_principal(
        300,
        -49,
        esperar=False,
        apretar=False
    )

    wait(300)

    robot.avanzar_recto(
        distancia_cm=14,
        velocidad_max=750,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(600, 15)

    # En el recorrido anterior aparecía apretar=80.
    # Se interpreta como potencia de apriete de 80%.
    robot.mover_garra_principal(
        300,
        -31,
        esperar=False,
        potencia_apriete=80,
        apretar=True
    )

    robot.avanzar_recto(
        distancia_cm=-15.3,
        velocidad_max=550,
        perfil="seguro"
    )

    wait(500)

    robot.girar(
        90,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=14,
        lado="derecha",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    wait(200)

    robot.girar(
        90,
        potencia_max=90,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=80,
        distancia_cm=13,
        lado="derecha",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.mover_garra_principal(
        300,
        80,
        esperar=False
    )

    robot.mover_garra_delantera(600, -90)

    robot.avanzar_recto(
        distancia_cm=-13,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(600, 95)

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=13,
        lado="derecha",
        tiempo_acomodo_ms=140,
        tiempo_aceleracion_ms=140,
        kp=1.25,
        kd=2.7,
        k_freno=0.16,
        correccion_max=100,
        objetivo_reflexion=27,
        captura_inicial=True,
        tiempo_captura_ms=280,
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.mover_garra_principal(
        500,
        -50,
        esperar=False,
        potencia_apriete=100
    )

    robot.mover_garra_delantera(600, -150)

    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(400)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-11)

    robot.avanzar_recto(
        distancia_cm=14,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(400, 99)

    robot.mover_garra_rapida(
        potencia=100,
        grados=50,
        abrir=True
    )

    robot.avanzar_recto(
        distancia_cm=0.2,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(400, 55)

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(4):
        robot.girar_corto(8 ,potencia_max=75, potencia_min=45)
        robot.girar_corto(-8, potencia_max=75, potencia_min=45)


    robot.avanzar_recto(
        distancia_cm=-1,
        velocidad_max=400,
        zona_rampa_cm=0.5,
        perfil="seguro"
    )

    robot.mover_garra_delantera(400, -120)

    robot.avanzar_recto(
        distancia_cm=-12,
        velocidad_max=400,
        perfil="seguro"
    )

    


if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_2(robot)