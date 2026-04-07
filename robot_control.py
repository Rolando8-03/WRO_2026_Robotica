from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Clase de integración general del robot
class Base:
    def __init__(self):
        self.Hub = PrimeHub()  # Hub
        
        # --- ÚNICA COSA AGREGADA: Calibración profunda del giroscopio ---
        self.calibrar_giroscopio()
        # ----------------------------------------------------------------
        
        wait(2000)  # pausa para esperar el robot (lo dejamos por si acaso)

        # Motores
        self.motor_derecho   = Motor(Port.B, Direction.CLOCKWISE)
        self.motor_izquierdo = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.motor_torque    = Motor(Port.E)
        self.motor_garra     = Motor(Port.A)  # Agregado el motor de la garra

        # Sensores
        self.seguidor = ColorSensor(Port.C)
        self.sensor_matriz = ColorSensor(Port.D)
        

        # DriveBase (configuración)
        self.drive_base = DriveBase(
            self.motor_izquierdo,  # izquierdo primero
            self.motor_derecho,     # derecho segundo para coincidir con el código 2
            wheel_diameter=56,   # diámetro mm
            axle_track=170       # distancia entre ruedas mm (usando valor del código 2)
        )

        self.drive_base.use_gyro(True)

        # Ajustes de movimiento (usando valores del código 2)
        self.drive_base.settings(
            straight_speed=900,          # velocidad máxima en línea recta
            straight_acceleration=900,   # qué tan rápido llega a la velocidad máxima
            turn_rate=400,               # velocidad máxima al girar sobre su propio eje
            turn_acceleration=400        # qué tan rápido empieza y frena el giro
        )
        
        # Factor de calibración para los motores (ajusta según necesites)
        self.factor_calibracion = 0.9875  # Tomado de tu código del giroscopio
        
        # Para seguimiento de línea con giroscopio
        self.heading_inicial = 0

    # ------------- ÚNICA FUNCIÓN NUEVA AGREGADA ----------------
    def calibrar_giroscopio(self):
        """
        Calibración profunda del giroscopio.
        El robot DEBE estar quieto durante este proceso.
        """
        print("Calibrando giroscopio... NO MOVER EL ROBOT")
        self.Hub.light.on(Color.RED)
        
        # Paso 1: Reset inicial y espera para que el giroscopio se estabilice
        self.Hub.imu.reset_heading(0)
        wait(500)
        
        # Paso 2: Lecturas repetidas para asentar la calibración
        # Hacemos 10 lecturas con pequeñas pausas para que el IMU se ajuste
        for i in range(10):
            _ = self.Hub.imu.heading()  # Leemos para forzar actualización
            wait(100)
        
        # Paso 3: Reset final después de la calibración
        self.Hub.imu.reset_heading(0)
        wait(500)
        
        # Verificación rápida (opcional)
        lectura_final = self.Hub.imu.heading()
        print(f"Calibración completada. Lectura inicial: {lectura_final}°")
        
        self.Hub.light.on(Color.GREEN)
        wait(500)
    # ------------------------------------------------------------

    # ------------- FUNCIONES DE UTILIDAD ----------------
    def esperar(self, ms):
        wait(ms)

    def frenar(self):
        # hacemos que ambos motores frenen y esperamos un momento
        self.motor_derecho.brake()
        self.motor_izquierdo.brake()
        wait(30)

    def reset_imu_y_base(self):
        # resetea la distancia recorrida
        self.drive_base.reset()
        # resetea la orientación
        self.Hub.imu.reset_heading(0)
        wait(50)  # Pequeña pausa después del reset

    # ---------- MOVIMIENTOS DE LA BASE --------------------
    def avanzar(self, distancia_mm):
        self.drive_base.straight(distancia_mm)

    def girar(self, angulo_deg):
        self.drive_base.turn(angulo_deg)

    # ----------------- FUNCIONES DEL GIROSCOPIO (de tu código) -----------------
    def movimiento_giroscopio(self, velocidad, distancia_cm, kp=4.5, kd=2.0):
        """
        Movimiento recto perfecto con control PD.
        - velocidad: potencia base para el motor izquierdo
        - distancia_cm: distancia en centímetros (EXACTA)
        - El motor derecho automáticamente usa velocidad - 20
        """
        self.Hub.imu.reset_heading(0)
        wait(100)
        bias = self.Hub.imu.heading()
        
        # Reseteamos el ángulo del motor izquierdo para medir distancia
        self.motor_izquierdo.reset_angle(0)
        
        # Aplicamos tu regla mecánica: derecho siempre 20 menos
        if distancia_cm >= 0:
            base_izq = velocidad
            base_der = velocidad - 20
        else:
            base_izq = -velocidad
            base_der = -(velocidad - 20)
        
        # Convertir distancia a grados del motor
        # Diámetro rueda: 56mm → circunferencia = 56 * pi = 175.93 mm
        # 1 cm = 10 mm → grados por cm = (360° / 175.93 mm) * 10 mm = 20.46°
        grados_por_cm = (360 / (56 * 3.1416)) * 10  # ≈ 20.46 grados/cm
        grados_objetivo = abs(distancia_cm) * grados_por_cm * self.factor_calibracion
        
        error_anterior = 0
        
        while abs(self.motor_izquierdo.angle()) < grados_objetivo:
            error = 0 - (self.Hub.imu.heading() - bias)
            derivada = (error - error_anterior) / 0.01
            correccion = error * kp + derivada * kd
            correccion = max(-150, min(150, correccion))
            
            if distancia_cm >= 0:
                self.motor_izquierdo.run(base_izq + correccion)
                self.motor_derecho.run(base_der - correccion)
            else:
                self.motor_izquierdo.run(base_izq - correccion)
                self.motor_derecho.run(base_der + correccion)
            
            error_anterior = error
            wait(10)
        
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

    def movimiento_adelante(self, velocidad, distancia):
        """Movimiento hacia adelante con corrección giroscópica"""
        self.Hub.imu.reset_heading(0)
        self.motor_izquierdo.reset_angle(0)

        grados = (distancia*10 / (56 * 3.1416)) * 360 * self.factor_calibracion

        while abs(self.motor_izquierdo.angle()) < abs(grados):
            restante = abs(grados) - abs(self.motor_izquierdo.angle())

            v = velocidad
            if restante < 150:
                v = velocidad * 0.4

            error = self.Hub.imu.heading()
            correccion = error * 1.8  # Ajusta este valor según necesites

            self.motor_izquierdo.run(v - correccion)
            self.motor_derecho.run(v + correccion)

            wait(10)

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(50)
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

    def girar_giroscopio(self, velocidad, angulo):
        """Giro con ambas ruedas usando giroscopio"""
        self.Hub.imu.reset_heading(0)

        while abs(self.Hub.imu.heading()) < abs(angulo * self.factor_calibracion):
            restante = abs(angulo * self.factor_calibracion) - abs(self.Hub.imu.heading())

            v = velocidad
            if restante < 20:          # desaceleración final
                v = velocidad * 0.35

            direccion = 1 if angulo > 0 else -1

            self.motor_izquierdo.run(v * direccion)
            self.motor_derecho.run(-v * direccion)

            wait(10)

        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        wait(50)
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()

    # ----------------- GIROS CON UNA SOLA RUEDA -----------------
    def giro_con_derecha(self, grados_rueda):
        self.drive_base.stop()
        self.motor_derecho.run_angle(900, grados_rueda)
        self.reset_imu_y_base()

    def giro_con_izquierda(self, grados_rueda):
        self.drive_base.stop()
        self.motor_izquierdo.run_angle(900, grados_rueda)
        self.reset_imu_y_base()

    def giro_izquierda(self, velocidad, grados):
        """Giro usando solo la rueda izquierda con corrección giroscópica"""
        self.Hub.imu.reset_heading(0)
        self.motor_derecho.hold()

        direccion = 1 if grados > 0 else -1
        objetivo = abs(grados)

        while True:
            angulo = abs(self.Hub.imu.heading())
            error = objetivo - angulo

            if error <= 0:
                break

            if error < 20:
                vel = max(130, velocidad * 0.35)
            elif error < 8:
                vel = 110
            else:
                vel = velocidad

            self.motor_izquierdo.run(vel * direccion)
            wait(5)  # Pequeña pausa para no saturar

        self.motor_izquierdo.brake()
        self.motor_derecho.stop()

    def giro_derecha(self, velocidad, grados):
        """Giro usando solo la rueda derecha con corrección giroscópica"""
        self.Hub.imu.reset_heading(0)
        self.motor_izquierdo.hold()

        direccion = 1 if grados > 0 else -1
        objetivo = abs(grados)

        while True:
            angulo = abs(self.Hub.imu.heading())
            error = objetivo - angulo

            if error <= 0:
                break

            if error < 20:
                vel = max(130, velocidad * 0.35)
            elif error < 8:
                vel = 110
            else:
                vel = velocidad

            self.motor_derecho.run(vel * direccion)
            wait(5)

        self.motor_derecho.brake()
        self.motor_izquierdo.stop()

    # ----------------- MECANISMOS -----------------

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
        self.motor_garra.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)

    def movimiento_giroscopio_hasta_linea_n(self, velocidad=600, umbral=20, lineas_a_saltar=1):
        """
        Movimiento recto con giroscopio que avanza hasta encontrar la línea negra
        número 'lineas_a_saltar + 1' (salta las primeras 'lineas_a_saltar' líneas)
        """
        print(f"🔍 Movimiento recto - Saltando {lineas_a_saltar} línea(s) negra(s)...")
        
        self.Hub.imu.reset_heading(0)
        
        contador_lineas = 0
        ya_detecto_linea = False
        
        while True:
            error = self.Hub.imu.heading()
            correccion = error * 1.8
            
            self.motor_izquierdo.run(velocidad - correccion)
            self.motor_derecho.run(velocidad + correccion)
            
            # Leer reflexión para detectar líneas negras
            reflexion = self.seguidor.reflection()
            
            # Detectar línea negra
            if reflexion < umbral and not ya_detecto_linea:
                contador_lineas += 1
                ya_detecto_linea = True
                print(f"📍 Línea negra #{contador_lineas} detectada")
                
                # Si es la línea objetivo (después de saltar las primeras), detener
                if contador_lineas > lineas_a_saltar:
                    print(f"⚫ ¡Línea negra objetivo (#{contador_lineas}) alcanzada!")
                    break
            
            # Resetear detección cuando sale de la línea
            elif reflexion >= umbral and ya_detecto_linea:
                ya_detecto_linea = False
            
            self.esperar(5)
        
        # Detener
        self.motor_izquierdo.stop()
        self.motor_derecho.stop()
        self.esperar(50)
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        
        print("✅ Movimiento completado")

    def seguir_linea_con_giroscopio(self, distancia_cm=None, velocidad=900, ref=30):
        """
        SEGUIDOR MAGNÉTICO - Se adhiere a la línea como un imán
        - Máxima fijación a la línea recta
        - Sin curvas ni oscilaciones
        - Corrección agresiva pero estable
        """
        print("🧲 SEGUIDOR MAGNÉTICO ACTIVADO - ADHERENCIA TOTAL A LA LÍNEA")
        
        # ===== CONSTANTES OPTIMIZADAS PARA COMPORTAMIENTO MAGNÉTICO =====
        kp = 8.0      # ALTO - Responde fuertemente al error (imán)
        kd = 12.0     # MUY ALTO - Elimina oscilaciones (amortiguador)
        ki = 0.01     # MÍNIMO - Solo para compensación de error constante
        
        # ===== BANDA MUERTA Y UMBRALES =====
        # Si el error es menor que esto, consideramos que está perfectamente centrado
        banda_muerta = 2
        
        # ===== FACTORES DE CORRECCIÓN DE HARDWARE =====
        # Compensación fija si el robot tiende a desviarse siempre al mismo lado
        sesgo_izquierdo = 0.98    # Reduce ligeramente izquierda (1.0 = neutral)
        sesgo_derecho = 1.02      # Aumenta ligeramente derecha
        
        # ===== VARIABLES PID =====
        last_error = 0
        integral = 0
        last_time = StopWatch()
        last_time.reset()
        
        # ===== CONFIGURACIÓN INICIAL =====
        self.Hub.imu.reset_heading(0)
        
        # Rampa de velocidad (más rápida para llegar pronto al modo magnético)
        velocidad_actual = 400
        incremento = 30
        
        # Para distancia
        if distancia_cm is not None:
            self.drive_base.reset()
            distancia_mm = distancia_cm * 10
        
        # Contador para estabilidad
        contador_estable = 0
        
        print(f"⚡ Velocidad objetivo: {velocidad}")
        
        while True:
            # ===== CONTROL DE DISTANCIA =====
            if distancia_cm is not None and abs(self.drive_base.distance()) >= distancia_mm:
                break
            
            # ===== RAMPA DE VELOCIDAD =====
            if velocidad_actual < velocidad:
                velocidad_actual += incremento
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad
            
            # ===== LECTURA DEL SENSOR =====
            current_reflection = self.seguidor.reflection()
            error_linea = ref - current_reflection
            
            # ===== BANDA MUERTA =====
            # Si el error es muy pequeño, lo tratamos como cero (robot centrado)
            if abs(error_linea) < banda_muerta:
                error_linea = 0
                contador_estable += 1
            else:
                contador_estable = 0
            
            # ===== CÁLCULO DEL TIEMPO =====
            dt = last_time.time()
            if dt > 0:
                # Integral limitada
                integral += error_linea * dt * 0.001
                integral = max(-20, min(20, integral))  # Anti-windup estricto
                
                # Derivada filtrada
                derivative = (error_linea - last_error) / (dt/1000 + 0.001)
                
                # Filtro pasa-bajos para la derivada (suaviza)
                derivative = derivative * 0.7 + self._last_derivative * 0.3 if hasattr(self, '_last_derivative') else derivative
                self._last_derivative = derivative
            else:
                derivative = 0
            
            # ===== CORRECCIÓN PID PRINCIPAL =====
            correccion_linea = (error_linea * kp) + (integral * ki) + (derivative * kd)
            
            # ===== CORRECCIÓN DEL GIROSCOPIO (MÍNIMA) =====
            error_giroscopio = self.Hub.imu.heading()
            
            # Solo corregimos si el error de giro es significativo
            if abs(error_giroscopio) > 1.5:
                # Corrección suave pero efectiva
                correccion_giro = error_giroscopio * 1.5
            else:
                correccion_giro = 0
            
            # ===== CORRECCIÓN TOTAL =====
            # La línea tiene prioridad, el giroscopio solo ayuda
            correccion_total = correccion_linea + (correccion_giro * 0.5)
            
            # ===== POTENCIAS BASE =====
            # Invertimos la corrección: positivo = derecha más rápido
            potencia_izq_base = velocidad_actual + correccion_total
            potencia_der_base = velocidad_actual - correccion_total
            
            # ===== APLICAR SESGO DE HARDWARE =====
            # Esto compensa diferencias mecánicas entre motores
            potencia_izq = potencia_izq_base * sesgo_izquierdo
            potencia_der = potencia_der_base * sesgo_derecho
            
            # ===== LÍMITES DE SEGURIDAD =====
            potencia_izq = max(-1000, min(1000, potencia_izq))
            potencia_der = max(-1000, min(1000, potencia_der))
            
            # ===== COMPORTAMIENTO MAGNÉTICO =====
            # Si estamos muy centrados (error pequeño), vamos a máxima velocidad magnética
            if abs(error_linea) < 5 and contador_estable > 3:
                # Modo "imán" - máxima adherencia
                # Ajuste fino para mantener el centro perfecto
                if error_linea != 0:
                    # Corrección microscópica
                    potencia_izq += error_linea * 2
                    potencia_der -= error_linea * 2
            
            # ===== APLICAR A MOTORES =====
            self.motor_izquierdo.run(int(potencia_izq))
            self.motor_derecho.run(int(potencia_der))
            
            # ===== ACTUALIZAR VARIABLES =====
            last_error = error_linea
            last_time.reset()
            
            # Loop rápido para respuesta inmediata
            wait(5)
        
        # ===== FRENADO SUAVE =====
        print("🛑 Finalizando seguidor magnético")
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        
        # Pequeña pausa para estabilizar
        wait(50)