from control_drivebase import Base
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait
from robot_control_rapidez import Base
from MATRIZ2 import ejecutar_matriz_2

robot = Base() 
print("Voltaje:", robot.Hub.battery.voltage()) 
matriz_detectada = None 

# SECCION 1: =================================================================================
# Giro de salida y seguidor hasta el cemento
robot.giro_de_arco(
    radio_cm=30,        # Radio del arco
    angulo_deg=100,      # Ángulo a girar
    potencia_max=90,    # Velocidad máxima del arco
    lado="derecha"      # La rueda derecha va por fuera
)

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=80,           
    velocidad_max=100,         
    lado="derecha",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=80,  
    
    #CEREBRO PREDICTIVO (PID):
    kp=1.15,                   
    kd=3.8,                    
    k_freno=0.05,              
    
    correccion_max=100,
    objetivo_reflexion=27,     
    
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=60,
    kp_captura=2.5,
    perfil_salida="encadenado"
)

# Giro para posicionarse frente al cemento y movimiento simultáneo para tomarlo
robot.girar(angulo_deg=-90, potencia_max=100, perfil="encadenado")

# ACTIVAMOS TORQUE SIN ESPERAR Y LUEGO RETROCEDEMOS
robot.mover_torque(grados_torque=-169.5, velocidad_torque=500, esperar=False)
robot.avanzar_recto(distancia_cm=-18, velocidad_max=900, perfil="encadenado") 

# Pequeño avance despues de tomar el cemento y giro en direccion a la llana
robot.avanzar_recto(distancia_cm=7, velocidad_max=900, perfil="encadenado")
robot.girar(angulo_deg=77, potencia_max=100, perfil="encadenado") 

# Retroceso para dejar la llana en su lugar y mov.recto para regresar a la linea
robot.avanzar_recto(distancia_cm=-35, velocidad_max=900, perfil="seguro")
# Cruzar 3 líneas y detenerse un poquito después de la tercera
robot.avanzar_cruzando_lineas(
    cruces_objetivo=3, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=0 # Sigue retrocediendo 150 milisegundos después de ver la 3ra línea
)

# Giro de arco para posicionarse sobre la linea
robot.giro_de_arco(
    radio_cm=13,        # Radio del arco
    angulo_deg=19,      # Ángulo a girar
    potencia_max=90,    # Velocidad máxima del arco
    lado="derecha"      # La rueda derecha va por fuera
)

# SECCIÓN 2 (DEJAR EL CEMENTO) =================================================================================

# Seguir linea hasta lugar de cemento. Giro y movimiento torque para dejarlo en su lugar
robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=42,           
    velocidad_max=100,         
    lado="derecha",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=80,  
    
    #CEREBRO PREDICTIVO (PID):
    kp=1.15,                   
    kd=3.8,                    
    k_freno=0.05,              
    
    correccion_max=100,
    objetivo_reflexion=27,     
    
    captura_inicial=True,
    tiempo_captura_ms=450,
    potencia_captura=35,
    kp_captura=3.5,
    margen_captura=4,
    lecturas_estables_captura=4,
    perfil_salida="encadenado"
)

robot.girar(angulo_deg=90, potencia_max=85, perfil="encadenado")
wait(100) 

robot.mover_torque(grados_torque=166, velocidad_torque=300, esperar=False)
robot.avanzar_recto(distancia_cm=-2.5, velocidad_max=900, perfil="encadenado") 

# SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =======================================================================
robot.giro_derecha(-96, 900)
robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=14,           
    velocidad_max=100,
    lado="derecha",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=80,  
    
    #CEREBRO PREDICTIVO (PID):
    kp=1.15,                   
    kd=3.8,                    
    k_freno=0.05,              
    
    correccion_max=100,
    objetivo_reflexion=27,     
    
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=55,
    kp_captura=3.8,
    perfil_salida="encadenado"
)
robot.girar(angulo_deg=-185, potencia_max=100, perfil="encadenado")  

