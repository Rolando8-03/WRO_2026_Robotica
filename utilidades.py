"""Funciones auxiliares compartidas por todo el robot.

Este archivo contiene operaciones generales de reinicio, medición, límites y
finalización de movimientos. No controla recorridos completos ni mecanismos
específicos como la garra o el torque.
"""

from pybricks.tools import wait


# -----------------------------------------------------------------------------
# frenar
# Frena inmediatamente los dos motores de tracción.
# -----------------------------------------------------------------------------
def frenar(self):
    self.motor_izquierdo.brake()
    self.motor_derecho.brake()
    wait(3)


# -----------------------------------------------------------------------------
# limitar
# Mantiene un valor dentro de los límites mínimo y máximo indicados.
# Se usa principalmente para evitar potencias o correcciones excesivas.
# -----------------------------------------------------------------------------
def limitar(self, valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


# -----------------------------------------------------------------------------
# reset_imu
# Reinicia el rumbo medido por el giroscopio y lo establece en cero grados.
# -----------------------------------------------------------------------------
def reset_imu(self):
    self.Hub.imu.reset_heading(0)
    wait(20)


# -----------------------------------------------------------------------------
# reset_motores
# Reinicia a cero los encoders de los dos motores de tracción.
# -----------------------------------------------------------------------------
def reset_motores(self):
    self.motor_izquierdo.reset_angle(0)
    self.motor_derecho.reset_angle(0)


# -----------------------------------------------------------------------------
# distancia_promedio_grados
# Devuelve el promedio absoluto de los grados recorridos por ambas ruedas.
# Se utiliza para estimar la distancia recorrida por el robot.
# -----------------------------------------------------------------------------
def distancia_promedio_grados(self):
    return (
        abs(self.motor_izquierdo.angle())
        + abs(self.motor_derecho.angle())
    ) / 2


# -----------------------------------------------------------------------------
# _error_angular
# Calcula la diferencia más corta entre el rumbo objetivo y el rumbo actual.
# El resultado siempre permanece entre -180 y 180 grados.
# -----------------------------------------------------------------------------
def _error_angular(self, objetivo, actual):
    error = objetivo - actual

    while error > 180:
        error -= 360

    while error < -180:
        error += 360

    return error


# -----------------------------------------------------------------------------
# preparar_movimiento
# Reinicia, cuando se solicita, los encoders, DriveBase y giroscopio antes de
# comenzar un movimiento.
# -----------------------------------------------------------------------------
def preparar_movimiento(
    self,
    reset_motores=True,
    reset_gyro=True,
    perfil="seguro",
    pausa=None
):
    if reset_motores:
        self.reset_motores()
        self.drive_base.reset()

    if reset_gyro:
        self.Hub.imu.reset_heading(0)
        wait(15)

    if pausa is not None:
        wait(pausa)


# -----------------------------------------------------------------------------
# terminar_movimiento
# Aplica el tipo de detención solicitado y una pausa distinta según el perfil.
# Puede liberar los motores después de frenar para evitar mantenerlos forzados.
# -----------------------------------------------------------------------------
def terminar_movimiento(
    self,
    perfil="seguro",
    modo="brake",
    pausa=None,
    soltar=True
):
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

    elif perfil == "seguro":
        wait(18)

    elif perfil == "encadenado":
        wait(6)

    else:
        wait(15)

    if soltar and modo == "brake":
        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(2)