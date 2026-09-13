"""Recorrido de la matriz 4 basado en los recorridos de matriz 2."""

from control_drivebase import Base
from pybricks.tools import wait
import gc

from matriz import dejar_bloques_matriz
from matriz import dejar_bloques_matriz2


def ejecutar_matriz_4(robot):

    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 4")

    gc.collect()

    # ==========================================================
    # PRIMEROS 4 BLOQUES
    # Igual que el inicio de matriz 2.
    # ==========================================================

    robot.motor_garra.reset_angle(0)
    robot.motor_garra_delantera.reset_angle(0)

    robot.avanzar_recto(distancia_cm=-6, velocidad_max=900)

    robot.girar(
        90,
        potencia_max=65,
        potencia_min=45,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    wait(200)

    robot.avanzar_cruzando_lineas(
        cruces_objetivo=2,
        velocidad=900,
        escape_inicial_cm=8,
        retraso_freno_ms=80,
        perfil="seguro"
    )

    wait(200)

    robot.girar_hasta_negro("izquierda", potencia=65)

    robot.mover_garra_principal(
        900,
        300,
        apretar=False,
        duty_cierre=100
    )

    robot.avanzar_hasta_salir_negro(
        velocidad_max=900,
        velocidad_min=200,
        objetivo_reflexion=15,
        lecturas_salida=4
    )

    robot.avanzar_recto(
        distancia_cm=4.3,
        velocidad_max=900,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(290)

    robot.avanzar_recto(
        distancia_cm=-21,
        velocidad_max=900,
        perfil="seguro"
    )

    robot.girar(
        -90,
        potencia_max=75,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    # Sale de los azules por la misma línea corta de matriz 2.
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=50,
        distancia_cm=8,
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

    # ==========================================================
    # UN AMARILLO
    # Matriz 2 usa 12.5 cm para dos amarillos.
    # Aquí se recorta a 6.5 cm para tomar solo uno.
    # ==========================================================

    robot.girar(
        90,
        potencia_max=65,
        potencia_min=45,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(250)

    robot.mover_garra_principal(
        900,
        125,
        apretar=False,
        duty_cierre=100
    )

    robot.avanzar_recto(
        distancia_cm=6.5,
        velocidad_max=750,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(260)

    robot.mover_garra_principal(
        450,
        esperar=False,
        potencia_apriete=100,
        apretar=True
    )

    robot.avanzar_recto(
        distancia_cm=-8,
        velocidad_max=550,
        perfil="seguro"
    )

    # ==========================================================
    # PRIMER BLOQUE VERDE
    # 10.5 cm es la primera distancia para probar con el
    # seguidor de línea hacia ese verde.
    # ==========================================================

    robot.girar(
        90,
        potencia_max=65,
        potencia_min=45,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=80,
        distancia_cm=18,
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

    robot.girar(
        90,
        potencia_max=65,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(265)

    robot.mover_garra_principal(
        900,
        125,
        apretar=False,
        duty_cierre=60
    )

    # Entrada al primer verde.
    robot.avanzar_recto(
        distancia_cm=5.5,
        velocidad_max=500,
        perfil="seguro"
    )

    robot.mover_garra_delantera(275)

    robot.mover_garra_principal(
        500,
        esperar=False,
        potencia_apriete=80,
        apretar=True
    )

    # Sale del verde para volver al carril de entrega.
    robot.avanzar_recto(
        distancia_cm=-12,
        velocidad_max=550,
        perfil="seguro"
    )

    # ==========================================================
    # PRIMERA ENTREGA EN LA MATRIZ
    # ==========================================================

    robot.girar(
        90,
        potencia_max=75,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=90,
        distancia_cm=8,
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

    robot.girar(
        -92,
        potencia_max=90,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    dejar_bloques_matriz(robot)

    gc.collect()

    # ==========================================================
    # BUSCAR LOS DOS AZULES
    # Misma segunda ruta de recolección de matriz 2.
    # ==========================================================

    robot.mover_garra_principal(
        900,
        250,
        apretar=False,
        duty_cierre=60
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=80,
        distancia_cm=25,
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

    robot.girar(
        -90,
        potencia_max=75,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.avanzar_recto(
        distancia_cm=4.3,
        velocidad_max=500,
        perfil="seguro"
    )

    robot.girar(
        90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=60,
        distancia_cm=8,
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
        distancia_cm=24,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(300, velocidad=900)

    robot.avanzar_recto(
        distancia_cm=-28,
        velocidad_max=600,
        perfil="seguro"
    )

    robot.girar(
        -90,
        potencia_max=90,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=70,
        distancia_cm=14,
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

    # ==========================================================
    # UN BLOQUE Y LOS DOS DEL MEDIO
    # Matriz 2 usa 12 cm para dos; aquí se usa 6.5 cm para uno.
    # ==========================================================

    robot.girar(
        90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(265)

    robot.mover_garra_principal(
        900,
        150,
        apretar=False,
        duty_cierre=60
    )

    robot.avanzar_recto(
        distancia_cm=6.5,
        velocidad_max=750,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(275)

    robot.mover_garra_principal(
        500,
        esperar=False,
        potencia_apriete=80,
        apretar=True
    )

    # Levanta la garra para no botar los bloques y pasar
    # a recoger los dos bloques centrales.
    robot.girar(
        90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(190)

    robot.mover_garra_principal(
        900,
        180,
        apretar=False,
        duty_cierre=100
    )
    
    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.avanzar_recto(
        distancia_cm=9.5,
        velocidad_max=350,
        perfil="seguro"
    )

    robot.mover_garra_delantera(260)

    robot.avanzar_recto(
        distancia_cm=-8,
        velocidad_max=350,
        perfil="seguro"
    )

    robot.girar(
        90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=70,
        distancia_cm=17,
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

    # ==========================================================
    # ÚLTIMO BLOQUE VERDE
    # ==========================================================

    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.avanzar_recto(
        distancia_cm=7,
        velocidad_max=350,
        perfil="seguro"
    )

    robot.mover_garra_delantera(275)

    robot.mover_garra_principal(
        500,
        esperar=False,
        potencia_apriete=100,
        apretar=True
    )

    robot.mover_garra_delantera(260)

    # ==========================================================
    # ENTREGA FINAL
    # Conserva el mismo retroceso largo de matriz 2.
    # ==========================================================

    robot.avanzar_recto(
        distancia_cm=-38.5,
        velocidad_max=600,
        perfil="seguro"
    )

    robot.girar(
        89.9,
        potencia_max=70,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.avanzar_recto(
        distancia_cm=-40,
        velocidad_max=600,
        perfil="seguro"
    )

    robot.mover_torque(
        grados_torque=-170,
        velocidad_torque=900,
        esperar=False
    )

    # Segunda entrega de Matriz 4.
    dejar_bloques_matriz2(robot)

    gc.collect()


if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_4(robot)
