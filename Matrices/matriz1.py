def matriz1_verdes_azules():
        print("Ejecutando recorrido de matriz 1")

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
    robot.mover_garra(150, -130)
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