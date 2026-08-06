"""Recorrido adaptado para la matriz 2.
Todas las llamadas usan las funciones del proyecto organizado.
"""

# Importación de la clase principal para el control del robot
from control_drivebase import Base
# Importación de utilidades de Pybricks (colores y pausas)
from pybricks.parameters import Color
from pybricks.tools import wait
# Importación de rutinas específicas para la entrega/manipulación de bloques en la matriz
from matriz import dejar_bloques_matriz
from matriz import dejar_bloques_matriz2
from matriz import dejar_bloques_matriz3

def ejecutar_matriz_2(robot):
    """Ejecuta la secuencia de navegación y manipulación para la matriz 2."""
    
    # Muestra el estado de la batería del Hub en milivoltios antes de iniciar
    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 2")

    # ==========================================
    # PRIMERA PARTE DE LA MATRIZ: BLOQUES AZULES
    # ==========================================

    # Reiniciar la posición angular del motor de la garra delantera a cero
    robot.motor_garra_delantera.reset_angle(0)
    wait(500)
    
    # Avanza detectando 2 líneas negras a alta velocidad (900 deg/s)
    robot.avanzar_cruzando_lineas(cruces_objetivo=2, velocidad=900, escape_inicial_cm=8, retraso_freno_ms=90)
    
    # Pequeño ajuste en línea recta encadenado
    robot.avanzar_recto(distancia_cm=0.5, velocidad_max=900, perfil="encadenado")
    wait(400)
    
    # Giro de 90° a la izquierda (antihorario) para orientarse hacia los bloques azules
    robot.girar(-90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Abre/posiciona la garra principal a 90° de manera asíncrona (esperar=False)
    robot.mover_garra_principal(300, 90, esperar=False)

    # Avanza hacia la zona de recolección del bloque azul
    robot.avanzar_recto(distancia_cm=12, velocidad_max=900, perfil="encadenado")
    
    # Baja/activa la garra delantera a la posición 300 para sujetar el bloque azul
    robot.mover_garra_delantera(300)
    
    # --- Salir de la zona del bloque azul ---
    
    # Retrocede en modo seguro para despejar la zona
    robot.avanzar_recto(distancia_cm=-21, velocidad_max=900, perfil="seguro")
    wait(200)
    
    # Giro de 90° a la izquierda para alinearse con la línea guía
    robot.girar(-90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Sigue la línea usando el sensor por el lado izquierdo durante 8 cm
    robot.seguir_linea(
        sensor_color=robot.seguidor, 
        velocidad_max=70, 
        distancia_cm=8, 
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

    # ============================================
    # PRIMERA PARTE DE LA MATRIZ: BLOQUES AMARILLOS
    # ============================================

    # Giro de 90° a la derecha para orientarse a los bloques amarillos
    robot.girar(90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Ajusta garra delantera y garra principal con apriete para sujetar
    robot.mover_garra_delantera(260)
    robot.mover_garra_principal(300, -50, esperar=False, apretar=False)
    wait(200)
    
    # Avanza hacia los bloques amarillos
    robot.avanzar_recto(distancia_cm=13, velocidad_max=750, perfil="encadenado")
    robot.mover_garra_delantera(285)

    # Aplica presión adicional con la garra principal
    robot.mover_garra_principal(300, -31, esperar=False, potencia_apriete=80, apretar=True)
    
    # Retrocede con la carga asegurada
    robot.avanzar_recto(distancia_cm=-14, velocidad_max=550, perfil="seguro")
    wait(200)
    
    # Giro de 90° a la derecha para reconectarse con el trayecto
    robot.girar(90, potencia_max=85, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Sigue línea por la derecha durante 13 cm para llegar a la zona de descarga
    robot.seguir_linea(
        sensor_color=robot.seguidor, 
        velocidad_max=100, 
        distancia_cm=13, 
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
    wait(200)

    # Giro final de 90° a la derecha para encarar la entrega
    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Ejecuta la función de descarga de la primera etapa
    dejar_bloques_matriz(robot)

    # ==========================================
    # SEGUNDA PARTE DE LA MATRIZ: RECOLECCIÓN Y DESCARGA
    # ==========================================

    # Avanza siguiendo línea 25 cm por la izquierda
    robot.seguir_linea(
        sensor_color=robot.seguidor, 
        velocidad_max=90, 
        distancia_cm=25, 
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
    wait(200)
    
    # Reorientación para cambio de carril/pasillo
    robot.girar(-90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.avanzar_recto(distancia_cm=4.65, velocidad_max=500, perfil="seguro")
    wait(200)
    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Alineación final mediante seguimiento de línea por el lado derecho
    robot.seguir_linea(
        sensor_color=robot.seguidor, 
        velocidad_max=80, 
        distancia_cm=8, 
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
    
    # Avance recto seguro de aproximación
    robot.avanzar_recto(distancia_cm=22, velocidad_max=350, perfil="seguro")

    # Ajuste de garra delantera, maniobra de retroceso y giro para la toma final
    robot.mover_garra_delantera(300)
    robot.avanzar_recto(distancia_cm=-27.5, velocidad_max=600, perfil="seguro")
    robot.girar(-90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    
    # Seguimiento de línea por la izquierda para aproximación a los últimos bloques
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
    wait(200)

    # Posicionamiento final frente al objetivo
    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.mover_garra_delantera(280)
    robot.mover_garra_principal(400, 30, esperar=False)
    wait(300)

    # Secuencia de agarre de precisión
    robot.avanzar_recto(distancia_cm=12.5, velocidad_max=750, perfil="encadenado")
    robot.mover_garra_delantera(290)
    
    # Cierre de garra principal con fuerza (potencia_apriete=150)
    robot.mover_garra_principal(500, -30, esperar=False, potencia_apriete=140)
    robot.mover_garra_delantera(190)

    # Ajuste posicional con carga tomada
    robot.avanzar_recto(distancia_cm=16, velocidad_max=450, perfil="seguro")
    robot.mover_garra_delantera(290)
    
    # Salida y retroceso final
    robot.avanzar_recto(distancia_cm=-40.9, velocidad_max=600, perfil="seguro")
    robot.girar(90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.avanzar_recto(distancia_cm=-17, velocidad_max=600, perfil="seguro")
    
    # Acciona mecanismo por torque para liberación o mecanismo secundario
    robot.mover_torque(grados_torque=-170.5, velocidad_torque=900, esperar=False)

    # Ejecuta función de descarga final para matriz 3
    dejar_bloques_matriz3(robot)


# Punto de entrada principal si el script se ejecuta directamente
if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_2(robot)
