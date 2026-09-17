"""Recorrido de la matriz 2.
"""
from control_drivebase import Base
from pybricks.tools import wait
import gc

from matriz import dejar_bloques_matriz
from matriz import dejar_bloques_matriz2


def ejecutar_matriz_2(robot):


    print("Voltaje:", robot.Hub.battery.voltage(), "mV")
    print("Ejecutando recorrido de matriz 2")

    gc.collect()

    # ==========================================================
    # 1. ENTRADA A LOS PRIMEROS CUATRO BLOQUES AZULES
    # ==========================================================

    # Toma 0° como referencia de ambas garras para que sus posiciones sean repetibles.
    robot.motor_garra.reset_angle(0)
    robot.motor_garra_delantera.reset_angle(0)

    # Retroceso inicial para quedar en la distancia correcta antes del giro.
    robot.avanzar_recto(distancia_cm=-6, velocidad_max=900)

    # Giro hacia el carril que entra a la zona de los bloques azules
    robot.girar(90, potencia_max=65, potencia_min=45, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Espera corta de asentamiento: se conserva porque el siguiente movimiento cuenta líneas.
    wait(200)

    # Cruza las dos líneas negras de entrada. El retraso de 80 ms está probado y se mantiene.
    robot.avanzar_cruzando_lineas(cruces_objetivo=2, velocidad=900, escape_inicial_cm=8, retraso_freno_ms=80, perfil="seguro")
    
    # Deja que el chasis se asiente.
    wait(200)

    # NO uses girar(-90): busca el negro y queda alineado con él.
    robot.girar_hasta_negro(
        "izquierda",
        potencia=67,
        potencia_correccion=22
    )

    # El chasis debe asentarse antes de girar usando la línea negra como referencia.
    wait(200)
     
    '''
    # Gira hasta encontrar negro para alinear el robot con la entrada de los bloques.
    robot.girar(-90, potencia_max=75, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    '''
    '''
    robot.avanzar_recto(distancia_cm=-6, velocidad_max=900)
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=7, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
    '''
    
    # Abre/prepara la garra principal antes de entrar al grupo de cuatro azules.
    robot.mover_garra_principal(900, 300, apretar=False, duty_cierre=100)

    # Sale de la línea negra para no quedarse detenido sobre ella.
    robot.avanzar_hasta_salir_negro(velocidad_max=800, velocidad_min=200, objetivo_reflexion=15, lecturas_salida=4)

    # Entra hasta la posición de toma de los primeros cuatro bloques.
    robot.avanzar_recto(distancia_cm=4.3, velocidad_max=900, perfil="encadenado")

    # Baja la garra delantera; aquí espera porque es una posición crítica para el agarre.
    robot.mover_garra_delantera(290)

    # Sale del grupo azul y vuelve al pasillo central.
    robot.avanzar_recto(distancia_cm=-20, velocidad_max=900, perfil="seguro")

    # Se conserva antes del giro para evitar que el chasis arranque inclinado.
    wait(200)

    # Giro hacia la línea corta que lleva a los amarillos.
    robot.girar(-90, potencia_max=75, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Tramo corto y lento: la velocidad 50 es de acomodo, por eso no se aumenta.
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=8, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    # Da tiempo a que el freno del seguidor deje el robot estable antes del giro siguiente.
    wait(200)

    # ==========================================================
    # 2. TOMA DE LOS DOS AMARILLOS
    # ==========================================================

    # Giro desde el pasillo hacia la fila de amarillos.
    robot.girar(90, potencia_max=65, potencia_min=45, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # La garra delantera y la principal son motores diferentes.
    # La delantera comienza a ir a 250 mientras la principal se prepara a 125.
    robot.mover_garra_delantera(250, simultaneo=True)
    robot.mover_garra_principal(900, 125, apretar=False, duty_cierre=100)

    # Recorre la distancia calibrada para tomar los dos amarillos.
    robot.avanzar_recto(distancia_cm=12.5, velocidad_max=750, perfil="encadenado")

    # Esta posición sí debe terminar antes del apriete: define la altura de agarre.
    robot.mover_garra_delantera(260)

    # Cierra contra los bloques. esperar=False permite que el cierre continúe durante el retroceso.
    robot.mover_garra_principal(450, esperar=False, potencia_apriete=100, apretar=True)

    # Sale con los amarillos sujetos y vuelve al corredor.
    robot.avanzar_recto(distancia_cm=-14, velocidad_max=550, perfil="seguro")

    # Asentamiento antes del giro hacia la ruta de entrega.
    wait(200)

    # Giro para tomar la línea que apunta a la matriz.
    robot.girar(90, potencia_max=65, potencia_min=45, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Este tramo es de alineación hacia la matriz; conserva su velocidad probada.
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=90, distancia_cm=14, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    # Mantiene estabilidad antes del giro de entrada a la matriz.
    wait(200)

    # Queda orientado hacia la zona de la primera entrega.
    robot.girar(92, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Primera descarga. La función se encarga de encontrar la marca azul y soltar los bloques.
    dejar_bloques_matriz(robot)

    # Punto seguro de recolección: la primera descarga terminó y el robot está detenido.
    # No se llama gc.collect() después de cada movimiento porque también puede crear pausas.
    gc.collect()

    # ==========================================================
    # 3. REGRESO PARA LA SEGUNDA TANDA AZUL
    # ==========================================================

    # Pasillo largo de salida desde la primera entrega.
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=80, distancia_cm=25, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    # El seguidor termina frenado; esta espera evita iniciar el giro con inercia lateral.
    wait(200)

    # Secuencia de giros que lleva al segundo grupo azul.
    robot.girar(-90, potencia_max=75, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.avanzar_recto(distancia_cm=4.3, velocidad_max=500, perfil="seguro")
    wait(200)
    robot.girar(90, potencia_max=80, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Tramo corto de acomodo antes de entrar a los siguientes azules.
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=8, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    # Entrada controlada al segundo grupo azul.
    robot.avanzar_recto(distancia_cm=23, velocidad_max=400, perfil="seguro")

    # Baja la garra antes de salir del grupo; se conserva el valor 290 de tu versión actual.
    robot.mover_garra_delantera(290, velocidad=800, simultaneo=True)
    # Prepara la garra principal para la siguiente carga.
    robot.mover_garra_principal(900, 250, apretar=False, duty_cierre=60)

    # Retroceso hacia el corredor principal con la segunda tanda.
    robot.avanzar_recto(distancia_cm=-26, velocidad_max=600, perfil="seguro")

    # Giro y seguidor hacia la fila final de bloques.
    robot.girar(-90, potencia_max=90, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")
    robot.seguir_linea(sensor_color=robot.seguidor, velocidad_max=70, distancia_cm=14, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

    # Mantiene el chasis estable antes de entrar al último grupo.
    wait(200)

    # ==========================================================
    # 4. ÚLTIMA TANDA Y RETORNO A LA ENTREGA FINAL
    # ==========================================================

    # Giro hacia la última fila de bloques.
    robot.girar(90, potencia_max=80, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Ambas garras se preparan a la vez. La espera de la principal da tiempo a la delantera.
    robot.mover_garra_delantera(265, simultaneo=True)
    robot.mover_garra_principal(900, 150, apretar=False, duty_cierre=100)

    # Espera conservada: antes de la toma las dos garras deben estar en su posición.
    wait(200)

    # Entrada a la última fila de bloques.
    robot.avanzar_recto(distancia_cm=12, velocidad_max=750, perfil="encadenado")

    # Baja hasta la altura exacta de agarre antes de cerrar la garra principal.
    robot.mover_garra_delantera(270)

    # El cierre sigue trabajando mientras la garra delantera se levanta para proteger la carga.
    robot.mover_garra_principal(500, esperar=False, potencia_apriete=100, apretar=True)
    robot.mover_garra_delantera(190, simultaneo=True, velocidad=800)

    # Avance lento por la zona central; se mantiene porque requiere control de carga.
    robot.avanzar_recto(distancia_cm=16.5, velocidad_max=350, perfil="seguro")

    # Inicia el acomodo de la garra durante el retroceso largo de salida.
    robot.mover_garra_delantera(260, velocidad=900)
    robot.avanzar_recto(distancia_cm=-38.5, velocidad_max=600, perfil="seguro")

    # Esta espera es antes del giro final; evita variar la orientación por inercia.
    wait(300)

    # Se orienta hacia el carril que lleva a la segunda entrega.
    robot.girar(89.9, potencia_max=70, potencia_min=35, kp_base=5.0, tolerancia_fin=1.0, perfil="encadenado")

    # Último retroceso antes de la rutina de descarga final.
    robot.avanzar_recto(distancia_cm=-17, velocidad_max=600, perfil="seguro")

    # Prepara el torque sin bloquear: el motor puede terminar de acomodarse al entrar a dejar bloques.
    robot.mover_torque(grados_torque=-170, velocidad_torque=900, esperar=False)

    # Segunda descarga y final de Matriz 2.
    dejar_bloques_matriz2(robot)

    # Limpieza final: no influye en el recorrido porque ya terminó.
    gc.collect()


if __name__ == "__main__":
    robot = Base()
    ejecutar_matriz_2(robot)
