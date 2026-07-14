from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase 

class Base:

    def __init__(self):
        # =========================
        # CONFIGURACIÓN DEL ROBOT
        # =========================
        self.Hub = PrimeHub()

        # Tu orientación física real indestructible (Espejo mecánico)
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

        # Inicializamos la DriveBase limpia (100% compatible con tu firmware v3.x)
        self.drive_base = DriveBase(
            self.motor_izquierdo, 
            self.motor_derecho, 
            wheel_diameter=56, 
            axle_track=205
        )
        
        self.velocidad_base = 600  
        self._last_derivative = 0

    # =========================
    # FUNCIONES BÁSICAS
    # =========================

    def frenar(self):
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(3)

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

    def _error_angular(self, objetivo, actual):
        error = objetivo - actual
        while error > 180: error -= 360
        while error < -180: error += 360
        return error

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

    # ====================================================================
    # FUSIÓN ESTRATÉGICA DEFINITIVA: DRIVEBASE + TU CONTROL SUPREMO
    # ====================================================================

    def avanzar_recto(
            self,
            distancia_cm,
            velocidad_max=900,
            velocidad_min=100,     
            kp_gyro=20.0,          
            zona_rampa_cm=8, 
            perfil="encadenado",
            rumbo_esperado=None   # 🔥 Parámetro de Memoria de Rumbo (IMU Shock)
        ):
            if distancia_cm == 0:
                return

            self.preparar_movimiento(reset_motores=False, reset_gyro=False, perfil=perfil)
            
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(90) # Arranque veloz
            
            self.drive_base.reset()
            
            # =========================================================
            # 🔥 LÓGICA DE MEMORIA DE RUMBO
            # Si le mandamos un rumbo pre-guardado, usa ese. 
            # Si no, lee el giroscopio en este instante.
            # =========================================================
            if rumbo_esperado is not None:
                heading_objetivo = rumbo_esperado
            else:
                heading_objetivo = self.Hub.imu.heading()
            
            # Corrección exacta basada en tu circunferencia
            grados_por_cm = 360 / (self.circunferencia / 10) 
            grados_objetivo = abs(distancia_cm) * grados_por_cm
            
            rampa_efectiva_cm = min(zona_rampa_cm, abs(distancia_cm) / 2.0)
            grados_rampa = rampa_efectiva_cm * grados_por_cm
            
            signo = 1 if distancia_cm > 0 else -1
            
            cronometro = StopWatch()
            cronometro.reset()

            while True:
                # Usamos la distancia real de la DriveBase
                recorrido = abs(self.drive_base.distance()) * self.grados_por_mm
                restante = grados_objetivo - recorrido
                
                # Cortar milimétricamente
                if restante <= 1.5: 
                    break

                actual_heading = self.Hub.imu.heading()
                error_gyro = self._error_angular(heading_objetivo, actual_heading)
                
                if recorrido < grados_rampa:
                    proporcion = recorrido / grados_rampa
                    vel_base = velocidad_min + (velocidad_max - velocidad_min) * proporcion
                elif restante < grados_rampa:
                    proporcion = restante / grados_rampa
                    vel_base = (velocidad_min * 0.4) + (velocidad_max - (velocidad_min * 0.4)) * proporcion
                else:
                    vel_base = velocidad_max

                tiempo_ms = cronometro.time()
                if tiempo_ms < 150:
                    vel = vel_base * (tiempo_ms / 150)
                else:
                    vel = vel_base

                vel = self.limitar(vel, 25, velocidad_max)
                correccion_giro = error_gyro * kp_gyro

                self.drive_base.drive(vel * signo, correccion_giro)

            # =======================================================
            # 🔥 MODIFICACIÓN ÉLITE: Frenado de Dos Fases (Anti-Rebote)
            # =======================================================
            self.drive_base.stop() 
            
            # Fase 1: Freno pasivo (cortocircuito) para disipar inercia sin rebotar
            self.motor_izquierdo.brake() 
            self.motor_derecho.brake()
            wait(60) 
            
            # Fase 2: Freno activo. Ya sin inercia, clavamos el robot en su lugar.
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)

    # ========================================================
    # SECCIÓN DE GIROS (MODO BESTIA AJUSTADO A DRIVEBASE SIMÉTRICA)
    # ========================================================
