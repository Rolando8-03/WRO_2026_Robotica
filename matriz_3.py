"""Recorrido adaptado para la matriz 3.

Todas as llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait
import gc


def ejecutar_matriz_3(robot):
    """Ejecuta el recorrido activo de la matriz 3."""
    robot.establecer_norte()

    robot.avanzar_recto(-10)
    robot.girar_a_rumbo(89)

    robot.motor_garra_delantera.reset_angle(0)
    robot.motor_garra.reset_angle(0)

    
    gc.collect()
    #Tomar los primeros dos cementos blancos y verdes ==========
    wait(400)
    robot.avanzar_cruzando_lineas(cruces_objetivo=3, velocidad=700, distancia_extra_cm=12)
    robot.mover_garra_principal(velocidad=900, grados=195, esperar=False)
    wait(50)
    robot.girar(-90)
    robot.mover_garra_delantera(260)
    robot.avanzar_recto(6, 800)
    robot.mover_garra_principal(900, grados=0)
    robot.avanzar_recto(-20)
    #giro para ir por los cementos amarillos ===========
    robot.girar(-90)
    robot.avanzar_recto(10.3)
    robot.girar(-90)

    gc.collect()

    #Secuencia para ri por los cementos amarillos ==========
    robot.mover_garra_principal(velocidad=900, grados=70, esperar= True)
    robot.mover_garra_delantera(0)
    robot.mover_garra_principal(velocidad=900, grados=200, esperar= False)

    robot.avanzar_recto(-5.3, 800)
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
    robot.mover_garra_delantera(270)
    robot.avanzar_recto(-24, 750)

    robot.girar(90)
    wait(100)
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=300, escape_inicial_cm=5, distancia_extra_cm=5)

    robot.girar(90)

    #Acomodar los bloques
    robot.dejar_bloques_matriz3(distancia_entrada=13)

    #INICIO DE LA SEGUNDA PORCION DE LA MATRIZ

    wait(30)
    robot.mover_garra_principal(800, 80, esperar=False)
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
    robot.mover_garra_delantera(260, simultaneo=True)
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
    wait(50)
    robot.girar(-90)
    robot.mover_garra_delantera(0, simultaneo=False)

    robot.avanzar_recto(23.7, 600) #Avanzar para meter en los compartimentos los verdes
    robot.mover_garra_delantera(260, simultaneo=False)
    robot.avanzar_recto(-20)
    robot.girar(90)

    #ir por los cementos blancos
    robot.avanzar_recto(14.5)
    robot.girar(-90)

    robot.mover_garra_principal(velocidad=900, grados=130, esperar= True)
    robot.avanzar_recto(14)
    robot.mover_garra_principal(800, grados=0) #Aqui toma los blancos

    robot.avanzar_recto(-20.4)
    robot.girar(-90)
    robot.avanzar_recto(17)
    robot.girar(-90)
    robot.mover_garra_principal(velocidad=900, grados=120)

    robot.dejar_bloques_matriz3(distancia_entrada=3)


    
if __name__ == "__main__":
    robot = Base()
    print(robot.Hub.battery.voltage())
    ejecutar_matriz_3(robot)
