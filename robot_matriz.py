def ejecutar_matriz(robot, matriz_detectada):
    """
    Ejecuta el recorrido de matriz dependiendo de lo que
    el robot detectó durante el reto principal.
    """

    print("Matriz detectada:", matriz_detectada)

    if matriz_detectada == 1:
        ejecutar_matriz_1(robot)

    elif matriz_detectada == 2:
        ejecutar_matriz_2(robot)

    elif matriz_detectada == 3:
        ejecutar_matriz_3(robot)

    elif matriz_detectada == 4:
        ejecutar_matriz_4(robot)

    else:
        print("No se detectó una matriz válida. No se ejecuta recorrido de matriz.")


def ejecutar_matriz_1(robot):
    print("Ejecutando recorrido de matriz 1")

    # Aquí pones el recorrido real de la matriz 1.
    # Por ahora puedes dejarlo vacío o copiar aquí cuando lo tengas.
    pass


def ejecutar_matriz_2(robot):
    print("Ejecutando recorrido de matriz 2")

    # Aquí pones el recorrido real de la matriz 2.
    pass


def ejecutar_matriz_3(robot):
    print("Ejecutando recorrido de matriz 3")

    # Aquí pones el recorrido real de la matriz 3.
    pass


def ejecutar_matriz_4(robot):
    print("Ejecutando recorrido de matriz 4")

    # CODIGO PARA LA PRIMERA MATRIZ
    robot.seguir_linea(
        robot.seguidor,
        velocidad_max=100,
        distancia_cm=31.5,
        kp=0.48,
        kd=1.70,
        k_freno=0.52,
        tiempo_acomodo_ms=400
    )

    robot.girar(-89, 500)
    robot.mover_recto(15.5, 850)
    robot.mover_garra(150, -130)  # abrir la garra
    robot.mover_garra_delantera(300, 286)

    robot.retroceder_recto(25, 600)
    robot.girar(90, 500)
    robot.retroceder_recto(14.5, 600)
    robot.girar(-89, 500)

    robot.mover_garra_delantera(300, -286)
    robot.mover_recto(24.5, 850)
    robot.mover_garra_delantera(300, 279)
    robot.retroceder_recto(14.5, 600)
    robot.girar(89, 500)
    robot.mover_recto(8.75, 800)
    robot.girar(-88, 500)

    robot.mover_garra(150, 105)
    robot.mover_garra_delantera(300, -60)
    robot.mover_recto(16.5, 900)
    robot.mover_garra_delantera(300, 63)
    robot.mover_garra(150, 25)

    robot.retroceder_recto(30, 600)
    robot.girar(90, 500)
    robot.mover_garra(150, -130)
    robot.mover_garra_delantera(300, -286)

    robot.retroceder_recto(20, 600)
    robot.mover_garra_delantera(300, 286)
    robot.mover_recto(22, 900)

    robot.mover_garra(150, 115)
    robot.esperar(10)
    robot.mover_garra(150, -115)

    robot.retroceder_recto(13, 600)
    robot.mover_garra_delantera(300, -286)

    # Segunda matriz
    robot.girar(-91, 500)
    robot.mover_garra(150, 130)
    robot.mover_recto(40, 900)
    robot.mover_garra_delantera(300, 286)
