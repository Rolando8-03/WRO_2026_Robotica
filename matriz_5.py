from control_drivebase import Base
from pybricks.tools import wait
import gc

from matriz import dejar_bloques_matriz
from matriz import dejar_bloques_matriz2


def ejecutar_matriz_5(robot):

    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de MATRIZ 5")

    gc.collect()

    # ==========================================================
    # POSICION INICIAL DE LAS GARRAS
    # ==========================================================

    robot.motor_garra.reset_angle(0)
    robot.motor_garra_delantera.reset_angle(0)
    wait(200)


    # Cruzar las 2 primeras líneas
    robot.avanzar_cruzando_lineas(
        cruces_objetivo=2,
        velocidad=900,
        escape_inicial_cm=8,
        retraso_freno_ms=91
    )

    robot.avanzar_recto(
        distancia_cm=6,
        velocidad_max=900,
        perfil="seguro"
    )


    gc.collect()
    wait(200)

    # Girar hacia la primera zona de bloques
    robot.girar(
        -90,
        potencia_max=65,
        potencia_min=45,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    # Abrir la garra principal
    robot.mover_garra_principal(
        900,
        300,
        apretar=False,
        duty_cierre=100
    )

    # Bajar completamente la garra delantera
    robot.mover_garra_delantera(290)

    # Aquí el robot entra sobre el grupo azul.
    # Se conserva la distancia usada en matriz_2.
    robot.avanzar_recto(
        distancia_cm=18,
        velocidad_max=900,
        perfil="seguro"
    )

    wait(200)

    robot.avanzar_recto(
        distancia_cm=-22,
        velocidad_max=900,
        perfil="seguro"
    )

    # Reposicionar el robot para continuar con los amarillos
    robot.girar(
        -90,
        potencia_max=75,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    '''
    # Desplazamiento por la línea hasta la zona amarilla
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=60,
        distancia_cm=9,
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

    gc.collect()
    wait(200)
    '''
    