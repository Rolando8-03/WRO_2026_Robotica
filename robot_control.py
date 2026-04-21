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

    def retroceder_recto(self, distancia_cm, velocidad=700, kp=2.5, kd=4.0, velocidad_min=220):
        self.mover_recto(-abs(distancia_cm), velocidad=velocidad, kp=kp, kd=kd, velocidad_min=velocidad_min)

    def girar(self, angulo_deg, velocidad=500, velocidad_min=140):
        if angulo_deg == 0:
            return

        self.reset_imu()

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

        self.frenar()

        error_final = objetivo - abs(self.Hub.imu.heading())
        if error_final > 1.5:
            ajuste = error_final if angulo_deg > 0 else -error_final
            self.reset_imu()
            while abs(self.Hub.imu.heading()) < abs(ajuste):
                pot = 120 if ajuste > 0 else -120
                self.motor_izquierdo.run(pot)
                self.motor_derecho.run(-pot)
                wait(8)
            self.frenar()

    lista_L = []  # lista como atributo de la clase
    
    def iden_matriz(self):
        c = self.sensor_matriz.color()   # leer color
        codigo = self.codificar_color(c) # convertir a número
        self.lista_L.append(codigo)      # guardar en lista

    def seguir_linea(self, distancia_cm=None, velocidad=950, ref=30, kp=4.8, kd=7.5, ki=0.0):
        self.frenar()
        wait(50)

        self.reset_motores()
        self._last_derivative = 0

        integral = 0
        last_error = 0
        reloj = StopWatch()
        reloj.reset()

        velocidad_actual = 350
        incremento = 18
        correccion_max = 320

        if distancia_cm is not None:
            grados_objetivo = abs(distancia_cm * 10 * self.grados_por_mm)

        while True:
            if distancia_cm is not None and self.distancia_promedio_grados() >= grados_objetivo:
                break

            if velocidad_actual < velocidad:
                velocidad_actual += incremento
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad

            lectura = self.seguidor.reflection()
            error = ref - lectura

            dt = reloj.time() / 1000
            if dt <= 0:
                dt = 0.001

            integral += error * dt
            integral = max(-10, min(10, integral))

            derivada = (error - last_error) / dt
            derivada = derivada * 0.65 + self._last_derivative * 0.35
            self._last_derivative = derivada

            correccion = (kp * error) + (kd * derivada) + (ki * integral)
            correccion = max(-correccion_max, min(correccion_max, correccion))

            pot_izq = int((velocidad_actual + correccion) * self.bias_izq)
            pot_der = int((velocidad_actual - correccion) * self.bias_der)

            pot_izq = max(-1000, min(1000, pot_izq))
            pot_der = max(-1000, min(1000, pot_der))

            self.motor_izquierdo.run(pot_izq)
            self.motor_derecho.run(pot_der)

            last_error = error
            reloj.reset()
            wait(5)

        self.frenar()

    '''
    def mover_torque(self, grados_torque, velocidad_torque=150):
        self.motor_torque.run_angle(velocidad_torque, grados_torque, then=Stop.HOLD, wait=True)
    '''
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
        self.mover_recto(distancia_cm, velocidad=velocidad_robot)

    def mover_garra(self, velocidad, grados):
        self.motor_garra.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)


    def mover_garra(self, velocidad, grados):
        self.motor_garra.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)

    def giro_izquierda(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()

        objetivo = abs(angulo_deg)
        signo = 1 if angulo_deg > 0 else -1

        self.motor_derecho.hold()

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

        self.motor_izquierdo.brake()
        self.motor_derecho.stop()
        wait(30)

    def giro_derecha(self, angulo_deg, velocidad=450, velocidad_min=120):
        if angulo_deg == 0:
            return

        self.reset_imu()

        objetivo = abs(angulo_deg)
        signo = -1 if angulo_deg > 0 else 1

        self.motor_izquierdo.hold()

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

        self.motor_derecho.brake()
        self.motor_izquierdo.stop()
        wait(30)