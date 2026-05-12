from robot_control_prueba import Base  # Importa la clase Base, donde están todas las funciones del robot.
from pybricks.parameters import Color, Direction, Port, Stop  # Importa parámetros de Pybricks para colores, puertos, direcciones y frenado.
from matriz import ejecutar_matriz  # Importa la función para ejecutar acciones según la matriz detectada.

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()  # Crea el objeto robot usando la clase Base.
print(robot.Hub.battery.voltage())  # Muestra el voltaje actual de la batería.
matriz_detectada = None  # Variable donde se guardará la matriz cuando sea escaneada.


# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================

# SECCIÓN 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_arco_dc(radio_cm=9.6, angulo_deg=140, potencia=100, lado="derecha")  # Sale haciendo un arco hacia la derecha con radio 9.6 cm y giro de 140 grados.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color principal para seguir la línea.
    velocidad_max=100,  # Usa potencia máxima en la función dc().
    distancia_cm=65,  # Sigue la línea durante 65 centímetros.
    lado="derecha",  # Sigue el borde derecho de la línea.
    tiempo_acomodo_ms=80,  # Da 80 ms para acomodarse suavemente al inicio.
    kp=1.15,  # Corrección proporcional para ajustar el robot según el error.
    kd=2.6,  # Corrección derivativa para suavizar cambios bruscos.
    k_freno=0.0,  # No reduce velocidad aunque haya error.
    perfil_salida="encadenado"  # Termina rápido para continuar con el siguiente movimiento.
)


# SECCIÓN 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-90, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados en sentido negativo para orientarse al balde.

robot.avanzar_con_torque(distancia_cm=-17.5, grados_torque=-170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 17.5 cm y activa el torque después de 1 cm para agarrar el balde.

robot.mover_recto( distancia_cm=1, velocidad=1000, perfil="encadenado")  # Avanza 1 cm para acomodar el mecanismo o liberar presión.

# SECCIÓN 1.3 -> DEJAR LA PALA DE ALBAÑILERÍA
robot.girar( 68.5, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado"
)  # Gira 68.5 grados para orientarse hacia la zona de la pala.

robot.esperar(80)  # Espera 80 ms para estabilizar el robot después del giro.

robot.retroceder(distancia_cm=42, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)  # Retrocede 42 cm usando giroscopio para mantenerse recto.

robot.mover_recto( distancia_cm=42, velocidad=1000, perfil="encadenado")  # Avanza 42 cm después de dejar o acomodar la pala.

robot.giro_arco_dc( radio_cm=13, angulo_deg=19, potencia=80, lado="derecha")  # Hace un arco pequeño hacia la derecha para ajustar la dirección.

# ===================== SECCIÓN 2 (DEJAR EL CEMENTO) =====================

# SECCIÓN 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color principal.
    velocidad_max=100,  # Sigue línea con potencia máxima.
    distancia_cm=34,  # Sigue la línea durante 34 cm.
    lado="derecha",  # Sigue el borde derecho de la línea.
    tiempo_acomodo_ms=80,  # Tiempo inicial para estabilizar el seguimiento.
    kp=1.15,  # Fuerza de corrección proporcional.
    kd=2.6,  # Corrección derivativa para controlar oscilaciones.
    k_freno=0.0,  # No aplica frenado por error.
    perfil_salida="encadenado"  # Sale rápido del movimiento.
)

# SECCIÓN 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados para apuntar al estacionamiento.

robot.esperar(300)  # Espera 300 ms para estabilizarse antes de soltar el cemento.

robot.avanzar_con_torque(distancia_cm=-8, grados_torque=166, velocidad_robot=1200, velocidad_torque=300,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 8 cm y mueve el torque para soltar o colocar el cemento.

# ===================== SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.giro_derecha( -90, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira usando principalmente el motor derecho para reposicionarse.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color.
    velocidad_max=100,  # Usa potencia máxima.
    distancia_cm=9,  # Sigue la línea solo 9 cm para alinearse.
    lado="derecha",  # Sigue el borde derecho.
    tiempo_acomodo_ms=80,  # Tiempo corto de acomodo.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No frena por error.
    perfil_salida="encadenado"  # Termina rápido para seguir.
)

