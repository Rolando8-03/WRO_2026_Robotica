from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait, StopWatch


class Base:
    def __init__(self):
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

    # =========================================================
    # UTILIDADES BÁSICAS
    # =========================================================

    def calibrar_giroscopio(self):
        print("Calibrando giroscopio... NO MOVER")
        self.Hub.light.on(Color.RED)
        self.Hub.imu.reset_heading(0)
        wait(500)

        for _ in range(10):
            _ = self.Hub.imu.heading()
            wait(100)

        self.Hub.imu.reset_heading(0)
        self.Hub.light.on(Color.GREEN)
        wait(300)

    def reset_imu(self):
        self.Hub.imu.reset_heading(0)
        wait(20)

    def esperar(self, ms):
        wait(ms)

    def frenar(self):
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(30)

    def distancia_promedio_grados(self):
        return (
            abs(self.motor_izquierdo.angle()) +
            abs(self.motor_derecho.angle())
        ) / 2

    def reset_motores(self):
        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

    # =========================================================
    # MATRIZ
    # =========================================================

    def matriz(self):
        # Dejé tu lógica, pero corregí el sensor.
        # Antes decía self.sensor_matriz, pero ese atributo no existe.
        color = self.seguidor.color()
        self.lista_colores.append(color)

    def escanear_matriz(self):
        colores_detectados = []

        # Asegura que el robot esté quieto antes de leer
        self.frenar()
        wait(250)

        # Toma más lecturas para evitar fallos por una lectura falsa
        for i in range(25):
            color = self.seguidor.color()

            # Ignora lecturas vacías
            if color is not None:
                colores_detectados.append(color)

            wait(40)

            print("Colores detectados en matriz:", colores_detectados)

            verdes = colores_detectados.count(Color.GREEN)
            amarillos = colores_detectados.count(Color.YELLOW)
            azules = colores_detectados.count(Color.BLUE)
            rojos = colores_detectados.count(Color.RED)
            blancos = colores_detectados.count(Color.WHITE)

            print("Verdes:", verdes)
            print("Amarillos:", amarillos)
            print("Azules:", azules)
            print("Rojos:", rojos)
            print("Blancos:", blancos)

            mayor = max(verdes, amarillos, azules, rojos, blancos)

            # Si ninguna lectura aparece varias veces, la detección no es confiable
            if mayor < 3:
                print("Detección débil. No se detectó matriz válida.")
                return None

            if mayor == verdes:
                print("Matriz detectada: 1")
                return 1

            elif mayor == amarillos:
                print("Matriz detectada: 2")
                return 2

            elif mayor == azules:
                print("Matriz detectada: 3")
                return 3

            elif mayor == rojos:
                print("Matriz detectada: 4")
                return 4

            elif mayor == blancos:
                print("Matriz detectada: 5")
                return 5

    # =========================================================
    # MOVIMIENTOS RÁPIDOS
    # =========================================================

    def mover_recto_rapido(
        self,
        distancia_cm,
        velocidad=1200,
        kp=2.2,
        kd=3.5,
        velocidad_min=350,
        torque_grados=None,
        torque_velocidad=150,
        torque_despues_cm=0
    ):
        if distancia_cm == 0:
            return

        self.reset_motores()
        self.reset_imu()

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm
        signo = 1 if distancia_cm > 0 else -1

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        velocidad_actual = velocidad_min
        rampa = 45

        # NUEVO:
        # Permite lanzar el torque después de cierta distancia
        # sin perder la velocidad rápida original.
        torque_lanzado = False
        grados_para_torque = abs(torque_despues_cm) * 10 * self.grados_por_mm

        while self.distancia_promedio_grados() < grados_objetivo:

            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            # =========================
            # TORQUE RETRASADO
            # =========================
            if torque_grados is not None and not torque_lanzado:
                if recorrido >= grados_para_torque:
                    self.motor_torque.run_angle(
                        torque_velocidad,
                        torque_grados,
                        then=Stop.HOLD,
                        wait=False
                    )
                    torque_lanzado = True

            # =========================
            # ACELERACIÓN RÁPIDA ORIGINAL
            # =========================
            if velocidad_actual < velocidad:
                velocidad_actual += rampa

                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            # Frenado más tardío original
            if restante < 140:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad * restante / 140)
                )

            dt = reloj.time() / 1000

            if dt <= 0:
                dt = 0.001

            error = self.Hub.imu.heading()
            derivada = (error - error_anterior) / dt

            correccion = error * kp + derivada * kd
            correccion = max(-260, min(260, correccion))

            base = velocidad_actual * signo

            pot_izq = int((base - correccion) * self.bias_izq)
            pot_der = int((base + correccion) * self.bias_der)

            pot_izq = max(-1200, min(1200, pot_izq))
            pot_der = max(-1200, min(1200, pot_der))

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            error_anterior = error
            reloj.reset()

            wait(3)

        self.frenar()

    def retroceder_recto_rapido(
        self,
        distancia_cm,
        velocidad=750,
        torque_grados=None,
        torque_velocidad=150,
        torque_despues_cm=0
    ):
        if distancia_cm == 0:
            return

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(80)

        self.reset_motores()
        self.reset_imu()
        wait(60)

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm

        kp_gyro = 2.4
        kd_gyro = 3.0

        kp_encoder = 0.42

        umbral_roce = 38
        refuerzo_roce = 1.35

        correccion_max_normal = 125
        correccion_max_roce = 170

        velocidad_min = 240
        velocidad_actual = velocidad_min
        rampa = 18

        error_anterior = 0
        derivada_filtrada = 0

        recorrido_anterior = 0
        ciclos_roce = 0

        # NUEVO:
        # Control para lanzar el torque durante el retroceso,
        # sin iniciar el torque al mismo tiempo que el movimiento.
        torque_lanzado = False
        grados_para_torque = abs(torque_despues_cm) * 10 * self.grados_por_mm

        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            # =========================
            # TORQUE RETRASADO
            # =========================
            if torque_grados is not None and not torque_lanzado:
                if recorrido >= grados_para_torque:
                    self.motor_torque.run_angle(
                        torque_velocidad,
                        torque_grados,
                        then=Stop.HOLD,
                        wait=False
                    )
                    torque_lanzado = True

            # =========================
            # RAMPA RÁPIDA ORIGINAL
            # =========================
            if velocidad_actual < velocidad:
                velocidad_actual += rampa

                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            # Frenado más tardío original
            if restante < 170:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad * restante / 170)
                )

            # =========================
            # CORRECCIÓN POR GIROSCOPIO
            # =========================
            error_gyro = self.Hub.imu.heading()

            if abs(error_gyro) < 0.6:
                error_gyro = 0

            derivada_cruda = error_gyro - error_anterior
            derivada_filtrada = (
                0.35 * derivada_cruda
            ) + (
                0.65 * derivada_filtrada
            )

            correccion_gyro = (
                error_gyro * kp_gyro
            ) + (
                derivada_filtrada * kd_gyro
            )

            # =========================
            # CORRECCIÓN POR ENCODERS
            # =========================
            ang_izq = abs(self.motor_izquierdo.angle())
            ang_der = abs(self.motor_derecho.angle())

            error_encoder = ang_izq - ang_der
            correccion_encoder = error_encoder * kp_encoder

            # =========================
            # DETECCIÓN DE ROCE / DESBALANCE
            # =========================
            avance_ciclo = recorrido - recorrido_anterior

            hay_desbalance = abs(error_encoder) > umbral_roce
            hay_poco_avance = avance_ciclo < 1.2 and velocidad_actual > 300

            if hay_desbalance or hay_poco_avance:
                ciclos_roce += 1
            else:
                ciclos_roce = 0

            if ciclos_roce >= 3:
                velocidad_actual = max(
                    velocidad_min,
                    int(velocidad_actual * 0.92)
                )

                correccion_encoder = correccion_encoder * refuerzo_roce
                correccion_max = correccion_max_roce
            else:
                correccion_max = correccion_max_normal

            # =========================
            # CORRECCIÓN TOTAL
            # =========================
            correccion = correccion_gyro + correccion_encoder
            correccion = max(-correccion_max, min(correccion_max, correccion))

            base = -velocidad_actual

            pot_izq = int(base - correccion)
            pot_der = int(base + correccion)

            pot_izq = max(-1000, min(1000, pot_izq))
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            error_anterior = error_gyro
            recorrido_anterior = recorrido

            wait(3)

        self.frenar()

    # =========================================================
    # GARRAS Y TORQUE
    # =========================================================

    def mover_garra_delantera(self, velocidad, grados):
        self.motor_garra_delantera.run_angle(
            velocidad,
            grados,
            then=Stop.HOLD,
            wait=True
        )

    def mover_torque(self, grados_torque, velocidad_torque=150):
        KP = 1.2
        TOLERANCIA = 2

        pos_inicial = self.motor_torque.angle()
        pos_objetivo = pos_inicial + grados_torque

        cronometro = StopWatch()

        while True:
            error = pos_objetivo - self.motor_torque.angle()

            if abs(error) <= TOLERANCIA:
                self.motor_torque.stop()
                break

            potencia = KP * error
            potencia = max(-velocidad_torque, min(velocidad_torque, potencia))

            self.motor_torque.dc(potencia)

            if cronometro.time() > 1000:
                self.motor_torque.stop()
                print("Tiempo máximo excedido")
                break

            wait(10)

        self.motor_torque.hold()

    def avanzar_con_torque(
        self,
        distancia_cm,
        grados_torque,
        velocidad_robot=700,
        velocidad_torque=150,
        torque_despues_cm=3
    ):
        """
        Mueve rápido y activa el torque después de cierta distancia.

        distancia_cm:
            Negativo = retrocede.
            Positivo = avanza.

        grados_torque:
            Positivo o negativo según quieras subir o bajar.

        torque_despues_cm:
            Cuántos centímetros debe avanzar/retroceder antes de activar el torque.

        IMPORTANTE:
            Se conservan tus funciones rápidas:
            - retroceder_recto_rapido()
            - mover_recto_rapido()
        """

        if distancia_cm < 0:
            self.retroceder_recto_rapido(
                abs(distancia_cm),
                velocidad=velocidad_robot,
                torque_grados=grados_torque,
                torque_velocidad=velocidad_torque,
                torque_despues_cm=torque_despues_cm
            )

        elif distancia_cm > 0:
            self.mover_recto_rapido(
                distancia_cm,
                velocidad=velocidad_robot,
                torque_grados=grados_torque,
                torque_velocidad=velocidad_torque,
                torque_despues_cm=torque_despues_cm
            )

        # Mantiene tu lógica original:
        # si el torque no terminó al acabar el recorrido, espera.
        while self.motor_torque.control.done() == False:
            wait(5)

    def mover_garra(self, velocidad, grados):
        self.motor_garra.run_angle(
            velocidad,
            grados,
            then=Stop.HOLD,
            wait=True
        )

    # =========================================================
    # SEGUIDOR DE LÍNEA EXTREMO
    # =========================================================

    def seguir_linea_extremo(
        self,
        sensor_color,
        velocidad_max=100,
        distancia_cm=70,
        lado="derecha",
        tiempo_acomodo_ms=250,
        kp=0.82,
        kd=1.85,
        k_freno=0.01,
        margen_cm=0
    ):
        diametro_rueda = 5.6
        circunferencia = 3.1416 * diametro_rueda
        grados_objetivo = (distancia_cm / circunferencia) * 360
        grados_margen = (margen_cm / circunferencia) * 360 if margen_cm > 0 else 0
        grados_objetivo_real = max(0, grados_objetivo - grados_margen)

        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

        cronometro = StopWatch()

        velocidad_minima = 45
        tiempo_aceleracion_ms = 70

        last_error = 0
        last_derivative = 0

        objetivo_reflexion = 27

        if lado == "derecha":
            multiplicador_lado = 1
        else:
            multiplicador_lado = -1

        correccion_max = 95

        cronometro.reset()
        cronometro.resume()

        while True:
            grados_actuales = (
                abs(self.motor_izquierdo.angle()) +
                abs(self.motor_derecho.angle())
            ) / 2

            if grados_actuales >= grados_objetivo_real:
                break

            tiempo_actual = cronometro.time()

            if tiempo_actual < tiempo_acomodo_ms:
                velocidad_actual = velocidad_minima

            elif tiempo_actual < (tiempo_acomodo_ms + tiempo_aceleracion_ms):
                tiempo_en_rampa = tiempo_actual - tiempo_acomodo_ms
                progreso = tiempo_en_rampa / tiempo_aceleracion_ms

                velocidad_actual = velocidad_minima + (
                    (velocidad_max - velocidad_minima) * progreso
                )

            else:
                velocidad_actual = velocidad_max

            current_reflection = sensor_color.reflection()

            error = current_reflection - objetivo_reflexion

            derivative = (
                (error - last_error) * 0.82
            ) + (
                last_derivative * 0.18
            )

            correction = (
                (error * kp) +
                (derivative * kd)
            ) * multiplicador_lado

            correction = max(-correccion_max, min(correccion_max, correction))

            velocidad_base = velocidad_actual - (abs(error) * k_freno)

            potencia_izq = velocidad_base - correction
            potencia_der = velocidad_base + correction

            potencia_izq = max(-100, min(100, potencia_izq))
            potencia_der = max(-100, min(100, potencia_der))

            self.motor_izquierdo.dc(potencia_izq)
            self.motor_derecho.dc(potencia_der)

            last_error = error
            last_derivative = derivative

            wait(1)

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        cronometro.pause()

    # =========================================================
    # GIROS
    # =========================================================

    def salir_de_giro(self, pausa_brake=80, pausa_stop=40):
        # Frena ambos motores para cortar la inercia
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(pausa_brake)

        # Luego los libera para que no queden "amarrados"
        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(pausa_stop)

    def girar_rapido_preciso(
        self,
        angulo_deg,
        velocidad=700,
        velocidad_min=160,
        anticipacion=8
    ):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(3)

        objetivo = abs(angulo_deg)
        objetivo_corte = max(0, objetivo - anticipacion)

        signo = 1 if angulo_deg > 0 else -1

        while True:
            actual = abs(self.Hub.imu.heading())

            if actual >= objetivo_corte:
                break

            restante = objetivo_corte - actual

            if restante > 18:
                vel = velocidad
            else:
                vel = max(
                    velocidad_min,
                    int(velocidad * restante / 18)
                )

            self.motor_izquierdo.run(vel * signo)
            self.motor_derecho.run(-vel * signo)

            wait(1)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

        wait(70)

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()

        wait(5)

    def giro_izquierda(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(20)

        objetivo = abs(angulo_deg)
        signo = 1 if angulo_deg > 0 else -1

        self.motor_derecho.brake()
        wait(10)

        while True:
            actual = abs(self.Hub.imu.heading())

            if actual >= objetivo:
                break

            restante = objetivo - actual

            if restante > 20:
                vel = velocidad
            else:
                vel = max(
                    velocidad_min,
                    int(velocidad * restante / 20)
                )

            pot_izq = vel * signo
            pot_izq = max(-1000, min(1000, pot_izq))

            self.motor_izquierdo.run(pot_izq)
            wait(5)

        self.salir_de_giro()

    def giro_derecha(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(20)

        objetivo = abs(angulo_deg)
        signo = -1 if angulo_deg > 0 else 1

        self.motor_izquierdo.brake()
        wait(10)

        while True:
            actual = abs(self.Hub.imu.heading())

            if actual >= objetivo:
                break

            restante = objetivo - actual

            if restante > 20:
                vel = velocidad
            else:
                vel = max(
                    velocidad_min,
                    int(velocidad * restante / 20)
                )

            pot_der = vel * signo
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_derecho.run(pot_der)
            wait(5)

        self.salir_de_giro()

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
