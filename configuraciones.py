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
    "padding": 12,  # Espacio interno
    "background": "#1E90FF",  # Color de fondo (verde)
    "foreground": "white",  # Color del texto (blanco)
    "bordercolor": "#1E90FF",  # Color del borde
    "borderwidth": 2,  # Grosor del borde
    "relief": "raised",  # Estilo del borde
    "focuscolor": "#4682B4",  # Color cuando el botón tiene el foco
    "activebackground": "#5B9BD5",  # Color de fondo al hacer clic
    "activeforeground": "white",  # Color del texto al hacer clic
}

# Estilo para los botones de la ventana de consejos (Volver al inicio y Salir)
ESTILO_BOTON_SECUNDARIO = {
    "font": ("Helvetica", 12, "bold"),  # Fuente del botón
    "padding": 12,  # Espacio interno
    "background": "#2e232b",  # Color de fondo (naranja)
    "foreground": "white",  # Color del texto (blanco)
    "bordercolor": "#6C4F60",  # Color del borde
    "borderwidth": 2,  # Grosor del borde
    "relief": "raised",  # Estilo del borde
    "focuscolor": "#40212C",  # Color cuando el botón tiene el foco
    "activebackground": "#4A3C46",  # Naranja oscuro al presionar
    "activeforeground": "white",  # Mantener texto blanco
}

# Estilo para los labels de títulos
ESTILO_LABEL_TITULO = {
    "font": ("Helvetica", 26, "bold"),  # Fuente grande y en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "#FFFACD",  # Color de fondo
}

# Estilo para los labels de texto normal
ESTILO_LABEL_TEXTO = {
    "font": ("Helvetica", 12),  # Fuente normal
    "foreground": "#2E86C1",  # Color del texto
    #"background": "#FFFACD",  # Color de fondo
}

# Estilo para el texto de consejos
ESTILO_TEXTO_CONSEJO = {
    "font": ("Arial", 12),  # Fuente normal
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "#FFFACD",  # Color de fondo
    "wraplength": 600,  # Ancho máximo antes de saltar de línea
}

# Estilo para los labels de categorías (Procesador, RAM, Disco)
ESTILO_LABEL_CATEGORIA = {
    "font": ("Arial", 14, "bold"),  # Fuente en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
    #"background": "#FFFACD",  # Color de fondo
}

ESTILO_LABEL_PROMPTPERSONAL = {
    "font": ("Helvetica", 18, "bold"),  # Fuente grande y en negrita
    "foreground": "#2E86C1",  # Color del texto (azul)
   # "background": "#FFFACD",  # Color de fondo
}
ESTILO_LABEL_TEXTO1 = {
    "font": ("Helvetica", 14),
    "foreground": "#2E86C1",
    "wraplength": 290,
    #"background": "#FFFACD",  # Color de fondo
}

ESTILO_FRAMES = {
        "relief": "solid",  # Borde sólido para el frame
        "borderwidth": 2,  # Grosor del borde
}