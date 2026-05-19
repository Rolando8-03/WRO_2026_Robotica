from pybricks.tools import wait

import robot_config as config


class Giros:

    # ============================================================
    # GIRO RÁPIDO CON DOS MOTORES
    # ============================================================

    def girar(
        self,
        angulo_deg,
        velocidad=config.GIRO_VELOCIDAD,
        anticipacion=config.GIRO_ANTICIPACION,
        velocidad_min=config.GIRO_VELOCIDAD_MIN,
        perfil=config.PERFIL_ENCADENADO,
        zona_freno=config.GIRO_ZONA_FRENO
    ):
        """
        Gira sobre su eje usando los dos motores.

        angulo_deg:
            Positivo = gira hacia un lado.
            Negativo = gira hacia el otro lado.

        anticipacion:
            Si el giro se pasa, subir anticipacion.
            Si queda corto, bajar anticipacion.
        """

        if angulo_deg == 0:
            return

        self.preparar_movimiento(
            reset_motores=False,
            reset_gyro=True,
            perfil=perfil
        )

        objetivo = abs(angulo_deg)
        objetivo_corte = max(0, objetivo - anticipacion)

        signo = 1 if angulo_deg > 0 else -1

        while True:
            actual = abs(self.Hub.imu.heading())

            if actual >= objetivo_corte:
                break

            restante = objetivo_corte - actual

            if restante > zona_freno:
                vel = velocidad
            else:
                vel = max(
                    velocidad_min,
                    int(velocidad * restante / zona_freno)
                )

            pot_izq = vel * signo
            pot_der = -vel * signo

            pot_izq = self.limitar(pot_izq, -1000, 1000)
            pot_der = self.limitar(pot_der, -1000, 1000)

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            wait(1)

        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

    # ============================================================
    # GIRO CON UN SOLO MOTOR
    # ============================================================

    def _giro_un_motor(
        self,
        motor_activo,
        motor_fijo,
        angulo_deg,
        sentido_motor,
        velocidad=config.GIRO_UN_MOTOR_VELOCIDAD,
        anticipacion=config.GIRO_UN_MOTOR_ANTICIPACION,
        velocidad_min=config.GIRO_UN_MOTOR_VELOCIDAD_MIN,
        perfil=config.PERFIL_SEGURO,
        zona_freno=config.GIRO_UN_MOTOR_ZONA_FRENO
    ):
        """
        Giro interno usando un motor activo y otro fijo.

        No se llama directamente desde el reto.
        Para el reto se usan:
        - giro_izquierda()
        - giro_derecha()
        """

        if angulo_deg == 0:
            return

        self.preparar_movimiento(
            reset_motores=False,
            reset_gyro=True,
            perfil=perfil
        )

        objetivo = abs(angulo_deg)
        objetivo_corte = max(0, objetivo - anticipacion)

        signo = 1 if angulo_deg > 0 else -1

        motor_fijo.brake()
        wait(2)

        while True:
            actual = abs(self.Hub.imu.heading())

            if actual >= objetivo_corte:
                break

            restante = objetivo_corte - actual

            if restante > zona_freno:
                vel = velocidad
            else:
                vel = max(
                    velocidad_min,
                    int(velocidad * restante / zona_freno)
                )

            potencia = vel * signo * sentido_motor
            potencia = self.limitar(potencia, -1000, 1000)

            motor_activo.run(potencia)

            wait(1)

        motor_activo.brake()
        motor_fijo.brake()

        if perfil == config.PERFIL_ENCADENADO:
            wait(8)
        else:
            wait(22)

        motor_activo.stop()
        motor_fijo.stop()
        wait(2)

    def giro_izquierda(
        self,
        angulo_deg,
        velocidad=config.GIRO_UN_MOTOR_VELOCIDAD,
        anticipacion=config.GIRO_UN_MOTOR_ANTICIPACION,
        velocidad_min=config.GIRO_UN_MOTOR_VELOCIDAD_MIN,
        perfil=config.PERFIL_SEGURO,
        zona_freno=config.GIRO_UN_MOTOR_ZONA_FRENO
    ):
        """
        Giro usando principalmente el motor izquierdo.
        """

        self._giro_un_motor(
            motor_activo=self.motor_izquierdo,
            motor_fijo=self.motor_derecho,
            angulo_deg=angulo_deg,
            sentido_motor=1,
            velocidad=velocidad,
            velocidad_min=velocidad_min,
            anticipacion=anticipacion,
            zona_freno=zona_freno,
            perfil=perfil
        )

    def giro_derecha(
        self,
        angulo_deg,
        velocidad=config.GIRO_UN_MOTOR_VELOCIDAD,
        anticipacion=config.GIRO_UN_MOTOR_ANTICIPACION,
        velocidad_min=config.GIRO_UN_MOTOR_VELOCIDAD_MIN,
        perfil=config.PERFIL_SEGURO,
        zona_freno=config.GIRO_UN_MOTOR_ZONA_FRENO
    ):

        self._giro_un_motor(
            motor_activo=self.motor_derecho,
            motor_fijo=self.motor_izquierdo,
            angulo_deg=angulo_deg,
            sentido_motor=-1,
            velocidad=velocidad,
            velocidad_min=velocidad_min,
            anticipacion=anticipacion,
            zona_freno=zona_freno,
            perfil=perfil
        )

    # ============================================================
    # GIRO EN ARCO CON POTENCIA DC
    # ============================================================

    def arcgirar(
        self,
        radio_cm,
        angulo_deg,
        potencia=80,
        lado="derecha",
        distancia_ruedas_cm=12
    ):
        """
        Hace un giro en arco usando potencia directa dc().

        radio_cm:
            Radio del arco.

        angulo_deg:
            Grados del arco.

        potencia:
            Potencia directa de los motores, de -100 a 100.

        lado:
            "derecha" o "izquierda".
        """

        if angulo_deg == 0:
            return

        pi = 3.1416

        radio_interno = radio_cm - (distancia_ruedas_cm / 2)
        radio_externo = radio_cm + (distancia_ruedas_cm / 2)

        if radio_interno <= 0:
            print("Radio muy pequeño para hacer arco.")
            return

        distancia_interna = (
            2 * pi * radio_interno * (abs(angulo_deg) / 360)
        )

        distancia_externa = (
            2 * pi * radio_externo * (abs(angulo_deg) / 360)
        )

        relacion = distancia_interna / distancia_externa

        potencia_externa = potencia
        potencia_interna = potencia * relacion

        potencia_externa = max(-100, min(100, potencia_externa))
        potencia_interna = max(-100, min(100, potencia_interna))

        self.reset_motores()

        grados_objetivo_externo = (
            distancia_externa * 10 * self.grados_por_mm
        )

        signo = 1 if angulo_deg > 0 else -1

        if lado == "derecha":
            pot_izq = potencia_externa * signo
            pot_der = potencia_interna * signo
            motor_externo = self.motor_izquierdo
        else:
            pot_izq = potencia_interna * signo
            pot_der = potencia_externa * signo
            motor_externo = self.motor_derecho

        while abs(motor_externo.angle()) < grados_objetivo_externo:
            self.motor_izquierdo.dc(pot_izq)
            self.motor_derecho.dc(pot_der)
            wait(5)

        self.frenar()