# AGARRAR LOS CEMENTOS BLANCOS
robot.mover_torque(grados_torque=-170, velocidad_torque=250, esperar=False)
robot.avanzar_recto(distancia_cm=-24, velocidad_max=900, perfil="encadenado")


# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.avanzar_recto(10, 900)
robot.girar(angulo_deg=54, potencia_max=90, perfil="encadenado")
wait(80)

robot.avanzar_cruzando_lineas(
    cruces_objetivo=3, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=90 
)

robot.girar(angulo_deg=-54.5, potencia_max=100, perfil="encadenado") 

#SEGUIR LINEA HASTA LA MATRIZ
robot.seguir_linea_hasta_color(
    color_objetivo=Color.GREEN, 
    velocidad_max=100, 
    lado="izquierda"
)
robot.giro_izquierda(15, 800)
robot.avanzar_recto(13, 700)

matriz_detectada = robot.escanear_matriz()
print("Resultado final:", matriz_detectada)

#Salir de la matriz
robot.avanzar_recto(distancia_cm=-40, velocidad_max=900, perfil="seguro") 
wait(90)
robot.girar(angulo_deg=-181, potencia_max=100, perfil="encadenado")
robot.avanzar_recto(distancia_cm=-21, velocidad_max=900, perfil="seguro") 
wait(300)

# Giro para entrar en los cementos blancos y dejarlos =====================
robot.girar(angulo_deg=43.8, potencia_max=100, perfil="encadenado")

# DEJAR LOS CEMENTOS BLANCOS
robot.mover_torque(grados_torque=150, velocidad_torque=500, esperar=False)
robot.avanzar_recto(distancia_cm=-18.5, velocidad_max=900, perfil="encadenado") #dejar los cementos blancos

robot.avanzar_cruzando_lineas(
    cruces_objetivo=1, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=120 # Sigue retrocediendo 150 milisegundos después de ver la 3ra línea
)

wait(100)
robot.girar(angulo_deg=-36, potencia_max=100, perfil="encadenado")

#===================================================================================================================== AQUI ESTA BIEN
robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=54,           
    velocidad_max=100,
    lado="derecha",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=80,  
    
    #CEREBRO PREDICTIVO (PID):
    kp=1.15,                   
    kd=3.8,                    
    k_freno=0.05,              
    
    correccion_max=100,
    objetivo_reflexion=27,     
    
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=55,
    kp_captura=3.8,
    perfil_salida="encadenado"
)
robot.avanzar_recto(-10, 900) #RETROCESO DESPUES DE SEGUIR LA LINEA HASTA LA SECCIÓN DE LOS VERDES
wait(100)
robot.girar(angulo_deg=181, potencia_max=90, perfil="encadenado")

#AGARRAR LOS CEMENTOS VERDES
robot.mover_torque(grados_torque=-155, velocidad_torque=250, esperar=False)
robot.avanzar_recto(distancia_cm=-22, velocidad_max=900, perfil="encadenado")

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=40,           
    velocidad_max=100,
    lado="izquierda",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=80,  
    
    #CEREBRO PREDICTIVO (PID):
    kp=1.15,                   
    kd=3.8,                    
    k_freno=0.05,              
    
    correccion_max=100,
    objetivo_reflexion=27,     
    
    captura_inicial=True,
    tiempo_captura_ms=280,
    potencia_captura=55,
    kp_captura=3.8,
    perfil_salida="encadenado"
)

wait(400)
robot.girar(angulo_deg=180, potencia_max=90, perfil="encadenado")

# DEJAR LOS CEMENTOS VERDES
robot.mover_torque(grados_torque=170, velocidad_torque=350, esperar=False)
robot.avanzar_recto(distancia_cm=-22.5, velocidad_max=900, perfil="encadenado")


