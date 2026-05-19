# 🤖 Hexagon Force — WRO 2026 RoboMission Senior

Proyecto oficial del equipo **Hexagon Force** para la categoría **WRO RoboMission Senior 2026**.

> **Temporada:** World Robot Olympiad 2026  
> **Categoría:** RoboMission Senior  
> **Reto:** Mosaic Masters  
> **País:** Nicaragua 🇳🇮  
> **Institución:** Universidad Americana (UAM)  
> **Tecnología principal:** LEGO SPIKE Prime + Pybricks  

---

## 📌 Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Integrantes del equipo](#-integrantes-del-equipo)
- [Contexto del reto](#-contexto-del-reto)
- [Objetivo del robot](#-objetivo-del-robot)
- [Misiones principales](#-misiones-principales)
- [Sistema de puntuación](#-sistema-de-puntuación)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Estrategia de programación](#-estrategia-de-programación)
- [Estado del proyecto](#-estado-del-proyecto)
- [Referencia oficial](#-referencia-oficial)

---

## 🧠 Descripción general

**Hexagon Force — WRO 2026 RoboMission Senior** es un proyecto de robótica autónoma desarrollado para resolver el reto oficial **Mosaic Masters** de la temporada WRO 2026.

El robot está construido con **LEGO SPIKE Prime** y programado con **Pybricks**, utilizando Python para controlar movimientos, sensores, mecanismos y secuencias de misión.

El proyecto se enfoca en crear un robot capaz de moverse con precisión dentro del campo, transportar herramientas, entregar cementos de distintos colores, detectar patrones de mosaico y manipular piezas dentro de zonas específicas del tablero.

---

## 👥 Integrantes del equipo

- **Elydariana de León García Espinoza**
- **Rolando Enrique Mayorga Mena**
- **Lesther Josias Galeano Meza**

🎓 **Universidad Americana (UAM)**  
📍 **Managua, Nicaragua**

---

## 🌍 Contexto del reto

El reto **Mosaic Masters** está inspirado en la restauración de murales y mosaicos culturales. En esta temporada, el robot representa una solución tecnológica capaz de apoyar en la preservación de obras dañadas por el tiempo, el clima o desastres naturales.

La misión consiste en transportar herramientas, entregar materiales de construcción y colocar piezas de mosaico de forma precisa dentro del campo de juego.

La precisión es clave, ya que el robot debe completar las tareas sin dañar barreras ni mover objetos fuera de sus zonas permitidas.

---

## 🎯 Objetivo del robot

El objetivo principal del robot es completar la mayor cantidad posible de misiones dentro del tiempo permitido, obteniendo la máxima puntuación posible.

Para lograrlo, el robot debe:

- Seguir líneas con precisión.
- Realizar giros controlados con giroscopio.
- Transportar y entregar cementos de colores.
- Manipular herramientas del campo.
- Detectar patrones de mosaico mediante sensor de color.
- Ejecutar rutas automatizadas según la matriz detectada.
- Evitar dañar o mover barreras del campo.

---

## ✅ Misiones principales

### 1. Proveer herramientas

El robot debe manipular y transportar tres herramientas ubicadas en la parte inferior del campo:

- **Pala rectangular** hacia el área del patrocinador.
- **Balde de cemento** hacia el estacionamiento.
- **Pala de albañilería** hacia el área de inicio.

Cada herramienta obtiene mayor puntuación si queda completamente dentro de su zona objetivo.

---

### 2. Colocar el mosaico

El robot debe colocar piezas de mosaico dentro del marco central, respetando el patrón de colores indicado por la matriz.

Las piezas pueden ser de color:

- Amarillo
- Azul
- Verde
- Blanco

La puntuación depende de si la pieza queda correctamente colocada, con el color adecuado y estable sobre el suelo.

---

### 3. Entregar cementos

El robot debe transportar cementos de distintos colores hacia sus zonas correspondientes en el centro del campo.

Los colores de cemento son:

- Blanco
- Verde
- Amarillo
- Azul

Cada cemento debe quedar completamente dentro del área objetivo de su mismo color para sumar puntos.

---

### 4. Bonus por barreras

El campo contiene barreras que no deben ser dañadas ni movidas fuera de su área permitida.

Se considera daño si:

- Una pelota cae de la barrera.
- Un bloque se desprende.
- La barrera queda fuera del área gris permitida.

Mantener las barreras intactas permite obtener puntos extra.

---

## 🏆 Sistema de puntuación

| Misión | Descripción | Puntaje máximo |
|---|---|---:|
| Proveer herramientas | Colocar correctamente la pala rectangular, el balde de cemento y la pala de albañilería | 45 pts |
| Colocar mosaico | Colocar piezas de mosaico en el marco según el patrón indicado | 120 pts |
| Entregar cementos | Llevar cementos a sus zonas de color correspondiente | 40 pts |
| Bonus por barreras | No mover ni dañar las barreras | 28 pts |
| **Total máximo** |  | **233 pts** |

---

## ⚙️ Tecnologías utilizadas

### Hardware

- LEGO SPIKE Prime
- Hub SPIKE Prime
- Motores LEGO Powered Up
- Sensor de color
- Giroscopio integrado del Hub
- Mecanismos personalizados para garra, torque y manipulación de piezas

### Software

- Python
- Pybricks
- Visual Studio Code
- GitHub para control y organización del proyecto

---

## 📁 Estructura del proyecto

```text
WRO_2026/
│
├── Control/
│   ├── base.py
│   ├── giros.py
│   ├── linea.py
│   ├── manipuladores.py
│   ├── movimiento.py
│   ├── robot_config.py
│   └── utilidades.py
│
├── Matrices/
│   ├── matriz1.py
│   ├── matriz2.py
│   ├── matriz3.py
│   ├── matriz4.py
│   ├── matriz5.py
│   └── matriz6.py
│
├── Misiones/
│   ├── cementos.py
│   ├── herramientas.py
│   └── matriz_router.py
│
├── main.py
└── README.md