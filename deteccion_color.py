"""Funciones de detección de colores y líneas.

Este archivo contiene las calibraciones HSV y los movimientos que avanzan
buscando un color, contando cruces o combinando distancia con detección.
"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch


# Rangos calibrados con el tapete y la iluminación del robot.
HSV_RANGOS = {
    Color.BLUE: {
        "h": (215, 220),
        "s": (86, 90),
        "v": (20, 33)
    },
    Color.GREEN: {
        "h": (149, 161),
        "s": (52, 61),
        "v": (17, 25)
    },
    Color.YELLOW: {
        "h": (39, 48),
        "s": (67, 70),
        "v": (50, 68)
    },
    Color.WHITE: {
        "h": (204, 216),
        "s": (13, 20),
        "v": (74, 80),
        "reflection": (47, 53)
    },
    Color.BLACK: {
        "s": (10, 40),
        "v": (8, 16),
        "reflection": (0, 8)
    },

    # Color azul específico utilizado dentro de la matriz.
    # No es un valor nativo de Color en Pybricks.
    "BLUE_MATRIX": {
        "h": (221, 225),
        "s": (91, 94),
        "v": (33, 47)
    }
}


# -----------------------------------------------------------------------------
# _es_color
# Comprueba si la lectura actual se encuentra dentro de los rangos HSV
# calibrados para un color.
# -----------------------------------------------------------------------------
def _es_color(self, color):
    if color not in HSV_RANGOS:
        raise ValueError(
            "No existe una calibración para {}".format(color)
        )

    hsv = self.seguidor.hsv()

    lectura = {
        "h": hsv.h,
        "s": hsv.s,
        "v": hsv.v,
        "reflection": self.seguidor.reflection()
    }

    for componente, limites in HSV_RANGOS[color].items():
        minimo, maximo = limites
        valor = lectura[componente]

        if not minimo <= valor <= maximo:
            return False

    return True


# -----------------------------------------------------------------------------
# avanzar_hasta_color
# Avanza recto manteniendo el rumbo y se detiene después de detectar una
# cantidad determinada de cruces del color objetivo.
# -----------------------------------------------------------------------------
def avanzar_hasta_color(
    self,
    color_objetivo,
    velocidad=300,
    kp_gyro=20.0,
    cruces=1,
    perfil="seguro"
):
    self.preparar_movimiento(
        reset_motores=False,
        reset_gyro=False,
        perfil=perfil
    )

    self.drive_base.reset()

    heading_objetivo = self.Hub.imu.heading()
    signo = 1 if velocidad > 0 else -1

    conteo_cruces = 0

    # Evita contar repetidamente el mismo parche de color.
    viendo_color = False

    while True:
        color_actual = self.seguidor.color()
        hsv = self.seguidor.hsv()
        reflexion = self.seguidor.reflection()

        es_color_objetivo = False

        # El azul se distingue del negro por su saturación alta.
        if color_objetivo == Color.BLUE:
            if hsv.s > 70:
                es_color_objetivo = True

        # El negro se detecta mediante saturación y reflexión bajas.
        elif color_objetivo == Color.BLACK:
            if hsv.s < 30 and reflexion < 15:
                es_color_objetivo = True

        # Para los demás colores se usa la clasificación de Pybricks.
        else:
            if color_actual == color_objetivo:
                es_color_objetivo = True

        # Detección de flanco:
        # solo cuenta cuando el sensor entra por primera vez al color.
        if es_color_objetivo:
            if not viendo_color:
                viendo_color = True
                conteo_cruces += 1

                if conteo_cruces >= cruces:
                    break
        else:
            viendo_color = False

        actual_heading = self.Hub.imu.heading()

        error_gyro = self._error_angular(
            heading_objetivo,
            actual_heading
        )

        self.drive_base.drive(
            abs(velocidad) * signo,
            error_gyro * kp_gyro
        )

    self.drive_base.stop()

    self.motor_izquierdo.hold()
    self.motor_derecho.hold()

    wait(20)


# -----------------------------------------------------------------------------
# avanzar_cruzando_lineas
# Avanza recto contando líneas negras. Usa una distancia ciega después de cada
# detección para no contar varias veces el grosor de una misma línea.
# -----------------------------------------------------------------------------
def avanzar_cruzando_lineas(
    self,
    cruces_objetivo=1,
    velocidad=300,
    escape_inicial_cm=0,
    margen_linea_cm=3.5,
    kp_gyro=20.0,
    perfil="seguro",
    retraso_freno_ms=0
):
    self.preparar_movimiento(
        reset_motores=False,
        reset_gyro=False,
        perfil=perfil
    )

    self.drive_base.reset()

    heading_objetivo = self.Hub.imu.heading()
    signo = 1 if velocidad > 0 else -1

    conteo_cruces = 0

    # Distancia durante la que se ignora el sensor al comienzo.
    distancia_desbloqueo_mm = escape_inicial_cm * 10

    while True:
        distancia_actual_mm = abs(
            self.drive_base.distance()
        )

        actual_heading = self.Hub.imu.heading()

        error_gyro = self._error_angular(
            heading_objetivo,
            actual_heading
        )

        self.drive_base.drive(
            abs(velocidad) * signo,
            error_gyro * kp_gyro
        )

        # Ventana ciega para ignorar una línea inicial o el grosor
        # de una línea que acaba de ser contada.
        if distancia_actual_mm < distancia_desbloqueo_mm:
            continue

        hsv = self.seguidor.hsv()
        reflexion = self.seguidor.reflection()

        es_linea_negra = (
            hsv.s < 30
            and reflexion < 18
        )

        if es_linea_negra:
            conteo_cruces += 1

            if conteo_cruces >= cruces_objetivo:
                # Permite avanzar un poco más después de detectar
                # la última línea antes de frenar.
                if retraso_freno_ms > 0:
                    reloj_extra = StopWatch()
                    reloj_extra.reset()

                    while reloj_extra.time() < retraso_freno_ms:
                        actual_heading_extra = (
                            self.Hub.imu.heading()
                        )

                        error_gyro_extra = self._error_angular(
                            heading_objetivo,
                            actual_heading_extra
                        )

                        self.drive_base.drive(
                            abs(velocidad) * signo,
                            error_gyro_extra * kp_gyro
                        )

                break

            # Ignora el sensor durante cierta distancia para no volver
            # a contar la misma línea.
            distancia_desbloqueo_mm = (
                distancia_actual_mm
                + margen_linea_cm * 10
            )

    self.drive_base.stop()

    self.motor_izquierdo.brake()
    self.motor_derecho.brake()
    wait(60)

    self.motor_izquierdo.hold()
    self.motor_derecho.hold()
    wait(20)


# -----------------------------------------------------------------------------
# avanzar_hibrido
# Primero avanza una distancia determinada y después comienza a buscar el
# color objetivo. La detección no se activa antes de completar la distancia.
# -----------------------------------------------------------------------------
def avanzar_hibrido(
    self,
    distancia_inicial_cm,
    color_objetivo,
    velocidad_max=400,
    velocidad_min=150,
    kp_gyro=20.0,
    zona_transicion_cm=3,
    perfil="encadenado",
    cruces=1,
    **kwargs
):
    if distancia_inicial_cm == 0:
        return self.avanzar_hasta_color(
            color_objetivo=color_objetivo,
            velocidad=velocidad_max,
            kp_gyro=kp_gyro,
            cruces=cruces,
            perfil=perfil
        )

    self.preparar_movimiento(
        reset_motores=False,
        reset_gyro=False,
        perfil=perfil
    )

    self.drive_base.reset()

    heading_objetivo = self.Hub.imu.heading()
    signo = 1 if velocidad_max > 0 else -1

    zona_transicion_cm = min(
        zona_transicion_cm,
        distancia_inicial_cm / 2
    )

    fase_busqueda_activa = False
    conteo_cruces = 0
    viendo_color = False

    cronometro = StopWatch()
    cronometro.reset()

    velocidad_actual = velocidad_min
    distancia_actual = 0

    while True:
        distancia_actual = (
            abs(self.drive_base.distance()) / 10
        )

        distancia_restante = (
            distancia_inicial_cm
            - distancia_actual
        )

        # La detección se calcula en cada ciclo, pero solo se cuenta
        # después de completar la distancia inicial.
        if color_objetivo in HSV_RANGOS:
            es_color_objetivo = self._es_color(
                color_objetivo
            )
        else:
            es_color_objetivo = (
                self.seguidor.color()
                == color_objetivo
            )

        if fase_busqueda_activa and es_color_objetivo:
            if not viendo_color:
                viendo_color = True
                conteo_cruces += 1

                if conteo_cruces >= cruces:
                    break
        else:
            viendo_color = False

        if (
            distancia_actual >= distancia_inicial_cm
            and not fase_busqueda_activa
        ):
            fase_busqueda_activa = True

        # Fase 1: recorrer la distancia indicada.
        if not fase_busqueda_activa:
            tiempo_actual = cronometro.time()

            if tiempo_actual < 150:
                factor = tiempo_actual / 150

                velocidad_actual = (
                    velocidad_min
                    + (
                        velocidad_max - velocidad_min
                    ) * factor
                )
            else:
                velocidad_actual = velocidad_max

            # Desacelera suavemente antes de activar la búsqueda.
            if (
                distancia_restante < zona_transicion_cm
                and distancia_restante > 0
            ):
                progreso = (
                    distancia_restante
                    / zona_transicion_cm
                )

                velocidad_actual *= (
                    0.5 + 0.5 * progreso
                )

                if velocidad_actual < 60:
                    velocidad_actual = 60

            if distancia_restante <= 0:
                velocidad_actual = velocidad_max * 0.9

        # Fase 2: buscar los cruces del color solicitado.
        else:
            if conteo_cruces < cruces:
                if conteo_cruces > 0:
                    factor = (
                        1.0
                        - (conteo_cruces / cruces) * 0.3
                    )

                    velocidad_actual = (
                        velocidad_max
                        * 0.6
                        * factor
                    )
                else:
                    velocidad_actual = velocidad_max * 0.6

                velocidad_actual = max(
                    velocidad_actual,
                    100
                )
            else:
                velocidad_actual = velocidad_max * 0.5

        actual_heading = self.Hub.imu.heading()

        error_gyro = self._error_angular(
            heading_objetivo,
            actual_heading
        )

        velocidad_final = max(
            velocidad_actual,
            80
        )

        self.drive_base.drive(
            velocidad_final * signo,
            error_gyro * kp_gyro
        )

        wait(3)

    self.drive_base.stop()

    self.motor_izquierdo.brake()
    self.motor_derecho.brake()
    wait(60)

    self.motor_izquierdo.hold()
    self.motor_derecho.hold()
    wait(20)