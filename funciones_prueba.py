"""Funciones experimentales del robot.

Estas funciones se conservan para hacer pruebas y comparar comportamientos,
pero no forman parte de la versión principal del recorrido.
"""

from pybricks.tools import wait, StopWatch


# -----------------------------------------------------------------------------
# avanzar_hasta_color_prueba
# Versión experimental de avance hasta color.
# Confirma el color con varias lecturas consecutivas y permite avanzar una
# distancia adicional después de detectarlo.
# -----------------------------------------------------------------------------
def avanzar_hasta_color_prueba(
    self,
    color_objetivo,
    velocidad=400,
    kp_gyro=20.0,
    cruces=1,
    rebase_cm=0.0,
    perfil="encadenado"
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
    viendo_color = False
    lecturas_consecutivas = 0

    # Inicia el movimiento antes de entrar al bucle de detección.
    self.drive_base.drive(
        abs(velocidad) * signo,
        0
    )

    # =====================================================================
    # FASE 1: DETECCIÓN Y CONTEO DEL COLOR
    # Exige tres lecturas consecutivas para confirmar el color.
    # =====================================================================
    while True:
        es_color_actual = self._es_color(
            color_objetivo
        )

        if es_color_actual:
            lecturas_consecutivas += 1
        else:
            lecturas_consecutivas = 0

        es_color_confirmado = (
            lecturas_consecutivas >= 3
        )

        if es_color_confirmado:
            if not viendo_color:
                viendo_color = True
                conteo_cruces += 1

                if conteo_cruces >= cruces:
                    break
        else:
            if lecturas_consecutivas == 0:
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

        wait(2)

    # =====================================================================
    # FASE 2: REBASE POR DISTANCIA
    # Después de detectar el último color, avanza una distancia adicional.
    # =====================================================================
    if abs(rebase_cm) > 0:
        self.drive_base.reset()

        distancia_objetivo_mm = (
            abs(rebase_cm) * 10.0
        )

        while (
            abs(self.drive_base.distance())
            < distancia_objetivo_mm
        ):
            actual_heading = self.Hub.imu.heading()

            error_gyro = self._error_angular(
                heading_objetivo,
                actual_heading
            )

            self.drive_base.drive(
                abs(velocidad) * signo,
                error_gyro * kp_gyro
            )

            wait(2)

    # =====================================================================
    # FASE 3: SALIDA
    # =====================================================================
    self.drive_base.stop()

    if perfil != "encadenado":
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(20)


# -----------------------------------------------------------------------------
# seguir_linea_pro
# Versión experimental del seguidor de línea.
# Permite elegir una dirección de búsqueda inicial distinta del lado que se
# seguirá después y reduce las pausas para probar transiciones más fluidas.
# -----------------------------------------------------------------------------
def seguir_linea_pro(
    self,
    sensor_color=None,
    velocidad_max=100,
    distancia_cm=70,
    lado="derecha",
    dir_busqueda_inicial=None,
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
    tiempo_captura_ms=200,
    potencia_captura=55,
    kp_captura=2.4,
    margen_captura=5,
    lecturas_estables_captura=2
):
    if sensor_color is None:
        sensor_color = self.seguidor

    diametro_rueda_cm = (
        self.diametro_rueda / 10
    )

    circunferencia_cm = (
        3.14159 * diametro_rueda_cm
    )

    grados_objetivo = (
        distancia_cm
        / circunferencia_cm
    ) * 360

    if margen_cm > 0:
        grados_margen = (
            margen_cm
            / circunferencia_cm
        ) * 360
    else:
        grados_margen = 0

    grados_objetivo_real = max(
        0,
        grados_objetivo - grados_margen
    )

    multiplicador_lado = (
        1
        if lado == "derecha"
        else -1
    )

    # Permite buscar la línea inicialmente hacia un lado
    # y seguirla luego desde el borde contrario.
    if dir_busqueda_inicial is not None:
        multiplicador_captura = (
            1
            if dir_busqueda_inicial == "derecha"
            else -1
        )
    else:
        multiplicador_captura = multiplicador_lado

    self.reset_motores()

    # =====================================================================
    # FASE 1: CAPTURA INICIAL RÁPIDA
    # =====================================================================
    if captura_inicial:
        reloj_captura = StopWatch()
        reloj_captura.reset()

        estables = 0

        while (
            reloj_captura.time()
            < tiempo_captura_ms
        ):
            lectura = sensor_color.reflection()
            error = lectura - objetivo_reflexion

            if abs(error) <= margen_captura:
                estables += 1

                if (
                    estables
                    >= lecturas_estables_captura
                ):
                    break
            else:
                estables = 0

            correccion = (
                error
                * kp_captura
                * multiplicador_captura
            )

            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            velocidad_base = (
                35
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

        # En perfil encadenado no se introduce una parada extra.
        if perfil_salida != "encadenado":
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(5)

        self.reset_motores()

    # =====================================================================
    # FASE 2: SEGUIMIENTO DE LÍNEA
    # =====================================================================
    cronometro = StopWatch()
    cronometro.reset()

    velocidad_minima = 75
    error_anterior = 0
    derivada_anterior = 0

    while True:
        grados_actuales = (
            self.distancia_promedio_grados()
        )

        if (
            grados_actuales
            >= grados_objetivo_real
        ):
            break

        tiempo_actual = cronometro.time()

        if (
            tiempo_actual
            < tiempo_acomodo_ms
        ):
            velocidad_actual = velocidad_minima

        elif (
            tiempo_actual
            < tiempo_acomodo_ms
            + tiempo_aceleracion_ms
        ):
            progreso = (
                tiempo_actual
                - tiempo_acomodo_ms
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

        if velocidad_base < 60:
            velocidad_base = 60

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
    # SALIDA EXPERIMENTAL
    # =====================================================================
    if perfil_salida == "encadenado":
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

    else:
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(15)