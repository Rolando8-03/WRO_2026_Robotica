from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Side, Stop, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

class Base:
    def __init__(self):
        self.Hub = PrimeHub()
        wait(500)

        # Motores
        self.motor_derecho   = Motor(Port.B, Direction.CLOCKWISE)
        self.motor_izquierdo = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.motor_torque    = Motor(Port.C)
        self.motor_garra     = Motor(Port.A)

        # Sensores
        self.seguidor = ColorSensor(Port.E)

        # DriveBase necesario para algunas funciones (como reset de distancia)
        self.drive_base = DriveBase(
            self.motor_izquierdo,
            self.motor_derecho,
            wheel_diameter=56,
            axle_track=170
        )

        # Constantes
        self.diametro_rueda = 56  # mm
        self.distancia_entre_ruedas = 170  # mm
        self.factor_calibracion = 0.9875  # Ajuste mecánico
        self.pi = 3.1416

        # No activamos el giroscopio en DriveBase para tener control manual

    # ---------- UTILIDADES ----------
    def esperar(self, ms):
        wait(ms)

    def frenar(self):
        self.motor_derecho.brake()
        self.motor_izquierdo.brake()
        wait(30)

    def reset_imu(self):
        """Resetea el IMU asegurando que el robot está quieto"""
        wait(500)  # Espera a que se estabilice
        self.Hub.imu.reset_heading(0)
        # Lee el heading varias veces para asegurar que es 0
        for _ in range(5):
            if abs(self.Hub.imu.heading()) > 0.01:
                # Si hay desviación, resetea de nuevo
                self.Hub.imu.reset_heading(0)
            wait(100)
        print("IMU listo, heading:", self.Hub.imu.heading())

    # ---------- MOVIMIENTO RECTILÍNEO CON GIROSCOPIO (CORREGIDO) ----------
    def mover(self, velocidad, distancia_cm):
        """
        Avanza o retrocede en línea recta con compensación mecánica feedforward.
        - velocidad: rapidez (0-1000), siempre positiva.
        - distancia_cm: >0 adelante, <0 atrás.
        """
        self.reset_imu()
        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

        direccion = 1 if distancia_cm > 0 else -1
        distancia_abs = abs(distancia_cm)

        circunferencia = self.diametro_rueda * self.pi
        grados_totales = (distancia_abs * 10 / circunferencia) * 360 * self.factor_calibracion

        vel_objetivo = abs(velocidad)
        vel_actual = 0
        incremento = 100

        # Parámetros independientes para avance y retroceso
        if direccion == 1:  # Avance
            kp = 1.0
            ki = 0.0
            kd = 0.2
            ff_factor = -0.125      # Ajustado para avance
            offset_manual = 0        # Si aún se desvía, prueba valores pequeños (+/-)
        else:  # Retroceso
            kp = 1.5                 # Un poco más de proporcional
            ki = 0.1                  # Integral para eliminar error sistemático
            kd = 0.3
            ff_factor = -0.21          # Más negativo porque la desviación era a la izquierda
            offset_manual = -10       # Offset adicional (negativo = corrige izquierda)

        last_error = 0
        integral = 0
        dt = 10
        integral_max = 50

        while True:
            angulo_prom = (self.motor_izquierdo.angle() + self.motor_derecho.angle()) / 2
            if abs(angulo_prom) >= grados_totales:
                break

            if vel_actual < vel_objetivo:
                vel_actual += incremento
                if vel_actual > vel_objetivo:
                    vel_actual = vel_objetivo

            error = self.Hub.imu.heading()

            # PID con integral
            integral += error * dt * 0.001
            integral = max(-integral_max, min(integral_max, integral))
            derivada = (error - last_error) / (dt / 1000) if dt > 0 else 0

            # Feedforward + offset
            feedforward = ff_factor * vel_actual
            correccion_total = (error * kp) + (integral * ki) + (derivada * kd) + feedforward + offset_manual

            # Ajuste por dirección: multiplicamos por la dirección para que la corrección actúe igual en ambos sentidos
            correccion_ajustada = correccion_total * direccion

            potencia_base = vel_actual * direccion
            potencia_izq = potencia_base - correccion_ajustada
            potencia_der = potencia_base + correccion_ajustada

            potencia_izq = max(-1000, min(1000, potencia_izq))
            potencia_der = max(-1000, min(1000, potencia_der))

            self.motor_izquierdo.run(potencia_izq)
            self.motor_derecho.run(potencia_der)

            last_error = error
            wait(dt)

        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(50)
        print("Desviación final:", self.Hub.imu.heading())

    # ---------- GIROS MANUALES (SIN GIROSCOPIO) ----------
    def girar(self, velocidad, angulo_grados):
        """
        Gira sobre su propio eje.
        - angulo_grados > 0: derecha, < 0: izquierda
        """
        angulo_abs = abs(angulo_grados)
        sentido = 1 if angulo_grados > 0 else -1  # positivo = derecha

        # Cálculo: distancia lineal que recorre cada rueda = (ángulo_rad * distancia_entre_ruedas) / 2
        angulo_rad = angulo_abs * self.pi / 180
        distancia_lineal = (angulo_rad * self.distancia_entre_ruedas) / 2

        circunferencia = self.diametro_rueda * self.pi
        grados_motor = (distancia_lineal / circunferencia) * 360 * self.factor_calibracion

        self.motor_izquierdo.reset_angle(0)
        self.motor_derecho.reset_angle(0)

        # Asignar velocidades según sentido
        if sentido > 0:  # derecha
            vel_izq = -abs(velocidad)
            vel_der = abs(velocidad)
        else:  # izquierda
            vel_izq = abs(velocidad)
            vel_der = -abs(velocidad)

        while abs(self.motor_izquierdo.angle()) < grados_motor and abs(self.motor_derecho.angle()) < grados_motor:
            restante = grados_motor - abs(self.motor_izquierdo.angle())
            v = abs(velocidad)
            if restante < 100:
                v = max(150, v * 0.3)

            self.motor_izquierdo.run(v * (1 if vel_izq > 0 else -1))
            self.motor_derecho.run(v * (1 if vel_der > 0 else -1))
            wait(10)

        self.frenar()
        self.reset_imu()

    def giro_izquierdo_llanta(self, velocidad, angulo_grados):
        """
        Gira con rueda izquierda fija.
        - angulo_grados > 0: derecha, < 0: izquierda
        """
        angulo_abs = abs(angulo_grados)
        sentido = 1 if angulo_grados > 0 else -1

        angulo_rad = angulo_abs * self.pi / 180
        distancia_lineal = angulo_rad * self.distancia_entre_ruedas

        circunferencia = self.diametro_rueda * self.pi
        grados_motor = (distancia_lineal / circunferencia) * 360 * self.factor_calibracion

        self.motor_izquierdo.hold()
        self.motor_derecho.reset_angle(0)

        # Para girar a la derecha (+), la rueda derecha avanza (+)
        # Para girar a la izquierda (-), la rueda derecha retrocede (-)
        direccion = 1 if sentido > 0 else -1

        while abs(self.motor_derecho.angle()) < grados_motor:
            restante = grados_motor - abs(self.motor_derecho.angle())
            v = abs(velocidad)
            if restante < 100:
                v = max(150, v * 0.3)

            self.motor_derecho.run(v * direccion)
            wait(10)

        self.motor_derecho.brake()
        self.motor_izquierdo.stop()
        self.reset_imu()

    def giro_derecho_llanta(self, velocidad, angulo_grados):
        """
        Gira con rueda derecha fija.
        - angulo_grados > 0: izquierda, < 0: derecha
        """
        angulo_abs = abs(angulo_grados)
        sentido = 1 if angulo_grados > 0 else -1

        angulo_rad = angulo_abs * self.pi / 180
        distancia_lineal = angulo_rad * self.distancia_entre_ruedas

        circunferencia = self.diametro_rueda * self.pi
        grados_motor = (distancia_lineal / circunferencia) * 360 * self.factor_calibracion

        self.motor_derecho.hold()
        self.motor_izquierdo.reset_angle(0)

        # Para girar a la derecha (+), la rueda derecha avanza (+)
        # Para girar a la izquierda (-), la rueda derecha retrocede (-)
        direccion = 1 if sentido > 0 else -1

        while abs(self.motor_izquierdo.angle()) < grados_motor:
            restante = grados_motor - abs(self.motor_izquierdo.angle())
            v = abs(velocidad)
            if restante < 100:
                v = max(150, v * 0.3)

            self.motor_izquierdo.run(v * direccion)
            wait(10)

        self.motor_izquierdo.brake()
        self.motor_derecho.stop()
        self.reset_imu()

    # ---------- SEGUIDOR DE LÍNEA CORREGIDO (USA DRIVE_BASE PARA DISTANCIA) ----------
    def seguir_linea(self, velocidad, distancia_cm=None):
        """
        Sigue línea negra. Para retroceso (distancia_cm < 0) usa offset propio.
        - velocidad: rapidez (0-1000), siempre positiva.
        - distancia_cm: >0 avanza, <0 retrocede.
        """
        # Parámetros comunes (los mismos que funcionan en avance)
        REF = 30
        KP = 8.0
        KI = 0.01
        KD = 10.0

        # Offset independiente para retroceso (ajústalo aquí)
        OFFSET_ATRAS = -1   # negativo = corrige izquierda, positivo = derecha

        rapidez = abs(velocidad)

        # Dirección según distancia_cm
        if distancia_cm is not None:
            direccion = 1 if distancia_cm > 0 else -1
            distancia_objetivo_mm = abs(distancia_cm) * 10
            self.motor_izquierdo.reset_angle(0)
            self.motor_derecho.reset_angle(0)
            circunferencia = self.diametro_rueda * self.pi
            usar_distancia = True
        else:
            direccion = 1 if velocidad > 0 else -1
            usar_distancia = False

        # Seleccionar offset
        offset = 0 if direccion == 1 else OFFSET_ATRAS

        vel_actual = 500
        last_error = 0
        integral = 0
        dt = 10
        max_correccion = 200  # Límite suave para evitar saturación

        while True:
            if usar_distancia:
                angulo_prom = (self.motor_izquierdo.angle() + self.motor_derecho.angle()) / 2
                distancia_actual_mm = (angulo_prom / 360) * circunferencia * self.factor_calibracion
                if (direccion == 1 and distancia_actual_mm >= distancia_objetivo_mm) or \
                (direccion == -1 and distancia_actual_mm <= -distancia_objetivo_mm):
                    break

            # Rampa
            if vel_actual < rapidez:
                vel_actual += 200
                if vel_actual > rapidez:
                    vel_actual = rapidez

            # Sensor
            reflexion = self.seguidor.reflection()
            error = REF - reflexion

            # Reseteamos integral si el error es muy grande (hemos perdido la línea)
            if abs(error) > 20:
                integral = 0

            # PID con límite de integral
            integral += error * dt * 0.001
            integral = max(-100, min(100, integral))  # Límite fijo para integral
            derivada = (error - last_error) / (dt / 1000) if dt > 0 else 0

            correccion = (error * KP) + (integral * KI) + (derivada * KD) + offset

            # Limitar corrección a un valor razonable
            correccion = max(-max_correccion, min(max_correccion, correccion))

            # Potencia base (con signo)
            potencia_base = vel_actual * direccion

            # Aplicar corrección (siempre igual)
            potencia_izq = potencia_base + correccion
            potencia_der = potencia_base - correccion

            # Limitar a ±1000
            potencia_izq = max(-1000, min(1000, potencia_izq))
            potencia_der = max(-1000, min(1000, potencia_der))

            # Depuración (opcional)
            # print(f"dir:{direccion} err:{error:.1f} corr:{correccion:.1f} izq:{potencia_izq:.0f} der:{potencia_der:.0f}")

            self.motor_izquierdo.run(potencia_izq)
            self.motor_derecho.run(potencia_der)

            last_error = error
            wait(dt)

        self.frenar()

    # ---------- FUNCIONES PARA MECANISMOS ----------
    def mover_torque(self, velocidad, grados):
        """
        Mueve el motor torque con aceleración y desaceleración suave.
        - velocidad: máxima velocidad (0-1000), siempre positiva (la dirección la da grados)
        - grados: >0 un sentido, <0 sentido opuesto
        """
        direccion = 1 if grados > 0 else -1
        grados_abs = abs(grados)
        
        # Configuración del perfil
        vel_max = abs(velocidad)
        vel_actual = 0
        incremento = 200  # aceleración rápida
        zona_desaceleracion = 100  # grados antes del final donde empezar a frenar
        vel_min = 150  # velocidad mínima al final
        
        self.motor_torque.reset_angle(0)
        
        while abs(self.motor_torque.angle()) < grados_abs:
            restante = grados_abs - abs(self.motor_torque.angle())
            
            # Aceleración
            if vel_actual < vel_max:
                vel_actual += incremento
                if vel_actual > vel_max:
                    vel_actual = vel_max
            
            # Desaceleración si estamos cerca del final
            if restante < zona_desaceleracion:
                # Velocidad proporcional a la distancia restante
                factor = restante / zona_desaceleracion
                vel_actual = max(vel_min, vel_max * factor)
            
            # Aplicar potencia con la dirección adecuada
            self.motor_torque.run(vel_actual * direccion)
            wait(10)
        
        # Parar al final
        self.motor_torque.hold()

    def mover_garra(self, velocidad, grados):
        """Ángulo positivo = un sentido, negativo = opuesto"""
        self.motor_garra.run_angle(abs(velocidad), grados, then=Stop.HOLD, wait=True)
