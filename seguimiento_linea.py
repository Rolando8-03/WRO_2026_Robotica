"""Funciones de seguimiento de línea del robot.

Este archivo contiene los movimientos que mantienen al robot siguiendo el
borde de una línea mediante el sensor de color y un controlador PD.
"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch


# -----------------------------------------------------------------------------
# seguir_linea
# Sigue el borde de una línea durante una distancia determinada.
# Incluye una fase inicial para capturar la línea y luego un control PD.
# -----------------------------------------------------------------------------
def seguir_linea(
    self,
    sensor_color=None,
    velocidad_max=100,
    distancia_cm=70,
    lado="derecha",
    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=120,
    kp=1.15,
    kd=2.6,
    k_freno=0.15,
    objetivo_reflexion=27,
    correccion_max=100,
    margen_cm=0,
    perfil_salida="encadenado",
    captura_inicial=True,
    tiempo_captura_ms=260,
    potencia_captura=55,
    kp_captura=2.4,
    margen_captura=5,
    lecturas_estables_captura=2
):
    if sensor_color is None:
        sensor_color = self.seguidor

    diametro_rueda_cm = self.diametro_rueda / 10
    circunferencia_cm = 3.14159 * diametro_rueda_cm
    grados_objetivo = (distancia_cm / circunferencia_cm) * 360

    if margen_cm > 0:
        grados_margen = (margen_cm / circunferencia_cm) * 360
    else:
        grados_margen = 0

    grados_objetivo_real = max(0, grados_objetivo - grados_margen)
    multiplicador_lado = 1 if lado == "derecha" else -1

    self.reset_motores()

    # =====================================================================
    # FASE 1: CAPTURA INICIAL DE LA LÍNEA
    # Busca el borde de la línea antes de comenzar el seguimiento principal.
    # =====================================================================
    if captura_inicial:
        reloj_captura = StopWatch()
        reloj_captura.reset()
        estables = 0

        while reloj_captura.time() < tiempo_captura_ms:
            lectura = sensor_color.reflection()
            error = lectura - objetivo_reflexion

            if abs(error) <= margen_captura:
                estables += 1

                if estables >= lecturas_estables_captura:
                    break
            else:
                estables = 0

            correccion = error * kp_captura * multiplicador_lado
            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = 28 if abs(error) > 22 else potencia_captura

            potencia_izq = velocidad_base - correccion
            potencia_der = velocidad_base + correccion

            self.motor_izquierdo.dc(
                self.limitar(potencia_izq, -100, 100)
            )

            self.motor_derecho.dc(
                self.limitar(potencia_der, -100, 100)
            )

            wait(2)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(8)

        # La distancia recorrida durante la captura no cuenta como trayecto.
        self.reset_motores()

    # =====================================================================
    # FASE 2: SEGUIMIENTO DE LÍNEA POR DISTANCIA
    # =====================================================================
    cronometro = StopWatch()
    cronometro.reset()

    velocidad_minima = 75
    error_anterior = 0
    derivada_anterior = 0

    while True:
        grados_actuales = self.distancia_promedio_grados()

        if grados_actuales >= grados_objetivo_real:
            break

        tiempo_actual = cronometro.time()

        if tiempo_actual < tiempo_acomodo_ms:
            velocidad_actual = velocidad_minima

        elif tiempo_actual < tiempo_acomodo_ms + tiempo_aceleracion_ms:
            progreso = (
                tiempo_actual - tiempo_acomodo_ms
            ) / tiempo_aceleracion_ms

            velocidad_actual = (
                velocidad_minima
                + (velocidad_max - velocidad_minima) * progreso
            )

        else:
            velocidad_actual = velocidad_max

        lectura = sensor_color.reflection()
        error = lectura - objetivo_reflexion

        derivada = (
            (error - error_anterior) * 0.82
            + derivada_anterior * 0.18
        )

        correccion = (
            (error * kp)
            + (derivada * kd)
        ) * multiplicador_lado

        correccion = self.limitar(
            correccion,
            -correccion_max,
            correccion_max
        )

        velocidad_base = velocidad_actual - abs(error) * k_freno

        if velocidad_base < 55:
            velocidad_base = 55

        potencia_izq = velocidad_base - correccion
        potencia_der = velocidad_base + correccion

        self.motor_izquierdo.dc(
            self.limitar(potencia_izq, -100, 100)
        )

        self.motor_derecho.dc(
            self.limitar(potencia_der, -100, 100)
        )

        error_anterior = error
        derivada_anterior = derivada

        wait(2)

    self.terminar_movimiento(
        perfil=perfil_salida,
        modo="brake"
    )


# -----------------------------------------------------------------------------
# seguir_linea_hasta_color
# Sigue el borde de una línea sin una distancia fija y termina cuando el mismo
# sensor detecta un color objetivo.
# -----------------------------------------------------------------------------
def seguir_linea_hasta_color(
    self,
    color_objetivo,
    sensor_color=None,
    velocidad_max=100,
    lado="derecha",
    tiempo_acomodo_ms=140,
    tiempo_aceleracion_ms=120,
    kp=1.15,
    kd=2.6,
    k_freno=0.15,
    objetivo_reflexion=27,
    correccion_max=100,
    perfil_salida="encadenado",
    captura_inicial=True,
    tiempo_captura_ms=260,
    potencia_captura=55,
    kp_captura=2.4,
    margen_captura=5,
    lecturas_estables_captura=2
):
    if sensor_color is None:
        sensor_color = self.seguidor

    multiplicador_lado = 1 if lado == "derecha" else -1

    self.reset_motores()

    # =====================================================================
    # FASE 1: CAPTURA INICIAL DE LA LÍNEA
    # =====================================================================
    if captura_inicial:
        reloj_captura = StopWatch()
        reloj_captura.reset()
        estables = 0

        while reloj_captura.time() < tiempo_captura_ms:
            lectura = sensor_color.reflection()
            error = lectura - objetivo_reflexion

            if abs(error) <= margen_captura:
                estables += 1

                if estables >= lecturas_estables_captura:
                    break
            else:
                estables = 0

            correccion = error * kp_captura * multiplicador_lado
            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = 28 if abs(error) > 22 else potencia_captura

            potencia_izq = velocidad_base - correccion
            potencia_der = velocidad_base + correccion

            self.motor_izquierdo.dc(
                self.limitar(potencia_izq, -100, 100)
            )

            self.motor_derecho.dc(
                self.limitar(potencia_der, -100, 100)
            )

            wait(2)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(8)
        self.reset_motores()

    # =====================================================================
    # FASE 2: SEGUIMIENTO INDEFINIDO HASTA DETECTAR EL COLOR
    # =====================================================================
    cronometro = StopWatch()
    cronometro.reset()

    velocidad_minima = 75
    error_anterior = 0
    derivada_anterior = 0

    while True:
        color_actual = sensor_color.color()
        hsv = sensor_color.hsv()
        reflexion = sensor_color.reflection()

        encontrado = False

        if color_objetivo == Color.BLUE:
            if hsv.s > 70:
                encontrado = True

        elif color_objetivo == Color.BLACK:
            if hsv.s < 30 and reflexion < 15:
                encontrado = True

        elif color_objetivo == Color.GRAY:
            # El gris tiene baja saturación (falta de color puro) y una reflexión media.
            # Ajusta estos valores (20 y 60) según la iluminación y el tono de gris de tu pista.
            if hsv.s < 25 and 15 < reflexion < 60:
                encontrado = True

        else:
            if color_actual == color_objetivo:
                encontrado = True

        if encontrado:
            # Contramarcha breve para reducir el desplazamiento por inercia.
            self.motor_izquierdo.dc(-100)
            self.motor_derecho.dc(-100)
            wait(30)

            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)

            break

        tiempo_actual = cronometro.time()

        if tiempo_actual < tiempo_acomodo_ms:
            velocidad_actual = velocidad_minima

        elif tiempo_actual < tiempo_acomodo_ms + tiempo_aceleracion_ms:
            progreso = (
                tiempo_actual - tiempo_acomodo_ms
            ) / tiempo_aceleracion_ms

            velocidad_actual = (
                velocidad_minima
                + (velocidad_max - velocidad_minima) * progreso
            )

        else:
            velocidad_actual = velocidad_max

        lectura = sensor_color.reflection()
        error = lectura - objetivo_reflexion

        derivada = (
            (error - error_anterior) * 0.82
            + derivada_anterior * 0.18
        )

        correccion = (
            (error * kp)
            + (derivada * kd)
        ) * multiplicador_lado

        correccion = self.limitar(
            correccion,
            -correccion_max,
            correccion_max
        )

        velocidad_base = velocidad_actual - abs(error) * k_freno

        if velocidad_base < 55:
            velocidad_base = 55

        potencia_izq = velocidad_base - correccion
        potencia_der = velocidad_base + correccion

        self.motor_izquierdo.dc(
            self.limitar(potencia_izq, -100, 100)
        )

        self.motor_derecho.dc(
            self.limitar(potencia_der, -100, 100)
        )

        error_anterior = error
        derivada_anterior = derivada

        wait(2)
