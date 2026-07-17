"""Recorrido adaptado para la matriz 1.

Todas as llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait


def ejecutar_matriz_1(robot):
    """Ejecuta el recorrido activo de la matriz 2."""

    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 2")

    robot.avanzar_cruzando_lineas(cruces_objetivo=3,velocidad=900,retraso_freno_ms=95.5)
    robot.mover_garra_principal(850, 130)
    robot.girar(-90, potencia_max=100)
    robot.avanzar_recto(5, 800)
    robot.mover_garra_delantera(850, 286)
    #Aqui ya agarro los primeros dos bloques verdes

    robot.avanzar_recto(-8, 800)
    robot.girar(-90, potencia_max=100)
    robot.avanzar_recto(13)
    robot.girar(92, potencia_max=100)
    robot.mover_garra_delantera(850, -286)
    robot.avanzar_recto(8, 800)
    robot.mover_garra_delantera(850, 276)
    wait(300)
    #Aqui ya agarro los dos bloques azules

    robot.avanzar_recto(-8.5, 800)
    robot.girar(88, potencia_max=100)
    robot.avanzar_recto(9.5)
    robot.girar(-90, potencia_max=80)
    robot.mover_garra_principal(850, -105,apretar=False)
    robot.avanzar_recto(11)
    robot.mover_garra_principal(850, -30,apretar=True)
    #Aqui ya agarro los ultimos dos bloques de en medio de la matriz

    #Nuevo bloque de prueba
    robot.avanzar_recto(-11)
    robot.girar(-90)
    robot.avanzar_recto(3)
    robot.girar(-90)
    robot.avanzar_recto(3)

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

    robot.girar(-168)
    robot.avanzar_recto(7)
    robot.seguir_linea(distancia_cm=20)
    robot.avanzar_recto(18)
    robot.girar(-90)
    robot.avanzar_recto(7)
    robot.girar(90)
    robot.avanzar_recto(15)
    

    


if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_1(robot)

