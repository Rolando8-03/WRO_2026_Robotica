from pybricks.parameters import Stop
from matriz_router import identificar_matriz


def inicio(robot):
    #Inicio del robot a 3cm del borde azul
    robot.arcgirar(9.6, 140, 100, "derecha")
    robot.seguir_linea(65, "derecha")
    robot.girar(-90, 1000, 8)

    #Aqui se posiciona para agarrar el balde de cemento
    robot.avanzar_con_torque(-17.5,-169.5,velocidad_torque=500)
    robot.avanzar(2.5)
    robot.girar(67.2, 1000, 8)
    robot.esperar(80)

    #Aqui retrocede para empujar la pala 
    robot.retroceder(46, 870)


def dejar_balde_cemento(robot):
    #Aqui sale de la pala y se acomoda para seguir la linea hasta el parqueo
    robot.avanzar(36.8)
    robot.arcgirar(13, 19, 80, "derecha")
    robot.seguir_linea(37, "derecha")

    #Aqui se posiciona para dejar el balde de cemento
    robot.girar(90, 850, 8)
    robot.esperar(100)
    robot.avanzar_con_torque(-8,166,velocidad_torque=300)


def blancos(robot):
    #Aqui se corrige para seguir la línea y traer los cementos
    robot.esperar(150)  
    robot.giro_derecha(-90, 1200, 10, 160, "encadenado")
    robot.seguir_linea(10, "derecha")
    robot.esperar(300)

    #Aqui se posiciona enfrente de los cementos blancos
    robot.girar(-170, 1200, 0)
    robot.avanzar_con_torque(-24,-171, 350)
    robot.giro_izquierda(70, 1200, 10, 160, "encadenado")

    #Aqui avanza para posicionarse enfrente de la matriz
    robot.avanzar(51)
    robot.esperar(300)
    robot.girar(-50, 1200, 0)

    # Seguir línea hasta la matriz
    robot.seguir_linea(28,"derecha",92,110,100, kp=1.35, kd=3.0,k_freno=0.22, tiempo_captura_ms=330,
    potencia_captura=52,kp_captura=3.1,margen_captura=4,lecturas_estables_captura=1)

    #Entrar en la matriz para identificarla
    robot.esperar(100)
    robot.avanzar(30.5, 700)
    robot.esperar(400)
    matriz_detectada = identificar_matriz(robot)

    #Salir de la matriz y acomodarse para dejar los cementos blancos
    robot.retroceder(40, 750)
    robot.esperar(280)
    robot.girar(160, 1200, 0)
    robot.retroceder(15.5, 750)
    robot.esperar(300)

    # Girar y dejar cementos blancos
    robot.girar(42, 1200, 0)
    robot.avanzar_con_torque(-17.5, 150, 500)

    #Salir de la zona y posicionarse para seguir la línea hacia los verdes
    robot.avanzar(12.5)
    robot.girar(-41, 1200, 0)
    return matriz_detectada


def verdes(robot):
    #Después de posicionarse, sigue la linea y gira para agarrarlos
    robot.seguir_linea(39, "derecha")
    robot.esperar(250)
    robot.girar(-165, 1200, 0)
    robot.avanzar_con_torque(-19.5,-145,350)

    #Sigue la línea y deja los cementos verdes
    robot.seguir_linea(42, "izquierda")
    robot.esperar(300)
    robot.girar(-167, 1200, 0)
    robot.avanzar_con_torque(-23,170,350)


def amarillos(robot):
    #Sale de los verdes y maniobra para acomodarse en la línea de los amarillos
    robot.seguir_linea(10, "derecha")
    robot.girar(-55, 1200, 0)
    robot.avanzar(20)
    robot.esperar(300)
    robot.girar(47, 1200, 0)

    #Se acomoda y agarra los cementos amarillos
    robot.seguir_linea(10, "derecha")
    robot.esperar(300)
    robot.girar(-167, 1200, 0)
    robot.avanzar_con_torque(-21,-169.8,500)

    #Sale de los amarillos y maniobra para dejarlos
    robot.avanzar(10)
    robot.esperar(300)
    robot.girar(-70, 1200, 0)

    #Se posiciona en la línea y la sigue para dejar los cementos 
    robot.avanzar(56.5)
    robot.girar(60, 1200, 0)
    robot.seguir_linea(62.8, "izquierda")
    robot.esperar(300)

    #Gira y deja los cementos
    robot.girar(-80, 1200, 0)
    robot.avanzar_con_torque(-18.5, 160,350)

    # Salir de la sección amarilla
    robot.seguir_linea(9.5, "izquierda")
    robot.esperar(300)
    robot.girar(-65, 1200, 0)


def azules(robot):
    #Después de salir de la zona, se dirige a los azules
    robot.seguir_linea(46, "derecha")
    robot.esperar(300)
    robot.girar(129, 1200, 0)

    #Aquí se posiciona y agarra los cementos azules
    robot.retroceder(34, 800)
    robot.giro_derecha(28,1000,0,zona_freno=28)
    robot.avanzar_con_torque(-20,-168,600,torque_despues_cm=0,)

    #Aqui sale de la zona azul y se dirige a agarrar la paleta 
    robot.seguir_linea(15, "derecha")
    robot.esperar(300)
    robot.girar(-28, 1200, 0)

    #Aqui se posiciona y agarra la paleta
    robot.mover_garra(-95, velocidad=300)
    robot.mover_garra_delantera(253, velocidad=850)
    robot.avanzar(41)
    robot.mover_garra(90, velocidad=300)

    #Aqui se acomoda para seguir la línea e ir a la zona de inicio
    robot.retroceder(6.5, 870)
    robot.girar(28, 1200, 0)
    robot.seguir_linea(137, "izquierda")

    #Aqui llega al inicio, deja la paleta y se posiciona para hacer la matriz
    robot.mover_garra(-100, velocidad=300)
    robot.retroceder(15.5, 800)
    robot.esperar(280)
    robot.girar(75, 1200, 0)
    robot.mover_torque(175,800,esperar=False,modo_final=Stop.HOLD)