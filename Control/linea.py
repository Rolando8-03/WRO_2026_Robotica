from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

from Control import robot_config as config


class Linea:

    # ============================================================
    # SEGUIDOR DE LÍNEA POR BORDE
    # ============================================================

    def seguir_linea(
        self,
        distancia_cm,
        lado=config.LINEA_LADO_DEFAULT,
        velocidad_max=config.LINEA_VELOCIDAD_MAX,

        # Parámetros que a veces se calibran
        tiempo_acomodo_ms=config.LINEA_TIEMPO_ACOMODO_MS,
        tiempo_aceleracion_ms=config.LINEA_TIEMPO_ACELERACION_MS,
        kp=config.LINEA_KP,
        kd=config.LINEA_KD,
        k_freno=config.LINEA_K_FRENO,
        objetivo_reflexion=config.LINEA_OBJETIVO_REFLEXION,
        margen_cm=config.LINEA_MARGEN_CM,
        perfil_salida=config.LINEA_PERFIL_SALIDA,

        # Captura inicial
        captura_inicial=config.LINEA_CAPTURA_INICIAL,
        tiempo_captura_ms=config.LINEA_TIEMPO_CAPTURA_MS,
        potencia_captura=config.LINEA_POTENCIA_CAPTURA,
        kp_captura=config.LINEA_KP_CAPTURA,
        margen_captura=config.LINEA_MARGEN_CAPTURA,
        lecturas_estables_captura=config.LINEA_LECTURAS_ESTABLES_CAPTURA,

        # Casi nunca cambia
        correccion_max=config.LINEA_CORRECCION_MAX,
        sensor_color=None
    ):
        """
        Sigue el borde de una línea usando potencia directa dc().

        Uso simple:
            robot.seguir_linea_extremo(42)

        Uso calibrado:
            robot.seguir_linea_extremo(
                42,
                lado="izquierda",
                velocidad_max=90,
                kp=1.35,
                kd=3.0
            )
        """

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

        if lado == "derecha":
            multiplicador_lado = 1
        else:
            multiplicador_lado = -1

        self.reset_motores()

        # =====================================================
        # FASE 1: CAPTURA INICIAL DEL BORDE
        # =====================================================

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

                correction = error * kp_captura * multiplicador_lado
                correction = self.limitar(
                    correction,
                    -correccion_max,
                    correccion_max
                )

                if abs(error) > 22:
                    velocidad_base = 28
                else:
                    velocidad_base = potencia_captura

                potencia_izq = velocidad_base - correction
                potencia_der = velocidad_base + correction

                potencia_izq = self.limitar(potencia_izq, -100, 100)
                potencia_der = self.limitar(potencia_der, -100, 100)

                self.motor_izquierdo.dc(potencia_izq)
                self.motor_derecho.dc(potencia_der)

                wait(2)

            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(8)

            self.reset_motores()

        # =====================================================
        # FASE 2: SEGUIMIENTO RÁPIDO
        # =====================================================

        cronometro = StopWatch()
        cronometro.reset()

        velocidad_minima = 55

        last_error = 0
        last_derivative = 0

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

                velocidad_actual = velocidad_minima + (
                    (velocidad_max - velocidad_minima) * progreso
                )

            else:
                velocidad_actual = velocidad_max

            lectura = sensor_color.reflection()
            error = lectura - objetivo_reflexion

            derivative = (
                (error - last_error) * 0.82
            ) + (
                last_derivative * 0.18
            )

            correction = (
                (error * kp) +
                (derivative * kd)
            ) * multiplicador_lado

            correction = self.limitar(
                correction,
                -correccion_max,
                correccion_max
            )

            velocidad_base = velocidad_actual - (abs(error) * k_freno)

            if velocidad_base < 38:
                velocidad_base = 38

            potencia_izq = velocidad_base - correction
            potencia_der = velocidad_base + correction

            potencia_izq = self.limitar(potencia_izq, -100, 100)
            potencia_der = self.limitar(potencia_der, -100, 100)

            self.motor_izquierdo.dc(potencia_izq)
            self.motor_derecho.dc(potencia_der)

            last_error = error
            last_derivative = derivative

            wait(2)

        self.terminar_movimiento(
            perfil=perfil_salida,
            modo="brake"
        )

    # ============================================================
    # DETECTOR DE LÍNEAS NEGRAS
    # ============================================================

    def avanzar_hasta_n_lineas_negras(
        self,
        cantidad_lineas,
        velocidad=500,
        umbral_negro=config.UMBRAL_NEGRO,
        umbral_salida=config.UMBRAL_SALIDA_NEGRO,
        perfil=config.PERFIL_SEGURO
    ):
        """
        Avanza hasta contar cierta cantidad de líneas negras.
        """

        if cantidad_lineas <= 0:
            return

        self.preparar_movimiento(
            reset_motores=True,
            reset_gyro=False,
            perfil=perfil
        )

        contador_lineas = 0
        en_negro = False

        while contador_lineas < cantidad_lineas:
            lectura = self.seguidor.reflection()

            if lectura <= umbral_negro and not en_negro:
                contador_lineas += 1
                en_negro = True
                print("Línea negra detectada:", contador_lineas)

            elif lectura >= umbral_salida:
                en_negro = False

            self.motor_izquierdo.run(velocidad)
            self.motor_derecho.run(velocidad)

            wait(5)

        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

    def mover_hasta_linea(
        self,
        distancia_cm_max,
        velocidad=750,
        distancia_minima_cm=0,
        lineas_a_ignorar=0,

        # Sensor
        umbral_negro=config.UMBRAL_NEGRO,
        umbral_salida=config.UMBRAL_SALIDA_NEGRO,
        lecturas_negras_necesarias=config.LECTURAS_NEGRAS_NECESARIAS,
        lecturas_claras_necesarias=config.LECTURAS_CLARAS_NECESARIAS,

        # Movimiento
        kp=config.MOV_KP,
        kd=config.MOV_KD,
        correccion_max=config.MOV_CORRECCION_MAX,
        perfil=config.PERFIL_SEGURO
    ):
        """
        Avanza o retrocede hasta encontrar una línea negra,
        con límite máximo de distancia.
        """

        if distancia_cm_max == 0:
            return False

        self.preparar_movimiento(
            reset_motores=True,
            reset_gyro=True,
            perfil=perfil
        )

        signo = 1 if distancia_cm_max > 0 else -1

        distancia_mm = abs(distancia_cm_max) * 10
        grados_maximos = distancia_mm * self.grados_por_mm

        distancia_minima_mm = abs(distancia_minima_cm) * 10
        grados_minimos = distancia_minima_mm * self.grados_por_mm

        contador_lineas = 0

        lectura_inicial = self.seguidor.reflection()
        en_negro = lectura_inicial <= umbral_negro

        conteo_negro = 0
        conteo_claro = 0

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        while self.distancia_promedio_grados() < grados_maximos:
            recorrido = self.distancia_promedio_grados()
            lectura = self.seguidor.reflection()

            if recorrido >= grados_minimos:

                if lectura <= umbral_negro:
                    conteo_negro += 1
                    conteo_claro = 0

                    if conteo_negro >= lecturas_negras_necesarias and not en_negro:
                        en_negro = True
                        contador_lineas += 1

                        print("Línea detectada:", contador_lineas)

                        if contador_lineas > lineas_a_ignorar:
                            self.terminar_movimiento(
                                perfil=perfil,
                                modo="brake"
                            )
                            return True

                elif lectura >= umbral_salida:
                    conteo_claro += 1
                    conteo_negro = 0

                    if conteo_claro >= lecturas_claras_necesarias:
                        en_negro = False

            dt = reloj.time() / 1000
            if dt <= 0:
                dt = 0.001

            error = self.Hub.imu.heading()

            if abs(error) < 0.7:
                error = 0

            derivada = (error - error_anterior) / dt

            correccion = (error * kp) + (derivada * kd)
            correccion = self.limitar(
                correccion,
                -correccion_max,
                correccion_max
            )

            base = velocidad * signo

            if signo > 0:
                pot_izq = int(base - correccion)
                pot_der = int(base + correccion)
            else:
                pot_izq = int(base + correccion)
                pot_der = int(base - correccion)

            pot_izq = self.limitar(pot_izq, -1000, 1000)
            pot_der = self.limitar(pot_der, -1000, 1000)

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            error_anterior = error
            reloj.reset()

            wait(3)

        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

        print("No se encontró la línea dentro de la distancia máxima.")
        return False

    # ============================================================
    # VALIDACIONES DE SENSOR
    # ============================================================

    def leer_reflexion_promedio(
        self,
        sensor=None,
        muestras=5,
        pausa_ms=3
    ):
        """
        Devuelve un promedio de reflexión.
        """

        if sensor is None:
            sensor = self.seguidor

        total = 0

        for _ in range(muestras):
            total += sensor.reflection()
            wait(pausa_ms)

        return total / muestras

    def sobre_negro_estable(
        self,
        sensor=None,
        umbral_negro=config.UMBRAL_NEGRO,
        muestras=3,
        pausa_ms=3
    ):
        """
        Devuelve True si el sensor está sobre negro durante varias muestras.
        """

        if sensor is None:
            sensor = self.seguidor

        conteo_negro = 0

        for _ in range(muestras):
            if sensor.reflection() <= umbral_negro:
                conteo_negro += 1

            wait(pausa_ms)

        return conteo_negro >= muestras

    def esperar_salida_negro(
        self,
        sensor=None,
        umbral_salida=config.UMBRAL_SALIDA_NEGRO,
        timeout_ms=600
    ):
        """
        Espera hasta que el sensor salga de negro.
        """

        if sensor is None:
            sensor = self.seguidor

        reloj = StopWatch()
        reloj.reset()

        while reloj.time() < timeout_ms:
            if sensor.reflection() >= umbral_salida:
                return True

            wait(3)

        return False

    # ============================================================
    # ACOMODO SOBRE BORDE DE LÍNEA
    # ============================================================

    def acomodar_borde_linea(
        self,
        direccion=1,
        velocidad=180,
        objetivo_reflexion=config.LINEA_OBJETIVO_REFLEXION,
        margen=3,
        timeout_ms=450,
        perfil_salida=config.PERFIL_ENCADENADO
    ):
        """
        Mueve el robot lentamente hasta quedar cerca del borde de la línea.
        """

        reloj = StopWatch()
        reloj.reset()

        while reloj.time() < timeout_ms:
            lectura = self.seguidor.reflection()

            if objetivo_reflexion - margen <= lectura <= objetivo_reflexion + margen:
                break

            self.motor_izquierdo.run(velocidad * direccion)
            self.motor_derecho.run(velocidad * direccion)

            wait(4)

        self.terminar_movimiento(
            perfil=perfil_salida,
            modo="brake"
        )