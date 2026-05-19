from robot import Robot
from Misiones.retos_principales import inicio, dejar_balde_cemento, blancos, verdes, amarillos, azules
from Misiones.matriz_router import ejecutar_matriz


def main():
    #Inicializar clase, matriz y batería
    robot = Robot()
    robot.mostrar_bateria()
    matriz_detectada = None

    #Ejecutar herramientas
    inicio(robot)
    dejar_balde_cemento(robot)

    #Ejecutar cementos
    matriz_detectada = blancos(robot)
    verdes(robot)
    amarillos(robot)
    azules(robot)

    ejecutar_matriz(robot, matriz_detectada)


if __name__ == "__main__":
    main()