from pybricks.tools import wait, StopWatch

class Linea:

    def avanzar_hasta_n_lineas_negras(self,cantidad_lineas,velocidad=500,umbral_negro=20,umbral_salida=28,perfil="seguro"):
        self.preparar_movimiento(reset_motores=True, reset_gyro=False,perfil=perfil)
        contador_lineas = 0; en_negro = False
        while contador_lineas < cantidad_lineas:
            lectura = self.seguidor.reflection()
            if lectura <= umbral_negro and not en_negro: contador_lineas += 1; en_negro = True
            elif lectura >= umbral_salida: en_negro = False
            self.motor_izquierdo.run(velocidad); self.motor_derecho.run(velocidad); wait(5)

        self.terminar_movimiento(perfil=perfil, modo="brake")

    def mover_hasta_linea(self, distancia_cm_max, velocidad=750, umbral_negro=20,umbral_salida=28, distancia_minima_cm=0, lineas_a_ignorar=0,
        kp=2.0, kd=2.8, correccion_max=120, perfil="seguro", lecturas_negras_necesarias=2, lecturas_claras_necesarias=3):
        self.preparar_movimiento(reset_motores=True, reset_gyro=True, perfil=perfil)
        signo = 1 if distancia_cm_max > 0 else -1; distancia_mm = abs(distancia_cm_max) * 10
        grados_maximos = distancia_mm * self.grados_por_mm; distancia_minima_mm = abs(distancia_minima_cm) * 10
        grados_minimos = distancia_minima_mm * self.grados_por_mm; contador_lineas = 0
        lectura_inicial = self.seguidor.reflection(); en_negro = lectura_inicial <= umbral_negro
        conteo_negro = 0; conteo_claro = 0; error_anterior = 0; reloj = StopWatch(); reloj.reset()
        while self.distancia_promedio_grados() < grados_maximos:
            recorrido = self.distancia_promedio_grados(); lectura = self.seguidor.reflection()
            if recorrido >= grados_minimos:
                if lectura <= umbral_negro: 
                    conteo_negro += 1; conteo_claro = 0
                    if conteo_negro >= lecturas_negras_necesarias and not en_negro:
                        en_negro = True; contador_lineas += 1
                        if contador_lineas > lineas_a_ignorar:
                            self.terminar_movimiento(perfil=perfil,modo="brake"); return True
                elif lectura >= umbral_salida:
                    conteo_claro += 1;conteo_negro = 0;
                    if conteo_claro >= lecturas_claras_necesarias: en_negro = False
            dt = reloj.time() / 1000
            if dt <= 0: dt = 0.001
            error = self.Hub.imu.heading()
            if abs(error) < 0.7: error = 0
            derivada = (error - error_anterior) / dt; correccion = (error * kp) + (derivada * kd)
            correccion = self.limitar(correccion, -correccion_max,correccion_max); base = velocidad * signo
            if signo > 0: pot_izq = int(base - correccion); pot_der = int(base + correccion)
            else: pot_izq = int(base + correccion); pot_der = int(base - correccion)
            pot_izq = self.limitar(pot_izq, -1000, 1000); pot_der = self.limitar(pot_der, -1000, 1000)
            self.motor_izquierdo.run(pot_izq); self.motor_derecho.run(pot_der)
            error_anterior = error; reloj.reset(); wait(3)
        self.terminar_movimiento(perfil=perfil,modo="brake")
        return False

    def leer_reflexion_promedio(self,sensor=None,muestras=5,pausa_ms=3):
        total = 0
        for _ in range(muestras):total += sensor.reflection(); wait(pausa_ms)
        return total / muestras

    def sobre_negro_estable(self, sensor=None,umbral_negro=20,muestras=3,pausa_ms=3):
        conteo_negro = 0
        for _ in range(muestras): 
            if sensor.reflection() <= umbral_negro:conteo_negro += 1
            wait(pausa_ms)
        return conteo_negro >= muestras

    def esperar_salida_negro(self,sensor=None,umbral_salida=28, timeout_ms=600):
        reloj = StopWatch(); reloj.reset()
        while reloj.time() < timeout_ms: 
            if sensor.reflection() >= umbral_salida: return True
            wait(3)
        return False

    def acomodar_borde_linea(self, direccion=1,velocidad=180,objetivo_reflexion=27,margen=3,timeout_ms=450,perfil_salida="encadenado"):
        reloj = StopWatch(); reloj.reset()
        while reloj.time() < timeout_ms:
            lectura = self.seguidor.reflection()
            if objetivo_reflexion - margen <= lectura <= objetivo_reflexion + margen:break
            self.motor_izquierdo.run(velocidad * direccion); self.motor_derecho.run(velocidad * direccion); wait(4)
        self.terminar_movimiento(perfil=perfil_salida,modo="brake")

    def seguir_linea_extremo(self, sensor_color=None, velocidad_max=100, distancia_cm=0, lado="derecha", tiempo_acomodo_ms=180,
        tiempo_aceleracion_ms=70, kp=0.82, kd=1.85, k_freno=0.01, objetivo_reflexion=27, correccion_max=95,
        margen_cm=0, perfil_salida="encadenado"):
        diametro_rueda_cm = self.diametro_rueda / 10; circunferencia_cm = 3.14159 * diametro_rueda_cm
        grados_objetivo = (distancia_cm / circunferencia_cm) * 360
        if margen_cm > 0: grados_margen = (margen_cm / circunferencia_cm) * 360
        else: grados_margen = 0; grados_objetivo_real = max(0, grados_objetivo - grados_margen)
        self.reset_motores(); cronometro = StopWatch(); cronometro.reset(); velocidad_minima = 45
        last_error = 0; last_derivative = 0
        if lado == "derecha": multiplicador_lado = 1
        else: multiplicador_lado = -1
        while True:
            grados_actuales = self.distancia_promedio_grados()
            if grados_actuales >= grados_objetivo_real: break
            tiempo_actual = cronometro.time()
            if tiempo_actual < tiempo_acomodo_ms: velocidad_actual = velocidad_minima
            elif tiempo_actual < tiempo_acomodo_ms + tiempo_aceleracion_ms:
                progreso = (tiempo_actual - tiempo_acomodo_ms) / tiempo_aceleracion_ms
                velocidad_actual = velocidad_minima + ((velocidad_max - velocidad_minima) * progreso)
            else:velocidad_actual = velocidad_max
            lectura = sensor_color.reflection(); error = lectura - objetivo_reflexion
            derivative = ((error - last_error) * 0.82)+(last_derivative * 0.18)
            correction = ((error * kp) +(derivative * kd)) * multiplicador_lado
            correction = self.limitar(correction, -correccion_max,correccion_max)
            velocidad_base = velocidad_actual - (abs(error) * k_freno)
            potencia_izq = velocidad_base - correction; potencia_der = velocidad_base + correction
            potencia_izq = self.limitar(potencia_izq, -100, 100); potencia_der = self.limitar(potencia_der, -100, 100)
            self.motor_izquierdo.dc(potencia_izq); self.motor_derecho.dc(potencia_der)
            last_error = error; last_derivative = derivative; wait(2)
        self.terminar_movimiento(perfil=perfil_salida,modo="brake")