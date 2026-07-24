import pygame
from styles import *

class Slider:
    """Clase para crear un control deslizante interactivo en Pygame."""
    def __init__(self, x, y, ancho, alto, val_min, val_max, val_init, etiqueta, unidad=""):
        self.rect_linea = pygame.Rect(x, y + alto // 2 - 2, ancho, 4)
        self.val_min = val_min
        self.val_max = val_max
        self.valor = val_init
        self.etiqueta = etiqueta
        self.unidad = unidad
        
        # Posición del botón deslizable
        self.ancho_boton = 16
        self.alto_boton = alto
        self.arrastrando = False
        self.actualizar_pos_boton_desde_valor()

    def actualizar_pos_boton_desde_valor(self):
        proporcion = (self.valor - self.val_min) / (self.val_max - self.val_min)
        cx = self.rect_linea.x + proporcion * self.rect_linea.width
        self.rect_boton = pygame.Rect(cx - self.ancho_boton // 2, self.rect_linea.y - self.alto_boton // 2 + 2,
                                      self.ancho_boton, self.alto_boton)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_boton.collidepoint(event.pos) or self.rect_linea.collidepoint(event.pos):
                self.arrastrando = True
                self.actualizar_valor_desde_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.arrastrando = False
        elif event.type == pygame.MOUSEMOTION and self.arrastrando:
            self.actualizar_valor_desde_mouse(event.pos[0])

    def actualizar_valor_desde_mouse(self, mouse_x):
        x_rel = max(self.rect_linea.x, min(mouse_x, self.rect_linea.x + self.rect_linea.width))
        proporcion = (x_rel - self.rect_linea.x) / self.rect_linea.width
        self.valor = self.val_min + proporcion * (self.val_max - self.val_min)
        self.actualizar_pos_boton_desde_valor()

    def draw(self, surface):
        # Dibujar etiqueta y valor
        texto = f"{self.etiqueta}: {self.valor:.3f} {self.unidad}"
        surf_texto = FUENTE_TEXTO.render(texto, True, COLOR_TEXTO)
        surface.blit(surf_texto, (self.rect_linea.x, self.rect_linea.y - 22))

        # Dibujar riel
        pygame.draw.rect(surface, COLOR_SLIDER_LINEA, self.rect_linea, border_radius=2)
        # Dibujar botón
        pygame.draw.rect(surface, COLOR_SLIDER_BOTON, self.rect_boton, border_radius=4)