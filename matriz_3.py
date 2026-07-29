"""Recorrido adaptado para la matriz 3.

Todas as llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait


def ejecutar_matriz_3(robot):
    """Ejecuta el recorrido activo de la matriz 2."""
    robot.motor_garra_delantera.reset_angle(0)
    
    #Tomar los bloques verdes ================================================
    robot.motor_garra_delantera.reset_angle(0)

    robot.avanzar_cruzando_lineas(cruces_objetivo=2, velocidad=500, distancia_extra_cm=15)
    robot.girar(-90, 100, perfil="encadenado")

    robot.mover_garra_principal(
        velocidad=600,
        grados=40
    )
    robot.mover_garra_delantera(posicion=281)

    robot.avanzar_recto(9, 800)

    robot.mover_garra_principal(
        velocidad=500,
        grados=-36,
        potencia_apriete=40,
        apretar=True
    ) #Aqui ya tomó los bloques verdes
    
    robot.avanzar_recto(-20.8, velocidad_max=800)
    robot.girar(-89, 100)
    
    wait(100)

    robot.mover_garra_principal(
        velocidad=500,
        grados=34
    )

    robot.mover_garra_delantera(
        posicion=0
    )
    robot.avanzar_recto(-7, 700)

    #Giros para meter los bloques verdes dentro de sus compartimentos
    robot.giro_izquierda(35)
    robot.giro_derecha(-35)

    #Ir por los bloques amarillos======================================================
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=24,
        lado="derecha",
        perfil_salida="encadenado"    
    )

    robot.girar(90, 100)

    robot.mover_garra_delantera(
        posicion=281
    )

    robot.avanzar_recto(12, 800) #Entrar a tomar los bloques

    robot.mover_garra_principal(
        velocidad=500,
        grados=-36,
        potencia_apriete=40,
        apretar=True
    ) #Tomarlos

    robot.avanzar_recto(distancia_cm=-15, velocidad_max=800)

    robot.girar(90)

    robot.mover_garra_principal(
        velocidad=500,
        grados=34
    )

    robot.avanzar_recto(-7, 700)

    robot.mover_garra_delantera(
        posicion=0
    )

    #Giros para acomodar los bloques en el compartimento del robot
    robot.giro_derecha(-28)
    robot.giro_izquierda(28)
    
    #Ir por los bloques blancos============================================================
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=37,
        lado="izquierda",
        perfil_salida="encadenado"    
    )

    robot.avanzar_recto(5) #Avance que hace que choque a veces (En evaluación :|)

    robot.mover_garra_delantera(
        posicion=281
    )

    robot.girar(-91)

    robot.avanzar_recto(12, 500) #Avance para tomar los bloques

    robot.mover_garra_principal(
        velocidad=500,
        grados=-36,
        potencia_apriete=40,
        apretar=True
    ) #Tomar los bloques
    robot.avanzar_recto(-15, 500)

    robot.girar(-90)
    robot.avanzar_recto(17)
    robot.girar(-90)

    #Entrar en la matriz a partir de seguir la linea =======================================================
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

    robot.mover_garra_delantera(100)

    robot.avanzar_recto(
        distancia_cm=-13,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(290)

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

    robot.mover_garra_delantera(100)

    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(400)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-9)
    robot.avanzar_recto(
        distancia_cm=14.5,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(280)

    robot.mover_garra_rapida(
        potencia=100,
        grados=43,
        abrir=True
    )

    robot.avanzar_recto(
        distancia_cm=0.2,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(290)

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(4):
        robot.girar_corto(8 ,potencia_max=75, potencia_min=45)
        robot.girar_corto(-8, potencia_max=75, potencia_min=45)

    robot.mover_garra_delantera(0)
    robot.mover_garra_principal(600, -40)
    #Aquí termina la sección de movimientos para entrar en la matriz =========================================================
#Tomar los siguientes seis bloques de la matriz==============================================================================
    robot.avanzar_recto(-60, 850)
    robot.girar(-88)
    wait(100)
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=500, distancia_extra_cm=8)
    robot.girar(-90, 100, perfil="encadenado")

    #Estos movimientos son lo que hay que ajustar para despues solo copiar y pegar todo
    #Fin de la seccion para posicionarse delante de los cementos verdes otra vez ==========================================

    robot.mover_garra_principal(
        velocidad=600,
        grados=40
    )
    robot.mover_garra_delantera(posicion=281)

    robot.avanzar_recto(9, 800)

    robot.mover_garra_principal(
        velocidad=500,
        grados=-36,
        potencia_apriete=40,
        apretar=True
    ) #Aqui ya tomó los bloques verdes
    
    robot.avanzar_recto(-19.8, velocidad_max=800)
    robot.girar(-90, 100)
    
    wait(100)

    robot.mover_garra_principal(
        velocidad=500,
        grados=34
    )

    robot.mover_garra_delantera(
        posicion=0
    )
    robot.avanzar_recto(-7, 700)

    #Giros para meter los bloques verdes dentro de sus compartimentos
    robot.giro_izquierda(35)
    robot.giro_derecha(-35)

    #Ir por los bloques amarillos======================================================
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=24,
        lado="derecha",
        perfil_salida="encadenado"    
    )

    robot.girar(90, 100)

    robot.mover_garra_delantera(
        posicion=281
    )

    robot.avanzar_recto(12, 800) #Entrar a tomar los bloques

    robot.mover_garra_principal(
        velocidad=500,
        grados=-36,
        potencia_apriete=40,
        apretar=True
    ) #Tomarlos

    robot.avanzar_recto(distancia_cm=-14.5, velocidad_max=800)

    robot.girar(90)

    robot.mover_garra_principal(
        velocidad=500,
        grados=34
    )

    robot.avanzar_recto(-7, 700)

    robot.mover_garra_delantera(
        posicion=0
    )

    #Giros para acomodar los bloques en el compartimento del robot
    robot.giro_derecha(-28)
    robot.giro_izquierda(28)
    
    #Ir por los bloques blancos============================================================
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=30,
        lado="izquierda",
        perfil_salida="encadenado"    
    )

    robot.mover_garra_delantera(
        posicion=281
    )

    robot.mover_garra_principal(500, 110)

    robot.giro_derecha(-90, velocidad=800)

    robot.avanzar_recto(7, 500) #Avance para tomar los bloques

    robot.mover_garra_principal(
        velocidad=500,
        grados=-140,
        potencia_apriete=40,
        apretar=True
    ) #Tomar los bloques
    robot.avanzar_recto(-14, 500)

    robot.girar(-90)
    robot.avanzar_recto(22.9)
    robot.girar(-90)

#Entrar en la matriz
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=80,
        distancia_cm=15,
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

    robot.mover_garra_delantera(100)

    robot.avanzar_recto(
        distancia_cm=-13,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(290)

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

    robot.mover_garra_delantera(100)

    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(400)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-9)
    robot.avanzar_recto(
        distancia_cm=3,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(280)

    robot.mover_garra_rapida(potencia=100, grados=50, abrir=True)   

    robot.avanzar_recto(
        distancia_cm=0.2,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(290)

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(4):
        robot.girar_corto(8 ,potencia_max=75, potencia_min=45)
        robot.girar_corto(-8, potencia_max=75, potencia_min=45)

    robot.mover_garra_delantera(0)
    robot.mover_garra_principal(600, -40)

if __name__ == "__main__":
    robot = Base()
    print(robot.Hub.battery.voltage())
    ejecutar_matriz_3(robot)
