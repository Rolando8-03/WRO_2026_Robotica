"""Funciones de los mecanismos y actuadores del robot.

Este archivo controla el motor de torque, la garra principal y la garra
delantera. No contiene movimientos de las ruedas ni lectura de sensores.
"""

from pybricks.parameters import Stop
from pybricks.tools import wait, StopWatch


# -----------------------------------------------------------------------------
# mover_torque
# Mueve el mecanismo de torque una cantidad determinada de grados.
# Puede ejecutarse de forma bloqueante o al mismo tiempo que otra acción.
# -----------------------------------------------------------------------------
def mover_torque(
    self,
    grados_torque,
    velocidad_torque=180,
    esperar=True,
    modo_final=Stop.HOLD,
    retraso_inicial_ms=0
):
    if retraso_inicial_ms > 0:
        wait(retraso_inicial_ms)

    if grados_torque == 0:
        return

    self.motor_torque.run_angle(
        velocidad_torque,
        grados_torque,
        then=modo_final,
        wait=esperar
    )


# -----------------------------------------------------------------------------
# mover_garra_delantera
# Mueve la garra delantera una cantidad determinada de grados y mantiene
# su posición al terminar.
# -----------------------------------------------------------------------------
def mover_garra_delantera(
    self,
    velocidad,
    grados,
    esperar=True,
    modo_final=Stop.HOLD
):
    if grados == 0:
        return

    self.motor_garra_delantera.run_angle(
        velocidad,
        grados,
        then=modo_final,
        wait=esperar
    )


# -----------------------------------------------------------------------------
# mover_garra_principal
# Abre o cierra la garra principal. Cuando cierra, puede mantener una presión
# constante para sujetar el objeto después de completar el movimiento.
#
# Convención conservada del código original:
# - grados positivos: mueve la garra en dirección de apertura.
# - grados negativos: mueve la garra en dirección de cierre.
# -----------------------------------------------------------------------------
def mover_garra_principal(
    self,
    velocidad,
    grados,
    esperar=True,
    potencia_apriete=60,
    tiempo_apriete_ms=120,
    apretar=True
):
    if grados == 0:
        return

    self.motor_garra.stop()

    # Abrir la garra.
    if grados > 0:
        wait(40)

        self.motor_garra.run_angle(
            velocidad,
            -abs(grados),
            then=Stop.BRAKE,
            wait=esperar
        )

    # Cerrar la garra.
    else:
        wait(20)

        # La presión posterior depende de que primero se complete el cierre.
        # Por eso esta parte conserva wait=True.
        self.motor_garra.run_angle(
            velocidad,
            abs(grados),
            then=Stop.BRAKE,
            wait=True
        )

        if apretar:
            self.motor_garra.dc(potencia_apriete)
            wait(tiempo_apriete_ms)

            # Mantiene la presión después de terminar la función.
            self.motor_garra.dc(potencia_apriete)


# -----------------------------------------------------------------------------
# soltar_garra_principal
# Detiene la presión continua de la garra principal.
# Debe usarse antes de abrirla o cuando ya no sea necesario sujetar el objeto.
# -----------------------------------------------------------------------------
def soltar_garra_principal(self, modo="brake"):
    if modo == "hold":
        self.motor_garra.hold()

    elif modo == "stop":
        self.motor_garra.stop()

    else:
        self.motor_garra.brake()


# -----------------------------------------------------------------------------
# mover_torque_seguro
# Mueve el motor de torque hasta encontrar resistencia física.
# Esta función es útil para buscar un tope mecánico y evitar forzar el motor.
#
# IMPORTANTE:
# run_until_stalled() no se detiene al alcanzar grados_torque; se detiene
# únicamente cuando detecta que el motor se ha atascado. El argumento
# grados_torque se usa aquí para elegir la dirección y comparar el recorrido.
# -----------------------------------------------------------------------------
def mover_torque_seguro(
    self,
    grados_torque,
    velocidad_torque=180,
    esperar=True,
    modo_final=Stop.HOLD,
    retraso_inicial_ms=0,
    duty_limit=50,
    detener_en_tope=True
):
    if retraso_inicial_ms > 0:
        wait(retraso_inicial_ms)

    if grados_torque == 0:
        return False

    self.motor_torque.stop()
    wait(10)
    self.motor_torque.reset_angle(0)

    velocidad_real = (
        abs(velocidad_torque)
        if grados_torque > 0
        else -abs(velocidad_torque)
    )

    modo_tope = (
        Stop.HOLD
        if detener_en_tope
        else Stop.COAST
    )

    angulo_final = self.motor_torque.run_until_stalled(
        speed=velocidad_real,
        then=modo_tope,
        duty_limit=duty_limit
    )

    angulo_real = abs(angulo_final)
    angulo_objetivo = abs(grados_torque)

    # Si se detuvo antes del ángulo de referencia, probablemente encontró
    # resistencia antes de completar el recorrido esperado.
    tope_detectado = angulo_real < angulo_objetivo

    if not detener_en_tope:
        if modo_final == Stop.HOLD:
            self.motor_torque.hold()

        elif modo_final == Stop.BRAKE:
            self.motor_torque.brake()

        else:
            self.motor_torque.stop()

    if esperar:
        wait(20)

    return tope_detectado

