# 🤖 Hexagon Force — WRO 2026 RoboMission Senior

Proyecto oficial del equipo **Hexagon Force** 
## 🏆 World Robot Olympiad (WRO) 2026 — RoboMission Senior

---

# 👥 Integrantes del equipo

- Elydariana de León García Espinoza
- Rolando Enrique Mayorga Mena
- Lesther Josias Galeano Meza

🎓 Universidad Americana (UAM)  
📍 Managua, Nicaragua

---

# 🧠 Descripción del proyecto

Este proyecto consiste en el desarrollo de un robot autónomo utilizando LEGO SPIKE Prime y Pybricks para resolver el reto oficial de la categoría **WRO RoboMission Senior 2026**.

El robot fue programado para realizar múltiples misiones relacionadas con la construcción inteligente de una ciudad, utilizando:

- Seguimiento de línea
- Control PID
- Giros con giroscopio
- Manipulación de objetos
- Detección de colores
- Control de torque
- Secuencias automatizadas

---

# 🎯 Objetivo del reto

El robot debe completar distintas tareas dentro de un tiempo límite, obteniendo la mayor cantidad posible de puntos.

Las misiones principales incluyen:

## ✅ 1. Proveer herramientas

El robot debe:

- Llevar la pala rectangular al área del patrocinador.
- Colocar el balde de cemento en el estacionamiento.
- Regresar la pala de albañilería al área de inicio.

---

## ✅ 2. Colocar el mosaico

El robot debe colocar correctamente las piezas de mosaico dentro de su marco correspondiente.

---

## ✅ 3. Entregar cementos

El robot debe transportar cementos de diferentes colores hacia sus zonas correspondientes:

- Cementos blancos
- Cementos verdes
- Cementos amarillos
- Cementos azules

Cada cemento debe quedar completamente dentro de su zona objetivo para obtener la puntuación máxima.

---

## ✅ 4. Bonus por barreras

El robot debe evitar mover o dañar las barreras durante el recorrido.

Se considera daño si:

- Se cae una pelota
- Se cae un bloque
- La barrera sale del área gris permitida

---

# 🏆 Sistema de puntuación

|        Misión        |    Puntos   |
|----------------------|-------------|
| Proveer herramientas |    45 pts   |
| Colocar mosaicos     |    120 pts  |
| Entregar cementos    |    40 pts   |
| Bonus por barreras   |    28 pts   |
|      **TOTAL**       | **233 pts** |

Información basada en el reglamento oficial WRO 2026 RoboMission Senior:
https://drive.google.com/file/d/1pa7YLOmh9L7Tba4PrCgpwdBuhMukqLua/view?usp=sharing

---

# ⚙️ Tecnologías utilizadas

## Hardware

- LEGO SPIKE Prime
- Motores LEGO Powered Up
- Sensor de color
- Giroscopio integrado del Hub

---

## Software

- Python
- Pybricks
- Visual Studio Code

---

# 🧩 Arquitectura del proyecto

El proyecto fue organizado utilizando principios de programación modular y programación orientada a objetos (POO).

├── main.py
│
├── Control/
│   ├── base.py
│   ├── movimiento.py
│   ├── giros.py
│   ├── linea.py
│   ├── manipuladores.py
│   ├── utilidades.py
│   └── matriz_router.py
│
├── Misiones/
│   ├── herramientas.py
│   ├── cementos.py
│   ├── inicio.py
│   └── reto_principal.py
│
└── Matrices/
    ├── matriz_1.py
    ├── matriz_2.py
    ├── matriz_3.py
    ├── matriz_4.py
    └── matriz_5.py