from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait, StopWatch


class Base:

    def __init__(self):
        # =========================
        # CONFIGURACIÓN DEL ROBOT
        # =========================
        self.Hub = PrimeHub()

        self.motor_derecho = Motor(Port.A, Direction.CLOCKWISE)
        self.motor_izquierdo = Motor(Port.E, Direction.COUNTERCLOCKWISE)

        self.motor_torque = Motor(Port.D)
        self.motor_garra = Motor(Port.F)
        self.motor_garra_delantera = Motor(Port.B)

        self.seguidor = ColorSensor(Port.C)

        self.lista_colores = []

        self.diametro_rueda = 56
        self.circunferencia = self.diametro_rueda * 3.14159
        self.grados_por_mm = 360 / self.circunferencia

        # Compensación mecánica base
        self.bias_izq = 1.00
        self.bias_der = 1.00

        self._last_derivative = 0

    # =========================
    # FUNCIONES BÁSICAS
    # =========================

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

    # =========================
    # INICIO Y SALIDA DE MOVIMIENTOS
    # =========================

    def preparar_movimiento(
        self,
        reset_motores=True,
        reset_gyro=True,
        perfil="seguro",
        pausa=None
    ):
        """
        perfil="seguro":
            Más estable. Úsalo al inicio o después de movimientos bruscos.

        perfil="encadenado":
            Más fluido. Úsalo cuando quieres pasar rápido de una función a otra.
        """

        if perfil == "seguro":
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(8)

            self.motor_izquierdo.stop()
            self.motor_derecho.stop()
            wait(4)

            pausa_gyro = 18

        elif perfil == "encadenado":
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
        perfil="seguro",
        modo="brake",
        pausa=None,
        soltar=True
    ):
        """
        modo="brake":
            Frena con control.

        modo="stop":
            Suelta los motores.

        modo="hold":
            Mantiene la posición con fuerza.

        soltar=True:
            Después de frenar, libera un poco los motores con stop().
            Esto ayuda a que el siguiente movimiento no salga amarrado.
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

    # =========================
    # MOVIMIENTO RECTO HACIA ADELANTE
    # =========================

    def mover_recto(
        self,
        distancia_cm,
        velocidad=950,
        kp=2.1,
        kd=2.9,
        correccion_max=130,
        velocidad_min=380,
        perfil="seguro"
    ):
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

            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

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

    # =========================
    # RETROCESO ESTABLE
    # =========================
    def retroceder(
        self,
        distancia_cm,
        velocidad=950,
        kp=2.1,
        kd=2.9,
        correccion_max=130,
        velocidad_min=380,
        perfil="seguro",
        invertir_correccion=False,
        pausa_gyro=None
    ):
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

            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

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

            # MODO 1: corrección normal para retroceso.
            if not invertir_correccion:
                pot_izq = int(base - correccion)
                pot_der = int(base + correccion)

            # MODO 2: corrección invertida.
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

    # =========================
    # GIRO RÁPIDO CON DOS MOTORES
    # =========================

    def girar(
        self,
        angulo_deg,
        velocidad=950,
        velocidad_min=220,
        anticipacion=9,
        zona_freno=22,
        perfil="seguro"
    ):
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

    # =========================
    # GIRO RÁPIDO CON UN SOLO MOTOR
    # =========================

    def _giro_un_motor(
        self,
        motor_activo,
        motor_fijo,
        angulo_deg,
        sentido_motor,
        velocidad=1000,
        velocidad_min=260,
        anticipacion=12,
        zona_freno=28,
        perfil="seguro"
    ):
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

        if perfil == "encadenado":
            wait(8)
        else:
            wait(22)

        motor_activo.stop()
        motor_fijo.stop()
        wait(2)

    def giro_izquierda(
        self,
        angulo_deg,
        velocidad=1000,
        velocidad_min=260,
        anticipacion=12,
        zona_freno=28,
        perfil="seguro"
    ):
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
        velocidad=1000,
        velocidad_min=260,
        anticipacion=12,
        zona_freno=28,
        perfil="seguro"
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

    # NOTA:
    # Si el giro se pasa del ángulo, aumenta la anticipación.
    # Si el giro queda corto, baja la anticipación.

    # =========================
    # MOTOR DE TORQUE
    # =========================

    def mover_torque(
        self,
        grados_torque,
        velocidad_torque=180,
        esperar=True,
        modo_final=Stop.HOLD
    ):
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
        Espera solo hasta que el motor de torque haya recorrido cierta cantidad.
        Sirve para no esperar toda la bajada de la celda.
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

    # =========================
    # AVANZAR / RETROCEDER CON TORQUE
    # =========================

    def avanzar_con_torque(
        self,
        distancia_cm,
        grados_torque,
        velocidad_robot=950,
        velocidad_torque=180,
        torque_despues_cm=3,
        kp=2.1,
        kd=2.9,
        correccion_max=130,
        velocidad_min=380,
        esperar_torque=False,
        levantar_final_grados=0,
        perfil_entrada="seguro",
        perfil_salida="encadenado"
    ):
        """
        Mueve el robot mientras activa el motor de torque después de cierta distancia.

        distancia_cm:
            Positivo = avanza.
            Negativo = retrocede.

        grados_torque:
            Positivo o negativo según quieras subir o bajar la celda.

        torque_despues_cm:
            Distancia recorrida antes de activar el torque.

        esperar_torque:
            False = más fluido.
            True = más seguro, pero puede perder tiempo.

        levantar_final_grados:
            Si la celda roza el suelo, puedes levantarla un poquito al final.
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

            # Activa el torque después de cierta distancia.
            if not torque_activado and recorrido >= grados_inicio_torque:
                self.motor_torque.run_angle(
                    velocidad_torque,
                    grados_torque,
                    then=Stop.HOLD,
                    wait=False
                )
                torque_activado = True

            # Aceleración progresiva.
            if velocidad_actual < velocidad_robot:
                velocidad_actual += rampa

                if velocidad_actual > velocidad_robot:
                    velocidad_actual = velocidad_robot

            # Frenado suave al final.
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

            # Corrección diferente para avance y retroceso.
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

        # Si el recorrido fue muy corto y nunca activó el torque, lo activa al final.
        if not torque_activado and grados_torque != 0:
            self.motor_torque.run_angle(
                velocidad_torque,
                grados_torque,
                then=Stop.HOLD,
                wait=False
            )
            torque_activado = True

        # Espera opcional a que el torque termine.
        if esperar_torque and torque_activado:
            while self.motor_torque.control.done() == False:
                wait(5)

        # Si quieres levantar al final, primero debe terminar el torque principal.
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

    # =========================
    # GARRAS
    # =========================

    def mover_garra(
        self,
        velocidad,
        grados
    ):
        self.motor_garra.run_angle(
            velocidad,
            grados,
            then=Stop.HOLD,
            wait=True
        )

    def mover_garra_delantera(
        self,
        velocidad,
        grados
    ):
        self.motor_garra_delantera.run_angle(
            velocidad,
            grados,
            then=Stop.HOLD,
            wait=True
        )

    # =========================
    # DETECTOR DE LÍNEA NEGRA
    # =========================

    def avanzar_hasta_n_lineas_negras(
    self,
    cantidad_lineas,
    velocidad=500,
    umbral_negro=20,
    umbral_salida=28,
    perfil="seguro"
    ):
 
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

            # Detecta entrada a una línea negra
            if lectura <= umbral_negro and not en_negro:
                contador_lineas += 1
                en_negro = True

                print("Línea negra detectada:", contador_lineas)

            # Detecta que ya salió de la línea negra
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
        umbral_negro=20,
        umbral_salida=28,
        distancia_minima_cm=0,
        lineas_a_ignorar=0,
        kp=2.0,
        kd=2.8,
        correccion_max=120,
        perfil="seguro",
        lecturas_negras_necesarias=2,
        lecturas_claras_necesarias=3
    ):
        """
        Mueve el robot hasta detectar una línea negra válida.

        distancia_cm_max:
            Positivo = avanza.
            Negativo = retrocede.

        distancia_minima_cm:
            Antes de esta distancia, ignora cualquier línea negra.

        lineas_a_ignorar:
            Cantidad de líneas negras válidas que debe ignorar antes de detenerse.

        umbral_negro:
            Valor de reflexión para considerar que está sobre negro.

        umbral_salida:
            Valor de reflexión para considerar que ya salió del negro.
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

            # =========================
            # DETECCIÓN DE LÍNEA
            # =========================

            if recorrido >= grados_minimos:

                if lectura <= umbral_negro:
                    conteo_negro += 1
                    conteo_claro = 0

                    if conteo_negro >= lecturas_negras_necesarias and not en_negro:
                        en_negro = True
                        contador_lineas += 1

                        print("Linea detectada:", contador_lineas)

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

            # =========================
            # CONTROL GIROSCÓPICO
            # =========================

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

        # Si llegó aquí, no encontró la línea.
        self.terminar_movimiento(
            perfil=perfil,
            modo="brake"
        )

        print("No se encontró la línea dentro de la distancia máxima.")
        return False

    # =========================
    # VALIDACIONES DE SENSOR
    # =========================

    def leer_reflexion_promedio(
        self,
        sensor=None,
        muestras=5,
        pausa_ms=3
    ):
        """
        Devuelve un promedio de reflexión para reducir lecturas falsas.
        Útil antes de tomar decisiones importantes con líneas negras.
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
        umbral_negro=20,
        muestras=3,
        pausa_ms=3
    ):
        """
        Confirma si el sensor está sobre negro usando varias lecturas.
        Evita que una sola lectura falsa active una función.
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
        umbral_salida=28,
        timeout_ms=600
    ):
        """
        Espera hasta que el robot salga de una línea negra.
        Sirve para no contar dos veces la misma línea.
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


    # =========================
    # ACOMODO SOBRE BORDE DE LÍNEA
    # =========================

    def acomodar_borde_linea(
        self,
        direccion=1,
        velocidad=180,
        objetivo_reflexion=27,
        margen=3,
        timeout_ms=450,
        perfil_salida="encadenado"
    ):
        """
        Mueve el robot lentamente hasta quedar cerca del borde de la línea.

        direccion:
            1 = hacia adelante.
            -1 = hacia atrás.

        objetivo_reflexion:
            Valor aproximado del borde de línea.
            Si tu negro es 15 y blanco es 60, un borde puede andar entre 25 y 35.
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

    # =========================
    # SEGUIDOR DE LÍNEA POR BORDE
    # =========================

    def seguir_linea_extremo(
        self,
        sensor_color=None,
        velocidad_max=100,
        distancia_cm=70,
        lado="derecha",
        tiempo_acomodo_ms=180,
        tiempo_aceleracion_ms=70,
        kp=0.82,
        kd=1.85,
        k_freno=0.01,
        objetivo_reflexion=27,
        correccion_max=95,
        margen_cm=0,
        perfil_salida="encadenado"
    ):
        """
        Seguidor de línea usando dc().
        IMPORTANTE:
        velocidad_max aquí va de 0 a 100, no es igual a 950 de run().
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

        self.reset_motores()

        cronometro = StopWatch()
        cronometro.reset()

        velocidad_minima = 45

        last_error = 0
        last_derivative = 0

        if lado == "derecha":
            multiplicador_lado = 1
        else:
            multiplicador_lado = -1

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

    def giro_arco_dc(
        self,
        radio_cm,
        angulo_deg,
        potencia=80,
        lado="derecha",
        distancia_ruedas_cm=12
    ):
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
