from pybricks.parameters import Stop
from pybricks.tools import wait, StopWatch

import robot_config as config


class Manipuladores:

    # ============================================================
    # MOTOR DE TORQUE
    # ============================================================

    def mover_torque(
        self,
        grados_torque,
        velocidad_torque=config.TORQUE_VELOCIDAD_MOTOR,
        esperar=True,
        modo_final=Stop.HOLD
    ):
        """
        Mueve el motor de torque.

        grados_torque:
            Positivo o negativo según el sentido del mecanismo.

        velocidad_torque:
            Velocidad del motor de torque.

        esperar:
            True = espera a que termine.
            False = continúa mientras el motor se mueve.

        modo_final:
            Stop.HOLD, Stop.BRAKE, Stop.COAST, etc.
        """

        self.motor_torque.run_angle(
            velocidad_torque,
            grados_torque,
            then=modo_final,
            wait=esperar
        )

    def esperar_torque_hasta(
        self,
        grados_relativos,
        timeout_ms=700
    ):
        """
        Espera hasta que el motor de torque haya recorrido
        cierta cantidad de grados, o hasta que se acabe el tiempo.

        Sirve cuando no querés esperar todo el movimiento,
        sino solo una parte.
        """

        inicio = self.motor_torque.angle()
        objetivo = abs(grados_relativos)

        reloj = StopWatch()
        reloj.reset()

        while True:
            recorrido = abs(self.motor_torque.angle() - inicio)

            if recorrido >= objetivo:
                break

            if reloj.time() > timeout_ms:
                break

            wait(3)

    # ============================================================
    # GARRA TRASERA
    # ============================================================

    def mover_garra(
        self,
        grados,
        velocidad=config.GARRA_VELOCIDAD,
        esperar=False,
        modo_final=Stop.HOLD
    ):
        self.motor_garra.run_angle(
            velocidad,
            grados,
            then=modo_final,
            wait=esperar
        )

    # ============================================================
    # GARRA DELANTERA
    # ============================================================

    def mover_garra_delantera(
        self,
        grados,
        velocidad=config.GARRA_DELANTERA_VELOCIDAD,
        esperar=True,
        modo_final=Stop.HOLD
    ):
        self.motor_garra_delantera.run_angle(
            velocidad,
            grados,
            then=modo_final,
            wait=esperar
        )