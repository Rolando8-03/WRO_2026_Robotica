def ejecutar_matriz_1(robot):
    print("Ejecutando recorrido de matriz 1")

    robot.mover_garra(-130, velocidad=850)
    robot.seguir_linea(30, "derecha")
    robot.girar(-92, 1000, 8)
    robot.avanzar(8.75)
    robot.mover_garra_delantera(286, velocidad=850)
    #Aqui ya agarro los primeros dos bloques verdes
    
    robot.retroceder(8, 800)
    robot.girar(-91, 1000, 8)
    robot.avanzar(17)
    robot.girar(73.05, 1000)
    robot.esperar(300)
    '''
    robot.mover_garra_delantera(-140, velocidad=850)
    robot.avanzar(13.75)
    robot.mover_garra_delantera(140, velocidad=850)
    #Aqui ya agarro los dos bloques azules
    
    robot.retroceder(9, 800)
    robot.girar(89, 1000,8)
    robot.avanzar(4.5)
    robot.girar(-86, 1000,8)
    robot.mover_garra(100, velocidad=850)
    robot.avanzar(16)
    robot.mover_garra(50, velocidad=850)
    #Aqui ya agarro los ultimos dos bloques de en medio de la matriz
    
    robot.retroceder(10)
    robot.giro_izquierda(-92)
    robot.mover_garra(-130, velocidad=850)
    robot.mover_garra_delantera(-140, velocidad=850)
    robot.retroceder(10)
    robot.mover_garra_delantera(140, velocidad=850)
    robot.avanzar(15)
    robot.mover_garra(100, velocidad=850)
    robot.giro_derecha(-90)
    #Aqui se posiciona enfrente de la linea de la matriz
    
    robot.seguir_linea(20)
    robot.avanzar(10)
    robot.mover_garra_delantera(-140, velocidad=850)
    robot.avanzar(15)
    robot.mover_garra_delantera(100, velocidad=850)
    robot.mover_garra(-130, velocidad=850)
    robot.mover_garra_delantera(-100, velocidad=850)
    #Aqui ya puso los bloques en la matriz

    robot.retroceder(40)
    robot.girar(90,1000,8)
    robot.avanzar(10)
    robot.girar(-90,1000,8)
    robot.mover_garra_delantera(-140, velocidad=850)
    robot.avanzar(15)
    robot.mover_garra_delantera(140, velocidad=850)
    #Aqui ya agarro los otros dos bloques de la matriz

    robot.retroceder(15)
    robot.giro_derecha(90)
    robot.avanzar(15)
    robot.girar(-90,1000,8)
    '''

from robot import Robot

def main():
    robot = Robot()
    robot.mostrar_bateria()

    ejecutar_matriz_1(robot)

if __name__ == "__main__":
    main()