# ============================================================
# REEMPLAZA TU FUNCIÓN girar() ACTUAL CON ESTA VERSIÓN MEJORADA
# ============================================================
    def girar(
        self,
        angulo_deg,
        potencia_max=85,
        potencia_min=35,
        kp_base=3.5,
        kd_base=5.0,
        tiempo_curva_s_ms=100,
        tolerancia_fin=1.2,
        perfil="encadenado"
    ):
        """
        Giro con control de giroscopio y detección automática de bloqueos.
        Esta versión reemplaza completamente a la anterior.
        """
        if angulo_deg == 0:
            return

        # Preparar motores
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(40)

        self.preparar_movimiento(reset_motores=False, reset_gyro=True, perfil=perfil)

        inicio = self.Hub.imu.heading()
        objetivo = inicio + angulo_deg
        
        error_anterior = self._error_angular(objetivo, inicio)
        derivada_anterior = 0
        
        cronometro = StopWatch()
        cronometro.reset()
        
        # ============================================================
        # 🔥 VARIABLES PARA DETECCIÓN DE BLOQUEO
        # ============================================================
        ultimo_angulo_imu = inicio
        ultimo_angulo_motores = (self.motor_izquierdo.angle() + self.motor_derecho.angle()) / 2
        contador_sin_cambio = 0
        bloqueo_detectado = False

        while True:
            # ============================================================
            # 1. LECTURA DE SENSORES
            # ============================================================
            actual_imu = self.Hub.imu.heading()
            error = self._error_angular(objetivo, actual_imu)
            
            # Lectura de motores (odometría)
            angulo_motores = (self.motor_izquierdo.angle() + self.motor_derecho.angle()) / 2
            
            # ============================================================
            # 2. DETECCIÓN DE BLOQUEO
            # ============================================================
            if abs(error) > 5:
                # Calculamos cuánto debería haber girado según el IMU
                delta_imu = abs(actual_imu - ultimo_angulo_imu)
                delta_motores = abs(angulo_motores - ultimo_angulo_motores)
                
                # Si el IMU dice que no estamos girando pero los motores dicen que sí
                if delta_imu < 1.0 and delta_motores > 5.0:
                    contador_sin_cambio += 1
                    if contador_sin_cambio > 5:
                        # ¡BLOQUEO DETECTADO!
                        bloqueo_detectado = True
                        
                        # Identificar qué rueda está patinando
                        if abs(self.motor_izquierdo.angle() - ultimo_angulo_motores) > abs(self.motor_derecho.angle() - ultimo_angulo_motores):
                            # La izquierda está patinando - frenarla
                            self.motor_izquierdo.dc(-20)
                            wait(20)
                        else:
                            # La derecha está patinando - frenarla
                            self.motor_derecho.dc(-20)
                            wait(20)
                        
                        # Reseteamos y continuamos
                        self.reset_motores()
                        angulo_motores = 0
                        bloqueo_detectado = False
                        contador_sin_cambio = 0
                else:
                    contador_sin_cambio = max(0, contador_sin_cambio - 1)
                
                ultimo_angulo_imu = actual_imu
                ultimo_angulo_motores = angulo_motores

            # ============================================================
            # 3. CONTROL DE GIRO NORMAL
            # ============================================================
            if abs(error) <= tolerancia_fin:
                break

            # Ganancia dinámica
            if abs(error) > 25:
                kp_dinamico = kp_base * 1.1
                kd_dinamico = kd_base * 1.1
            else:
                kp_dinamico = kp_base * 1.5
                kd_dinamico = kd_base * 0.3

            derivada_cruda = error - error_anterior
            derivada = (derivada_cruda * 0.7) + (derivada_anterior * 0.3)
            
            correccion = (error * kp_dinamico) + (derivada * kd_base)

            tiempo_transcurrido = cronometro.time()
            if tiempo_transcurrido < tiempo_curva_s_ms:
                limite_potencia = potencia_min + (potencia_max - potencia_min) * (tiempo_transcurrido / tiempo_curva_s_ms)
            else:
                limite_potencia = potencia_max

            potencia_final = self.limitar(correccion, -limite_potencia, limite_potencia)
            
            # Si hay bloqueo, más agresivo
            if bloqueo_detectado:
                potencia_final = potencia_final * 1.5
                potencia_final = self.limitar(potencia_final, -limite_potencia, limite_potencia)
                
                if abs(potencia_final) < potencia_min * 0.5:
                    potencia_final = potencia_min * 0.5 if potencia_final > 0 else -potencia_min * 0.5
            
            # Aplicar potencia a los motores
            pot_izq = int(potencia_final)
            pot_der = int(-potencia_final)
            
            self.motor_izquierdo.dc(self.limitar(pot_izq, -100, 100))
            self.motor_derecho.dc(self.limitar(pot_der, -100, 100))

            error_anterior = error
            derivada_anterior = derivada
            wait(2)

        # Frenado final
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(20)

    def seguir_linea(
            self,
            sensor_color=None,
            velocidad_max=100,
            distancia_cm=70,
            lado="derecha",
            tiempo_acomodo_ms=140,
            tiempo_aceleracion_ms=120,
            kp=1.15,
            kd=2.6,
            k_freno=0.15,
            objetivo_reflexion=27,
            correccion_max=100,
            margen_cm=0,
            perfil_salida="encadenado",
            captura_inicial=True,
            tiempo_captura_ms=260,
            potencia_captura=55,
            kp_captura=2.4,
            margen_captura=5,
            lecturas_estables_captura=2
        ):
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
            multiplicador_lado = 1 if lado == "derecha" else -1

            self.reset_motores()

            # ==========================================
            # FASE 1: CAPTURA INICIAL DE LA LÍNEA
            # ==========================================
            if captura_inicial:
                reloj_captura = StopWatch()
                reloj_captura.reset()
                estables = 0

                while reloj_captura.time() < tiempo_captura_ms:
                    lectura = sensor_color.reflection()
                    error = lectura - objetivo_reflexion

                    if abs(error) <= margen_captura:
                        estables += 1
                        if estables >= lecturas_estables_captura:
                            break
                    else:
                        estables = 0

                    correction = error * kp_captura * multiplicador_lado
                    correction = self.limitar(correction, -correccion_max, correccion_max)

                    velocidad_base = 28 if abs(error) > 22 else potencia_captura

                    potencia_izq = velocidad_base - correction
                    potencia_der = velocidad_base + correction

                    self.motor_izquierdo.dc(self.limitar(potencia_izq, -100, 100))
                    self.motor_derecho.dc(self.limitar(potencia_der, -100, 100))
                    wait(2)

                self.motor_izquierdo.brake()
                self.motor_derecho.brake()
                wait(8)
                self.reset_motores()

            # ==========================================
            # FASE 2: SEGUIDOR ÉLITE DE ALTA VELOCIDAD
            # ==========================================
            cronometro = StopWatch()
            cronometro.reset()
            
            # 🔥 MODIFICACIÓN ÉLITE 1: Elevamos el piso de arranque de 55 a 75
            velocidad_minima = 75  
            last_error = 0
            last_derivative = 0

            while True:
                grados_actuales = self.distancia_promedio_grados()
                if grados_actuales >= grados_objetivo_real:
                    break

                tiempo_actual = cronometro.time()
                if tiempo_actual < tiempo_acomodo_ms:
                    velocidad_actual = velocidad_minima
                elif tiempo_actual < tiempo_acomodo_ms + tiempo_aceleracion_ms:
                    progreso = (tiempo_actual - tiempo_acomodo_ms) / tiempo_aceleracion_ms
                    velocidad_actual = velocidad_minima + ((velocidad_max - velocidad_minima) * progreso)
                else:
                    velocidad_actual = velocidad_max

                lectura = sensor_color.reflection()
                error = lectura - objetivo_reflexion
                derivative = ((error - last_error) * 0.82) + (last_derivative * 0.18)
                correction = ((error * kp) + (derivative * kd)) * multiplicador_lado
                correction = self.limitar(correction, -correccion_max, correccion_max)

                velocidad_base = velocidad_actual - (abs(error) * k_freno)
                
                # 🔥 MODIFICACIÓN ÉLITE 2: Jamás permitimos que la velocidad baje de 55 (antes 38)
                if velocidad_base < 55:
                    velocidad_base = 55

                potencia_izq = velocidad_base - correction
                potencia_der = velocidad_base + correction

                self.motor_izquierdo.dc(self.limitar(potencia_izq, -100, 100))
                self.motor_derecho.dc(self.limitar(potencia_der, -100, 100))

                last_error = error
                last_derivative = derivative
                wait(2)

            self.terminar_movimiento(perfil=perfil_salida, modo="brake")

    def mover_torque(self, grados_torque, velocidad_torque=180, esperar=True, modo_final=Stop.HOLD, retraso_inicial_ms=0):
            if retraso_inicial_ms > 0:
                wait(retraso_inicial_ms)
                
            self.motor_torque.run_angle(velocidad_torque, grados_torque, then=modo_final, wait=esperar)

    def mover_garra_delantera(self, velocidad, grados):
        self.motor_garra_delantera.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)

    def mover_garra_principal(self, velocidad, grados, esperar=True, potencia_apriete=60, tiempo_apriete_ms=120, apretar=True):
        if grados > 0:
            self.motor_garra.stop()
            wait(40)
            self.motor_garra.run_angle(velocidad, -abs(grados), then=Stop.BRAKE, wait=esperar)
        elif grados < 0:
            self.motor_garra.stop()
            wait(20)
            self.motor_garra.run_angle(velocidad, abs(grados), then=Stop.BRAKE, wait=True)
            if apretar:
                self.motor_garra.dc(potencia_apriete)
                wait(tiempo_apriete_ms)
                self.motor_garra.dc(potencia_apriete)
        else:
            return

    def giro_de_arco(
        self,
        radio_cm,
        angulo_deg,
        potencia_max=80,
        potencia_min=35,        # Potencia mínima para mantener movimiento suave
        lado="derecha",
        distancia_ruedas_cm=12.3, # Ajusta según tu robot real
        kp_gyro=2.8,            # Ganancia proporcional para corregir el error
        tolerancia_fin=1.5,     # Grados de tolerancia para considerar que el giro terminó
        perfil="encadenado"
    ):
        """
        Giro en arco con control de giroscopio para compensar resbalones.
        
        Args:
            radio_cm: Radio del arco en centímetros (positivo = arco a la derecha, 
                    negativo = arco a la izquierda)
            angulo_deg: Ángulo a girar en grados (positivo = horario, negativo = antihorario)
            potencia_max: Potencia máxima para el motor externo (0-100)
            potencia_min: Potencia mínima para mantener el movimiento
            lado: "derecha" o "izquierda" - determina qué rueda va por fuera del arco
            distancia_ruedas_cm: Distancia entre las ruedas del robot
            kp_gyro: Ganancia del controlador del giroscopio
            tolerancia_fin: Tolerancia en grados para finalizar el giro
            perfil: Perfil de finalización ("seguro", "encadenado", etc.)
        """
        if angulo_deg == 0 or radio_cm == 0:
            return

        # Preparamos el robot (motores y giroscopio)
        self.preparar_movimiento(reset_motores=False, reset_gyro=True, perfil=perfil)
        
        # Aseguramos que los motores estén listos
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(20)

        # ============================================================
        # PASO 1: CALCULAR LAS VELOCIDADES PARA EL ARCO
        # ============================================================
        pi = 3.1416
        
        # Distancia desde el centro de giro hasta cada rueda
        radio_interno = abs(radio_cm) - (distancia_ruedas_cm / 2)
        radio_externo = abs(radio_cm) + (distancia_ruedas_cm / 2)
        
        # Protección contra radio muy pequeño
        if radio_interno <= 0:
            print("⚠️ Radio demasiado pequeño, ajustando...")
            radio_interno = 2  # Valor mínimo seguro
        
        # Distancia que recorre cada rueda para el ángulo deseado
        distancia_interna = 2 * pi * radio_interno * (abs(angulo_deg) / 360)
        distancia_externa = 2 * pi * radio_externo * (abs(angulo_deg) / 360)
        
        # Relación de velocidades para que el robot describa el arco perfecto
        relacion = distancia_interna / distancia_externa
        
        # Ajustamos la potencia para que el motor externo trabaje a la potencia deseada
        potencia_externa = potencia_max
        potencia_interna = potencia_max * relacion
        
        # ============================================================
        # PASO 2: DETERMINAR QUÉ MOTOR VA MÁS RÁPIDO
        # ============================================================
        signo = 1 if angulo_deg > 0 else -1
        direccion = -1 if radio_cm > 0 else 1  # Si radio positivo = arco a derecha
        
        if (radio_cm > 0 and lado == "derecha") or (radio_cm < 0 and lado == "izquierda"):
            # El motor externo es el izquierdo (gira a la derecha)
            potencia_izq = potencia_externa * signo
            potencia_der = potencia_interna * signo
            motor_rapido = self.motor_izquierdo
            motor_lento = self.motor_derecho
        else:
            # El motor externo es el derecho (gira a la izquierda)
            potencia_izq = potencia_interna * signo
            potencia_der = potencia_externa * signo
            motor_rapido = self.motor_derecho
            motor_lento = self.motor_izquierdo
        
        # ============================================================
        # PASO 3: EJECUTAR EL GIRO CON CONTROL DE GIROSCOPIO
        # ============================================================
        heading_inicial = self.Hub.imu.heading()
        heading_objetivo = heading_inicial + angulo_deg
        
        # Variables de control para suavizar
        error_anterior = self._error_angular(heading_objetivo, heading_inicial)
        
        # Limitamos la potencia mínima para que el motor lento no se detenga
        potencia_interna = max(potencia_interna, potencia_min * 0.3)
        potencia_externa = max(potencia_externa, potencia_min)
        
        # Variables para monitoreo
        cronometro = StopWatch()
        cronometro.reset()
        
        while True:
            # Verificamos el ángulo actual con el giroscopio
            heading_actual = self.Hub.imu.heading()
            error_actual = self._error_angular(heading_objetivo, heading_actual)
            
            # Si llegamos al objetivo, salimos
            if abs(error_actual) <= tolerancia_fin:
                break
            
            # ========================================================
            # CONTROL PROPORCIONAL PARA CORREGIR DESVIACIONES
            # ========================================================
            correccion_gyro = error_actual * kp_gyro
            
            # Limitamos la corrección para que no sea demasiado agresiva
            correccion_gyro = self.limitar(correccion_gyro, -25, 25)
            
            # Aplicamos la corrección a las potencias base
            pot_izq_final = potencia_izq + correccion_gyro
            pot_der_final = potencia_der - correccion_gyro
            
            # ========================================================
            # ZONA DE FRENADO SUAVE (Rampa al final)
            # ========================================================
            # Si estamos cerca del objetivo, reducimos la velocidad suavemente
            if abs(error_actual) < 10:
                factor_freno = abs(error_actual) / 10
                pot_izq_final *= factor_freno
                pot_der_final *= factor_freno
                
                # Aseguramos que no bajemos de la potencia mínima
                pot_izq_final = max(pot_izq_final, potencia_min * signo * 0.5)
                pot_der_final = max(pot_der_final, potencia_min * signo * 0.5)
            
            # Limitamos las potencias finales
            pot_izq_final = self.limitar(pot_izq_final, -100, 100)
            pot_der_final = self.limitar(pot_der_final, -100, 100)
            
            # Aplicamos las potencias a los motores
            self.motor_izquierdo.dc(pot_izq_final)
            self.motor_derecho.dc(pot_der_final)
            
            # Actualizamos variables de control
            error_anterior = error_actual
            
            # Pequeña pausa para no saturar el bucle
            wait(2)
        
        # ============================================================
        # PASO 4: FRENADO CONTROLADO
        # ============================================================
        # Frenado en dos fases para evitar rebotes
        self.motor_izquierdo.brake()
        self.motor_derecho.brake()
        wait(40)
        
        # Hold para mantener la posición
        self.motor_izquierdo.hold()
        self.motor_derecho.hold()
        wait(20)
        
        # Finalización según el perfil solicitado
        self.terminar_movimiento(perfil=perfil, modo="hold", pausa=None)

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