# -----------------------------------------------------------------------------
# mover_garra_delantera
# Mueve la garra delantera una cantidad determinada de grados.
# Al terminar mantiene la posición usando Stop.HOLD.
# -----------------------------------------------------------------------------
def mover_garra_delantera(
    self,
    velocidad,
    grados,
    esperar=True,
    modo_final=Stop.HOLD
):
    if grados == 0:
        return

    self.motor_garra_delantera.run_angle(
        velocidad,
        grados,
        then=modo_final,
        wait=esperar
    )

# -----------------------------------------------------------------------------
# mover_garra_principal
# Abre o cierra la garra principal.
#
# Convención:
# - grados positivos: abrir.
# - grados negativos: cerrar.
#
# Cuando cierra, puede mantener una potencia constante para seguir sujetando
# el objeto mientras el robot ejecuta otras acciones.
# -----------------------------------------------------------------------------
def mover_garra_principal(
    self,
    velocidad,
    grados,
    esperar=True,
    potencia_apriete=60,
    tiempo_apriete_ms=120,
    apretar=True
):
    if grados == 0:
        return

    # Evita enviar valores fuera del rango permitido por dc().
    potencia_apriete = self.limitar(
        potencia_apriete,
        -100,
        100
    )

    self.motor_garra.stop()

    # ABRIR
    if grados > 0:
        wait(40)

        self.motor_garra.run_angle(
            velocidad,
            -abs(grados),
            then=Stop.BRAKE,
            wait=esperar
        )

    # CERRAR
    else:
        wait(20)

        # Para aplicar presión después del cierre, primero debe completar
        # físicamente el movimiento.
        self.motor_garra.run_angle(
            velocidad,
            abs(grados),
            then=Stop.BRAKE,
            wait=True
        )

        if apretar:
            self.motor_garra.dc(
                potencia_apriete
            )

            wait(
                tiempo_apriete_ms
            )

            # El motor continúa aplicando presión mientras se ejecutan
            # las siguientes acciones.
            self.motor_garra.dc(
                potencia_apriete
            )

# -----------------------------------------------------------------------------
# mover_garra_rapida
# Abre la garra usando potencia directa y el encoder del motor.
# También permite cerrar usando run_angle y mantener presión.
#
# El tiempo máximo evita que el programa quede atrapado si la garra se atasca.
# -----------------------------------------------------------------------------
def mover_garra_rapida(
    self,
    potencia=100,
    grados=90,
    abrir=True,
    velocidad=200,
    potencia_apriete=40,
    tiempo_apriete_ms=300,
    tiempo_max_ms=1500
):
    if grados == 0:
        return

    potencia = self.limitar(
        potencia,
        0,
        100
    )

    potencia_apriete = self.limitar(
        potencia_apriete,
        -100,
        100
    )

    self.motor_garra.reset_angle(0)

    # ABRIR RÁPIDAMENTE
    if abrir:
        cronometro = StopWatch()
        cronometro.reset()

        self.motor_garra.dc(
            -abs(potencia)
        )

        while (
            abs(self.motor_garra.angle()) < abs(grados)
            and cronometro.time() < tiempo_max_ms
        ):
            wait(1)

        self.motor_garra.brake()

    # CERRAR
    else:
        self.motor_garra.stop()
        wait(20)

        self.motor_garra.run_angle(
            abs(velocidad),
            abs(grados),
            then=Stop.BRAKE,
            wait=True
        )

        self.motor_garra.dc(
            potencia_apriete
        )

        wait(
            tiempo_apriete_ms
        )

        # Mantiene presión para sujetar el objeto.
        self.motor_garra.dc(
            potencia_apriete
        )

def soltar_garra_principal(
    self,
    modo="brake"
):
    if modo == "hold":
        self.motor_garra.hold()

    elif modo == "stop":
        self.motor_garra.stop()

    else:
        self.motor_garra.brake()