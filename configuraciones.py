import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables desde el archivo .env
load_dotenv()
# Configuración de la API Key
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Estilo para los botones de inicio y análisis
ESTILO_BOTON_PRIMARIO = {
    "font": ("Arial", 14, "bold"),  # Fuente del botón
    "padding": 10,  # Espacio interno
    "background": "#1E2F59",  # Color de fondo (verde)
    "foreground": "#2E86C1",  # Color del texto (blanco)
    "bordercolor": "#991FA6",  # Color del borde
    "borderwidth": 2,  # Grosor del borde
    "relief": "raised",  # Estilo del borde
    "focuscolor": "#FF5733",  # Color cuando el botón tiene el foco
}

# Estilo para los botones de la ventana de consejos (Volver al inicio y Salir)
ESTILO_BOTON_SECUNDARIO = {
    "font": ("Helvetica", 12, "bold"),  # Fuente del botón
    "padding": 8,  # Espacio interno
   # "background": "#FF5733",  # Color de fondo (naranja)
    "foreground": "white",  # Color del texto (blanco)
    "bordercolor": "#E64A19",  # Color del borde
    "borderwidth": 2,  # Grosor del borde
    "relief": "raised",  # Estilo del borde
    "focuscolor": "#FF5733",  # Color cuando el botón tiene el foco
}

# Estilo para los labels de títulos
ESTILO_LABEL_TITULO = {
    "font": ("Helvetica", 26, "bold"),  # Fuente grande y en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "white",  # Color de fondo
}

# Estilo para los labels de texto normal
ESTILO_LABEL_TEXTO = {
    "font": ("Helvetica", 12),  # Fuente normal
    "foreground": "#F5F0A1",  # Color del texto
    #"background": "white",  # Color de fondo
}

# Estilo para el texto de consejos
ESTILO_TEXTO_CONSEJO = {
    "font": ("Arial", 12),  # Fuente normal
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "white",  # Color de fondo
    "wraplength": 600,  # Ancho máximo antes de saltar de línea
}

# Estilo para los labels de categorías (Procesador, RAM, Disco)
ESTILO_LABEL_CATEGORIA = {
    "font": ("Arial", 14, "bold"),  # Fuente en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
    "background": "white",  # Color de fondo
}

ESTILO_LABEL_PROMPTPERSONAL = {
    "font": ("Helvetica", 18, "bold"),  # Fuente grande y en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "white",  # Color de fondo
}