#FUNCION DE PRUEBA PARA AVANZAR HASTA LA LINEA
    def avanzar_hasta_color(
            self,
            color_objetivo, 
            velocidad=300,
            kp_gyro=20.0,
            perfil="seguro"
        ):
            self.preparar_movimiento(reset_motores=False, reset_gyro=False, perfil=perfil)
            self.drive_base.reset()
            heading_objetivo = self.Hub.imu.heading()
            signo = 1 if velocidad > 0 else -1

            while True:
                # Leemos todos los datos del sensor de una vez
                color_actual = self.seguidor.color()
                hsv = self.seguidor.hsv()
                reflexion = self.seguidor.reflection()
                
                encontrado = False

                # ========================================================
                # LÓGICA INTELIGENTE DE DETECCIÓN DEPENDIENDO DEL COLOR
                # ========================================================
                if color_objetivo == Color.BLUE:
                    # Si buscamos azul: Alta saturación (>70)
                    if hsv.s > 70:
                        encontrado = True

                elif color_objetivo == Color.BLACK:
                    # Si buscamos la línea negra: Baja saturación (<30) y Baja reflexión (<15)
                    # Esto evita que confunda el azul oscuro con el negro
                    if hsv.s < 30 and reflexion < 15:
                        encontrado = True
                
                else:
                    # Para cualquier otro color (Rojo, Amarillo, Verde, etc.)
                    # Usamos la detección normal de Pybricks
                    if color_actual == color_objetivo:
                        encontrado = True

                # Si la lógica determinó que ya encontramos el color, rompemos el bucle
                if encontrado:
                    break
                    
                # Mantenimiento del rumbo recto perfecto con el giroscopio
                actual_heading = self.Hub.imu.heading()
                error_gyro = self._error_angular(heading_objetivo, actual_heading)
                self.drive_base.drive(abs(velocidad) * signo, error_gyro * kp_gyro)

            # Frenado exacto y seco
            self.drive_base.stop()
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)

    def avanzar_hasta_color(
            self,
            color_objetivo, 
            velocidad=300,
            kp_gyro=20.0,
            cruces=1,          # 🔥 NUEVO PARÁMETRO: Cantidad de líneas a cruzar
            perfil="seguro"
        ):
            self.preparar_movimiento(reset_motores=False, reset_gyro=False, perfil=perfil)
            self.drive_base.reset()
            heading_objetivo = self.Hub.imu.heading()
            signo = 1 if velocidad > 0 else -1

            conteo_cruces = 0
            viendo_color = False # Bandera para saber si estamos PARADOS sobre el color

            while True:
                # Leemos todos los datos del sensor
                color_actual = self.seguidor.color()
                hsv = self.seguidor.hsv()
                reflexion = self.seguidor.reflection()
                
                es_color_objetivo = False

                # ========================================================
                # 1. VERIFICAMOS SI ESTAMOS SOBRE EL COLOR
                # ========================================================
                if color_objetivo == Color.BLUE:
                    if hsv.s > 70:
                        es_color_objetivo = True

                elif color_objetivo == Color.BLACK:
                    if hsv.s < 30 and reflexion < 15:
                        es_color_objetivo = True
                
                else:
                    if color_actual == color_objetivo:
                        es_color_objetivo = True

                # ========================================================
                # 2. LÓGICA DE CONTEO INTELIGENTE (DETECCIÓN DE FLANCO)
                # ========================================================
                if es_color_objetivo:
                    # Si vemos el color, pero ANTES NO lo estábamos viendo, es una línea nueva
                    if not viendo_color:
                        viendo_color = True
                        conteo_cruces += 1
                        
                        # Si ya llegamos al número de cruces que pediste, ¡Rompemos y frenamos!
                        if conteo_cruces >= cruces:
                            break
                else:
                    # Si dejamos de ver el color (estamos en blanco/gris), reseteamos la bandera
                    viendo_color = False
                    
                # Mantenimiento del rumbo recto perfecto con el giroscopio
                actual_heading = self.Hub.imu.heading()
                error_gyro = self._error_angular(heading_objetivo, actual_heading)
                self.drive_base.drive(abs(velocidad) * signo, error_gyro * kp_gyro)

            # Frenado exacto y seco
            self.drive_base.stop()
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)
                
    def seguir_linea_hasta_color(
            self,
            color_objetivo,
            sensor_color=None,
            velocidad_max=100,
            lado="derecha",
            tiempo_acomodo_ms=140,
            tiempo_aceleracion_ms=120,
            kp=1.15,
            kd=2.6,
            k_freno=0.15,
            objetivo_reflexion=27,
            correccion_max=100,
            perfil_salida="encadenado",
            captura_inicial=True,
            tiempo_captura_ms=260,
            potencia_captura=55,
            kp_captura=2.4,
            margen_captura=5,
            lecturas_estables_captura=2
        ):
            """
            Sigue la línea de forma indefinida usando el control PD élite 
            hasta que el mismo sensor detecta el color_objetivo (usando filtros HSV).
            Aplica un freno de contramarcha instantáneo al detectar el color para anular inercia.
            """
            if sensor_color is None:
                sensor_color = self.seguidor

            multiplicador_lado = 1 if lado == "derecha" else -1
            self.reset_motores()

            # ==========================================
            # FASE 1: CAPTURA INICIAL DE LA LÍNEA
            # ==========================================
            if captura_inicial:
                reloj_captura = StopWatch()
                reloj_captura.reset()
                estables = 0

                while reloj_captura.time() < tiempo_captura_ms:
                    lectura = sensor_color.reflection()
                    error = lectura - objetivo_reflexion

                    if abs(error) <= margen_captura:
                        estables += 1
                        if estables >= lecturas_estables_captura:
                            break
                    else:
                        estables = 0

                    correction = error * kp_captura * multiplicador_lado
                    correction = self.limitar(correction, -correccion_max, correccion_max)

                    velocidad_base = 28 if abs(error) > 22 else potencia_captura

                    potencia_izq = velocidad_base - correction
                    potencia_der = velocidad_base + correction

                    self.motor_izquierdo.dc(self.limitar(potencia_izq, -100, 100))
                    self.motor_derecho.dc(self.limitar(potencia_der, -100, 100))
                    wait(2)

                self.motor_izquierdo.brake()
                self.motor_derecho.brake()
                wait(8)
                self.reset_motores()

            # ==========================================
            # FASE 2: SEGUIDOR INDEFINIDO HASTA COLOR
            # ==========================================
            cronometro = StopWatch()
            cronometro.reset()
            
            velocidad_minima = 75  
            last_error = 0
            last_derivative = 0

            while True:
                # =======================================================
                # LÓGICA DE CONDICIÓN DE PARO (ESCUDO HSV)
                # =======================================================
                color_actual = sensor_color.color()
                hsv = sensor_color.hsv()
                reflexion = sensor_color.reflection()
                
                encontrado = False

                if color_objetivo == Color.BLUE:
                    # Si buscas azul: Tu lona da ~90% de saturación. El negro da <20%.
                    if hsv.s > 70:
                        encontrado = True
                elif color_objetivo == Color.BLACK:
                    # Si buscas una línea negra de cruce
                    if hsv.s < 30 and reflexion < 15:
                        encontrado = True
                else:
                    # Para otros colores del mapa (Verde, Rojo, Amarillo)
                    if color_actual == color_objetivo:
                        encontrado = True

                # =========================================================
                # 🔥 FRENO ÉLITE DE CONTRAMARCHA (REVERSE THRUST) 🔥
                # =========================================================
                if encontrado:
                    # 1. Inyectamos reversa absoluta para matar la energía cinética
                    self.motor_izquierdo.dc(-100)
                    self.motor_derecho.dc(-100)
                    
                    # Mantenemos el choque eléctrico por 30 milisegundos.
                    wait(30) 
                    
                    # 2. Con la inercia en cero, clavamos los motores en posición
                    self.motor_izquierdo.hold()
                    self.motor_derecho.hold()
                    wait(20) # Breve pausa para asentar el golpe mecánico
                    break

                # ─── LÓGICA DE CONTROL DE VELOCIDAD POR TIEMPO ───
                tiempo_actual = cronometro.time()
                if tiempo_actual < tiempo_acomodo_ms:
                    velocidad_actual = velocidad_minima
                elif tiempo_actual < tiempo_acomodo_ms + tiempo_aceleracion_ms:
                    progreso = (tiempo_actual - tiempo_acomodo_ms) / tiempo_aceleracion_ms
                    velocidad_actual = velocidad_minima + ((velocidad_max - velocidad_minima) * progreso)
                else:
                    velocidad_actual = velocidad_max

                # ─── SEGUIDOR DE LÍNEA PD TRADICIONAL ───
                lectura = sensor_color.reflection()
                error = lectura - objetivo_reflexion
                derivative = ((error - last_error) * 0.82) + (last_derivative * 0.18)
                correction = ((error * kp) + (derivative * kd)) * multiplicador_lado
                correction = self.limitar(correction, -correccion_max, correccion_max)

                velocidad_base = velocidad_actual - (abs(error) * k_freno)
                
                if velocidad_base < 55:
                    velocidad_base = 55

                potencia_izq = velocidad_base - correction
                potencia_der = velocidad_base + correction

                self.motor_izquierdo.dc(self.limitar(potencia_izq, -100, 100))
                self.motor_derecho.dc(self.limitar(potencia_der, -100, 100))

                last_error = error
                last_derivative = derivative
                wait(2)

    def avanzar_cruzando_lineas(
            self,
            cruces_objetivo=1,
            velocidad=300,
            escape_inicial_cm=0,   
            margen_linea_cm=3.5,   
            kp_gyro=20.0,
            perfil="seguro",
            retraso_freno_ms=0     # 🔥 NUEVO PARÁMETRO: Tiempo extra antes de frenar
        ):
            """
            Avanza recto y cuenta intersecciones de líneas negras usando odometría para 
            ignorar el grosor de las líneas y evitar conteos falsos por basura en el tapete.
            Permite agregar un retraso en milisegundos para frenar un poco después de la línea.
            """
            self.preparar_movimiento(reset_motores=False, reset_gyro=False, perfil=perfil)
            self.drive_base.reset()
            heading_objetivo = self.Hub.imu.heading()
            signo = 1 if velocidad > 0 else -1

            conteo_cruces = 0
            
            distancia_desbloqueo_mm = escape_inicial_cm * 10 

            while True:
                distancia_actual_mm = abs(self.drive_base.distance())

                # Mantenimiento del rumbo recto perfecto con el giroscopio
                actual_heading = self.Hub.imu.heading()
                error_gyro = self._error_angular(heading_objetivo, actual_heading)
                self.drive_base.drive(abs(velocidad) * signo, error_gyro * kp_gyro)

                # ========================================================
                # ESCUDO FÍSICO (VENTANA CIEGA)
                # ========================================================
                if distancia_actual_mm < distancia_desbloqueo_mm:
                    continue 
                
                hsv = self.seguidor.hsv()
                reflexion = self.seguidor.reflection()
                
                es_linea_negra = (hsv.s < 30 and reflexion < 18)

                if es_linea_negra:
                    conteo_cruces += 1
                    
                    if conteo_cruces >= cruces_objetivo:
                        # =========================================================
                        # 🔥 LÓGICA DE RETRASO DE FRENO (SOBREPASAR LA LÍNEA)
                        # =========================================================
                        if retraso_freno_ms > 0:
                            reloj_extra = StopWatch()
                            reloj_extra.reset()
                            # Mini-bucle para seguir avanzando recto el tiempo indicado
                            while reloj_extra.time() < retraso_freno_ms:
                                actual_heading_extra = self.Hub.imu.heading()
                                error_gyro_extra = self._error_angular(heading_objetivo, actual_heading_extra)
                                self.drive_base.drive(abs(velocidad) * signo, error_gyro_extra * kp_gyro)
                                
                        break # ¡Terminó el tiempo extra, rompemos para frenar!
                    else:
                        distancia_desbloqueo_mm = distancia_actual_mm + (margen_linea_cm * 10)

            # =======================================================
            # 🔥 FRENADO DE DOS FASES (Evita el rebote a altas velocidades)
            # =======================================================
            self.drive_base.stop()
            
            # Fase 1: Freno pasivo para matar inercia suavemente
            self.motor_izquierdo.brake()
            self.motor_derecho.brake()
            wait(60)
            
            # Fase 2: Clavamos el motor
            self.motor_izquierdo.hold()
            self.motor_derecho.hold()
            wait(20)

            # =========================
    # DETECCIÓN DE MATRIZ
    # =========================

    def matriz(self):
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
            if mayor < 1:
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