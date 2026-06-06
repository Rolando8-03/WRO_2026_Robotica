def ejecutar_matriz_3(robot):
    print("Ejecutando recorrido de matriz 3")
    pass

from robot_control_rapidez import Base
import gc

robot = Base()
print(robot.Hub.battery.voltage()) 

# SECCION DE MOVIMIENTO PARA LOS VERDES ------------------------------------
# seguir la linea hasta llegar a los verdes
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=45.5,
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

# el robot gira para agarrar los cementos verdes
robot.girar_modo_bestia_elite(
    angulo_deg=-90,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)
robot.mover_garra_rapida(potencia=300, grados=39, abrir=True) # abrir la garra
robot.mover_garra_delantera(850, 276) # bajar la garra
robot.mover_recto_supremo(distancia_cm=12) # avanzar un poco para agarrar los cementos
robot.mover_garra_rapida(potencia=300, grados=-38, abrir=False) # cerrar la garra para tomar los verdes

robot.mover_recto_supremo(distancia_cm=-8.5) # RETROCESO PARA AGARRAR LA LINEA DESPUES DE TOMAR LOS VERDES
robot.girar_modo_bestia_elite(
    angulo_deg=-90,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
) # giro sobre la linea

robot.mover_garra_rapida(potencia=300, grados=50, abrir=True) # abrir la garra
robot.mover_garra_delantera(850, -285) # subir la garra 

robot.esperar(100)
robot.mover_recto_supremo(distancia_cm=-3) # retroceder un poco antes de acomodar los verdes
robot.esperar(100)

# Seguir la linea para acomodar los verdes
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=33.2,
    lado="derecha",
    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,
    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,
    objetivo_reflexion=27.1,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
) 


# SECCION PARA AGARRAR LOS CEMENTOS AMARILLOS----------------------------------------
# giro para agarrar los blancos
robot.girar_modo_bestia_elite(
    angulo_deg=92,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)
robot.mover_garra_rapida(potencia=300, grados=12, abrir=True) # abrir la garra
robot.mover_garra_delantera(850, 285) # bajar la garra
robot.mover_recto_supremo(distancia_cm=11) # mover recto para tomar los amarillos
robot.mover_garra_rapida(potencia=300, grados=-38, abrir=False) # cerrar la garra

robot.mover_recto_supremo(distancia_cm=-15.5) # Retroceder despues de agarrar los amarillos

# girar para tomar la linea con los amarillos
robot.girar_modo_bestia_elite(
    angulo_deg=92,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)
robot.esperar(100)


robot.mover_recto_supremo(distancia_cm=-16.8) # retroceder para acomodar los amarillos
robot.mover_garra_rapida(potencia=300, grados=50, abrir=True) # Soltar la garra
robot.mover_garra_delantera(850, -285) # subir la garra

# seguir la linea para acomodar la amarillos
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=55.3,
    lado="izquierda",
    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,
    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,
    objetivo_reflexion=27.1,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)

# SECCION DE AGARRAR LOS BLANCOS -----------------------------------------------------

# bajar la garra antes de girar por los blancos
robot.mover_garra_delantera(850, 285)
robot.mover_recto_supremo(distancia_cm=2) # avanzar para tomar los cementos blancos

# girar para tomar los cementos blancos
robot.girar_modo_bestia_elite(
    angulo_deg=-92,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)

robot.mover_garra_rapida(potencia=300, grados=13, abrir=True) # abrir la garra
robot.mover_recto_supremo(distancia_cm=13) # avanzar para tomar los cementos blancos

robot.mover_garra_rapida(potencia=300, grados=-43, abrir=False) # cerrar la garra para tomar los blancos
robot.mover_garra_delantera(850, -10) # subir un poco la garra

robot.mover_recto_supremo(distancia_cm=-14) # retroceder con los blancos


robot.esperar(300)
# girar para seguir la linea con los blancos
robot.girar_modo_bestia_elite(
    angulo_deg=-96.3,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)

robot.mover_garra_rapida(potencia=300, grados=45, abrir=True) # soltar los blancos de la garra
robot.mover_garra_delantera(850, -290) # subir la garra

robot.mover_recto_supremo(distancia_cm=-25) # retroceder para acomodar los amarillos

robot.mover_garra_rapida(potencia=300, grados=53, abrir=True) # abrir por completo la garra
robot.mover_garra_delantera(850, 291) # bajar la garra

robot.esperar(300)
# SECCION DE ACOMODO DE LOS CEMENTOS----------------------------------------------------
robot.mover_recto_supremo(
    distancia_cm=40, 
    velocidad_max=700,     # Velocidad de tortuga
    velocidad_min=20,      # Apenas lo suficiente para romper inercia
    kp_gyro=0.0,           # ¡La clave! Relajamos al dictador espacial
    zona_rampa_cm=2        # Rampa cortita para 4 cm
)


robot.esperar(100)
robot.mover_recto_supremo(distancia_cm=-1) 

robot.mover_garra_rapida(potencia=300, grados=-55, abrir=False) # Cerrar la garra
robot.mover_garra_delantera(850, -25) # bajar la garra
robot.girar_modo_bestia_elite(
    angulo_deg=-91,          
    potencia_max=100,       
    potencia_min=18,
    kp_base=2.2,
    kd_base=1.8,
    tolerancia_fin=2.0 
)


robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=90,
    distancia_cm=20,
    lado="izquierda",
    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=140,
    kp=1.25,
    kd=2.7,
    k_freno=0.16,
    correccion_max=100,
    objetivo_reflexion=27.1,
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)

robot.mover_garra_delantera(850, -70) # subir la garra

robot.mover_recto(30, 750)
