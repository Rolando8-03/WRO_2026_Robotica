from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait, StopWatch


class Base:
    def __init__(self):
        self.Hub = PrimeHub()

        self.calibrar_giroscopio()
        wait(1500)

        self.motor_derecho = Motor(Port.B, Direction.CLOCKWISE)
        self.motor_izquierdo = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.motor_torque = Motor(Port.E)
        self.motor_garra = Motor(Port.A)

        self.seguidor = ColorSensor(Port.C)
        self.sensor_matriz = ColorSensor(Port.D)

        self.lista_colores = []

        self.diametro_rueda = 56
        self.circunferencia = self.diametro_rueda * 3.14159
        self.grados_por_mm = 360 / self.circunferencia

        # Compensación mecánica base
        self.bias_izq = 1.00
        self.bias_der = 1.00

        self._last_derivative = 0

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
    
    
    def matriz(self):
        color = self.sensor_matriz.color()
        self.lista_colores.append(color)
    

    def distancia_promedio_grados(self):
        return (abs(self.motor_izquierdo.angle()) + abs(self.motor_derecho.angle())) / 2

    def reset_motores(self):
        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

    def mover_recto(self, distancia_cm, velocidad=900, kp=2.2, kd=3.5, velocidad_min=250):
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
        rampa = 25

        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados()
            restante = grados_objetivo - recorrido

            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            if restante < 220:
                velocidad_actual = max(velocidad_min, int(velocidad * restante / 220))

            dt = reloj.time() / 1000
            if dt <= 0:
                dt = 0.001

            error = self.Hub.imu.heading()
            derivada = (error - error_anterior) / dt
            correccion = error * kp + derivada * kd
            correccion = max(-180, min(180, correccion))

            base = velocidad_actual * signo

            pot_izq = int((base - correccion) * self.bias_izq)
            pot_der = int((base + correccion) * self.bias_der)

            pot_izq = max(-1000, min(1000, pot_izq))
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            error_anterior = error
            reloj.reset()
            wait(5)

        self.frenar()

    def retroceder_recto(self, distancia_cm, velocidad=700):
        if distancia_cm == 0:
            return

        self.reset_motores()
        self.reset_imu()

        distancia_mm = abs(distancia_cm) * 10
        grados_objetivo = distancia_mm * self.grados_por_mm

        error_anterior = 0
        reloj = StopWatch()
        reloj.reset()

        # Valores fijos que funcionan bien (puedes ajustarlos si quieres)
        kp = 2.5
        kd = 4.0
        velocidad_min = 220

        velocidad_actual = velocidad_min
        rampa = 25

        while abs(self.distancia_promedio_grados()) < grados_objetivo:
            recorrido_abs = abs(self.distancia_promedio_grados())
            restante = grados_objetivo - recorrido_abs

            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            if restante < 220:
                velocidad_actual = max(velocidad_min, int(velocidad * restante / 220))

            dt = reloj.time() / 1000
            if dt <= 0:
                dt = 0.001

            error = self.Hub.imu.heading()
            derivada = (error - error_anterior) / dt
            correccion = error * kp + derivada * kd
            correccion = max(-180, min(180, correccion))

            # Velocidad negativa para retroceder
            base = -velocidad_actual

            pot_izq = int((base - correccion) * self.bias_izq)
            pot_der = int((base + correccion) * self.bias_der)

            pot_izq = max(-1000, min(1000, pot_izq))
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            error_anterior = error
            reloj.reset()
            wait(5)

        self.frenar()

    def seguir_linea(
        self,
        sensor_color,
        velocidad_max,
        distancia_cm,
        lado="derecha",
        tiempo_acomodo_ms=800,
        kp=0.52,
        kd=1.10,
        k_freno=0.28,
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
        velocidad_minima = 30
        tiempo_aceleracion_ms = 180

        last_error = 0
        last_derivative = 0
        last_correction = 0
        error_filtrado = 0

        objetivo_reflexion = 35
        multiplicador_lado = 1 if lado == "derecha" else -1

        umbral_fino = 4
        correccion_max = 34

        cronometro.reset()
        cronometro.resume()

        while True:
            grados_actuales = (abs(self.motor_izquierdo.angle()) + abs(self.motor_derecho.angle())) / 2
            if grados_actuales >= grados_objetivo_real:
                break

            tiempo_actual = cronometro.time()

            if tiempo_actual < tiempo_acomodo_ms:
                velocidad_actual = velocidad_minima
            elif tiempo_actual < (tiempo_acomodo_ms + tiempo_aceleracion_ms):
                tiempo_en_rampa = tiempo_actual - tiempo_acomodo_ms
                progreso = tiempo_en_rampa / tiempo_aceleracion_ms
                velocidad_actual = velocidad_minima + ((velocidad_max - velocidad_minima) * progreso)
            else:
                velocidad_actual = velocidad_max

            # --------- FILTRADO CORTO DEL SENSOR ---------
            lectura_1 = sensor_color.reflection()
            lectura_2 = sensor_color.reflection()
            lectura_3 = sensor_color.reflection()
            current_reflection = (lectura_1 + lectura_2 + lectura_3) / 3

            error_crudo = current_reflection - objetivo_reflexion

            # Suaviza el error, pero no demasiado
            error_filtrado = (0.55 * error_crudo) + (0.45 * error_filtrado)
            error = error_filtrado

            derivative_raw = error - last_error
            derivative = (0.35 * derivative_raw) + (0.65 * last_derivative)

            # --------- DOS MODOS DE CORRECCIÓN ---------
            if abs(error) <= umbral_fino:
                kp_actual = 0.26
                kd_actual = 0.28
                k_freno_actual = 0.08
            else:
                kp_actual = kp
                kd_actual = kd
                k_freno_actual = k_freno

            correction_raw = ((error * kp_actual) + (derivative * kd_actual)) * multiplicador_lado

            # Suavizado moderado: evita ondulación, pero sin perder reacción
            correction = (0.35 * correction_raw) + (0.65 * last_correction)

            correction = max(-correccion_max, min(correccion_max, correction))

            velocidad_base = velocidad_actual - (abs(error) * k_freno_actual)
            velocidad_base = max(velocidad_minima, velocidad_base)

            potencia_izq = velocidad_base - correction
            potencia_der = velocidad_base + correction

            potencia_izq = max(-100, min(100, potencia_izq))
            potencia_der = max(-100, min(100, potencia_der))

            self.motor_izquierdo.dc(potencia_izq)
            self.motor_derecho.dc(potencia_der)

            last_error = error
            last_derivative = derivative
            last_correction = correction

            wait(4)

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        cronometro.pause()

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
            
            wait(10)  # Pequeña pausa de 10 ms para el control
        
        self.motor_torque.hold()
        
    def avanzar_con_torque(self, distancia_cm, grados_torque, velocidad_robot=700, velocidad_torque=150):
        self.motor_torque.run_angle(velocidad_torque, grados_torque, then=Stop.HOLD, wait=False)
        if distancia_cm < 0:
            self.retroceder_recto(abs(distancia_cm), velocidad_robot)
        self.mover_recto(distancia_cm, velocidad=velocidad_robot)

    def mover_garra(self, velocidad, grados):
        self.motor_garra.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)
        
    def mover_garra_delantera(self, velocidad, grados):
        self.motor_garra_delantera.run_angle(
            velocidad,
            grados,
            then=Stop.HOLD,
            wait=True
        )

    def salir_de_giro(self, pausa_brake=80, pausa_stop=40):
        # Frena ambos motores para cortar la inercia
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(pausa_brake)

        # Luego los libera para que no queden "amarrados"
        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(pausa_stop)

    def girar(self, angulo_deg, velocidad=500, velocidad_min=140):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(20)

        objetivo = abs(angulo_deg)
        signo = 1 if angulo_deg > 0 else -1

        while True:
            actual = abs(self.Hub.imu.heading())
            if actual >= objetivo:
                break

            restante = objetivo - actual

            if restante > 25:
                vel = velocidad
            else:
                vel = max(velocidad_min, int(velocidad * restante / 25))

            pot_izq = vel * signo
            pot_der = -vel * signo

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)
            wait(5)

        # Cierre limpio del giro
        self.salir_de_giro()

        # Microajuste fino si quedó corto
        error_final = objetivo - abs(self.Hub.imu.heading())
        if error_final > 1.5:
            ajuste = error_final if angulo_deg > 0 else -error_final

            self.reset_imu()
            wait(15)

            while abs(self.Hub.imu.heading()) < abs(ajuste):
                pot = 120 if ajuste > 0 else -120
                self.motor_izquierdo.run(pot)
                self.motor_derecho.run(-pot)
                wait(8)

            self.salir_de_giro()

    def giro_izquierda(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(20)

        objetivo = abs(angulo_deg)
        signo = 1 if angulo_deg > 0 else -1

        # Antes usabas hold(); ahora mejor brake para no dejar tensión tan agresiva
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
                vel = max(velocidad_min, int(velocidad * restante / 20))

            pot_izq = vel * signo
            pot_izq = max(-1000, min(1000, pot_izq))

            self.motor_izquierdo.run(pot_izq)
            wait(5)

        # Soltar limpio ambos motores al terminar
        self.salir_de_giro()

    def giro_derecha(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()
        wait(20)

        objetivo = abs(angulo_deg)
        signo = -1 if angulo_deg > 0 else 1

        # Antes usabas hold(); ahora mejor brake para evitar que quede trabado
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
                vel = max(velocidad_min, int(velocidad * restante / 20))

            pot_der = vel * signo
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_derecho.run(pot_der)
            wait(5)

        # Soltar limpio ambos motores al terminar
        self.salir_de_giro()