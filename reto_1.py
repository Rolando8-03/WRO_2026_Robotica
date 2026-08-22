"""Recorrido secuencial del reto 1.

Este archivo conserva el orden original de las acciones. Las funciones están
organizadas en módulos, pero el recorrido permanece secuencial para facilitar
las pruebas físicas y el ajuste de parámetros.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait
import gc 
from matriz_2 import ejecutar_matriz_2
robot = Base()
print("Voltaje:", robot.Hub.battery.voltage())

# SECCION 1: =================================================================================
# Giro de salida y seguidor hasta el cemento

robot.motor_garra_delantera.reset_angle(0)
robot.giro_de_arco(
    radio_cm=22,        # Radio del arco
    angulo_deg=90,      # Ángulo a girar
    potencia_max=90,    # Velocidad máxima del arco
    lado="derecha"      # La rueda derecha va por fuera
)

gc.collect()

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=82,           
    velocidad_max=100,         
    lado="derecha",            
    
    tiempo_acomodo_ms=50,      
    tiempo_aceleracion_ms=50,  
    
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

gc.collect()

# Giro para posicionarse frente al cemento y movimiento simultáneo para tomarlo
robot.girar(angulo_deg=-90, potencia_max=100, perfil="encadenado")

# ACTIVAMOS TORQUE SIN ESPERAR Y LUEGO RETROCEDEMOS
robot.mover_torque(grados_torque=-170, velocidad_torque=600, esperar=False)
robot.avanzar_recto(distancia_cm=-16, velocidad_max=1000, perfil="encadenado") 

# Pequeño avance despues de tomar el cemento y giro en direccion a la llana
robot.avanzar_recto(distancia_cm=6, velocidad_max=1000, perfil="encadenado")
robot.girar(angulo_deg=77, potencia_max=100, perfil="encadenado") 

# Retroceso para dejar la llana en su lugar y mov.recto para regresar a la linea
robot.avanzar_recto(distancia_cm=-32, velocidad_max=1000, perfil="seguro")
# Cruzar 3 líneas y detenerse un poquito después de la tercera
robot.avanzar_cruzando_lineas(
    cruces_objetivo=3, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=0 # Sigue retrocediendo 150 milisegundos después de ver la 3ra línea
)

gc.collect()

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

#wait(100) 

robot.mover_torque(grados_torque=166, velocidad_torque=300, esperar=False)
robot.avanzar_recto(distancia_cm=-8.5, velocidad_max=1000, perfil="encadenado") 
robot.avanzar_recto(4, 950)

# SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =======================================================================
robot.giro_derecha(-92, 900)

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=19,           
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
robot.avanzar_recto(-6, velocidad_max=700)
robot.girar(angulo_deg=180, potencia_max=100, perfil="encadenado")  

gc.collect()
# AGARRAR LOS CEMENTOS BLANCOS
robot.mover_torque(grados_torque=-171, velocidad_torque=250, esperar=False)
robot.avanzar_recto(distancia_cm=-23, velocidad_max=700, perfil="encadenado")

gc.collect()
# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=20,           
    velocidad_max=100,
    lado="derecha",            
    
    tiempo_acomodo_ms=200,      
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
robot.girar(angulo_deg=75, potencia_max=90, perfil="encadenado",)
wait(70)

robot.avanzar_cruzando_lineas(
    cruces_objetivo=4, 
    velocidad=850, 
    escape_inicial_cm=8,
    retraso_freno_ms=0,
    distancia_extra_cm=3
)

robot.girar(angulo_deg=-75, potencia_max=100, perfil="encadenado") 
wait(80)

#SEGUIR LINEA HASTA LA MATRIZ
robot.seguir_linea_hasta_color(
    color_objetivo=Color.GREEN, 
    velocidad_max=95, 
    lado="izquierda"
)
robot.girar_corto(6, potencia_max=60, potencia_min=40)
robot.avanzar_recto(14.5, 700)
robot.girar_corto(-3, potencia_max=60, potencia_min=40)
matriz_detectada = robot.escanear_matriz()

#Salir de la matriz-----------------
robot.avanzar_recto(distancia_cm=-37.5, velocidad_max=900, perfil="seguro") 

robot.girar(angulo_deg=-181, potencia_max=100, perfil="encadenado")
robot.avanzar_recto(distancia_cm=-23.5, velocidad_max=670, perfil="seguro") 
robot.avanzar_recto(distancia_cm=8, velocidad_max=900, perfil="seguro") 

# Giro para entrar en los cementos blancos y dejarlos =====================
robot.girar(angulo_deg=41.5, potencia_max=100, perfil="encadenado")

# DEJAR LOS CEMENTOS BLANCOS
robot.mover_torque(grados_torque=150, velocidad_torque=500, esperar=False)
robot.avanzar_recto(distancia_cm=-18.5, velocidad_max=900, perfil="encadenado") #dejar los cementos blancos

#posicionarse en la linea para traer los cementos verdes
robot.avanzar_cruzando_lineas(
    cruces_objetivo=1, 
    velocidad=900, 
    escape_inicial_cm=8,
    retraso_freno_ms=120 # Sigue retrocediendo 150 milisegundos después de ver la 3ra línea
)

robot.girar(angulo_deg=-36, potencia_max=100, perfil="encadenado")

#Seguir la linea para ir a los verdes
robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=50,           
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
robot.avanzar_recto(-5, 900) #RETROCESO DESPUES DE SEGUIR LA LINEA HASTA LA SECCIÓN DE LOS VERDES

robot.girar(angulo_deg=-184, potencia_max=90, perfil="encadenado")

#AGARRAR LOS CEMENTOS VERDES---------------------
robot.mover_torque(grados_torque=-155, velocidad_torque=300, esperar=False)
robot.avanzar_recto(distancia_cm=-22, velocidad_max=900, perfil="encadenado")

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=45,           
    velocidad_max=100,
    lado="derecha",            
    
    tiempo_acomodo_ms=100,      
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

robot.girar(angulo_deg=180, potencia_max=90, perfil="encadenado")

# DEJAR LOS CEMENTOS VERDES --------------------------------------------------
robot.avanzar_recto(distancia_cm=-20, velocidad_max=900, perfil="encadenado")
robot.mover_torque(grados_torque=170, velocidad_torque=350, esperar=False)

#Avance para ir por los amarillos y giro
robot.avanzar_recto(distancia_cm=26, velocidad_max=900, perfil="encadenado")
robot.girar(angulo_deg=-48, potencia_max=100, perfil="encadenado")

wait(80)

robot.avanzar_cruzando_lineas(2, 900, retraso_freno_ms=80)
#avance hasta la linea para tomar los amarillos
#robot.avanzar_hibrido(distancia_inicial_cm=15,color_objetivo=Color.BLACK,velocidad_max=350,cruces=1)

robot.girar(angulo_deg=-129, potencia_max=100, perfil="encadenado")

#robot.seguir_linea_hasta_color(color_objetivo=Color.YELLOW, velocidad_max=500, lado="derecha")

#robot.girar(angulo_deg=-177, potencia_max=100, perfil="encadenado")

# AGARRAR LOS CEMENTOS AMARILLOS
robot.mover_torque(grados_torque=-171, velocidad_torque=200, esperar=False)
robot.avanzar_recto(distancia_cm=-25, velocidad_max=900, perfil="encadenado")
robot.girar(angulo_deg=-70, potencia_max=100, perfil="encadenado")
# Avanzar a la linea para ir a los amarillos
wait(80)
robot.avanzar_cruzando_lineas(2,900, escape_inicial_cm=8,retraso_freno_ms=0,distancia_extra_cm=22)

robot.girar(angulo_deg=56, potencia_max=100, perfil="encadenado")

robot.seguir_linea(
    sensor_color=robot.seguidor,
    distancia_cm=70,           
    velocidad_max=100,
    lado="izquierda",            
    
    tiempo_acomodo_ms=100,      
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

'''

wait(80)

robot.seguir_linea(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=60,
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
'''
robot.girar(angulo_deg=-90, potencia_max=100, perfil="encadenado")

# DEJAR LOS CEMENTOS AMARILLOS
robot.avanzar_recto(distancia_cm=-15, velocidad_max=900, perfil="encadenado")
robot.mover_torque(grados_torque=155, velocidad_torque=350, esperar=False)

# Salir de la seccion amarilla
robot.avanzar_recto(14, 900)

robot.girar(angulo_deg=-88, potencia_max=100, perfil="encadenado")

robot.seguir_linea(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=45,
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

wait(80)

# Movimiento para tomar la pala.
robot.girar(
    angulo_deg=-40,
    potencia_max=100,
    perfil="encadenado"
)

# Empieza a bajar el torque.
robot.mover_torque(
    grados_torque=-148,
    velocidad_torque=230,
    esperar=False
)

# Retrocede mientras el torque baja.
robot.avanzar_recto(
    distancia_cm=-12,
    velocidad_max=900,
    perfil="seguro"
)

# Empieza a avanzar inmediatamente.
# El torque permanece abajo durante el retraso indicado.
# Después comienza a subir mientras el robot continúa avanzando.
robot.avanzar_recto(
    distancia_cm=38,
    velocidad_max=800,
    torque_grados=160,
    torque_velocidad=250,
    torque_retraso_ms=800
)

robot.girar(angulo_deg=40, potencia_max=100, perfil="encadenado")
robot.seguir_linea(
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
robot.avanzar_hasta_color(color_objetivo=Color.BLUE, velocidad=500)

robot.avanzar_recto(-9, 800)
robot.girar(angulo_deg=-180, potencia_max=100, perfil="encadenado")

robot.mover_torque(grados_torque=-164, velocidad_torque=300, esperar=False)
robot.avanzar_recto(distancia_cm=-25, velocidad_max=800, perfil="seguro")

# Salir de la seccion de azul y tomar la linea
robot.avanzar_recto(distancia_cm=15, velocidad_max=800, perfil="seguro")
robot.girar(angulo_deg=-40, potencia_max=80)

robot.avanzar_recto(25, 900)

robot.girar(angulo_deg=40, potencia_max=80)

robot.seguir_linea(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=127,
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
#wait(100)
robot.mover_torque(grados_torque=180, velocidad_torque=500, esperar=True)
robot.seguir_linea(
    sensor_color=robot.seguidor,
    velocidad_max=70,
    distancia_cm=13,
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
robot.avanzar_recto(4, 900)

robot.avanzar_recto(-10.5, 900)
wait(500)
robot.girar(90, potencia_max=70)

# =================================================================================
# INICIALIZACIÓN DE LA MATRIZ DETECTADA
# =================================================================================
# Al terminar todo el reto 1, según lo que haya devuelto escanear_matriz()
# más arriba (guardado en matriz_detectada), se ejecuta el recorrido de la
# matriz correspondiente. Por ahora solo está implementada la matriz 2.

print("Matriz detectada:", matriz_detectada)
 
if matriz_detectada == 2:
    print("Iniciando recorrido de la matriz 2...")
    ejecutar_matriz_2(robot)
else:
    print("No hay recorrido definido para la matriz detectada:", matriz_detectada)
