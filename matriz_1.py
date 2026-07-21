from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait

def ejecutar_matriz_1(robot):
    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 1")

    robot.avanzar_cruzando_lineas(cruces_objetivo=3,velocidad=900,retraso_freno_ms=95.5)
    robot.mover_garra_principal(850, 130)
    robot.girar(-90, potencia_max=100)
    robot.avanzar_recto(5, 800)
    robot.mover_garra_delantera(850, 286)
    #Aqui ya agarro los primeros dos bloques verdes

    robot.avanzar_recto(-8, 800)
    robot.girar(-90, potencia_max=100)
    robot.avanzar_recto(13)
    robot.girar(92, potencia_max=100)
    robot.mover_garra_delantera(850, -286)
    robot.avanzar_recto(8, 800)
    robot.mover_garra_delantera(850, 276)
    wait(300)
    #Aqui ya agarro los dos bloques azules

    robot.avanzar_recto(-8.5, 800)
    robot.girar(88, potencia_max=100)
    robot.avanzar_recto(9.5)
    robot.girar(-90, potencia_max=80)
    robot.mover_garra_principal(850, -105,apretar=False)
    robot.avanzar_recto(11)
    robot.mover_garra_principal(850, -30,apretar=True)
    #Aqui ya agarro los ultimos dos bloques de en medio de la matriz

    robot.avanzar_recto(-11)
    robot.girar(-90)
    robot.avanzar_recto(3)
    robot.girar(-90)
    robot.avanzar_recto(3)
    #Aqui se coloca en la línea del seguidor para la matriz

    robot.dejar_bloques_matriz(robot)
    
    robot.girar(-168)
    '''
    robot.avanzar_recto(7)
    robot.seguir_linea(distancia_cm=15)
    robot.avanzar_recto(18)
    robot.girar(-90)
    robot.avanzar_recto(7)
    robot.girar(90)
    robot.avanzar_recto(15)
    robot.mover_garra_delantera(850, 286)
    #Aqui ya agarró los últimos 4 bloques azules

    robot.avanzar_recto(-8)
    robot.girar(90)
    robot.avanzar_recto(12)
    robot.girar(-90)
    robot.mover_garra_principal(850, -105,apretar=False)
    robot.avanzar_recto(11)
    robot.mover_garra_principal(850, -30,apretar=True)
    #Aqui ya agarró los últimos dos bloques verdes de la matriz

    robot.avanzar_recto(-11)
    robot.girar(-90)
    robot.avanzar_recto(6)
    robot.girar(-90)
    robot.avanzar_recto(3)
    #Aqui se coloca en la línea del seguidor para la matriz

    robot.dejar_bloques_matriz(robot)
    '''
    
if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_1(robot)
