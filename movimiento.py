from pybricks.parameters import Stop
from pybricks.tools import wait, StopWatch

import robot_config as config


class Movimiento:

    # ============================================================
    # INICIO Y SALIDA DE MOVIMIENTOS
    # ============================================================

    def preparar_movimiento(
        self,
        reset_motores=True,
        reset_gyro=True,
        perfil=config.PERFIL_SEGURO,
        pausa=None
    ):
        """
        Prepara el robot antes de un movimiento.

        perfil="seguro":
            Más estable. Útil después de movimientos bruscos.

        perfil="encadenado":
            Más rápido. Útil cuando una función sigue a otra.
        """

        if perfil == config.PERFIL_SEGURO:
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(8)

            self.motor_izquierdo.stop()
            self.motor_derecho.stop()
            wait(4)

            pausa_gyro = 18

        elif perfil == config.PERFIL_ENCADENADO:
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(4)

            self.motor_izquierdo.stop()
            self.motor_derecho.stop()
            wait(2)

            pausa_gyro = 7

        else:
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(8)

            self.motor_izquierdo.stop()
            self.motor_derecho.stop()
            wait(4)

            pausa_gyro = 18

        if pausa is not None:
            pausa_gyro = pausa

        if reset_motores:
            self.reset_motores()

        if reset_gyro:
            self.Hub.imu.reset_heading(0)
            wait(pausa_gyro)

    def terminar_movimiento(
        self,
        perfil=config.PERFIL_SEGURO,
        modo="brake",
        pausa=None,
        soltar=True
    ):
        """
        Termina un movimiento.

        modo="brake":
            Frena con control pasivo.

        modo="stop":
            Detiene y libera el motor.

        modo="hold":
            Mantiene la posición con fuerza.

        soltar=True:
            Después de brake(), hace stop() para no dejar el motor amarrado.
        """

        if modo == "brake":
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()

        elif modo == "stop":
            self.motor_izquierdo.stop()
            self.motor_derecho.stop()

        elif modo == "hold":
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()

        if pausa is not None:
            wait(pausa)

        elif perfil == config.PERFIL_SEGURO:
            wait(18)

        elif perfil == config.PERFIL_ENCADENADO:
            wait(6)

        else:
            wait(15)

        if soltar and modo == "brake":
            self.motor_izquierdo.stop()
            self.motor_derecho.stop()
            wait(2)

    # ============================================================
    # AVANZAR
    # ============================================================

    def avanzar(
        self,
        distancia_cm,
        velocidad=config.MOV_VELOCIDAD_RECTA,
        perfil=config.PERFIL_ENCADENADO,

        # Control interno, pero libre de cambiar si se necesita calibrar
        kp=config.MOV_KP,
        kd=config.MOV_KD,
        correccion_max=config.MOV_CORRECCION_MAX,
        velocidad_min=config.MOV_VELOCIDAD_MIN
    ):
        """
        Avanza o retrocede según el signo de distancia_cm.

        distancia_cm:
            Positivo = avanza.
            Negativo = retrocede.

        Esta función reemplaza a mover_recto().
        """

        if distancia_cm == 0:
            return

        self.preparar_movimiento(
            reset_motores=True,
            reset_gyro=True,
            perfil=perfil
        )

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm

        signo = 1 if distancia_cm > 0 else -1

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        velocidad_actual = velocidad_min
        rampa = 40

        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            # Aceleración progresiva
            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            # Frenado al final
            if restante < 170:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad * restante / 170)
                )

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

            base = velocidad_actual * signo

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

            wait(2)

        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

    # ============================================================
    # RETROCEDER
    # ============================================================

    def retroceder(
        self,
        distancia_cm,
        velocidad=config.MOV_VELOCIDAD_RETROCESO,
        perfil=config.PERFIL_SEGURO,
        pausa_gyro=config.MOV_PAUSA_GYRO_RETROCESO,
        invertir_correccion=False,

        # Control interno, pero libre de cambiar si se necesita calibrar
        kp=config.MOV_KP,
        kd=config.MOV_KD,
        correccion_max=config.MOV_CORRECCION_MAX,
        velocidad_min=config.MOV_VELOCIDAD_MIN
    ):
        """
        Retrocede de forma estable usando corrección con giroscopio.

        distancia_cm:
            Se escribe positivo.
            Ejemplo: robot.retroceder(40)
        """

        if distancia_cm == 0:
            return

        self.preparar_movimiento(
            reset_motores=True,
            reset_gyro=True,
            perfil=perfil,
            pausa=pausa_gyro
        )

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        velocidad_actual = velocidad_min
        rampa = 35

        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            # Aceleración progresiva
            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            # Frenado al final
            if restante < 170:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad * restante / 170)
                )

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

            base = -velocidad_actual

            if not invertir_correccion:
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

            wait(2)

        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

    # ============================================================
    # AVANZAR / RETROCEDER CON TORQUE
    # ============================================================

    def avanzar_con_torque(
        self,
        distancia_cm,
        grados_torque,
        velocidad_torque=config.TORQUE_VELOCIDAD_MOTOR,
        velocidad_robot=config.TORQUE_VELOCIDAD_ROBOT,
        torque_despues_cm=config.TORQUE_DESPUES_CM,

        # Casos especiales
        esperar_torque=config.TORQUE_ESPERAR,
        levantar_final_grados=config.TORQUE_LEVANTAR_FINAL_GRADOS,

        # Control interno, pero libre de cambiar si se necesita calibrar
        kp=config.MOV_KP,
        kd=config.MOV_KD,
        correccion_max=config.MOV_CORRECCION_MAX,
        velocidad_min=config.MOV_VELOCIDAD_MIN,

        # Perfiles
        perfil_entrada=config.PERFIL_ENCADENADO,
        perfil_salida=config.PERFIL_ENCADENADO
    ):
        """
        Mueve el robot y activa el motor de torque después de cierta distancia.

        distancia_cm:
            Positivo = avanza.
            Negativo = retrocede.

        grados_torque:
            Positivo o negativo según el mecanismo.

        torque_despues_cm:
            Distancia que recorre el robot antes de activar el torque.
        """

        if distancia_cm == 0:
            return

        self.preparar_movimiento(
            reset_motores=True,
            reset_gyro=True,
            perfil=perfil_entrada
        )

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm

        torque_despues_mm = abs(torque_despues_cm) * 10
        grados_inicio_torque = torque_despues_mm * self.grados_por_mm

        signo = 1 if distancia_cm > 0 else -1

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        velocidad_actual = velocidad_min
        rampa = 40

        torque_activado = False

        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            # Activar torque después de cierta distancia
            if not torque_activado and recorrido >= grados_inicio_torque:
                self.motor_torque.run_angle(
                    velocidad_torque,
                    grados_torque,
                    then=Stop.HOLD,
                    wait=False
                )
                torque_activado = True

            # Aceleración progresiva
            if velocidad_actual < velocidad_robot:
                velocidad_actual += rampa
                if velocidad_actual > velocidad_robot:
                    velocidad_actual = velocidad_robot

            # Frenado al final
            if restante < 170:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad_robot * restante / 170)
                )

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

            base = velocidad_actual * signo

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

            wait(2)

        self.terminar_movimiento(
            perfil=perfil_salida,
            modo="brake"
        )

        # Si el recorrido fue corto y nunca activó el torque, lo activa al final.
        if not torque_activado and grados_torque != 0:
            self.motor_torque.run_angle(
                velocidad_torque,
                grados_torque,
                then=Stop.HOLD,
                wait=False
            )
            torque_activado = True

        # Esperar opcionalmente a que termine el torque.
        if esperar_torque and torque_activado:
            while self.motor_torque.control.done() == False:
                wait(5)

        # Levantar o corregir al final si se solicita.
        if levantar_final_grados != 0:
            if torque_activado:
                while self.motor_torque.control.done() == False:
                    wait(5)

            self.motor_torque.run_angle(
                velocidad_torque,
                levantar_final_grados,
                then=Stop.HOLD,
                wait=True
            )