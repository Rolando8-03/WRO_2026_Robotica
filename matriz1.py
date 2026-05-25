def main():
    #Inicializar clase, matriz y batería
    robot = Robot()
    robot.mostrar_bateria()
    matriz_detectada = None

    ejecutar_matriz1()

if __name__ == "__main__":
    main()
    
def ejecutar_matriz_1(robot):
    print("Ejecutando recorrido de matriz 1")

    robot.seguir_linea(31.5,"derecha",100,tiempo_acomodo_ms=400,kp=0.48,kd=1.70,k_freno=0.52)

    robot.girar(-89, 500)

    robot.avanzar(15.5, 850)

    robot.mover_garra(-130, velocidad=150)
    robot.mover_garra_delantera(286, velocidad=300)

    robot.retroceder(25, 600)

    robot.girar(90, 500)

    robot.retroceder(14.5, 600)

    robot.girar(-89, 500)

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
