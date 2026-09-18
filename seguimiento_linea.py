"""Funciones de seguimiento de línea del robot.

Este archivo contiene los movimientos que mantienen al robot siguiendo el
borde de una línea mediante el sensor de color y un controlador PD.
"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Stop
from deteccion_color import HSV_RANGOS


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
    lecturas_estables_captura=2,
    zona_desaceleracion_cm=0,
    velocidad_fin_rampa=75
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

    grados_objetivo_real = max(
        0,
        grados_objetivo - grados_margen
    )

    # Convertimos la zona de desaceleración de cm a grados de rueda.
    if zona_desaceleracion_cm > 0:
        grados_desaceleracion = (
            zona_desaceleracion_cm / circunferencia_cm
        ) * 360
    else:
        grados_desaceleracion = 0

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

            correccion = (
                error
                * kp_captura
                * multiplicador_lado
            )

            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = (
                28 if abs(error) > 22
                else potencia_captura
            )

            potencia_izq = velocidad_base - correccion
            potencia_der = velocidad_base + correccion

            self.motor_izquierdo.dc(
                self.limitar(
                    potencia_izq,
                    -100,
                    100
                )
            )

            self.motor_derecho.dc(
                self.limitar(
                    potencia_der,
                    -100,
                    100
                )
            )

            wait(2)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(8)

        # La distancia recorrida durante la captura
        # no cuenta como trayecto.
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

        # ================================================================
        # RAMPA DE ACELERACIÓN INICIAL
        # ================================================================
        if tiempo_actual < tiempo_acomodo_ms:
            velocidad_actual = velocidad_minima

        elif (
            tiempo_actual
            < tiempo_acomodo_ms + tiempo_aceleracion_ms
        ):
            progreso = (
                tiempo_actual - tiempo_acomodo_ms
            ) / tiempo_aceleracion_ms

            velocidad_actual = (
                velocidad_minima
                + (velocidad_max - velocidad_minima)
                * progreso
            )

        else:
            velocidad_actual = velocidad_max

        # ================================================================
        # RAMPA DE DESACELERACIÓN FINAL
        #
        # Cuando el robot entra en los últimos
        # "zona_desaceleracion_cm", empieza a reducir progresivamente
        # su velocidad hasta "velocidad_fin_rampa".
        # ================================================================
        if grados_desaceleracion > 0:
            grados_restantes = (
                grados_objetivo_real - grados_actuales
            )

            if grados_restantes <= grados_desaceleracion:

                progreso_freno = 1 - (
                    grados_restantes
                    / grados_desaceleracion
                )

                # Seguridad por si existe alguna pequeña
                # variación en las mediciones.
                progreso_freno = self.limitar(
                    progreso_freno,
                    0,
                    1
                )

                velocidad_actual = (
                    velocidad_actual
                    + (
                        velocidad_fin_rampa
                        - velocidad_actual
                    )
                    * progreso_freno
                )

        # ================================================================
        # CONTROL PD DEL SEGUIDOR
        # ================================================================
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

        velocidad_base = (
            velocidad_actual
            - abs(error) * k_freno
        )

        if velocidad_base < 55:
            velocidad_base = 55

        potencia_izq = (
            velocidad_base - correccion
        )

        potencia_der = (
            velocidad_base + correccion
        )

        self.motor_izquierdo.dc(
            self.limitar(
                potencia_izq,
                -100,
                100
            )
        )

        self.motor_derecho.dc(
            self.limitar(
                potencia_der,
                -100,
                100
            )
        )

        error_anterior = error
        derivada_anterior = derivada

        wait(2)

    # =====================================================================
    # FINALIZACIÓN
    # =====================================================================
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
    lecturas_estables_captura=2,
    lecturas_color_estables=3
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

            correccion = (
                error
                * kp_captura
                * multiplicador_lado
            )

            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = (
                28
                if abs(error) > 22
                else potencia_captura
            )

            potencia_izq = velocidad_base - correccion
            potencia_der = velocidad_base + correccion

            self.motor_izquierdo.dc(
                self.limitar(
                    potencia_izq,
                    -100,
                    100
                )
            )

            self.motor_derecho.dc(
                self.limitar(
                    potencia_der,
                    -100,
                    100
                )
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

    # Evita detenerse por una sola lectura accidental.
    lecturas_color = 0

    while True:
        hsv = sensor_color.hsv()
        reflexion = sensor_color.reflection()

        encontrado = False

        # ================================================================
        # DETECCIÓN USANDO LA LIBRERÍA HSV CALIBRADA
        # ================================================================
        if color_objetivo in HSV_RANGOS:
            limites_color = HSV_RANGOS[color_objetivo]

            encontrado = True

            for componente, limites in limites_color.items():
                minimo, maximo = limites

                if componente == "h":
                    valor = hsv.h

                elif componente == "s":
                    valor = hsv.s

                elif componente == "v":
                    valor = hsv.v

                elif componente == "reflection":
                    valor = reflexion

                else:
                    encontrado = False
                    break

                if not minimo <= valor <= maximo:
                    encontrado = False
                    break

        # Si el color no está calibrado, usa Pybricks como respaldo.
        else:
            encontrado = (
                sensor_color.color()
                == color_objetivo
            )

        # ================================================================
        # CONFIRMACIÓN MEDIANTE VARIAS LECTURAS CONSECUTIVAS
        # ================================================================
        if encontrado:
            lecturas_color += 1
        else:
            lecturas_color = 0

        if lecturas_color >= lecturas_color_estables:
            # Contramarcha breve para compensar la inercia.
            self.motor_izquierdo.dc(-100)
            self.motor_derecho.dc(-100)
            wait(30)

            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)

            break

        # ================================================================
        # PERFIL DE VELOCIDAD
        # ================================================================
        tiempo_actual = cronometro.time()

        if tiempo_actual < tiempo_acomodo_ms:
            velocidad_actual = velocidad_minima

        elif (
            tiempo_actual
            < tiempo_acomodo_ms + tiempo_aceleracion_ms
        ):
            progreso = (
                tiempo_actual - tiempo_acomodo_ms
            ) / tiempo_aceleracion_ms

            velocidad_actual = (
                velocidad_minima
                + (
                    velocidad_max - velocidad_minima
                ) * progreso
            )

        else:
            velocidad_actual = velocidad_max

        # ================================================================
        # CONTROL PD DEL SEGUIDOR DE LÍNEA
        # ================================================================
        lectura = reflexion
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

        velocidad_base = (
            velocidad_actual
            - abs(error) * k_freno
        )

        if velocidad_base < 55:
            velocidad_base = 55

        potencia_izq = velocidad_base - correccion
        potencia_der = velocidad_base + correccion

        self.motor_izquierdo.dc(
            self.limitar(
                potencia_izq,
                -100,
                100
            )
        )

        self.motor_derecho.dc(
            self.limitar(
                potencia_der,
                -100,
                100
            )
        )

        error_anterior = error
        derivada_anterior = derivada

        wait(2)


#=================SEGUIR LINEA Y MOVER TORQUE ==============================================

def seguir_linea_y_mover_torque(
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
    lecturas_estables_captura=2,
    zona_desaceleracion_cm=0,
    velocidad_fin_rampa=75,
    distancia_torque_cm=None,
    grados_torque=0,
    velocidad_torque=180,
    modo_final_torque=Stop.HOLD
):
    """
    Combina seguir_linea() + mover_torque() en un solo recorrido.

    - Sigue la línea mediante el mismo control de seguir_linea().
    - Al superar distancia_torque_cm dentro del recorrido, dispara
      mover_torque() en modo NO bloqueante.
    - Incluye la misma rampa de desaceleración final de seguir_linea().
    - El robot continúa siguiendo la línea mientras el torque se mueve
      en paralelo.

    Si distancia_torque_cm es None o grados_torque es 0, el torque
    simplemente no se activa.
    """

    if sensor_color is None:
        sensor_color = self.seguidor

    diametro_rueda_cm = self.diametro_rueda / 10
    circunferencia_cm = 3.14159 * diametro_rueda_cm

    grados_objetivo = (
        distancia_cm / circunferencia_cm
    ) * 360

    if margen_cm > 0:
        grados_margen = (
            margen_cm / circunferencia_cm
        ) * 360
    else:
        grados_margen = 0

    grados_objetivo_real = max(
        0,
        grados_objetivo - grados_margen
    )

    # =====================================================================
    # CONVERSIÓN DE ZONA DE DESACELERACIÓN DE CM A GRADOS
    # =====================================================================

    if zona_desaceleracion_cm > 0:
        grados_desaceleracion = (
            zona_desaceleracion_cm / circunferencia_cm
        ) * 360
    else:
        grados_desaceleracion = 0

    multiplicador_lado = (
        1 if lado == "derecha"
        else -1
    )

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

            correccion = (
                error
                * kp_captura
                * multiplicador_lado
            )

            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = (
                28
                if abs(error) > 22
                else potencia_captura
            )

            potencia_izq = (
                velocidad_base - correccion
            )

            potencia_der = (
                velocidad_base + correccion
            )

            self.motor_izquierdo.dc(
                self.limitar(
                    potencia_izq,
                    -100,
                    100
                )
            )

            self.motor_derecho.dc(
                self.limitar(
                    potencia_der,
                    -100,
                    100
                )
            )

            wait(2)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

        wait(8)

        # La distancia recorrida durante la captura
        # no cuenta como trayecto.
        self.reset_motores()

    # =====================================================================
    # FASE 2: SEGUIMIENTO DE LÍNEA + TORQUE
    # =====================================================================

    cronometro = StopWatch()
    cronometro.reset()

    velocidad_minima = 75

    error_anterior = 0
    derivada_anterior = 0

    torque_aplicado = False

    while True:

        # -------------------------------------------------------------
        # DISTANCIA RECORRIDA
        # -------------------------------------------------------------

        grados_actuales = (
            self.distancia_promedio_grados()
        )

        if grados_actuales >= grados_objetivo_real:
            break

        distancia_actual_cm = (
            grados_actuales / 360
        ) * circunferencia_cm

        # -------------------------------------------------------------
        # DISPARO DEL TORQUE
        # -------------------------------------------------------------

        if (
            not torque_aplicado
            and distancia_torque_cm is not None
            and grados_torque != 0
            and distancia_actual_cm >= distancia_torque_cm
        ):

            self.mover_torque(
                grados_torque,
                velocidad_torque=velocidad_torque,
                esperar=False,
                modo_final=modo_final_torque
            )

            torque_aplicado = True

        # -------------------------------------------------------------
        # RAMPA DE ACELERACIÓN INICIAL
        # -------------------------------------------------------------

        tiempo_actual = cronometro.time()

        if tiempo_actual < tiempo_acomodo_ms:

            velocidad_actual = velocidad_minima

        elif (
            tiempo_actual
            < tiempo_acomodo_ms + tiempo_aceleracion_ms
        ):

            progreso = (
                tiempo_actual - tiempo_acomodo_ms
            ) / tiempo_aceleracion_ms

            velocidad_actual = (
                velocidad_minima
                + (
                    velocidad_max
                    - velocidad_minima
                ) * progreso
            )

        else:

            velocidad_actual = velocidad_max

        # -------------------------------------------------------------
        # RAMPA DE DESACELERACIÓN FINAL
        # -------------------------------------------------------------
        #
        # Cuando el robot entra en los últimos
        # "zona_desaceleracion_cm", comienza a reducir
        # progresivamente la velocidad hasta
        # "velocidad_fin_rampa".
        # -------------------------------------------------------------

        if grados_desaceleracion > 0:

            grados_restantes = (
                grados_objetivo_real
                - grados_actuales
            )

            if grados_restantes <= grados_desaceleracion:

                progreso_freno = 1 - (
                    grados_restantes
                    / grados_desaceleracion
                )

                # Seguridad ante pequeñas variaciones
                # en las mediciones.
                progreso_freno = self.limitar(
                    progreso_freno,
                    0,
                    1
                )

                velocidad_actual = (
                    velocidad_actual
                    + (
                        velocidad_fin_rampa
                        - velocidad_actual
                    ) * progreso_freno
                )

        # -------------------------------------------------------------
        # CONTROL PD DEL SEGUIDOR
        # -------------------------------------------------------------

        lectura = sensor_color.reflection()

        error = (
            lectura
            - objetivo_reflexion
        )

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

        # -------------------------------------------------------------
        # FRENO SEGÚN ERROR DEL SENSOR
        # -------------------------------------------------------------

        velocidad_base = (
            velocidad_actual
            - abs(error) * k_freno
        )

        if velocidad_base < 55:
            velocidad_base = 55

        # -------------------------------------------------------------
        # POTENCIA DE MOTORES
        # -------------------------------------------------------------

        potencia_izq = (
            velocidad_base
            - correccion
        )

        potencia_der = (
            velocidad_base
            + correccion
        )

        self.motor_izquierdo.dc(
            self.limitar(
                potencia_izq,
                -100,
                100
            )
        )

        self.motor_derecho.dc(
            self.limitar(
                potencia_der,
                -100,
                100
            )
        )

        error_anterior = error
        derivada_anterior = derivada

        wait(2)

    # =====================================================================
    # FINALIZACIÓN
    # =====================================================================

    self.terminar_movimiento(
        perfil=perfil_salida,
        modo="brake"
    )
