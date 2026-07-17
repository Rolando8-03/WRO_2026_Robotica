"""Funciones para identificar la matriz de colores.

Este archivo contiene la lectura estática por votación y la lógica que asigna
un número de matriz según los colores observados por el sensor.
"""

from pybricks.parameters import Color
from pybricks.tools import wait


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

