def ejecutar_matriz_2(robot):
    print("Ejecutando recorrido de matriz 2")

    robot.seguir_linea(36)
    robot.esperar(300)
    robot.girar(-80)
    robot.mover_garra(300)
    robot.seguir_linea(7)
    robot.esperar(100)
    robot.avanzar(12.5)

    robot.mover_garra_delantera(293, velocidad=800)
    robot.retroceder(22)
    robot.esperar(300)
    robot.girar(-80)
    robot.seguir_linea(12)

    robot.esperar(300)
    robot.girar(79)
    robot.mover_garra_delantera(-30, velocidad=600)
    robot.mover_garra(500)

    robot.avanzar(14)
    robot.mover_garra_delantera(30, velocidad=600)
    robot.mover_garra(500)

    robot.retroceder(3)
    robot.retroceder(11)
    robot.esperar(500)
    robot.girar(75)
    robot.seguir_linea(18)
    robot.esperar(500)
    robot.girar(80)
    robot.seguir_linea(13)

    robot.mover_garra(500, 80)
    robot.mover_garra_delantera(600, -90)
    robot.esperar(300)
    robot.retroceder(12)
    robot.mover_garra_delantera(600, 80)
    robot.avanzar(14)
    robot.mover_garra(500)

    robot.mover_garra_delantera(600, -50)
    robot.seguir_linea(10)
    robot.esperar(100)

    robot.mover_garra_delantera(500, -250)
    robot.esperar(300)
    robot.avanzar(13)
    robot.mover_garra_delantera(400, 235)

    robot.mover_garra(100)

'''
#Para pruebas solo con la matriz descomentar esta parte
from robot import Robot

def main():
    robot = Robot()
    robot.mostrar_bateria()

    ejecutar_matriz_1(robot)

if __name__ == "__main__":
    main()
'''
