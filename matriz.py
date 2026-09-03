"""Funciones para identificar la matriz de colores.

Este archivo contiene la lectura estática por votación y la lógica que asigna
un número de matriz según los colores observados por el sensor.
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# -----------------------------------------------------------------------------
# _realizar_lectura_estatica
# Detiene el robot, toma varias lecturas del sensor y devuelve el color con
# mayor cantidad de votos si alcanza el nivel mínimo de confianza.
# -----------------------------------------------------------------------------
def _realizar_lectura_estatica(
    self,
    cantidad_lecturas=25,
    espera_inicial_ms=250,
    intervalo_lecturas_ms=40,
    votos_minimos=5
):
    colores_detectados = []

    self.frenar()
    wait(espera_inicial_ms)

    for _ in range(cantidad_lecturas):
        color = self.seguidor.color()

        if color is not None:
            colores_detectados.append(color)

        wait(intervalo_lecturas_ms)

    if not colores_detectados:
        return None

    colores_validos = (
        Color.GREEN,
        Color.YELLOW,
        Color.BLUE,
        Color.RED,
        Color.WHITE
    )

    conteos = {}

    for color in colores_validos:
        conteos[color] = colores_detectados.count(color)

    color_ganador = max(
        conteos,
        key=conteos.get
    )

    if conteos[color_ganador] < votos_minimos:
        return None

    return color_ganador


# -----------------------------------------------------------------------------
# escanear_matriz
# Realiza una primera lectura de color y devuelve el número de matriz.
# Cuando detecta verde, avanza para hacer una segunda lectura y diferenciar
# entre la matriz 1 y la matriz 4.
# -----------------------------------------------------------------------------
def escanear_matriz(self):
    primer_color = self._realizar_lectura_estatica()

    if primer_color is None:
        print("No se detecto un color de matriz valido.")
        return None

    if primer_color == Color.GREEN:
        # Distancia mínima y velocidad más alta: solo necesitamos
        # salir de la zona verde para leer la siguiente matriz.
        self.avanzar_recto(
            distancia_cm=4,          # antes 6cm; ajustar solo si la geometría real lo permite
            velocidad_max=300,       # antes 200; tramo corto, no requiere tanto control
            perfil="rapido"          # cambia a un perfil sin aceleración/frenado suave, si existe
        )

        segundo_color = self._realizar_lectura_estatica()
        matriz_detectada = 4 if segundo_color == Color.YELLOW else 1

    elif primer_color == Color.YELLOW:
        matriz_detectada = 2
    elif primer_color == Color.BLUE:
        matriz_detectada = 3
    elif primer_color == Color.RED:
        matriz_detectada = 4
    elif primer_color == Color.WHITE:
        matriz_detectada = 5
    else:
        matriz_detectada = None

    self.matriz_detectada = matriz_detectada
    print("Matriz detectada:", matriz_detectada)

    return matriz_detectada

def dejar_bloques_matriz(robot):
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=65,
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

    robot.mover_garra_principal(900, 230, apretar=False, duty_cierre=60)

    robot.mover_garra_delantera(100)

    robot.avanzar_recto(
        distancia_cm=-14,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(270)

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

    robot.mover_garra_principal(300, esperar=False, potencia_apriete=150, apretar=True)

    robot.mover_garra_delantera(100)

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

    robot.mover_garra_delantera(220)

    robot.mover_garra_rapida(130)

    robot.avanzar_recto(
        distancia_cm=-0.6,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    
    robot.mover_garra_delantera(290)

    robot.avanzar_recto(
        distancia_cm=1.2,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(5):
        robot.girar_corto(8 ,potencia_max=80, potencia_min=50)
        robot.girar_corto(-8, potencia_max=80, potencia_min=50)

    robot.avanzar_recto(distancia_cm=-1, velocidad_max=500, zona_rampa_cm=0.5, perfil="seguro")
    robot.mover_garra_delantera(190)
    robot.avanzar_recto(distancia_cm=-18, velocidad_max=500, perfil="seguro")
    robot.girar(
        angulo_deg=180,
        direccion="derecha",
        potencia_max=80,
        potencia_min=40,
        kp_base=4.0,
        kd_base=6.0,
        tolerancia_fin=0.6,
        perfil="seguro"
    
    )
    #Aquí termina la sección de movimientos para entrar en la matriz =========================================================

def dejar_bloques_matriz2(robot):

    """
    Secuencia: cruza líneas, gira, sigue línea, agarra con garra principal,
    retrocede, reajusta con garra delantera, sigue línea hasta azul,
    hace un giro corto, avanza, suelta con garra rápida, sacude 3 veces
    y retrocede.
    """
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=900, escape_inicial_cm=8, retraso_freno_ms=90)

    robot.girar(95, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    robot.seguir_linea(
        sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=7, lado="derecha",
        tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16,
        correccion_max=100, objetivo_reflexion=27, captura_inicial=True,
        tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado"
    )

    robot.mover_garra_principal(900, 230, apretar=False, duty_cierre=60)

    robot.mover_garra_delantera(230)
    robot.avanzar_recto(distancia_cm=-17, velocidad_max=400, perfil="seguro")
    robot.mover_garra_delantera(270)

    robot.seguir_linea(
        sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=16, lado="derecha",
        tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16,
        correccion_max=100, objetivo_reflexion=27, captura_inicial=True,
        tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado"
    )

    robot.mover_garra_principal(300, esperar=False, potencia_apriete=150, apretar=True)
    robot.mover_garra_delantera(100)
    robot.seguir_linea_hasta_color(color_objetivo=Color.BLUE, velocidad_max=100, lado="derecha")

    wait(200)

    # Se conserva girar() porque este movimiento es de -3°.
    robot.girar_corto(-11.5)

    robot.avanzar_recto(distancia_cm=3, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")
    robot.mover_garra_delantera(220)
    robot.mover_garra_rapida(130)
    robot.avanzar_recto(distancia_cm=-0.6, velocidad_max=650, zona_rampa_cm=0.1, perfil="encadenado")
    robot.mover_garra_delantera(290)
    robot.avanzar_recto(distancia_cm=2, velocidad_max=750, zona_rampa_cm=0.1, perfil="encadenado")
    

    # Sacudida: aquí sí se usa exclusivamente girar_corto().
    for i in range(5):
        robot.girar_corto(8, potencia_max=80, potencia_min=50)
        robot.girar_corto(-8, potencia_max=80, potencia_min=50)

    robot.mover_garra_delantera(0)
    robot.avanzar_recto(distancia_cm=-30, velocidad_max=900, zona_rampa_cm=0.1, perfil="encadenado")
    robot.girar(180, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.avanzar_recto(distancia_cm=-21, velocidad_max=900, zona_rampa_cm=0.1, perfil="encadenado")

def dejar_bloques_matriz3(robot, distancia_entrada=0):

    robot.mover_garra_delantera(80)
    robot.avanzar_recto(-8)
    robot.mover_garra_principal(100, grados=180, esperar=False)
    robot.mover_garra_delantera(275)
    

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
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
        grados=50,
        esperar=False,
        potencia_apriete=180,
        apretar=True
    )

    robot.mover_garra_delantera(100)

    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(400)

    robot.girar_corto(-9.8)

    robot.avanzar_recto(
        distancia_cm=distancia_entrada,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(220)

    robot.mover_garra_rapida(125)

    robot.avanzar_recto(
        distancia_cm=-0.6,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(290)

    robot.avanzar_recto(
        distancia_cm=2,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    for i in range(4):
        robot.girar_corto(8, potencia_max=75, potencia_min=45)
        robot.girar_corto(-8, potencia_max=75, potencia_min=45)

    robot.avanzar_recto(
        distancia_cm=-1,
        velocidad_max=500,
        zona_rampa_cm=0.5,
        perfil="seguro"
    )

    robot.mover_garra_delantera(190)

    robot.avanzar_recto(
        distancia_cm=-18,
        velocidad_max=500,
        perfil="seguro"
    )

    robot.girar(
        180,
        potencia_max=90,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
