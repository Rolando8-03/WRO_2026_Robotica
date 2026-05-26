def ejecutar_matriz_2(robot):
    print("Ejecutando recorrido de matriz 2")
"Inicio del recorrido para ir a buscar el primer color para llevar del mosaico seleccionado
    robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=34,
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

"Giro para ponerse frente a los colores"
robot.esperar(300)
robot.girar(-84, velocidad=900, velocidad_min=160, anticipacion=8, perfil="encadenado")

"Seguidor para acomodarse recto y utilizar un avance mecanico para alcanzar los 4 bloques y utilizar el torque para agarrarlos"
robot.mover_garra(300, 90, esperar= False)
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=7,
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
robot.esperar(100)
robot.mover_recto( distancia_cm=10, velocidad=1000, perfil="encadenado")
robot.mover_garra_delantera(600, 293)

"Retroceso mas giros para ir a buscar la otra parte de la mitad del mosaico, junto con seguidor de linea para poder acomodarse recto"
robot.esperar(500)
robot.retroceder(distancia_cm=23, velocidad=700, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(500)
robot.girar(-90, velocidad=900, velocidad_min=160, anticipacion=8, perfil="encadenado")
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=7,
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

"Giros para posicionarse frente a los colores, que en esta ocasion son dos amarillos y agarrarlos"
robot.esperar(500)
robot.girar(90, velocidad=800, velocidad_min=160, anticipacion=8, perfil="encadenado")
robot.esperar(500)
robot.mover_garra(300,-45, esperar= False, apretar= False)
robot.esperar(500)
robot.mover_recto( distancia_cm=14, velocidad=900, perfil="encadenado")
robot.mover_garra(300,-35, esperar= False, apretar= False)
robot.retroceder(distancia_cm=3, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=25)


"Retroceso con diferentes movimientos para tener espacio para poder acomodar los 6 bloques y poder llevarlos hacia el mosaico"
robot.retroceder(distancia_cm=14, velocidad=700, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.mover_garra(300, 80, esperar= False)
robot.mover_garra_delantera(600, -70)
robot.retroceder(distancia_cm=14, velocidad=700, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.mover_garra_delantera(600, 60)
robot.mover_recto( distancia_cm=18, velocidad=1000, perfil="encadenado")
robot.mover_garra(500,-50, esperar= False, potencia_apriete=70)
robot.retroceder(distancia_cm=6, velocidad=700, perfil="seguro", invertir_correccion=False, pausa_gyro=25)

"Giros y avance recto para ir a posicionarse frente al mosaico"
robot.esperar(500)
robot.girar(90, velocidad=700, velocidad_min=160, anticipacion=8, perfil="encadenado")
robot.mover_recto( distancia_cm=16, velocidad=1000, perfil="encadenado")
robot.esperar(500)
robot.girar(85, velocidad=700, velocidad_min=160, anticipacion=8, perfil="encadenado")

"Seguidor para quedar recto frente al mosaico"
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=12,
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
"Avance mecanico con levantamiento de garra con los 6 bloques y dejarlos en el mosaico"
robot.esperar(100)
robot.mover_garra_delantera(200, -60)
robot.mover_recto( distancia_cm=28, velocidad=800, perfil="encadenado")
robot.retroceder(distancia_cm=8, velocidad=700, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.mover_garra(500,55, esperar= False)
