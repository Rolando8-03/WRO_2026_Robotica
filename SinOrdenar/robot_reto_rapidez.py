from robot_control_rapidez import Base  
from pybricks.parameters import Color, Direction, Port, Stop 
from matriz import ejecutar_matriz 

robot = Base() 
print(robot.Hub.battery.voltage()) 
matriz_detectada = None 


#SECCION 1: =================================================================================
#giro de salida y seguidor hasta el cemento
robot.giro_arco_dc(radio_cm=9.6, angulo_deg=140, potencia=100, lado="derecha") 
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=65,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)

#giro para posicionarse frente al cemento y movimeinto torque para tomarlo
robot.girar(-90, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-17.5, grados_torque=-169.5, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 17.5 cm y activa el torque después de 1 cm para agarrar el balde.

#pequeño avance despues de tomar el cemento y giro en direccion a la llana
robot.mover_recto( distancia_cm=2.5, velocidad=1000, perfil="encadenado")
robot.girar(67.2, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado") 

robot.esperar(80)

#Retroceso para dejar la llana en su lugar y mov.recto para regresar a la linea
robot.retroceder(distancia_cm=46, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.mover_recto( distancia_cm=36.8, velocidad=1000, perfil="encadenado") 
#giro de arco para posicionarse sobre la linea
robot.giro_arco_dc( radio_cm=13, angulo_deg=19, potencia=80, lado="derecha")  # Hace un arco pequeño hacia la derecha para ajustar la dirección.

#SECCIÓN 2 (DEJAR EL CEMENTO) =================================================================================

#Seguir linea hasta lugar de cemento. Giro y moviminto toque para dejarlo en su lugar
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=37,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")
robot.esperar(100) 
robot.avanzar_con_torque(distancia_cm=-8, grados_torque=166, velocidad_robot=1200, velocidad_torque=300,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado") 

#SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =======================================================================

# SECCIÓN 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR

#Giro derecha para quedar frente a la linea. Seguidor hasta los blkancos y mov.torque para tomarlos
robot.esperar(150) #NO TOCAR ESA ESPERA
robot.giro_derecha(-90, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=10,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.esperar(300)
robot.girar( -170, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 170 grados en sentido negativo sin anticipación.

#AGARRAR LOS CEMENTOS BLANCOS
robot.avanzar_con_torque( distancia_cm=-24, grados_torque=-171, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 20 cm y activa el torque para tomar los cementos blancos.

# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.giro_izquierda( 70, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira usando principalmente el motor izquierdo para salir de la zona de agarre.

robot.mover_recto( distancia_cm=51, velocidad=1000, perfil="encadenado")  # Avanza 39 cm para acercarse a la línea frente a la matriz.

robot.esperar(300)
robot.girar( -50, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 60 grados en sentido negativo para alinearse con la línea.

#SEGUIR LINEA HASTA LA MATRIZ
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=92,
    distancia_cm=28,
    lado="derecha",

    tiempo_acomodo_ms=110,
    tiempo_aceleracion_ms=100,

    kp=1.35,
    kd=3.0,
    k_freno=0.22,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=330,
    potencia_captura=52,
    kp_captura=3.1,
    margen_captura=4,
    lecturas_estables_captura=1,

    perfil_salida="encadenado"
)

robot.esperar(100)
robot.mover_recto( distancia_cm=30.5, velocidad=700, perfil="encadenado")  # Avanza 40 cm para acercarse a la matriz.

robot.esperar(400)  # Espera 500 ms antes de escanear para que el robot esté quieto.

matriz_detectada = robot.escanear_matriz()  # Escanea la matriz y guarda el resultado en la variable.
print("Matriz guardada:", matriz_detectada)  # Muestra en pantalla la matriz detectada.


robot.retroceder(distancia_cm=40, velocidad=750, perfil="seguro", invertir_correccion=False, pausa_gyro=25)  # Retrocede 42 cm usando giroscopio para mantenerse recto.
robot.esperar(280)
robot.girar(160, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 60 grados en sentido negativo para alinearse con la línea.
robot.retroceder(distancia_cm=15.5, velocidad=750, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(300)
#giro para entrar en los cementos blancos y dejarlos
robot.girar(42, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
#dejar los cementos blancos
robot.avanzar_con_torque(distancia_cm=-17.5, grados_torque=150, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.mover_recto( distancia_cm=12.5, velocidad=1000, perfil="encadenado")
robot.girar(-41, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=39,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)

robot.esperar(250)
robot.girar(-165, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#AGARRAR LOS CEMENTOS VERDES
robot.avanzar_con_torque( distancia_cm=-19.5, grados_torque=-145, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")


robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=42,
    lado="izquierda",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.esperar(300)
robot.girar(-167, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#DEJAR LOS CEMENTOS VERDES
robot.avanzar_con_torque( distancia_cm=-23, grados_torque=170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=10,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.girar(-55, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.mover_recto( distancia_cm=20, velocidad=1000, perfil="encadenado")
robot.esperar(300)
robot.girar(47, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#SEGUIR LINEA HASTA LOS CEMENTOS AMARILLOS
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=10,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.esperar(300)
robot.girar(-167, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
#agarrar los cementos amarillos
robot.avanzar_con_torque( distancia_cm=-21, grados_torque=-169.8, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")


robot.mover_recto( distancia_cm=10, velocidad=1000, perfil="encadenado")
robot.esperar(300)
robot.girar(-70, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#avanzar a la linea para ir a los amarillos
robot.mover_recto( distancia_cm=56.5, velocidad=1000, perfil="encadenado") 
robot.girar(60, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=62.8,
    lado="izquierda",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.esperar(300)
robot.girar(-80, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#DEJAR LOS CEMENTOS AMARILLOS
robot.avanzar_con_torque( distancia_cm=-18.5, grados_torque=160, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

#salir de la seccion amarilla
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=9.5,
    lado="izquierda",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)
robot.esperar(300)
robot.girar(-65, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

#seguir linea para ir a los azules
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=46,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)

robot.esperar(300)

#Giro para ir a los azules
robot.girar(129, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.retroceder(distancia_cm=34, velocidad=800, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.giro_derecha(28, 1000, velocidad_min=260, anticipacion=0, zona_freno=28, perfil="seguro")

#AGARRAR LOS CEMENTOS AZULES
robot.avanzar_con_torque(distancia_cm=-20, grados_torque=-168, velocidad_robot=1200, velocidad_torque=600, torque_despues_cm=0,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=15,
    lado="derecha",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)

#giro para ir por los cementos azules
robot.esperar(300)
robot.girar(-28, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

robot.mover_garra(300, -95)
robot.mover_garra_delantera(850, 253)
robot.mover_recto( distancia_cm=41, velocidad=1000, perfil="encadenado")  # Avanza 1 cm para acomodar el mecanismo o liberar presión.
robot.mover_garra(300, 90)


robot.retroceder(distancia_cm=6.5, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.girar(28, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")


robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=137,
    lado="izquierda",

    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,

    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,

    objetivo_reflexion=27,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,

    perfil_salida="encadenado"
)
robot.mover_garra(300, -100)

#================================================

robot.retroceder(distancia_cm=11.5, velocidad=800, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(280)
robot.girar(85, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.mover_torque(-170, 800, esperar= False, modo_final= Stop.HOLD)
