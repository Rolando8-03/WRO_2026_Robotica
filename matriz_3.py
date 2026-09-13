"""Recorrido adaptado para la matriz 3.

Todas as llamadas usan las funciones del proyecto organizado.
"""

from control_drivebase import Base
from pybricks.parameters import Color
from pybricks.tools import wait
import gc


def ejecutar_matriz_3(robot):
    """Ejecuta el recorrido activo de la matriz 3."""
    
    
    robot.motor_garra_delantera.reset_angle(0)
    robot.motor_garra.reset_angle(0)
    robot.establecer_norte()

    wait(100)

    robot.avanzar_recto(distancia_cm=-6.5, velocidad_max=900)
    robot.girar_a_rumbo(90)


    wait(200)
    gc.collect()

    #Tomar los primeros dos cementos blancos y verdes ==========
    wait(400)
    robot.avanzar_cruzando_lineas(cruces_objetivo=3, velocidad=700, distancia_extra_cm=12)
    robot.mover_garra_principal(velocidad=900, grados=175, esperar=False)
    wait(50)
    robot.girar(
        -91,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    wait(400)
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=-500)
    robot.mover_garra_delantera(260, simultaneo=True)

    robot.avanzar_recto(20, 800)
    robot.mover_garra_principal(900, grados=40)
    robot.avanzar_recto(-13.4)
    #giro para ir por los cementos amarillos ===========
    robot.girar(
        -89,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    #ir por los cementos amarillos

    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=43.3,           
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
    
    robot.girar(
        90,
        potencia_max=80,
        potencia_min=50,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )


    gc.collect()
    wait(100)

    #Secuencia para ir por los cementos amarillos ==========
    robot.girar_corto(-10, potencia_max=50, potencia_min=34)
    robot.mover_garra_principal(velocidad=1000, grados=160, esperar=True, limite_apertura=230)
    robot.girar_corto(7.5, potencia_max=50, potencia_min=34)
    robot.avanzar_recto(15, 600)

    robot.mover_garra_principal(velocidad=1000, grados=0, esperar=True, limite_apertura=230)
    robot.avanzar_recto(-18, 750) ###

    
    robot.girar(
        90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    wait(100)
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=400, escape_inicial_cm=5, distancia_extra_cm=4)
    wait(100)

    robot.girar(
        89,
        potencia_max=90,
        potencia_min=55,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    #Acomodar los bloques
    robot.dejar_bloques_matriz3(distancia_entrada=11.8)

    #INICIO DE LA SEGUNDA PORCION DE LA MATRIZ ==============================================================================

    
    wait(30)
    robot.mover_garra_principal(800, 50, esperar=False)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=31,           
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
    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    wait(30)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        distancia_cm=16,           
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

    robot.girar(
        89,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(265, simultaneo=True)
    robot.avanzar_recto(16.5)
    robot.mover_garra_principal(800, grados=0) #Aqui toma los amarillos

    robot.avanzar_recto(-17)
    robot.girar(
        100,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    robot.mover_garra_principal(800, 100)
    robot.mover_garra_delantera(0, simultaneo=True)
    robot.girar_corto(-15)

    robot.mover_garra_delantera(240, simultaneo=True)
    robot.avanzar_recto(24.5) #Ir por los cmentos verdes
    robot.mover_garra_principal(velocidad=900, grados=200, esperar= True)
    wait(50)
    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(0, simultaneo=False)

    robot.avanzar_recto(19, 600) #Avanzar para meter en los compartimentos los verdes
    robot.mover_garra_delantera(260, simultaneo=False)
    robot.avanzar_recto(-20)
    robot.girar(
        90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    #ir por los cementos blancos
    robot.avanzar_recto(14.5)
    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.mover_garra_principal(velocidad=900, grados=130, esperar= True)
    robot.avanzar_recto(14)
    robot.mover_garra_principal(800, grados=0) #Aqui toma los blancos

    robot.avanzar_recto(-16.4)
    robot.girar(
        -90,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    
    robot.avanzar_cruzando_lineas(cruces_objetivo=1, velocidad=400, escape_inicial_cm=5, distancia_extra_cm=4)

    wait(100)
    robot.girar(
        -180,
        potencia_max=80,
        potencia_min=45,
        kp_base=6.2,
        kd_base=3.5,
        tiempo_curva_s_ms=90,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )

    robot.avanzar_recto(distancia_cm=-17, velocidad_max=600, perfil="seguro")

    robot.mover_torque(
        grados_torque=-170,
        velocidad_torque=900,
        esperar=False
    )

    gc.collect()

    dejar_bloques_matriz2(robot)

    """
    robot.mover_garra_principal(velocidad=900, grados=0)
    robot.mover_garra_delantera(posicion=0, velocidad=700)

    robot.avanzar_recto(-20)
    robot.mover_garra_principal(velocidad=900, grados=200, esperar=False)
    robot.mover_garra_delantera(posicion=260, velocidad=700)



    robot.dejar_bloques_matriz3(distancia_entrada=3)
    """


    
if __name__ == "__main__":
    robot = Base()
    print(robot.Hub.battery.voltage())
    ejecutar_matriz_3(robot)
