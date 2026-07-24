import pygame
import sys

from styles import *
from classes import Slider
from functions import *

def main():
    pygame.init()
    
    # Crear la ventana aquí usando las dimensiones de styles.py
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulación de recipiente girando en un ascensor")

    clock = pygame.time.Clock()

    # Panel lateral de controles (Sliders)
    x_panel = 30
    y_inicio = 80
    ancho_slider = 220
    alto_slider = 16
    separacion = 60

    slider_radio = Slider(x_panel, y_inicio, ancho_slider, alto_slider, 0.03, 0.20, 0.08, "Radio (R)", "m")
    slider_altura = Slider(x_panel, y_inicio + separacion, ancho_slider, alto_slider, 0.10, 0.50, 0.25, "Altura (H)", "m")
    slider_omega = Slider(x_panel, y_inicio + separacion * 2, ancho_slider, alto_slider, 0.0, 20.0, 0.0, "Vel. Angular (Ω)", "rad/s")
    slider_acel = Slider(x_panel, y_inicio + separacion * 3, ancho_slider, alto_slider, -9.0, 10.0, 0.0, "Acel. Ascensor (a)", "m/s²")

    sliders = [slider_radio, slider_altura, slider_omega, slider_acel]

    # Configuración de escala física
    ESCALA_PX_M = 1000  

    # Centro visual para dibujar el vaso
    CENTRO_X_VASO = 700
    BASE_Y_VASO = 550

    ejecutando = True
    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            for s in sliders:
                s.handle_event(event)

        # Obtener valores actuales de los sliders
        radio = slider_radio.valor
        altura = slider_altura.valor
        omega = slider_omega.valor
        acel = slider_acel.valor

        # Dibujar Escena
        pantalla.fill(COLOR_FONDO)

        # Panel de interfaz a la izquierda
        pygame.draw.rect(pantalla, COLOR_PANEL, (0, 0, 300, ALTO_VENTANA))
        pygame.draw.line(pantalla, COLOR_SLIDER_LINEA, (300, 0), (300, ALTO_VENTANA), 2)
        
        titulo_panel = FUENTE_TITULO.render("Parámetros del Recipiente", True, COLOR_TEXTO)
        pantalla.blit(titulo_panel, (30, 30))

        for s in sliders:
            s.draw(pantalla)

        # --- TARJETA CON LA ECUACIÓN ---
        # Posicionada a X = 20 (dentro de la franja de 300px) y Y = 380 (debajo del 4º slider)
        dibujar_panel_ecuacion(pantalla, 20, 380)

        # Dibujar suelo/base donde apoya el vaso
        pygame.draw.line(pantalla, COLOR_SLIDER_LINEA, (350, BASE_Y_VASO), (1050, BASE_Y_VASO), 3)

        # Definir posiciones horizontales para los dos vasos, además de la altura del agua inicial
        CENTRO_X_ESTATICO = 500
        CENTRO_X_ROTACION = 850
        BASE_Y_VASO = 550
        L_agua_inicial = 0.15

        # --- ENUNCIADO DEL PROBLEMA ---
        lineas_problema = [
            "Problema: Simulación de un fluido en un recipiente cilíndrico bajo rotación y aceleración vertical.",
            "Estudio del perfil parabólico de la superficie libre del agua en función de la velocidad angular (Ω) y la gravedad efectiva (g* = g + a)."
        ]

        y_texto = 18
        x_centro_pantalla = (ANCHO_VENTANA + 300) // 2  # Centrado en el área a la derecha del panel

        # Título principal del enunciado
        surf_titulo = FUENTE_ENUNCIADO.render(lineas_problema[0], True, COLOR_TEXTO)
        pantalla.blit(surf_titulo, (x_centro_pantalla - surf_titulo.get_width() // 2, y_texto))

        # Subtítulo / Descripción física
        surf_sub = FUENTE_TEXTO.render(lineas_problema[1], True, (70, 80, 95))
        pantalla.blit(surf_sub, (x_centro_pantalla - surf_sub.get_width() // 2, y_texto + 28))

        # --- DIBUJAR VASO 1: EN REPOSO (Izquierda) ---
        dibujar_agua(pantalla, CENTRO_X_ESTATICO, BASE_Y_VASO, radio, altura, 0.0, acel, L_agua_inicial, ESCALA_PX_M)
        dibujar_vaso_3d(pantalla, CENTRO_X_ESTATICO, BASE_Y_VASO, radio, altura, ESCALA_PX_M)

        # --- DIBUJAR VASO 2: EN ROTACIÓN (Derecha) ---
        dibujar_agua(pantalla, CENTRO_X_ROTACION, BASE_Y_VASO, radio, altura, omega, acel, L_agua_inicial, ESCALA_PX_M)
        dibujar_vaso_3d(pantalla, CENTRO_X_ROTACION, BASE_Y_VASO, radio, altura, ESCALA_PX_M)

        # --- INDICADORES Y FLECHAS ---
        dibujar_flecha_omega(pantalla, CENTRO_X_ROTACION, BASE_Y_VASO, altura, omega, ESCALA_PX_M)
        dibujar_flecha_aceleracion(pantalla, 1030, 320, acel)

        # --- TÍTULOS DEBAJO DE CADA VASO ---
        y_titulos = BASE_Y_VASO + 35

        txt_estatico = FUENTE_TITULOS.render("Vaso en Reposo (Ω = 0)", True, COLOR_TEXTO)
        pantalla.blit(txt_estatico, (CENTRO_X_ESTATICO - txt_estatico.get_width() // 2, y_titulos))

        txt_rotacion = FUENTE_TITULOS.render("Vaso en Rotación", True, COLOR_TEXTO)
        pantalla.blit(txt_rotacion, (CENTRO_X_ROTACION - txt_rotacion.get_width() // 2, y_titulos))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()