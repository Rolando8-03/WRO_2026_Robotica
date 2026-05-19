from pybricks.parameters import Port, Direction

# ============================================================
# PUERTOS DEL ROBOT
# ============================================================

PORT_MOTOR_DERECHO = Port.A
PORT_MOTOR_IZQUIERDO = Port.E

PORT_MOTOR_TORQUE = Port.D
PORT_MOTOR_GARRA = Port.F
PORT_MOTOR_GARRA_DELANTERA = Port.B

PORT_SENSOR_SEGUIDOR = Port.C


# ============================================================
# DIRECCIONES DE MOTORES
# ============================================================

DIR_MOTOR_DERECHO = Direction.CLOCKWISE
DIR_MOTOR_IZQUIERDO = Direction.COUNTERCLOCKWISE

DIR_MOTOR_TORQUE = None
DIR_MOTOR_GARRA = None
DIR_MOTOR_GARRA_DELANTERA = None


# ============================================================
# MEDIDAS FÍSICAS DEL ROBOT
# ============================================================

DIAMETRO_RUEDA_MM = 56
PI = 3.14159


# ============================================================
# PERFILES GENERALES
# ============================================================

PERFIL_SEGURO = "seguro"
PERFIL_ENCADENADO = "encadenado"


# ============================================================
# MOVIMIENTO RECTO / RETROCESO
# ============================================================

MOV_VELOCIDAD_RECTA = 1000
MOV_VELOCIDAD_RETROCESO = 800

MOV_KP = 2.1
MOV_KD = 2.9
MOV_CORRECCION_MAX = 130
MOV_VELOCIDAD_MIN = 380

MOV_PAUSA_GYRO_RETROCESO = 25


# ============================================================
# GIROS
# ============================================================

GIRO_VELOCIDAD = 1200
GIRO_VELOCIDAD_MIN = 160
GIRO_ANTICIPACION = 0
GIRO_ZONA_FRENO = 22

GIRO_UN_MOTOR_VELOCIDAD = 1000
GIRO_UN_MOTOR_VELOCIDAD_MIN = 260
GIRO_UN_MOTOR_ANTICIPACION = 0
GIRO_UN_MOTOR_ZONA_FRENO = 28


# ============================================================
# SEGUIDOR DE LÍNEA NORMAL
# ============================================================

LINEA_VELOCIDAD_MAX = 100
LINEA_LADO_DEFAULT = "derecha"

LINEA_TIEMPO_ACOMODO_MS = 140
LINEA_TIEMPO_ACELERACION_MS = 140

LINEA_KP = 1.25
LINEA_KD = 2.7
LINEA_K_FRENO = 0.16
LINEA_CORRECCION_MAX = 100

LINEA_OBJETIVO_REFLEXION = 27

LINEA_MARGEN_CM = 0
LINEA_PERFIL_SALIDA = PERFIL_ENCADENADO


# ============================================================
# CAPTURA INICIAL DE LÍNEA
# ============================================================

LINEA_CAPTURA_INICIAL = True
LINEA_TIEMPO_CAPTURA_MS = 280
LINEA_POTENCIA_CAPTURA = 60
LINEA_KP_CAPTURA = 2.5
LINEA_MARGEN_CAPTURA = 5
LINEA_LECTURAS_ESTABLES_CAPTURA = 2


# ============================================================
# LÍNEA NEGRA / DETECCIÓN
# ============================================================

UMBRAL_NEGRO = 20
UMBRAL_SALIDA_NEGRO = 28

LECTURAS_NEGRAS_NECESARIAS = 2
LECTURAS_CLARAS_NECESARIAS = 3


# ============================================================
# TORQUE
# ============================================================

TORQUE_VELOCIDAD_ROBOT = 1200
TORQUE_VELOCIDAD_MOTOR = 350
TORQUE_DESPUES_CM = 1

TORQUE_ESPERAR = False
TORQUE_LEVANTAR_FINAL_GRADOS = 0


# ============================================================
# GARRAS
# ============================================================

GARRA_VELOCIDAD = 300
GARRA_DELANTERA_VELOCIDAD = 850


# ============================================================
# ESPERAS COMUNES
# ============================================================

ESPERA_CORTA_MS = 100
ESPERA_MEDIA_MS = 300
ESPERA_LARGA_MS = 400