from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

# =========================
# HUB
# =========================

hub = PrimeHub()
pi = 3.1416

# =========================
# MOTORES
# =========================

motor_izquierdo = Motor(
    Port.E,
    Direction.COUNTERCLOCKWISE
)

motor_derecho = Motor(
    Port.A,
    Direction.CLOCKWISE
)


# =========================
# CONFIGURACIÓN ROBOT
# =========================

diametro_rueda = 56

circunferencia = (
    diametro_rueda * pi
)

grados_por_mm = (
    360 / circunferencia
)


# =========================
# FUNCIONES AUXILIARES
# =========================

def reset_motores():

    motor_izquierdo.reset_angle(0)

    motor_derecho.reset_angle(0)


def distancia_promedio_grados():

    return (
        abs(motor_izquierdo.angle()) +
        abs(motor_derecho.angle())
    ) / 2


def frenar():

    motor_izquierdo.brake()

    motor_derecho.brake()

    wait(30)


# =========================
# GIRO EN ARCO CON DC
# =========================

def giro_arco_dc(
    radio_cm,
    angulo_deg,
    potencia=80,
    lado="derecha"
):

    if angulo_deg == 0:
        return

    # =========================
    # DISTANCIA ENTRE RUEDAS
    # =========================

    distancia_ruedas_cm = 12

    # =========================
    # RADIOS
    # =========================

    radio_interno = (
        radio_cm -
        (distancia_ruedas_cm / 2)
    )

    radio_externo = (
        radio_cm +
        (distancia_ruedas_cm / 2)
    )

    # =========================
    # DISTANCIAS DEL ARCO
    # =========================

    distancia_interna = (
        2 * pi *
        radio_interno *
        (angulo_deg / 360)
    )

    distancia_externa = (
        2 * pi *
        radio_externo *
        (angulo_deg / 360)
    )

    # =========================
    # RELACIÓN ENTRE RUEDAS
    # =========================

    relacion = (
        distancia_interna /
        distancia_externa
    )

    potencia_externa = potencia

    potencia_interna = (
        potencia * relacion
    )

    # =========================
    # LIMITAR POTENCIAS
    # =========================

    potencia_externa = max(
        -100,
        min(100, potencia_externa)
    )

    potencia_interna = max(
        -100,
        min(100, potencia_interna)
    )

    # =========================
    # RESET
    # =========================

    reset_motores()

    # =========================
    # OBJETIVO
    # =========================

    grados_objetivo = (
        distancia_externa * 10 *
        grados_por_mm
    )

    # =========================
    # DEFINIR SENTIDO
    # =========================

    if lado == "derecha":

        pot_izq = potencia_externa
        pot_der = potencia_interna

    else:

        pot_izq = potencia_interna
        pot_der = potencia_externa

    # =========================
    # EJECUCIÓN
    # =========================

    while (
        distancia_promedio_grados()
        < grados_objetivo
    ):

        motor_izquierdo.dc(
            pot_izq
        )

        motor_derecho.dc(
            pot_der
        )

        wait(5)

    frenar()


# =========================
# EJEMPLOS
# =========================

# Arco derecha rápido
giro_arco_dc(
    radio_cm=15,
    angulo_deg=90,
    potencia=120,
    lado="derecha"
)
'''
wait(1000)

# Arco izquierda rápido
giro_arco_dc(
    radio_cm=20,
    angulo_deg=90,
    potencia=85,
    lado="izquierda"
)
'''
