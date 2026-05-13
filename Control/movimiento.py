from pybricks.tools import wait, StopWatch
from pybricks.parameters import Stop

class Movimiento:
    def avanzar(self,distancia_cm,velocidad=950,kp=2.1,kd=2.9,correccion_max=130,velocidad_min=380,perfil="seguro"):
        self.preparar_movimiento(reset_motores=True,reset_gyro=True,perfil=perfil)
        distancia_mm = abs(distancia_cm) * 10; grados_objetivo = distancia_mm * self.grados_por_mm
        signo = 1 if distancia_cm > 0 else -1; error_anterior = 0; reloj = StopWatch(); reloj.reset()
        velocidad_actual = velocidad_min; rampa = 40
        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados(); restante = grados_objetivo - recorrido
            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad
            if restante < 170: velocidad_actual = max(velocidad_min,int(velocidad * restante / 170))
            dt = reloj.time() / 1000
            if dt <= 0: dt = 0.001
            error = self.Hub.imu.heading()
            if abs(error) < 0.7: error = 0
            derivada = (error - error_anterior) / dt; correccion = (error * kp) + (derivada * kd)
            correccion = self.limitar(correccion,-correccion_max,correccion_max); base = velocidad_actual * signo
            if signo > 0:
                pot_izq = int(base - correccion); pot_der = int(base + correccion)
            else:
                pot_izq = int(base + correccion); pot_der = int(base - correccion)
            pot_izq = self.limitar(pot_izq, -1000, 1000); pot_der = self.limitar(pot_der, -1000, 1000)
            self.motor_izquierdo.run(pot_izq); self.motor_derecho.run(pot_der)
            error_anterior = error; reloj.reset(); wait(2)
        self.terminar_movimiento(perfil=perfil,modo="brake")

    def retroceder(self,distancia_cm,velocidad=950,kp=2.1,kd=2.9,correccion_max=130,velocidad_min=380,
        perfil="seguro",invertir_correccion=False,pausa_gyro=None):
        self.preparar_movimiento(reset_motores=True,reset_gyro=True,perfil=perfil,pausa=pausa_gyro)
        distancia_mm = abs(distancia_cm) * 10; grados_objetivo = distancia_mm * self.grados_por_mm
        error_anterior = 0; reloj = StopWatch(); reloj.reset(); velocidad_actual = velocidad_min; rampa = 35
        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados(); restante = grados_objetivo - recorrido
            if velocidad_actual < velocidad:
                velocidad_actual += rampa
                if velocidad_actual > velocidad:
                    velocidad_actual = velocidad
            if restante < 170: velocidad_actual = max(velocidad_min,int(velocidad * restante / 170))
            dt = reloj.time() / 1000
            if dt <= 0: dt = 0.001
            error = self.Hub.imu.heading()
            if abs(error) < 0.7: error = 0
            derivada = (error - error_anterior) / dt; correccion = (error * kp) + (derivada * kd)
            correccion = self.limitar(correccion, -correccion_max, correccion_max); base = -velocidad_actual
            if not invertir_correccion:
                pot_izq = int(base - correccion); pot_der = int(base + correccion)
            else:
                pot_izq = int(base + correccion); pot_der = int(base - correccion)
            pot_izq = self.limitar(pot_izq, -1000, 1000); pot_der = self.limitar(pot_der, -1000, 1000)
            self.motor_izquierdo.run(pot_izq); self.motor_derecho.run(pot_der)
            error_anterior = error; reloj.reset(); wait(2)
        self.terminar_movimiento(perfil=perfil, modo="brake")