import pygame
import math
from styles import *

def dibujar_vaso_3d(surface, centro_x, base_y, radio_m, altura_m, escala_pixels_m):
    
    """
    Dibuja un cilindro perfecto en perspectiva con base y borde superior elípticos.
    """
    radio_px = radio_m * escala_pixels_m
    altura_px = altura_m * escala_pixels_m
    
    # Factor de aplastamiento para la elipse de la perspectiva (3D)
    factor_perspectiva = 0.3
    radio_y_px = radio_px * factor_perspectiva

    y_top = base_y - altura_px

    # Crear superficie transparente para el vaso
    surf_vaso = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)

    # 1. Cuerpo del vaso (Rectángulo central + elipse de base y tapa)
    rect_cuerpo = pygame.Rect(centro_x - radio_px, y_top, radio_px * 2, altura_px)
    pygame.draw.rect(surf_vaso, COLOR_VASO_CRISTAL, rect_cuerpo)

    # 2. Tapa y base transparente
    rect_elipse_top = pygame.Rect(centro_x - radio_px, y_top - radio_y_px, radio_px * 2, radio_y_px * 2)
    rect_elipse_base = pygame.Rect(centro_x - radio_px, base_y - radio_y_px, radio_px * 2, radio_y_px * 2)

    pygame.draw.ellipse(surf_vaso, COLOR_VASO_CRISTAL, rect_elipse_top)
    pygame.draw.ellipse(surf_vaso, COLOR_VASO_CRISTAL, rect_elipse_base)

    surface.blit(surf_vaso, (0, 0))

    # 3. Dibujar contornos (Líneas sólidas para dar forma de vaso de vidrio)
    # Paredes laterales
    pygame.draw.line(surface, COLOR_VASO_LINEAS, (centro_x - radio_px, base_y), (centro_x - radio_px, y_top), 2)
    pygame.draw.line(surface, COLOR_VASO_LINEAS, (centro_x + radio_px, base_y), (centro_x + radio_px, y_top), 2)

    # Borde superior e inferior
    pygame.draw.ellipse(surface, COLOR_VASO_LINEAS, rect_elipse_top, 2)
    
    # Arco inferior (mitad frontal de la base)
    pygame.draw.arc(surface, COLOR_VASO_LINEAS, rect_elipse_base, math.pi, 2 * math.pi, 2)

def calcular_puntos_superficie(velocidad_angular, aceleracion_ascensor, radio_vaso, altura_agua_inicial, posicion_r):
    """
    Calcula la altura del agua en el vaso considerando la rotación y la aceleración del ascensor.
    z(r) = Ω²/(2g*) [r² - R²/2] + L
    """
    g_efectiva = 9.81 + aceleracion_ascensor  # Gravedad efectiva

    # Evitar división por cero en caída libre (g_efectiva -> 0)
    if abs(g_efectiva) < 1e-5:
        g_efectiva = 1e-5

    altura_agua = velocidad_angular**2 / (2 * g_efectiva) * (posicion_r**2 - radio_vaso**2 / 2) + altura_agua_inicial

    return altura_agua

def dibujar_agua(surface, centro_x, base_y, radio_m, altura_vaso_m, omega, acel, L_inicial, escala_px_m):
    """
    Calcula la masa de agua y la dibuja como un polígono parabólico en Pygame.
    """
    num_puntos = 50  # Resolución de la curva (cuantos más puntos, más suave la parábola)
    puntos_pantalla = []

    # 1. Generar los puntos de la superficie (parábola z(r)) de izquierda (-R) a derecha (+R)
    for i in range(num_puntos + 1):
        # Mapear 'i' a un radio entre -R y +R
        r = -radio_m + (2 * radio_m * i / num_puntos)
        
        # Evaluar la altura física z(r)
        z = calcular_puntos_superficie(omega, acel, radio_m, L_inicial, r)
        
        # Limitar la altura al fondo del vaso (z >= 0) y al borde superior (z <= H)
        z = max(0.0, min(z, altura_vaso_m))

        # Convertir coordenadas físicas (m) a píxeles de pantalla
        x_px = centro_x + (r * escala_px_m)
        y_px = base_y - (z * escala_px_m)  # Se resta porque el eje Y crece hacia abajo
        
        puntos_pantalla.append((x_px, y_px))

    # 2. Cerrar el polígono por la base del vaso
    x_derecha = centro_x + (radio_m * escala_px_m)
    x_izquierda = centro_x - (radio_m * escala_px_m)
    
    puntos_poligono = puntos_pantalla + [(x_derecha, base_y), (x_izquierda, base_y)]

    # 3. Dibujar la masa de agua en una superficie con transparencia (Alfa)
    surf_agua = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
    
    # Relleno del cuerpo de agua
    pygame.draw.polygon(surf_agua, COLOR_AGUA, puntos_poligono)
    
    # Dibujar la línea de la superficie con un tono más claro
    if len(puntos_pantalla) > 1:
        pygame.draw.lines(surf_agua, COLOR_AGUA_SUPERFICIE, False, puntos_pantalla, 3)

    surface.blit(surf_agua, (0, 0))

