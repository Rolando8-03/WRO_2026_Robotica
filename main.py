from Control.robot_config import Robot
from misiones.cementos import *
from misiones.matriz_router import escanear_matriz, ejecutar_matriz_router
from pybricks.tools import wait

def main():
    # 1. INICIALIZACIÓN
    # Cargamos hardware, PID y todas las funciones de control (28 funciones)
    robot = Robot()
    matriz_id = None

    # 2. ESPERA DE SEGURIDAD (Confirmación de salida)
    print(">>> ROBOT LISTO. Presiona cualquier botón para iniciar.")
    while not any(robot.Hub.buttons.pressed()):
        wait(10)
    
    wait(500) # Pausa para retirar la mano
    print(">>> INICIANDO RETO PRINCIPAL")

    # =============================================================
    # 3. SECUENCIA DE MISIONES (EL RETO)
    # =============================================================

    # MISION 1: Inicio y captura de la Pala
    mision_inicio_pala(robot)

    # MISION 2: Entrega de cemento en el estacionamiento
    mision_cemento_estacionamiento(robot)

    # MISION 3: Recolección de Cementos Blancos
    mision_blancos(robot)

    # --- NAVEGACIÓN HACIA LA MATRIZ ---
    robot.giro_izquierda(70, velocidad=1200, perfil="encadenado")
    robot.mover_recto(39, velocidad=1000, perfil="encadenado")
    robot.girar(-60, velocidad=1200, perfil="encadenado")
    robot.seguir_linea_extremo(distancia_cm=20, lado="derecha", perfil_salida="encadenado")
    robot.mover_recto(40, velocidad=1000, perfil="encadenado")

    # ESCANEO: Detección de color (25 muestras)
    matriz_id = escanear_matriz(robot)

    # --- NAVEGACIÓN HACIA CEMENTOS VERDES ---
    robot.mover_recto(17, velocidad=900, perfil="encadenado")
    robot.girar(-44, velocidad=850, perfil="encadenado")

    # MISION 4: Cementos Verdes
    mision_verdes(robot)

    # MISION 5: Cementos Amarillos
    mision_amarillos(robot)

    # MISION 6: Cementos Azules y Retorno con Pala
    mision_azules_final(robot)

    # =============================================================
    # 4. FINALIZACIÓN (MATRIZ DETECTADA)
    # =============================================================
    if matriz_id is not None:
        print(f">>> Ejecutando Matriz Final: {matriz_id}")
        ejecutar_matriz_router(robot, matriz_id)
    else:
        print(">>> ERROR: No se pudo ejecutar la matriz final (ID no válido).")

    print(">>> RETO COMPLETADO.")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()