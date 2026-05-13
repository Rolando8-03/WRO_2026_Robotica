from pybricks.parameters import Color
from pybricks.tools import wait
from matriz.matriz_1 import ejecutar_matriz_1
from matriz.matriz_2 import ejecutar_matriz_2
from matriz.matriz_3 import ejecutar_matriz_3
from matriz.matriz_4 import ejecutar_matriz_4
from matriz.matriz_5 import ejecutar_matriz_5

def escanear_matriz(robot):
    colores_detectados = [];robot.frenar(); wait(250)
    for i in range(25):
        color = robot.seguidor.color()
        if color is not None: colores_detectados.append(color)
        wait(40)
    if not colores_detectados: return None
    verdes = colores_detectados.count(Color.GREEN); amarillos = colores_detectados.count(Color.YELLOW)
    azules = colores_detectados.count(Color.BLUE); rojos = colores_detectados.count(Color.RED)
    blancos = colores_detectados.count(Color.WHITE); print(f"Resultados: V:{verdes} | A:{amarillos} | Az:{azules} | R:{rojos} | B:{blancos}")
    mayor = max(verdes, amarillos, azules, rojos, blancos)
    if mayor < 3: return None
    if mayor == verdes: id_matriz = 1
    elif mayor == amarillos: id_matriz = 2
    elif mayor == azules: id_matriz = 3
    elif mayor == rojos: id_matriz = 4
    elif mayor == blancos: id_matriz = 5
    else: id_matriz = None
    print(f"Matriz identificada: {id_matriz}")
    return id_matriz

def ejecutar_matriz(robot, matriz_detectada):
    print(f"Router activado para Matriz: {matriz_detectada}")
    if matriz_detectada == 1: ejecutar_matriz_1(robot)
    elif matriz_detectada == 2: ejecutar_matriz_2(robot)
    elif matriz_detectada == 3: ejecutar_matriz_3(robot)
    elif matriz_detectada == 4: ejecutar_matriz_4(robot)
    elif matriz_detectada == 5: ejecutar_matriz_5(robot)
    else:
        print("ALERTA: No se ejecutará ninguna matriz. ID no válido.")