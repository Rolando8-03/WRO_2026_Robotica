"""Recorrido adaptado para la matriz 3.

Todas as llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait



def ejecutar_matriz_3(robot):
    """Ejecuta el recorrido activo de la matriz 2."""

    #Tomar los primeros dos cementos blancos y verdes
    robot.avanzar_cruzando_lineas(cruces_objetivo=3, velocidad=700, distancia_extra_cm=12.5)
    robot.mover_garra_principal(velocidad=900, grados=70, esperar= False)
    robot.girar(-92.3)
    robot.mover_garra_delantera(245)
    robot.avanzar_recto(7, 800)

    robot.mover_garra_principal(900, grados=0)
    robot.avanzar_recto(-20)

    robot.girar(-90)
    robot.avanzar_recto(12)
    robot.girar(-90)

    #Ir por los amarillos
    robot.mover_garra_principal(velocidad=900, grados=70, esperar= True)
    robot.mover_garra_delantera(0)
    robot.mover_garra_principal(velocidad=900, grados=200, esperar= False)

    robot.avanzar_recto(-4, 800)
    robot.girar(90)

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=27,           
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
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.girar(90)
    robot.avanzar_recto(21.5, 600)
    robot.mover_garra_delantera(250)
    robot.avanzar_recto(-20, 750)

    robot.girar(90)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=25.3,           
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
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.girar(90)

    #Acomodar los bloques
    robot.mover_garra_delantera(80)
    robot.avanzar_recto(-10)
    robot.mover_garra_principal(100, grados=180, esperar=False)
    robot.mover_garra_delantera(260)

    robot.avanzar_recto(13)
    robot.dejar_bloques_matriz3(distancia_entrada=14)

    wait(30)
    robot.mover_garra_principal(800, 100, esperar=False)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=30,           
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
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )
    robot.girar(-90)
    wait(30)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=15,           
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
        potencia_captura=60,
        kp_captura=2.5,
        perfil_salida="encadenado"
    )

    robot.girar(90)
    robot.mover_garra_delantera(240, simultaneo=True)
    robot.avanzar_recto(14)
    robot.mover_garra_principal(800, grados=0) #Aqui toma los amarillos

    robot.avanzar_recto(-17)
    robot.girar(100)
    robot.mover_garra_principal(800, 100)
    robot.mover_garra_delantera(0, simultaneo=True)
    robot.girar_corto(-15)

    robot.mover_garra_delantera(240, simultaneo=True)
    robot.avanzar_recto(24.8) #Ir por los cmentos verdes
    robot.mover_garra_principal(velocidad=900, grados=200, esperar= True)
    wait(30)
    robot.girar(-90)
    robot.mover_garra_delantera(0, simultaneo=False)

    robot.avanzar_recto(24.1, 600) #Avanzar para meter en los compartimentos los verdes
    robot.mover_garra_delantera(240, simultaneo=False)
    robot.avanzar_recto(-20)
    robot.girar(90)

    #ir por los cementos blancos
    robot.avanzar_recto(14.5)
    robot.girar(-90)

    robot.mover_garra_principal(velocidad=900, grados=150, esperar= True)
    robot.avanzar_recto(15.2)
    robot.mover_garra_principal(800, grados=0) #Aqui toma los blancos

    robot.avanzar_recto(-20)
    robot.girar(-90)
    robot.avanzar_recto(17)
    robot.girar(-90)
    robot.dejar_bloques_matriz3(distancia_entrada=9)

    
if __name__ == "__main__":
    robot = Base()
    print(robot.Hub.battery.voltage())
    ejecutar_matriz_3(robot)

