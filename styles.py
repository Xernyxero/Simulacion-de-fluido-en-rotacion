import pygame

#   Inicializamos el módulo de fuentes para poder definir tipografías
pygame.font.init()

# --- Configuración de la ventana ---
ANCHO_VENTANA = 1100
ALTO_VENTANA = 700

# --- Colores (Paleta limpia y moderna) ---
COLOR_FONDO = (245, 247, 250)
COLOR_PANEL = (220, 226, 235)
COLOR_VASO_LINEAS = (40, 60, 90)
COLOR_VASO_CRISTAL = (180, 210, 235, 80)
COLOR_TEXTO = (30, 40, 60)
COLOR_SLIDER_LINEA = (160, 175, 200)
COLOR_SLIDER_BOTON = (50, 110, 220)

# --- Colores del agua (Azul semitransparente) --- 
COLOR_AGUA = (100, 180, 240, 160)
COLOR_AGUA_SUPERFICIE = (140, 200, 255, 200)

# --- Fuentes --- 
FUEN_CORTA = pygame.font.SysFont("sans-serif", 16)
FUENTE_TITULO = pygame.font.SysFont("sans-serif", 20, bold=True)

# --- TAMAÑOS DE FUENTE GLOBALES ---
TAMANO_ENUNCIADO = 22
TAMANO_TITULOS = 18
TAMANO_TEXTO_GENERAL = 16
TAMANO_ETIQUETAS = 12

# --- OBJETOS DE FUENTE REUTILIZABLES ---
FUENTE_ENUNCIADO = pygame.font.SysFont("sans-serif", TAMANO_ENUNCIADO, bold=True)
FUENTE_TITULOS = pygame.font.SysFont("sans-serif", TAMANO_TITULOS, bold=True)
FUENTE_TEXTO = pygame.font.SysFont("sans-serif", TAMANO_TEXTO_GENERAL)
FUENTE_ETIQUETAS = pygame.font.SysFont("sans-serif", TAMANO_ETIQUETAS)