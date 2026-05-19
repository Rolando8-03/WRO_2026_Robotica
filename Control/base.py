from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait

from Control import robot_config as config


class BaseRobot:

    def __init__(self):
        # =========================
        # HUB
        # =========================
        self.Hub = PrimeHub()

        # =========================
        # MOTORES PRINCIPALES
        # =========================
        self.motor_derecho = Motor(
            config.PORT_MOTOR_DERECHO,
            config.DIR_MOTOR_DERECHO
        )

        self.motor_izquierdo = Motor(
            config.PORT_MOTOR_IZQUIERDO,
            config.DIR_MOTOR_IZQUIERDO
        )

        # =========================
        # MOTORES DE MECANISMOS
        # =========================
        self.motor_torque = Motor(config.PORT_MOTOR_TORQUE)
        self.motor_garra = Motor(config.PORT_MOTOR_GARRA)
        self.motor_garra_delantera = Motor(config.PORT_MOTOR_GARRA_DELANTERA)

        # =========================
        # SENSOR
        # =========================
        self.seguidor = ColorSensor(config.PORT_SENSOR_SEGUIDOR)

        # =========================
        # MEDIDAS FÍSICAS
        # =========================
        self.diametro_rueda = config.DIAMETRO_RUEDA_MM
        self.circunferencia = self.diametro_rueda * config.PI
        self.grados_por_mm = 360 / self.circunferencia

        # =========================
        # VARIABLES AUXILIARES
        # =========================
        self.lista_colores = []
        self._last_derivative = 0

    # ============================================================
    # UTILIDADES BÁSICAS
    # ============================================================

    def limitar(self, valor, minimo, maximo):
        return max(minimo, min(maximo, valor))

    def reset_imu(self):
        self.Hub.imu.reset_heading(0)
        wait(20)

    def reset_motores(self):
        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

    def distancia_promedio_grados(self):
        return (
            abs(self.motor_izquierdo.angle()) +
            abs(self.motor_derecho.angle())
        ) / 2

    def esperar(self, ms):
        wait(ms)

    def frenar(self):
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(3)

    def detener(self):
        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(3)

    def bateria(self):
        return self.Hub.battery.voltage()

    def mostrar_bateria(self):
        print("Batería:", self.bateria(), "mV")

    def bateria_baja(self, minimo_mv=8000):
        return self.bateria() < minimo_mv