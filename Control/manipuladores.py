from pybricks.parameters import Stop
from pybricks.tools import wait, StopWatch

class Manipuladores:
    def mover_torque(self, grados_torque, velocidad_torque=180, esperar=True, modo_final=Stop.HOLD):
        self.motor_torque.run_angle(velocidad_torque, grados_torque, then=modo_final, wait=esperar)

    def esperar_torque_hasta(self, grados_relativos, timeout_ms=700):
        inicio = self.motor_torque.angle(); obj = abs(grados_relativos); reloj = StopWatch()
        while abs(self.motor_torque.angle() - inicio) < obj and reloj.time() < timeout_ms: wait(3)

    def mover_garra(self, velocidad, grados):
        self.motor_garra.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)

    def agarrar(self, velocidad, grados):
        self.motor_garra_delantera.run_angle(velocidad, grados, then=Stop.HOLD, wait=True)

    def avanzar_con_torque(self,distancia_cm,grados_torque,velocidad_robot=950,velocidad_torque=180,
        torque_despues_cm=3,kp=2.1,kd=2.9,correccion_max=130,velocidad_min=380,esperar_torque=False,
        levantar_final_grados=0,perfil_entrada="seguro",perfil_salida="encadenado"):
        self.preparar_movimiento(reset_motores=True,reset_gyro=True,perfil=perfil_entrada)
        distancia_mm = abs(distancia_cm) * 10; grados_objetivo = distancia_mm * self.grados_por_mm
        torque_despues_mm = abs(torque_despues_cm) * 10; grados_inicio_torque = torque_despues_mm * self.grados_por_mm
        signo = 1 if distancia_cm > 0 else -1; error_anterior = 0; reloj = StopWatch(); reloj.reset()
        velocidad_actual = velocidad_min; rampa = 40; torque_activado = False
        while self.distancia_promedio_grados() < grados_objetivo:
            recorrido = self.distancia_promedio_grados(); restante = grados_objetivo - recorrido
            if not torque_activado and recorrido >= grados_inicio_torque:
                self.motor_torque.run_angle(velocidad_torque,grados_torque,then=Stop.HOLD,wait=False)
                torque_activado = True
            if velocidad_actual < velocidad_robot:
                velocidad_actual += rampa
                if velocidad_actual > velocidad_robot: 
                    velocidad_actual = velocidad_robot
            if restante < 170:
                velocidad_actual = max(velocidad_min,int(velocidad_robot * restante / 170))
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
        self.terminar_movimiento(perfil=perfil_salida,modo="brake")
        if not torque_activado and grados_torque != 0:
            self.motor_torque.run_angle(velocidad_torque,grados_torque,then=Stop.HOLD,wait=False)
            torque_activado = True
        if esperar_torque and torque_activado:
            while self.motor_torque.control.done() == False: wait(5)
        if levantar_final_grados != 0:
            if torque_activado:
                while self.motor_torque.control.done() == False: wait(5)

            self.motor_torque.run_angle(velocidad_torque,levantar_final_grados,then=Stop.HOLD,wait=True)
