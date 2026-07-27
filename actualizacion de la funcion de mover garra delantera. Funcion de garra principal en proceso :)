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


#Funcion en desarollo JAJSHAJASHJH
def mover_garra_principal(
    self,
    velocidad,
    grados=0,
    esperar=True,
    potencia_apriete=60,
    tiempo_apriete_ms=120,
    apretar=True,
    modo_soltar=None
):
    # 1. FUNCIÓN "SOLTAR" FUSIONADA
    # Si envías un modo_soltar, ignora los grados y ejecuta la acción directa.
    if modo_soltar == "hold":
        self.motor_garra.hold()
        return
    elif modo_soltar == "stop":
        self.motor_garra.stop()
        return
    elif modo_soltar == "brake":
        self.motor_garra.brake()
        return

    if grados == 0:
        return

    # 2. TOPE DE SEGURIDAD (Protección directa)
    # Si le pides más de 170 grados, lo recorta a 170 automáticamente.
    if abs(grados) > 170:
        grados = 170 if grados > 0 else -170

    self.motor_garra.stop()

    # 3. ABRIR (grados positivos -> movimiento negativo)
    if grados > 0:
        wait(40)
        self.motor_garra.run_angle(
            abs(velocidad),
            -abs(grados),
            then=Stop.HOLD,  # ¡Esto ancla la garra rígidamente!
            wait=esperar
        )

    # 4. CERRAR (grados negativos -> movimiento positivo)
    else:
        wait(20)
        self.motor_garra.run_angle(
            abs(velocidad),
            abs(grados),
            then=Stop.HOLD,  # ¡Esto ancla la garra rígidamente!
            wait=True
        )

        if apretar:
            # Asegura que el valor esté en un rango seguro
            if hasattr(self, 'limitar'):
                potencia_apriete = self.limitar(potencia_apriete, -100, 100)
                
            self.motor_garra.dc(potencia_apriete)
            wait(tiempo_apriete_ms)
            # En lugar de dejar un voltaje continuo que resbala, forzamos HOLD
            self.motor_garra.hold()

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
#FUNCION ACTUALIZADA DE MOVER GARRA DELANTERA
def mover_garra_delantera(
    self,
    posicion,
    velocidad=500,
    simultaneo=False,
    modo_final=Stop.HOLD,
    limite_maximo=320
):

    # Impide posiciones menores que el tope superior.
    if posicion < 0:
        posicion = 0

    # Impide sobrepasar el límite inferior.
    if posicion > limite_maximo:
        posicion = limite_maximo

    self.motor_garra_delantera.run_target(
        speed=abs(velocidad),
        target_angle=posicion,
        then=modo_final,
        wait=not simultaneo
    )

    return posicion
