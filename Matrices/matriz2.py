def ejecutar_matriz_2(robot):
    print("Ejecutando recorrido de matriz 2")

    robot.seguir_linea(32, "derecha")

    robot.esperar(300)

    robot.girar(-84, 900, 8)

    robot.mover_garra(-90, velocidad=300)

    robot.seguir_linea(7, "derecha")

    robot.esperar(100)

    robot.avanzar(9.5)

    robot.mover_garra_delantera(293, velocidad=600)

    robot.esperar(280)

    robot.retroceder(24, 700)

    robot.esperar(300)

    robot.girar(-95, 900, 8)

    robot.avanzar(11)

    robot.esperar(300)

    robot.girar(82.5, 900, 8)

    robot.mover_garra_delantera(-50, velocidad=600)

    robot.mover_garra(50, velocidad=300)

    robot.avanzar(9)

    robot.mover_garra_delantera(70, velocidad=600)

    robot.mover_garra(45, velocidad=300)

    robot.avanzar(1)

    robot.mover_garra(50, velocidad=300)

    """
    robot.retroceder(20, 700)
    robot.girar(90, 900, 8)
    robot.avanzar(10)
    robot.girar(90, 900, 8)
    """