from pybricks.tools import wait

class Giros:
    def girar(self,angulo_deg, velocidad=950,velocidad_min=220,anticipacion=9,zona_freno=22,perfil="seguro"):
        self.preparar_movimiento(reset_motores=False, reset_gyro=True, perfil=perfil)
        objetivo = abs(angulo_deg); objetivo_corte = max(0, objetivo - anticipacion)
        signo = 1 if angulo_deg > 0 else -1
        while True:
            actual = abs(self.Hub.imu.heading())
            if actual >= objetivo_corte: break
            restante = objetivo_corte - actual
            if restante > zona_freno: vel = velocidad
            else: vel = max(velocidad_min, int(velocidad * restante / zona_freno))
            pot_izq = vel * signo; pot_der = -vel * signo
            pot_izq = self.limitar(pot_izq, -1000, 1000); pot_der = self.limitar(pot_der, -1000, 1000)
            self.motor_izquierdo.run(pot_izq); self.motor_derecho.run(pot_der); wait(1)
        self.terminar_movimiento(perfil=perfil,modo="brake")

    def _giro_un_motor(self,motor_activo,motor_fijo,angulo_deg,sentido_motor,velocidad=1000,velocidad_min=260,
        anticipacion=12,zona_freno=28,perfil="seguro"):
        self.preparar_movimiento(reset_motores=False,reset_gyro=True,perfil=perfil)
        objetivo = abs(angulo_deg); objetivo_corte = max(0, objetivo - anticipacion)
        signo = 1 if angulo_deg > 0 else -1; motor_fijo.brake(); wait(2)
        while True:
            actual = abs(self.Hub.imu.heading())
            if actual >= objetivo_corte: break
            restante = objetivo_corte - actual
            if restante > zona_freno: vel = velocidad
            else:
                vel = max(velocidad_min, int(velocidad * restante / zona_freno))
            potencia = vel * signo * sentido_motor; potencia = self.limitar(potencia, -1000, 1000)
            motor_activo.run(potencia); wait(1)
        motor_activo.brake(); motor_fijo.brake()
        if perfil == "encadenado":wait(8)
        else: wait(22)
        motor_activo.stop(); motor_fijo.stop(); wait(2)

    def giro_izquierda(self,angulo_deg,velocidad=1000,velocidad_min=260,anticipacion=12,zona_freno=28,perfil="seguro"):
        self._giro_un_motor(motor_activo=self.motor_izquierdo, motor_fijo=self.motor_derecho,angulo_deg=angulo_deg,
            sentido_motor=1,velocidad=velocidad,velocidad_min=velocidad_min,anticipacion=anticipacion,
            zona_freno=zona_freno,perfil=perfil)

    def giro_derecha(self,angulo_deg,velocidad=1000,velocidad_min=260,anticipacion=12,zona_freno=28,perfil="seguro"):
        self._giro_un_motor(motor_activo=self.motor_derecho, motor_fijo=self.motor_izquierdo, angulo_deg=angulo_deg,
            sentido_motor=-1, velocidad=velocidad,velocidad_min=velocidad_min, anticipacion=anticipacion,
            zona_freno=zona_freno, perfil=perfil)
    
    def arcgirar(self, radio_cm,angulo_deg,potencia=80,lado="derecha",distancia_ruedas_cm=12):
        pi = 3.1416; radio_interno = radio_cm - (distancia_ruedas_cm / 2); radio_externo = radio_cm + (distancia_ruedas_cm / 2)
        if radio_interno <= 0: return
        distancia_interna = (2 * pi * radio_interno * (abs(angulo_deg) / 360))
        distancia_externa = (2 * pi * radio_externo * (abs(angulo_deg) / 360))
        relacion = distancia_interna / distancia_externa; potencia_externa = potencia; potencia_interna = potencia * relacion
        potencia_externa = max(-100, min(100, potencia_externa)); potencia_interna = max(-100, min(100, potencia_interna))
        self.reset_motores(); grados_objetivo_externo = (distancia_externa * 10 * self.grados_por_mm)
        signo = 1 if angulo_deg > 0 else -1
        if lado == "derecha":
            pot_izq = potencia_externa * signo; pot_der = potencia_interna * signo; motor_externo = self.motor_izquierdo
        else:
            pot_izq = potencia_interna * signo; pot_der = potencia_externa * signo; motor_externo = self.motor_derecho
        while abs(motor_externo.angle()) < grados_objetivo_externo:
            self.motor_izquierdo.dc(pot_izq); self.motor_derecho.dc(pot_der); wait(5)
        self.frenar()
