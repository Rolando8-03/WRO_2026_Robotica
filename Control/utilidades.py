from pybricks.tools import wait

class Utilidades:
    def limitar(self, valor, minimo, maximo): return max(minimo, min(maximo, valor))

    def reset_imu(self): self.Hub.imu.reset_heading(0); wait(20)

    def reset_motores(self): self.motor_izquierdo.reset_angle(0); self.motor_derecho.reset_angle(0)

    def distancia_promedio_grados(self): return (abs(self.motor_izquierdo.angle()) + abs(self.motor_derecho.angle())) / 2

    def esperar(self, ms): wait(ms)

    def frenar(self): self.motor_izquierdo.brake(); self.motor_derecho.brake(); wait(3)

    def preparar_movimiento(self, reset_motores=True, reset_gyro=True, perfil="seguro", pausa=None):
        pausa_gyro = pausa if pausa else (18 if perfil == "seguro" else 7)
        self.motor_izquierdo.brake(); self.motor_derecho.brake(); wait(8)
        if reset_motores: self.reset_motores()
        if reset_gyro: self.Hub.imu.reset_heading(0); wait(pausa_gyro)

    def terminar_movimiento(self, perfil="seguro", modo="brake", pausa=None, soltar=True):
        if modo == "brake": self.motor_izquierdo.brake(); self.motor_derecho.brake()
        elif modo == "hold": self.motor_izquierdo.hold(); self.motor_derecho.hold()
        elif modo == "stop": self.motor_izquierdo.stop(); self.motor_derecho.stop()
        
        wait(pausa if pausa else (18 if perfil == "seguro" else 6))
        if soltar and modo == "brake":
            self.motor_izquierdo.stop(); self.motor_derecho.stop(); wait(2)