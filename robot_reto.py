from robot_control import Base

# ----------------- EJECUCIÓN PRINCIPAL -----------------
robot = Base()
print(robot.Hub.battery.voltage())

# ===================== SECCIÓN 1 (Tomar cemento y ubicar pala) =====================
#SECCION 1.1 -> SALIDA Y AVANZAR HASTA EL BALDE DE CEMENTO
robot.giro_izquierda(45, 620) 
robot.mover_recto(12, 900) 
robot.giro_izquierda(45, 620) 
robot.esperar(10)
robot.seguir_linea(robot.seguidor, 100, 65) 
#SECCION 1.2 -> AGARRAR EL BALDE DE CEMENTO
robot.girar(-91, 450) #giro hacia el cemento
robot.esperar(10)
robot.avanzar_con_torque(-19, 160, 700, 140) #tomar el cemento
robot.esperar(10)
#SECCION 1.3 -> DEJAR LA PALA DE ALBAÑILERIA
robot.mover_recto(1,500) 
robot.girar(80)
robot.retroceder_recto(40, 650) 

#===========================SECCION#2 (DEJAR EL CEMENTO)==============================
#SECCION 2.1 -> AVANZAR HASTA DEJAR EL CEMENTO
robot.mover_recto(30.5, 900)
robot.esperar(100)
robot.girar(-18, 500)
robot.mover_recto(9,800)
robot.girar(24, 500)
robot.esperar(120)
robot.seguir_linea(robot.seguidor, 100, 38)

# SECCION 2.2 -> PONER EL CEMENTO EN EL ESTACIONAMIENTO
robot.esperar(10)
robot.girar(91, 500)
robot.mover_torque(-70, 1000)
robot.retroceder_recto(10, 650) 

# ===================== SECCIÓN #3 (IR POR LOS CEMENTOS BLANCOS) =====================
robot.mover_recto(10, 900)
robot.giro_derecha(-85, 450)
robot.esperar(100)

robot.mover_recto(5, 800)
robot.seguir_linea(robot.seguidor, 100, 10) #SEGUIR LINEA HASTA LOS CEMENTOS
robot.girar(-175, 500)
robot.avanzar_con_torque(-24, 165, 750, 300)
#Aqui agarra los cementos blancos

# ===================== SECCION #4 (DEJAR LOS CEMENTOS) =====================
robot.mover_recto(10, 850)
robot.girar(77, 450)
robot.mover_recto(47) #MOVER RECTO HASTA SEGUIR LA LINEA A LA MATRIZ
robot.girar(-64, 500) 
robot.esperar(100)

robot.seguir_linea(robot.seguidor, 60, 26) #SEGUIR LINEA PARA IR A LA MATRIZ
robot.esperar(100)
robot.girar(-182, 500) #giro completo antes de entrar a la matriz
robot.retroceder_recto(10, 900)
robot.girar(38, 500)
robot.avanzar_con_torque(-26, -150, 700, 180)  # DEJAR LOS CEMENTOS BLANCOS

#==============================SECCION #4 (Escanear la matriz)==========================================
robot.mover_recto(19, 900) #Salida de la matriz
robot.girar(-45, 450) 
robot.esperar(100)

robot.seguir_linea(robot.seguidor, 60, 7)
robot.retroceder_recto(20, 700) 
robot.mover_torque(70, 100) 
robot.esperar(1000)
robot.retroceder_recto(2, 700)
robot.mover_torque(-70,100) #subir la celda
robot.esperar(10)

#==================================SECCION #5 (IR POR LOS CEMENTOS AMARILLOS) ==============================
robot.mover_torque(-120,150)
robot.mover_recto(8,900)
robot.seguir_linea(robot.seguidor, 100, 45)
robot.giro_derecha(-90,450)
robot.mover_recto(10,900)
robot.giro_derecha(-89,450)
robot.avanzar_con_torque(-30,120,700,100) #AQUI AGARRA LOS CEMENTOS AMARILLOS

#====================================SECCION #6 (DEJAR LOS CEMENTOS AMARILLOS)==================================
robot.mover_recto(8,900)
robot.seguir_linea(robot.seguidor, 100, 14)
robot.giro_derecha(-89,450)
robot.mover_recto(54,900)

robot.giro_izquierda(91,450)
robot.mover_recto(60,900)
robot.girar(-90,450)
robot.retroceder_recto(22,700)
robot.mover_torque(-120,150) #AQUI YA DEJO LOS CEMENTOS AMARILLOS EN SUI LUGAR

#=================================SECCION #7 (IR POR LOS AZULES) ========================================
robot.mover_recto(19, 800)
robot.girar(-89, 450) #GIRO PARA TOMAR LA PALA
robot.mover_recto(40, 800)
robot.girar(-90, 450)
robot.retroceder_recto(5,700)
robot.mover_torque(120, 150) #AQUI TOMA LA PALA
robot.girar(45, 450)
robot.mover_recto(32.5, 800)
robot.mover_torque(-120, 150) #aqui deja la pala en el camino
robot.girar(44, 500)

robot.seguir_linea(robot.seguidor, 100, 10)
robot.girar(-175, 450)
robot.retroceder_recto(10,700)
robot.mover_torque(120, 150) #Aqui toma los cementos azules

#========================SECCION #8 (DEJAR LOS CEMENTOS AZULES) ==========================
robot.retroceder_recto(10,700)
robot.mover_recto(25, 800)
robot.mover_garra(500, 110) #abrir la garra para llevar la pala

robot.girar(-45)
robot.mover_garra(500, -20)
robot.mover_recto(20, 700)
robot.girar(45)
robot.seguir_linea(robot.seguidor, 100, 140) #seguir la linea hasta el inicio

robot.mover_garra(500, 110) #AQUI YA DEJO LA PALA EN SU LUGAR
robot.retroceder_recto(15, 700)
robot.girar(90)
robot.mover_torque(-120, 150) #AQUI DEJA LOS AZULES A UN LADO
