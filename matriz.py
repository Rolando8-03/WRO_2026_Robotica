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

    # El verde puede corresponder a dos matrices.
    # Se necesita una segunda lectura para distinguirlas.
    if primer_color == Color.GREEN:
        self.avanzar_recto(
            distancia_cm=6,
            velocidad_max=200,
            perfil="seguro"
        )

        segundo_color = self._realizar_lectura_estatica()

        if segundo_color == Color.YELLOW:
            matriz_detectada = 4
        else:
            matriz_detectada = 1

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

    # Se guarda también en el robot para consultarlo después sin repetir
    # el escaneo, además de devolverlo directamente.
    self.matriz_detectada = matriz_detectada

    print(
        "Matriz detectada:",
        matriz_detectada
    )

    return matriz_detectada

def dejar_bloques_matriz(self, robot):
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
        -55,
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

    robot.mover_garra_delantera(250)

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

def dejar_bloques_matriz2(self, robot):
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
        distancia_cm=4,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(250)

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

    robot.avanzar_recto(distancia_cm=-1, velocidad_max=500, zona_rampa_cm=0.5, perfil="seguro")
    robot.mover_garra_delantera(190)
    robot.avanzar_recto(distancia_cm=-18, velocidad_max=500, perfil="seguro")
    robot.girar(180, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
