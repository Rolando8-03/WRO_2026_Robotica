def ejecutar_matriz_1(robot):
    print("Ejecutando recorrido de matriz 1")

    robot.mover_garra(-130, velocidad=850)
    robot.seguir_linea(29, "derecha")
    robot.girar(-92, 1000, 8)
    robot.avanzar(8.5)
    robot.mover_garra_delantera(286, velocidad=850)
    #Aqui ya agarro los primeros dos bloques verdes

    robot.retroceder(10, 800)
    robot.girar(-90, 1000, 8)
    robot.seguir_linea(13,"izquierda")
    robot.esperar(300)
    robot.girar(80, 1000, 8)
    robot.esperar(300)
    robot.mover_garra_delantera(-140, velocidad=850)
    robot.avanzar(16)
    robot.mover_garra_delantera(140, velocidad=850)
    #Aqui ya agarro los dos bloques azules

    robot.retroceder(12, 800)
    robot.girar(89, 1000,8)
    robot.avanzar(3)
    robot.girar(-82, 1000,8)
    robot.mover_garra(90, velocidad=850)
    robot.avanzar(15)
    robot.mover_garra(30, velocidad=850)
    #Aqui ya agarro los ultimos dos bloques de en medio de la matriz

    robot.retroceder(10)
    robot.giro_izquierda(-90)
    robot.mover_garra(-130, velocidad=850)
    '''
    robot.mover_garra_delantera(-286, velocidad=300)

    robot.avanzar(24.5, 850)

    robot.mover_garra_delantera(279, velocidad=300)

    robot.retroceder(14.5, 600)

    robot.girar(89, 500)

    robot.avanzar(8.75, 800)

    robot.girar(-88, 500)

    robot.mover_garra(105, velocidad=150)
    robot.mover_garra_delantera(-60, velocidad=300)

    robot.avanzar(16.5, 900)

    robot.mover_garra_delantera(63, velocidad=300)
    robot.mover_garra(25, velocidad=150)

    robot.retroceder(30, 600)

    robot.girar(90, 500)

    robot.mover_garra(-130, velocidad=150)
    robot.mover_garra_delantera(-286, velocidad=300)

    robot.retroceder(20, 600)

    robot.mover_garra_delantera(286, velocidad=300)

    robot.avanzar(22, 900)

    robot.mover_garra(115, velocidad=150)

    robot.esperar(10)

    robot.mover_garra(-115, velocidad=150)

    robot.retroceder(13, 600)

    robot.mover_garra_delantera(-286, velocidad=300)
    '''

from robot import Robot

def main():
    robot = Robot()
    robot.mostrar_bateria()

    ejecutar_matriz_1(robot)

if __name__ == "__main__":
    main()
