from robot_control import Base

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())

# ===================== SECCIÓN 1 =====================

robot.giro_izquierda(45, 620)
robot.mover_recto(12, 900)
robot.giro_izquierda(45, 620)
robot.mover_recto(10, 900)
robot.esperar(10)
#En este punto ya está acomodado para buscar la línea

# ===================== SECCIÓN 2 (CEMENTO) =====================
robot.seguir_linea(distancia_cm=60, velocidad=1000, ref=30)
robot.girar(-90, 450)
robot.esperar(10)
robot.avanzar_con_torque(-19, 160, 700, 140)
robot.esperar(10)
robot.mover_recto(1.5,500)
robot.girar(80)
robot.retroceder_recto(40, 650)
#Aqui ya dejó la paleta de albañilería

# ===================== TRANSICIÓN =====================
robot.mover_recto(30.5, 900)
robot.giro_derecha(-41, 620)
robot.giro_izquierda(53, 620)
robot.seguir_linea(distancia_cm=37, velocidad=1000, ref=30)
#Aqui ya llegó al lugar de estacionamiento

# ===================== ACCIÓN =====================
robot.esperar(10)
robot.girar(91, 500)
robot.mover_torque(-170, 1000)
robot.retroceder_recto(10, 650) #empujar el cemento
#Aqui ya dejó el cemento en el lugar de estacionamiento

# ===================== SECCIÓN FINAL =====================
robot.mover_recto(13.2, 900)
robot.girar(-89.5, 450)
robot.mover_recto(6,900)
robot.seguir_linea(distancia_cm=9, velocidad=1000, ref=30)
robot.girar(-179, 500)
robot.avanzar_con_torque(-22, 165, 750, 300)
#Aqui agarra los cementos blancos

# ===================== SALIDA =====================
robot.mover_recto(10, 850)
robot.girar(65, 450)
robot.mover_recto(51)
robot.girar(-63, 500)
robot.esperar(100)
robot.seguir_linea(distancia_cm=20, velocidad=1000, ref=30)
#Aqui se posicionó enfrente de la matriz

robot.esperar(100)
robot.girar(-176, 500)
robot.retroceder_recto(8.5, 700)
robot.giro_derecha(43, 450)
robot.avanzar_con_torque(-22, -150, 700, 180)  # dejar los cementos blancos
#Aqui ya dejó los cementos blancos

robot.mover_recto(21, 900)
robot.giro_derecha(-51, 450)
robot.esperar(100)
#Aqui ya se posiciona para detectar la matriz

robot.avanzar_con_torque(-14, 190, 700, 100)
robot.esperar (10)
robot.iden_matriz()
robot.mover_torque(-170, 1000)
robot.esperar(10)
robot.seguir_linea(distancia_cm=35, velocidad=1000, ref=40)


'''
#-----------------------------
robot.girar(-215, 500)
robot.avanzar_con_torque(-43, -150, 700, 180)  # dejar los cementos

robot.mover_torque(90, 400)

robot.mover_recto(15, 900)
robot.giro_derecha(-45, 450)
robot.mover_recto(46, 900)
robot.giro_izquierda(90, 450)
robot.esperar(100)

robot.seguir_linea(distancia_cm=55, velocidad=1300, ref=30)
robot.girar(-90, 500)
robot.avanzar_con_torque(-15, -165, 750)

robot.mover_recto(15, 900)
robot.giro_derecha(-90, 450)

#----
robot.mover_recto(45, 900)
robot.giro_derecha(-90, 450)
robot.mover_recto(10, 900)
robot.girar(90, 500)

robot.mover_recto(10,900)
robot.girar(-180, 500)


robot.avanzar_con_torque(-27, 150, 750, 100)


robot.girar(-20, 500)
robot.mover_recto(37, 900)
robot.girar(25, 900)
robot.esperar(100)
robot.seguir_linea(distancia_cm=140, velocidad=1300, ref=30)
'''