def dibujar_flecha_aceleracion(surface, x, y_centro, aceleracion):
    """
    Dibuja una flecha vertical representativa de la aceleración del ascensor
    y su etiqueta explicativa en varias líneas.
    """
    if abs(aceleracion) < 0.1:
        # Si la aceleración es prácticamente nula, no dibujamos flecha
        return

    # Mapeamos el módulo de la aceleración a una longitud en píxeles
    longitud_max_px = 90
    longitud = min(abs(aceleracion) * 10, longitud_max_px) + 20 

    # Rojo si acelera hacia arriba, Naranja si acelera hacia abajo
    color_flecha = (220, 60, 60) if aceleracion > 0 else (220, 140, 30) 
    grosor_linea = 4
    ancho_punta = 12
    alto_punta = 15

    if aceleracion > 0:
        # Flecha hacia ARRIBA
        y_inicio = y_centro + longitud // 2
        y_fin = y_centro - longitud // 2
        
        pygame.draw.line(surface, color_flecha, (x, y_inicio), (x, y_fin), grosor_linea)
        
        punta = [
            (x, y_fin), 
            (x - ancho_punta // 2, y_fin + alto_punta), 
            (x + ancho_punta // 2, y_fin + alto_punta)
        ]
        pygame.draw.polygon(surface, color_flecha, punta)

    else:
        # Flecha hacia ABAJO
        y_inicio = y_centro - longitud // 2
        y_fin = y_centro + longitud // 2
        
        pygame.draw.line(surface, color_flecha, (x, y_inicio), (x, y_fin), grosor_linea)
        
        punta = [
            (x, y_fin), 
            (x - ancho_punta // 2, y_fin - alto_punta), 
            (x + ancho_punta // 2, y_fin - alto_punta)
        ]
        pygame.draw.polygon(surface, color_flecha, punta)

    # --- TEXTO EN VARIAS LÍNEAS ---
    lineas_texto = [
        "Aceleración del ascensor",
        f"a = {aceleracion:.1f} m/s²"
    ]
    
    y_texto_inicio = y_centro + longitud_max_px // 2 + 10
    
    for i, linea in enumerate(lineas_texto):
        surf_linea = FUENTE_TEXTO.render(linea, True, COLOR_TEXTO)
        x_pos = x - surf_linea.get_width() // 2
        y_pos = y_texto_inicio + (i * 18)  # Salto de 18 px por línea
        
        surface.blit(surf_linea, (x_pos, y_pos))

def dibujar_flecha_omega(surface, centro_x, base_y, altura_vaso_m, omega, escala_px_m):
    """
    Dibuja el esquema de rotación:
    - Eje de simetría vertical centrado en el vaso.
    - Arco curvado HACIA ABAJO con punta de flecha subiendo a la derecha.
    - Etiqueta Ω = valor en diagonal hacia arriba a la derecha.
    """
    altura_px = altura_vaso_m * escala_px_m
    y_top = base_y - altura_px

    # 1. Eje vertical de simetría
    y_eje_top = y_top - 60
    y_eje_bottom = base_y + 20
    color_eje = (120, 140, 160)
    
    pygame.draw.line(surface, color_eje, (centro_x, y_eje_top), (centro_x, y_eje_bottom), 1)

    if omega <= 0.001:
        return

    # 2. Arco curvado HACIA ABAJO
    radio_x_arco = 30
    radio_y_arco = 12
    y_centro_arco = y_eje_top + 15
    
    rect_arco = pygame.Rect(
        centro_x - radio_x_arco, 
        y_centro_arco - radio_y_arco, 
        radio_x_arco * 2, 
        radio_y_arco * 2
    )

    color_omega = (180, 50, 50)  # Rojo/Granate
    
    # Dibujamos el arco por la parte inferior (de PI a 2*PI)
    pygame.draw.arc(surface, color_omega, rect_arco, math.pi, 2 * math.pi, 2)

    # 3. Punta de flecha en el extremo derecho apuntando HACIA ARRIBA
    x_punta = centro_x + radio_x_arco
    y_punta = y_centro_arco
    
    # Triángulo apuntando hacia arriba (termina la subida de la curva)
    punta_flecha = [
        (x_punta, y_punta - 6),                     # Vértice superior
        (x_punta - 5, y_punta + 4),                 # Esquina inferior izquierda
        (x_punta + 5, y_punta + 4)                  # Esquina inferior derecha
    ]
    pygame.draw.polygon(surface, color_omega, punta_flecha)

    # 4. Texto Ω = valor en diagonal (Arriba a la derecha)
    texto = FUENTE_TEXTO.render(f"Ω = {omega:.1f} rad/s", True, COLOR_TEXTO)
    
    x_texto = centro_x + radio_x_arco + 10
    y_texto = y_eje_top - 15
    
    surface.blit(texto, (x_texto, y_texto))

def dibujar_panel_ecuacion(surface, x, y):
    """
    Dibuja la tarjeta con la ecuación integrada dentro del panel lateral de controles.
    """
    ancho_panel = 260
    alto_panel = 110

    # Fondo semitransparente dentro del panel lateral
    surf_panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
    pygame.draw.rect(surf_panel, (255, 255, 255, 180), surf_panel.get_rect(), border_radius=8)
    pygame.draw.rect(surf_panel, COLOR_SLIDER_LINEA, surf_panel.get_rect(), width=1, border_radius=8)
    surface.blit(surf_panel, (x, y))

    # Textos de la ecuación
    surface.blit(FUENTE_TITULOS.render("Perfil de la superficie:", True, COLOR_TEXTO), (x + 12, y + 10))
    surface.blit(FUENTE_TEXTO.render("z(r) = ( Ω² / 2g* ) · [ r² - (R² / 2) ] + L", True, (180, 40, 40)), (x + 12, y + 38))
    surface.blit(FUENTE_ETIQUETAS.render("donde g* = g + a  (g = 9.81 m/s²)", True, (70, 80, 100)), (x + 12, y + 72))