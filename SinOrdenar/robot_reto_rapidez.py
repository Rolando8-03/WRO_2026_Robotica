from robot_control_rapidez import Base  # Importa la clase Base, donde están todas las funciones del robot.
from pybricks.parameters import Color, Direction, Port, Stop  # Importa parámetros de Pybricks para colores, puertos, direcciones y frenado.
from matriz import ejecutar_matriz  # Importa la función para ejecutar acciones según la matriz detectada.

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()  # Crea el objeto robot usando la clase Base.
print(robot.Hub.battery.voltage())  # Muestra el voltaje actual de la batería.
matriz_detectada = None  # Variable donde se guardará la matriz cuando sea escaneada.

'''
# ===================== SECCIÓN 1 (TOMAR CEMENTO Y UBICAR PALA) =====================

# SECCIÓN 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_arco_dc(radio_cm=9.6, angulo_deg=140, potencia=100, lado="derecha")  # Sale haciendo un arco hacia la derecha con radio 9.6 cm y giro de 140 grados.

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=65,
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

# SECCIÓN 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-90, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados en sentido negativo para orientarse al balde.

robot.avanzar_con_torque(distancia_cm=-17.5, grados_torque=-168, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 17.5 cm y activa el torque después de 1 cm para agarrar el balde.

robot.mover_recto( distancia_cm=1.2, velocidad=1000, perfil="encadenado")  # Avanza 1 cm para acomodar el mecanismo o liberar presión.

# SECCIÓN 1.3 -> DEJAR LA PALA DE ALBAÑILERÍA
robot.girar( 67, velocidad=1000, velocidad_min=160, anticipacion=8, perfil="encadenado"
)  # Gira 68.5 grados para orientarse hacia la zona de la pala.

robot.esperar(80)  # Espera 80 ms para estabilizar el robot después del giro.

robot.retroceder(distancia_cm=41, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)  # Retrocede 42 cm usando giroscopio para mantenerse recto.

robot.mover_recto( distancia_cm=38.5, velocidad=1000, perfil="encadenado")  # Avanza 42 cm después de dejar o acomodar la pala.

robot.giro_arco_dc( radio_cm=13, angulo_deg=19, potencia=80, lado="derecha")  # Hace un arco pequeño hacia la derecha para ajustar la dirección.

# ===================== SECCIÓN 2 (DEJAR EL CEMENTO) =====================

# SECCIÓN 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=32.5,
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

# SECCIÓN 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.girar( 90, velocidad=850, velocidad_min=160, anticipacion=8, perfil="encadenado")  # Gira 90 grados para apuntar al estacionamiento.

robot.esperar(100)  # Espera 100 ms para estabilizarse antes de soltar el cemento.

robot.avanzar_con_torque(distancia_cm=-8, grados_torque=166, velocidad_robot=1200, velocidad_torque=300,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 8 cm y mueve el torque para soltar o colocar el cemento.

# ===================== SECCIÓN 3 (IR POR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 3.1 -> POSICIONARSE ENFRENTE DE LA LÍNEA DEL SEGUIDOR
robot.esperar(150) #NO TOCAR ESA ESPERA
robot.giro_derecha(-90, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira usando principalmente el motor derecho para reposicionarse.

robot.seguir_linea_extremo(
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

robot.esperar(300)  # Espera 300 ms antes del giro grande. 300

robot.girar( -170, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 170 grados en sentido negativo sin anticipación.

robot.avanzar_con_torque( distancia_cm=-20, grados_torque=-170, velocidad_robot=1200, velocidad_torque=350, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")  # Retrocede 20 cm y activa el torque para tomar los cementos blancos.

# ===================== SECCIÓN 4 (DEJAR LOS CEMENTOS BLANCOS) =====================

# SECCIÓN 4.1 -> POSICIONARSE EN LA LÍNEA FRENTE A LA MATRIZ
robot.giro_izquierda( 70, velocidad=1200, velocidad_min=160, anticipacion=10, perfil="encadenado")  # Gira usando principalmente el motor izquierdo para salir de la zona de agarre.

robot.mover_recto( distancia_cm=51, velocidad=1000, perfil="encadenado")  # Avanza 39 cm para acercarse a la línea frente a la matriz.

robot.esperar(300)
robot.girar( -50, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 60 grados en sentido negativo para alinearse con la línea.


robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=20,
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

robot.mover_recto( distancia_cm=40, velocidad=1000, perfil="encadenado")  # Avanza 40 cm para acercarse a la matriz.

# SECCIÓN 4.2 -> ENTRAR EN LA MATRIZ Y ESCANEAR
robot.mover_recto( distancia_cm=8, velocidad=700, perfil="seguro")  # Entra 19.5 cm en la matriz con velocidad más controlada.

robot.esperar(500)  # Espera 500 ms antes de escanear para que el robot esté quieto.

matriz_detectada = robot.escanear_matriz()  # Escanea la matriz y guarda el resultado en la variable.
print("Matriz guardada:", matriz_detectada)  # Muestra en pantalla la matriz detectada.


robot.retroceder(distancia_cm=40, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)  # Retrocede 42 cm usando giroscopio para mantenerse recto.
robot.esperar(280)
robot.girar(160, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")  # Gira 60 grados en sentido negativo para alinearse con la línea.
robot.retroceder(distancia_cm=18, velocidad=870, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(300)
robot.girar(41, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-16, grados_torque=168, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.mover_recto( distancia_cm=11, velocidad=1000, perfil="encadenado")
robot.girar(-41, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=42,
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

robot.esperar(250)
robot.girar(-165, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-20, grados_torque=-168, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=44,
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
robot.esperar(300)
robot.girar(-167, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-20.8, grados_torque=168, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=10,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")


robot.mover_recto( distancia_cm=10, velocidad=1000, perfil="encadenado")
robot.girar(-45, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.mover_recto( distancia_cm=29, velocidad=1000, perfil="encadenado")
robot.esperar(300)
robot.girar(44, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
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
robot.esperar(300)
robot.girar(-168, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-20, grados_torque=-68, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")


robot.mover_recto( distancia_cm=10, velocidad=1000, perfil="encadenado")
robot.esperar(300)
robot.girar(-70, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.mover_recto( distancia_cm=55, velocidad=1000, perfil="encadenado") #avanzar a la linea para ir a los amarillos
robot.girar(60, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=66,
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
robot.esperar(300)
robot.girar(-80, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")
robot.avanzar_con_torque(distancia_cm=-17, grados_torque=168, velocidad_robot=1200, velocidad_torque=500, torque_despues_cm=1,
 esperar_torque=False, perfil_entrada="encadenado", perfil_salida="encadenado")

'''
robot.seguir_linea_extremo(
    sensor_color=robot.seguidor,
    velocidad_max=100,
    distancia_cm=10,
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
robot.esperar(300)
robot.girar(-65, velocidad=1200, velocidad_min=160, anticipacion=0, perfil="encadenado")


