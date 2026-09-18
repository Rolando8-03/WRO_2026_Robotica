from pybricks.parameters import Color
from pybricks.tools import wait

def _realizar_lectura_estatica(
    self,
    cantidad_lecturas=12,
    espera_inicial_ms=100,
    intervalo_lecturas_ms=20,
    votos_minimos=4
):
    self.frenar()
    wait(espera_inicial_ms)

    conteos = {
        Color.GREEN: 0,
        Color.YELLOW: 0,
        Color.BLUE: 0,
        Color.WHITE: 0
    }

    lecturas_validas = 0

    for _ in range(cantidad_lecturas):
        color = self.seguidor.color()

        if color in conteos:
            conteos[color] += 1
            lecturas_validas += 1

        wait(intervalo_lecturas_ms)

    if lecturas_validas == 0:
        return None

    color_ganador = max(conteos, key=conteos.get)

    if conteos[color_ganador] < votos_minimos:
        return None

    return color_ganador


def escanear_matriz(self):
    primer_color = self._realizar_lectura_estatica()

    if primer_color is None:
        print("No se detectó un color de matriz válido.")
        return None

    # Matriz 1 y 4 empiezan con verde.
    # Se avanza para leer el segundo color y diferenciarlas.
    if primer_color == Color.GREEN:
        self.avanzar_recto(
            distancia_cm=4,
            velocidad_max=300,
            perfil="rapido"
        )

        segundo_color = self._realizar_lectura_estatica()

        if segundo_color == Color.GREEN:
            matriz_detectada = 1

        elif segundo_color == Color.YELLOW:
            matriz_detectada = 4

        else:
            print("Segundo color verde no válido:", segundo_color)
            return None

    elif primer_color == Color.YELLOW:
        matriz_detectada = 2

    elif primer_color == Color.WHITE:
        matriz_detectada = 3

    elif primer_color == Color.BLUE:
        matriz_detectada = 5

    else:
        print("Color no válido:", primer_color)
        return None

    self.matriz_detectada = matriz_detectada
    print("Matriz detectada:", matriz_detectada)

    return matriz_detectada

def dejar_bloques_matriz(robot):
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=75,
        distancia_cm=16,
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
    robot.mover_garra_principal(900, 230, apretar=False, duty_cierre=100)
    robot.mover_garra_delantera(230)

    robot.avanzar_recto(
        distancia_cm=-15,
        velocidad_max=400,
        perfil="seguro"
    )

    robot.mover_garra_delantera(270, simultaneo=True, velocidad=800)
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
    robot.mover_garra_principal(
        500,
        esperar=False,
        potencia_apriete=150,
        apretar=True
    )
    robot.mover_garra_delantera(100)

    robot.seguir_linea_hasta_color(
    color_objetivo=Color.BLUE,
    velocidad_max=85,
    lado="derecha"
    )

    wait(200)
    robot.girar_corto(-11)
    robot.avanzar_recto(
        distancia_cm=11.5,
        velocidad_max=650,
        perfil="encadenado"
    )

    robot.mover_garra_delantera(220)
    robot.mover_garra_rapida(130)
    robot.avanzar_recto(
        distancia_cm=-0.6,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(290, simultaneo=True)
    robot.avanzar_recto(
        distancia_cm=1.7,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

    for _ in range(3):
        robot.girar_corto(9, potencia_max=70, potencia_min=40)
        robot.girar_corto(-9, potencia_max=70, potencia_min=40)

    robot.avanzar_recto(
        distancia_cm=-1.3,
        velocidad_max=500,
        zona_rampa_cm=0.5,
        perfil="seguro"
    )
    robot.mover_garra_delantera(100, simultaneo=True)
    robot.avanzar_recto(
        distancia_cm=-17,
        velocidad_max=500,
        perfil="seguro"
    )
    robot.girar_hasta_negro("izquierda", potencia=65, potencia_correccion=25)


# Aquí termina la sección de movimientos para entrar en la matriz.
def dejar_bloques_matriz2(robot):
    """Secuencia correspondiente al recorrido auxiliar de matriz 2."""
    robot.avanzar_cruzando_lineas(
    cruces_objetivo=1,
    velocidad=900,
    escape_inicial_cm=8,
    retraso_freno_ms=95
    )  
    robot.girar(
        90,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=50,
        distancia_cm=9,
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
    robot.mover_garra_principal(900, 230, apretar=False, duty_cierre=60)
    robot.mover_garra_delantera(230)
    robot.avanzar_recto(distancia_cm=-19, velocidad_max=400, perfil="seguro")
    robot.mover_garra_delantera(270)
    robot.seguir_linea(
        sensor_color=robot.seguidor,
        velocidad_max=100,
        distancia_cm=18,
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
    robot.mover_garra_principal(
        500,
        esperar=False,
        potencia_apriete=150,
        apretar=True
    )
    robot.mover_garra_delantera(100)
    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(200)
    robot.girar_corto(-11.5)
    robot.avanzar_recto(
        distancia_cm=2.5,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(220)
    robot.mover_garra_rapida(130)
    robot.avanzar_recto(
        distancia_cm=-0.6,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(290)
    robot.avanzar_recto(
        distancia_cm=1.8,
        velocidad_max=750,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    for _ in range(3):
        robot.girar_corto(9, potencia_max=70, potencia_min=40)
        robot.girar_corto(-9, potencia_max=70, potencia_min=40)

    robot.avanzar_recto(
        distancia_cm=-1,
        velocidad_max=900,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(0)
    robot.avanzar_recto(
        distancia_cm=-29,
        velocidad_max=900,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.girar(
        182,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
    robot.avanzar_recto(
        distancia_cm=-23,
        velocidad_max=900,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )

# NO MODIFICAR: dejar_bloques_matriz3
# Se mantiene exactamente con la lógica de la rama oficial_v1-2.
def dejar_bloques_matriz3(robot, distancia_entrada=0):

    #robot.mover_garra_delantera(80)
    #robot.avanzar_recto(-8)
    #robot.mover_garra_principal(100, grados=190, esperar=False)
    #robot.mover_garra_delantera(275)
    

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

    robot.mover_garra_principal(
        300,
        grados=55,
        esperar=False,
        potencia_apriete=190,
        apretar=True
    )

    robot.mover_garra_delantera(100)

    robot.seguir_linea_hasta_color(
        color_objetivo=Color.BLUE,
        velocidad_max=100,
        lado="derecha"
    )

    wait(200)
    robot.girar_corto(-11.6)

    robot.avanzar_recto(
        distancia_cm=distancia_entrada,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(230)
    robot.mover_garra_rapida(130)
    robot.avanzar_recto(
        distancia_cm=-0.6,
        velocidad_max=650,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(290)
    robot.avanzar_recto(
        distancia_cm=1.8,
        velocidad_max=750,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    for _ in range(3):
        robot.girar_corto(9, potencia_max=70, potencia_min=40)
        robot.girar_corto(-9, potencia_max=70, potencia_min=40)

    robot.avanzar_recto(
        distancia_cm=-2,
        velocidad_max=900,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.mover_garra_delantera(0)
    robot.avanzar_recto(
        distancia_cm=-15,
        velocidad_max=900,
        zona_rampa_cm=0.1,
        perfil="encadenado"
    )
    robot.girar(
        182,
        potencia_max=85,
        potencia_min=35,
        kp_base=5.0,
        tolerancia_fin=1.0,
        perfil="encadenado"
    )
