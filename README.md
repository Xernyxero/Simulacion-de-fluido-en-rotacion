# Simulación de Fluido Rotatorio en Ascensor Acelerado

Simulador interactivo desarrollado en **Python** y **Pygame** que modela el comportamiento de un fluido contenido en un recipiente cilíndrico sujeto a **rotación uniforme** ($\Omega$) y **aceleración vertical** ($a$) en un ascensor.

![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

---

## Descripción del Proyecto

El objetivo de esta aplicación es visualizar en tiempo real cómo cambia la perfilometría de la superficie libre de un fluido cuando interactúa en un sistema no inercial.

La simulación contrapone dos escenarios en vivo:
1. **Vaso en Reposo ($\Omega = 0$):** Representa el fluido plano con la altura inicial del agua ($L$).
2. **Vaso en Rotación ($\Omega > 0$):** Muestra el perfil paraboloidal generado por la combinación de la fuerza centrífuga y la gravedad efectiva ($g^*$).

---

## Fundamento Físico

La superficie libre del fluido adopta una forma parabólica descrita por la siguiente ecuación física:

$$z(r) = \frac{\Omega^2}{2g^*} \cdot \left( r^2 - \frac{R^2}{2} \right) + L$$

Donde:
* **$z(r)$**: Altura local del agua en función de la distancia radial $r$.
* **$\Omega$**: Velocidad angular de rotación ($\text{rad/s}$).
* **$R$**: Radio del recipiente cilíndrico ($\text{m}$).
* **$L$**: Altura media inicial del agua ($\text{m}$).
* **$g^*$**: Gravedad efectiva ($g^* = g + a$), donde $g = 9.81\text{ m/s}^2$ y $a$ es la aceleración vertical del ascensor.

---

## Características y Controles

* **Panel Lateral Interactivo:**
  * **Radio ($R$):** Ajusta las dimensiones del recipiente ($0.03\text{ m} \le R \le 0.20\text{ m}$).
  * **Altura ($H$):** Cambia la altura del cilindro ($0.10\text{ m} \le H \le 0.50\text{ m}$).
  * **Velocidad Angular ($\Omega$):** Modifica la tasa de giro ($0.0 \le \Omega \le 20.0\text{ rad/s}$).
  * **Aceleración ($a$):** Simula el movimiento del ascensor subiendo o bajando ($-9.0 \le a \le 10.0\text{ m/s}^2$).
* **Gráficos 3D en Perspectiva:** Renderización de cilindros transparentes con efecto elíptico y superficie parabólica dinámica.
* **Indicadores Visuales:**
  * Flechas dinámicas de aceleración vertical (color rojo hacia arriba, naranja hacia abajo).
  * Arco 3D en el eje de simetría con indicador en directo del valor de $\Omega$.
  * Tarjeta integrada con la fórmula matemática y la gravedad efectiva actualizada.

---

## Estructura del Proyecto

```text
├── main.py        # Punto de entrada principal y bucle del programa.
├── functions.py   # Lógica matemática (cálculos de la parábola) y funciones de dibujo.
├── classes.py     # Clase Slider para los controles interactivos de la interfaz.
├── styles.py      # Configuración de colores, dimensiones y fuentes globales.
└── README.md      # Documentación del proyecto.