robot.esperar(300)  # Espera 300 ms antes del giro grande.

robot.girar( -170, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 170 grados en sentido negativo sin anticipación.

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=-170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 20 cm y activa el torque para tomar los cementos blancos.

# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.giro_izquierda( 70, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira usando principalmente el motor izquierdo para salir de la zona de agarre.

robot.mover_recto( distancia_cm=39, velocidad=1000, perfil="encadenado")  # Avanza 39 cm para acercarse a la línea frente a la matriz.

robot.girar( -60, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 60 grados en sentido negativo para alinearse con la línea.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color para seguir la línea.
    velocidad_max=100,  # Potencia máxima en seguimiento.
    distancia_cm=20,  # Sigue la línea durante 20 cm.
    lado="derecha",  # Sigue el borde derecho.
    tiempo_acomodo_ms=80,  # Tiempo para acomodarse al borde.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No reduce velocidad por error.
    perfil_salida="encadenado"  # Sale rápido del seguimiento.
)

robot.mover_recto( distancia_cm=40, velocidad=1000, perfil="encadenado")  # Avanza 40 cm para acercarse a la matriz.

# SECCIÓN 4.2 -> ENTRAR EN LA MATRIZ Y ESCANEAR
robot.mover_recto( distancia_cm=19.5, velocidad=700, perfil="seguro")  # Entra 19.5 cm en la matriz con velocidad más controlada.

robot.esperar(500)  # Espera 500 ms antes de escanear para que el robot esté quieto.

matriz_detectada = robot.escanear_matriz()  # Escanea la matriz y guarda el resultado en la variable.
print("Matriz guardada:", matriz_detectada)  # Muestra en pantalla la matriz detectada.

'''
robot.retroceder( distancia_cm=38, velocidad=800, perfil="seguro", invertir_correccion=False, pausa_gyro=30)  # Retrocede 38 cm para salir de la matriz usando corrección con giroscopio.

robot.girar( 180, velocidad=800, velocidad_min=180, anticipacion=10, perfil="encadenado")  # Gira 180 grados para cambiar completamente la orientación del robot.

robot.retroceder( distancia_cm=14, velocidad=850, perfil="seguro", invertir_correccion=False, pausa_gyro=30)  # Retrocede 14 cm para acomodarse antes de dejar los cementos blancos.

robot.girar( 49, velocidad=800, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 49 grados para apuntar hacia el lugar donde soltará los cementos blancos.

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=145, velocidad_robot=900, velocidad_torque=200, 
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 20 cm y mueve el torque para dejar los cementos blancos.

robot.esperar(100)  # Espera 100 ms para estabilizar el robot después de soltar.


# ===================== SECCIÓN 5 (BUSCAR LÍNEA) =====================

robot.mover_recto( distancia_cm=17, velocidad=900, perfil="encadenado")  # Avanza 17 cm para buscar o acercarse a la siguiente línea.

robot.girar( -44, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 44 grados en sentido negativo para orientarse hacia la línea.


# ===================== SECCIÓN 6 (IR POR LOS CEMENTOS VERDES) =====================

# SECCIÓN 6.1 -> IR A BUSCAR LOS CEMENTOS VERDES
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color principal para seguir la línea.
    velocidad_max=100,  # Usa potencia máxima en dc().
    distancia_cm=34,  # Sigue la línea durante 34 cm.
    lado="derecha",  # Sigue el borde derecho de la línea.
    tiempo_acomodo_ms=80,  # Tiempo inicial para acomodarse al borde.
    kp=1.15,  # Corrección proporcional del seguidor.
    kd=2.6,  # Corrección derivativa para estabilizar el movimiento.
    k_freno=0.0,  # No reduce velocidad aunque haya error.
    perfil_salida="encadenado"  # Termina rápido para continuar la rutina.
)

robot.girar( 180, velocidad=850, velocidad_min=180, anticipacion=10, perfil="encadenado")  # Gira 180 grados para quedar de espaldas a los cementos verdes.

robot.avanzar_con_torque( distancia_cm=-29, grados_torque=-150, velocidad_robot=900, velocidad_torque=400,  torque_despues_cm=1,
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 29 cm y activa el torque para tomar los cementos verdes.


# SECCIÓN 6.2 -> DEJAR LOS CEMENTOS VERDES
robot.mover_recto( distancia_cm=5, velocidad=900, perfil="encadenado")  # Avanza 5 cm para salir de la zona de agarre.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color para seguir la línea.
    velocidad_max=100,  # Usa potencia máxima.
    distancia_cm=38,  # Sigue la línea durante 38 cm.
    lado="izquierda",  # Sigue el borde izquierdo de la línea.
    tiempo_acomodo_ms=80,  # Tiempo inicial de acomodo.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No aplica frenado por error.
    perfil_salida="encadenado"  # Termina de forma fluida.
)

robot.girar( -180, velocidad=850, velocidad_min=180, anticipacion=10, perfil="encadenado")  # Gira 180 grados en sentido negativo para orientarse al punto de entrega.

robot.avanzar_con_torque( distancia_cm=-16, grados_torque=175, velocidad_robot=900, velocidad_torque=400, 
esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 16 cm y mueve el torque para soltar los cementos verdes.


# ===================== SECCIÓN 7 (IR POR LOS CEMENTOS AMARILLOS) =====================

# SECCIÓN 7.1 -> TOMAR LOS CEMENTOS AMARILLOS
robot.mover_recto( distancia_cm=9, velocidad=900, perfil="encadenado")  # Avanza 9 cm para iniciar el recorrido hacia los cementos amarillos.

robot.girar( -43, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 43 grados en sentido negativo para acomodar la dirección.

robot.mover_recto( distancia_cm=34, velocidad=900, perfil="encadenado")  # Avanza 34 cm hacia la zona de los cementos amarillos.

robot.girar( 44, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 44 grados para volver a alinearse con el camino.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color principal.
    velocidad_max=100,  # Sigue línea a potencia máxima.
    distancia_cm=9,  # Sigue una línea corta de 9 cm para alinearse.
    lado="derecha",  # Sigue el borde derecho.
    tiempo_acomodo_ms=80,  # Tiempo de acomodo inicial.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No reduce velocidad por error.
    perfil_salida="encadenado"  # Sale rápido del seguimiento.
)

robot.girar( -180, velocidad=750, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira 180 grados en sentido negativo para quedar de espaldas a los cementos amarillos.

robot.avanzar_con_torque( distancia_cm=-18, grados_torque=-170, velocidad_robot=1000, velocidad_torque=400, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 18 cm y activa el torque para agarrar los cementos amarillos.


# SECCIÓN 7.2 -> IR A DEJAR LOS CEMENTOS AMARILLOS
robot.mover_recto( distancia_cm=10, velocidad=900, perfil="encadenado")  # Avanza 10 cm para salir de la zona de agarre.

robot.girar( -75, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 75 grados en sentido negativo para tomar dirección hacia la entrega.

robot.mover_recto( distancia_cm=69, velocidad=900, perfil="seguro")  # Avanza 69 cm con perfil seguro para recorrer una distancia larga con más estabilidad.

robot.girar( 76, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 76 grados para alinearse con la línea de entrega.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color.
    velocidad_max=100,  # Sigue línea con potencia máxima.
    distancia_cm=56,  # Sigue la línea durante 56 cm.
    lado="izquierda",  # Sigue el borde izquierdo de la línea.
    tiempo_acomodo_ms=80,  # Tiempo de acomodo al iniciar.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No frena por error.
    perfil_salida="encadenado"  # Termina rápido para continuar.
)


# SECCIÓN 7.3 -> DEJAR LOS CEMENTOS AMARILLOS
robot.girar(-90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados en sentido negativo para apuntar hacia el lugar de entrega.

robot.avanzar_con_torque( distancia_cm=-17, grados_torque=175, velocidad_robot=900, velocidad_torque=160,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 17 cm y mueve el torque lentamente para soltar los cementos amarillos.

robot.mover_recto( distancia_cm=14, velocidad=900, perfil="encadenado")  # Avanza 14 cm después de dejar los cementos.


# ===================== SECCIÓN 8 (IR POR LOS CEMENTOS AZULES) =====================

# SECCIÓN 8.1 -> TOMAR LOS CEMENTOS AZULES
robot.girar( -90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados en sentido negativo para iniciar el camino hacia los azules.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color principal.
    velocidad_max=100,  # Potencia máxima en seguimiento.
    distancia_cm=55,  # Sigue la línea durante 55 cm.
    lado="derecha",  # Sigue el borde derecho.
    tiempo_acomodo_ms=80,  # Tiempo inicial de acomodo.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No baja velocidad por error.
    perfil_salida="encadenado"  # Sale rápido para enlazar el siguiente movimiento.
)

robot.girar( 140, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 140 grados para orientarse hacia los cementos azules.

robot.retroceder( distancia_cm=27, velocidad=900, perfil="seguro", invertir_correccion=False, pausa_gyro=30)  # Retrocede 27 cm con corrección de giroscopio para acercarse a los azules.

robot.girar( 40, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 40 grados para ajustar la entrada hacia los azules.

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=-175, velocidad_robot=900, velocidad_torque=400, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 20 cm y activa el torque para agarrar los cementos azules.


# SECCIÓN 8.2 -> AGARRAR LA PALA
robot.mover_recto( distancia_cm=10,velocidad=900,perfil="encadenado"
)  # Avanza 10 cm para dirigirse hacia la pala.

robot.girar(-29, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 29 grados en sentido negativo para apuntar hacia la pala.

robot.mover_recto( distancia_cm=44.5, velocidad=900, perfil="seguro")  # Avanza 44.5 cm con perfil seguro hasta la posición de la pala.

robot.mover_garra( velocidad=400, grados=-61)  # Mueve la garra principal -61 grados, normalmente para abrir o preparar agarre.

robot.mover_garra_delantera( velocidad=1000, grados=265)  # Mueve la garra delantera 265 grados para tomar o acomodar la pala.

robot.mover_garra( velocidad=400, grados=61)  # Mueve la garra principal 61 grados, normalmente para cerrar o asegurar.


# SECCIÓN 8.3 -> SEGUIR LÍNEA PARA REGRESAR
robot.retroceder( distancia_cm=8.5, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=30)  # Retrocede 8.5 cm lentamente para salir de la zona de la pala.

robot.giro_derecha( 25, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Hace un giro pequeño de 25 grados usando principalmente el motor derecho.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,  # Usa el sensor de color.
    velocidad_max=100,  # Sigue línea con potencia máxima.
    distancia_cm=140,  # Sigue una línea larga de 140 cm para regresar.
    lado="izquierda",  # Sigue el borde izquierdo de la línea.
    tiempo_acomodo_ms=80,  # Tiempo inicial de acomodo.
    kp=1.15,  # Corrección proporcional.
    kd=2.6,  # Corrección derivativa.
    k_freno=0.0,  # No reduce velocidad por error.
    perfil_salida="encadenado"  # Termina rápido.
)


# SECCIÓN 8.4 -> DEJAR PALA Y CEMENTOS AZULES
robot.mover_garra( velocidad=400, grados=-120)  # Mueve la garra principal -120 grados para soltar o preparar la pala.

robot.retroceder( distancia_cm=12.5, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=30)  # Retrocede 12.5 cm lentamente para posicionarse en la entrega final.

robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados para orientar el robot hacia el punto de entrega.

robot.mover_torque( grados_torque=176, velocidad_torque=500)  # Mueve el motor de torque 176 grados para soltar o levantar el mecanismo.

robot.mover_garra_delantera( velocidad=500, grados=-265)  # Regresa la garra delantera -265 grados para soltar o volver a posición inicial.

robot.mover_garra( velocidad=400, grados=130)  # Mueve la garra principal 130 grados para dejarla en posición final.


# ===================== EJECUTAR MATRIZ =====================
ejecutar_matriz(robot, matriz_detectada)  # Ejecuta la lógica de matriz usando la matriz que fue detectada anteriormente.

'''
