from robot_control_rapidez import Base
from pybricks.hubs import PrimeHub

hub = PrimeHub()

print("Voltaje:", hub.battery.voltage(), "mV")

robot = Base()
print("Ejecutando recorrido de matriz 2")
'''

robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=32, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.esperar(300)
robot.girar(-77, velocidad=700, velocidad_min=650, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.mover_garra(300, 90, esperar=False)
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=7, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.mover_recto(distancia_cm=14, velocidad=900, perfil="encadenado")
robot.mover_garra_delantera(600, 290)
robot.esperar(200)

robot.retroceder(distancia_cm=22, velocidad=600, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(200)
robot.girar(-83, velocidad=700, velocidad_min=650, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=70, distancia_cm=12, lado="izquierda", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.esperar(200)
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.mover_garra_delantera(600, -25)
robot.esperar(300)
robot.mover_garra(300, -49, esperar=False, apretar=False)
robot.esperar(300)

robot.mover_recto(distancia_cm=14, velocidad=700, perfil="encadenado")
robot.mover_garra_delantera(600, 15)
robot.mover_garra(300, -31, esperar=False, apretar=80)
robot.retroceder(distancia_cm=14, velocidad=550, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.esperar(500)
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")

robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=80, distancia_cm=16, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.esperar(200)
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=60, distancia_cm=10, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

robot.mover_garra(300, 80, esperar=False)
robot.mover_garra_delantera(600, -90)
robot.retroceder(distancia_cm=13, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.mover_garra_delantera(600, 95)
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=80, distancia_cm=13, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.mover_garra(500, -50, esperar=False, potencia_apriete=100)
robot.mover_garra_delantera(600, -150)
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=7, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

robot.mover_recto(distancia_cm=27, velocidad=650, perfil="encadenado")
robot.mover_garra_delantera(400, 100)
robot.mover_garra_rapida(potencia=100, grados=20, abrir=True)
'''

robot.mover_garra_delantera(400, -100)
robot.retroceder(distancia_cm=13, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.girar(180, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=100, distancia_cm=16, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.girar(-80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.mover_recto(distancia_cm=2, velocidad=650, perfil="encadenado")
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=12, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")

robot.mover_garra(300, 90, esperar=False)
robot.mover_recto(distancia_cm=19, velocidad=650, perfil="encadenado")
robot.mover_garra_delantera(400,180)
robot.retroceder(distancia_cm=26, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.girar(-80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=16, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")

robot.mover_recto(distancia_cm=10, velocidad=650, perfil="encadenado")
robot.mover_garra_delantera(400,-10)
robot.mover_garra(300, -120, esperar=False)
robot.retroceder(distancia_cm=10, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.girar(-80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.mover_garra(300, 120, esperar=False)
robot.retroceder(distancia_cm=2, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)
robot.girar(80, velocidad=650, velocidad_min=600, kp=5.0, tolerancia=0.5, perfil="encadenado")
robot.seguir_linea_extremo(sensor_color=robot.seguidor, velocidad_max=50, distancia_cm=16, lado="derecha", tiempo_acomodo_ms=140, tiempo_aceleracion_ms=140, kp=1.25, kd=2.7, k_freno=0.16, correccion_max=100, objetivo_reflexion=27, captura_inicial=True, tiempo_captura_ms=280, potencia_captura=60, kp_captura=2.5, perfil_salida="encadenado")
robot.mover_recto(distancia_cm=19, velocidad=650, perfil="encadenado")
robot.mover_garra_delantera(400,10)
robot.mover_garra(300, -120, esperar=False)  
robot.retroceder(distancia_cm=27, velocidad=400, perfil="seguro", invertir_correccion=False, pausa_gyro=25)