robot.girar(angulo_deg=-30, potencia_max=100, perfil="encadenado")
wait(80)
robot.avanzar_cruzando_lineas(
    cruces_objetivo=3, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=110 # Sigue retrocediendo 150 milisegundos después de ver la 3ra línea
)
robot.girar(angulo_deg=40, potencia_max=100, perfil="encadenado")


robot.seguir_linea_hasta_color(
    color_objetivo=Color.YELLOW, 
    velocidad_max=100, 
    lado="izquierda"
)
robot.avanzar_recto(distancia_cm=-15, velocidad_max=900, perfil="encadenado")

wait(300)
robot.girar(angulo_deg=-167, potencia_max=100, perfil="encadenado")

# AGARRAR LOS CEMENTOS AMARILLOS
robot.mover_torque(grados_torque=-169.8, velocidad_torque=500, esperar=False)
robot.avanzar_recto(distancia_cm=-21, velocidad_max=900, perfil="encadenado")

robot.avanzar_recto(distancia_cm=10, velocidad_max=900, perfil="encadenado")
wait(300)
robot.girar(angulo_deg=-70, potencia_max=100, perfil="encadenado")

# Avanzar a la linea para ir a los amarillos
robot.avanzar_recto(distancia_cm=58, velocidad_max=900, perfil="encadenado") 
robot.girar(angulo_deg=60, potencia_max=100, perfil="encadenado")
robot.seguir_linea(
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
wait(300)
robot.girar(angulo_deg=-80, potencia_max=100, perfil="encadenado")

# DEJAR LOS CEMENTOS AMARILLOS
robot.mover_torque(grados_torque=160, velocidad_torque=350, esperar=False)
robot.avanzar_recto(distancia_cm=-18.5, velocidad_max=900, perfil="encadenado")

# Salir de la seccion amarilla
robot.seguir_linea(
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
wait(300)
robot.girar(angulo_deg=-65, potencia_max=100, perfil="encadenado")

# Seguir linea para ir a los azules
robot.seguir_linea(
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

wait(300)

# Giro para ir a los azules
robot.girar(angulo_deg=129, potencia_max=100, perfil="encadenado")
robot.avanzar_recto(distancia_cm=-34, velocidad_max=800, perfil="seguro")

# Ojo: Adapté tu giro derecha antiguo a usar la nueva función simétrica
robot.girar(angulo_deg=28, potencia_max=100, perfil="seguro")

# AGARRAR LOS CEMENTOS AZULES
robot.mover_torque(grados_torque=-168, velocidad_torque=600, esperar=False)
robot.avanzar_recto(distancia_cm=-20, velocidad_max=900, perfil="encadenado")

robot.seguir_linea(
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

# Giro para ir por los cementos azules
wait(300)
robot.girar(angulo_deg=-28, potencia_max=100, perfil="encadenado")

# CONTROLES DE GARRA ACTUALIZADOS
robot.mover_garra_principal(velocidad=300, grados=-95)
robot.mover_garra_delantera(velocidad=850, grados=253)

robot.avanzar_recto(distancia_cm=41, velocidad_max=900, perfil="encadenado")  
robot.mover_garra_principal(velocidad=300, grados=90)


robot.avanzar_recto(distancia_cm=-6.5, velocidad_max=870, perfil="seguro")
robot.girar(angulo_deg=28, potencia_max=100, perfil="encadenado")


robot.seguir_linea(
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
robot.mover_garra_principal(velocidad=300, grados=-100)

# ================================================

robot.avanzar_recto(distancia_cm=-12, velocidad_max=800, perfil="seguro")
wait(280)
robot.girar(angulo_deg=75, potencia_max=100, perfil="encadenado")
robot.mover_torque(grados_torque=-170, velocidad_torque=800, esperar=False)


from robot_control_rapidez import Base as BaseRapidez
from MATRIZ2 import ejecutar_matriz # el archivo donde guardaste la función
robot2 = BaseRapidez()
ejecutar_matriz(robot2)
