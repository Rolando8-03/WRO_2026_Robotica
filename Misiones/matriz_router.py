# Misiones/matriz_router.py

from pybricks.parameters import Color

from Matrices.matriz1 import ejecutar_matriz_1
from Matrices.matriz2 import ejecutar_matriz_2
from Matrices.matriz3 import ejecutar_matriz_3
from Matrices.matriz4 import ejecutar_matriz_4
from Matrices.matriz5 import ejecutar_matriz_5

MATRIZ_DEFAULT = 1


COLOR_A_MATRIZ = {
    "GREEN": 1,
    "YELLOW": 2,
    "BLUE": 3,
    "WHITE": 4,
}


RUTAS_MATRIZ = {
    1: ejecutar_matriz_1,
    2: ejecutar_matriz_2,
    3: ejecutar_matriz_3,
    4: ejecutar_matriz_4,
    5: ejecutar_matriz_5,
}


MATRIZ_1 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

MATRIZ_2 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

MATRIZ_3 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

MATRIZ_4 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

MATRIZ_5 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]


MATRICES_VISUALES = {
    1: MATRIZ_1,
    2: MATRIZ_2,
    3: MATRIZ_3,
    4: MATRIZ_4,
    5: MATRIZ_5,
}


def nombre_color(color):
    if color == Color.GREEN:
        return "GREEN"

    if color == Color.YELLOW:
        return "YELLOW"

    if color == Color.BLUE:
        return "BLUE"

    if color == Color.RED:
        return "RED"

    if color == Color.WHITE:
        return "WHITE"

    return "NONE"


def identificar_matriz(robot):

    color_detectado = robot.seguidor.color()
    color_nombre = nombre_color(color_detectado)

    robot.lista_colores.append(color_nombre)

    print("Color detectado:", color_nombre)

    matriz_detectada = COLOR_A_MATRIZ.get(color_nombre)

    print("Matriz detectada:", matriz_detectada)

    return matriz_detectada


def imprimir_matriz(matriz_detectada):
    matriz = MATRICES_VISUALES.get(matriz_detectada)

    if matriz is None:
        print("Matriz visual no configurada.")
        return

    print("Matriz:")

    for fila in matriz:
        print(fila)


def ejecutar_matriz(robot, matriz_detectada):
    if matriz_detectada not in RUTAS_MATRIZ:
        print("No se detectó matriz válida.")
        print("Matriz por default:", MATRIZ_DEFAULT)
        matriz_detectada = MATRIZ_DEFAULT

    print("Ejecutando matriz:", matriz_detectada)

    imprimir_matriz(matriz_detectada)

    ruta = RUTAS_MATRIZ[matriz_detectada]
    ruta(robot)