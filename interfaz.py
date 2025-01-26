# --- Clase de la Interfaz Gráfica ---

import ttkbootstrap as tb
from PIL import Image, ImageTk
from funciones import obtener_info_disco, obtener_consejo_ia, obtener_info_procesador, obtener_info_ram
from tkinter.messagebox import showerror
from tkinter import BOTH, X

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark del Sistema")
        self.style = tb.Style("superhero")
        self.root.geometry("1200x800")

        self.contenedor = tb.Frame(self.root)
        self.contenedor.pack(fill=BOTH, expand=True)

        self.ventana_inicio()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def ventana_inicio(self):
     self.limpiar_contenedor()

    # Fondo
     try:
        fondo = Image.open("Media/Modelo1.jpg").resize((576, 768), Image.LANCZOS)
        fondo_tk = ImageTk.PhotoImage(fondo)
        
        # Calcular posición centrada del fondo
        self.root.update()  # Asegurarse de que las dimensiones de la ventana sean correctas
        ventana_ancho = self.root.winfo_width()
        ventana_alto = self.root.winfo_height()
        fondo_x = (ventana_ancho - 576) // 2
        fondo_y = (ventana_alto - 768) // 2

        label_fondo = tb.Label(self.contenedor, image=fondo_tk)
        label_fondo.image = fondo_tk
        label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)  # Centrado

     except Exception as e:
        showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
        return

     label_titulo = tb.Label(
        self.contenedor,
        text="Bienvenido al Benchmark del Sistema",
        font=("Helvetica", 26, "bold"),
        bootstyle="primary",
    )
     label_titulo.pack(pady=20)

     boton_analizar = tb.Button(
        self.contenedor, text="Analizar", bootstyle="success", command=self.ventana_analisis
    )
     boton_analizar.place(relx=0.5, rely=0.8, anchor="center")

    def ventana_analisis(self):
     self.limpiar_contenedor()

     try:
        # Obtener la información del sistema
        self.info_procesador = obtener_info_procesador()
        self.info_ram = obtener_info_ram()
        self.info_disco = obtener_info_disco()

        # Fondo (la imagen de Atenea)
        fondo = Image.open("Media/Modelo2.jpg").resize((576, 768), Image.LANCZOS)
        fondo_tk = ImageTk.PhotoImage(fondo)
        
        # Calcular posición centrada del fondo
        ventana_ancho = self.root.winfo_width()
        ventana_alto = self.root.winfo_height()
        fondo_x = (ventana_ancho - 576) // 2
        fondo_y = (ventana_alto - 768) // 2

        label_fondo = tb.Label(self.contenedor, image=fondo_tk)
        label_fondo.image = fondo_tk
        label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)  # Centrado

        # Posiciones de los cuadros (ajusta estas coordenadas para alinear con la imagen)
        posiciones = {
            "Procesador": (320, 79),
            "RAM": (750, 199),
            "Disco": (660, 565),
        }

        # Mostrar la información en los cuadros
        for categoria, datos in {
            "Procesador": self.info_procesador,
            "RAM": self.info_ram,
            "Disco": self.info_disco,
        }.items():
            x, y = posiciones[categoria]
            frame_categoria = tb.Labelframe(
                self.contenedor, text=categoria, padding=10, bootstyle="secondary"
            )
            frame_categoria.place(x=x, y=y, width=200, height=100)
            for clave, valor in datos.items():
                label = tb.Label(frame_categoria, text=f"{clave}: {valor}")
                label.pack(anchor="w")

        # Botón para obtener consejo
        boton_consejo = tb.Button(
            self.contenedor, text="Dame un consejo Atenea", bootstyle="danger", command=self.ventana_consejo
        )
        boton_consejo.place(x=500, y=700)  # Ajusta coordenadas según diseño

     except Exception as e:
        showerror("Error", f"No se pudo completar el análisis: {e}")



    def ventana_consejo(self):
     self.limpiar_contenedor()

     frame_analisis = tb.Frame(self.contenedor)
     frame_analisis.pack(fill=BOTH, expand=True, padx=10, pady=10)

     try:
        # Generar el prompt personalizado con datos obtenidos
        prompt = (
            f"Basado en los datos obtenidos:\n"
            f"Procesador: {self.info_procesador}\n"
            f"RAM: {self.info_ram}\n"
            f"Disco: {self.info_disco}\n\n"
            "Proporciona un análisis del sistema y consejos para mejorar el rendimiento y el cuidado."
        )
        # Llama a la función para obtener el consejo
        consejo = obtener_consejo_ia(prompt)

        # Mostrar el consejo en la interfaz
        frame_categoria = tb.Labelframe(frame_analisis, text="Consejo", padding=10, bootstyle="secondary")
        frame_categoria.pack(fill=X, padx=10, pady=5)

        label = tb.Label(frame_categoria, text=consejo, wraplength=1000)
        label.pack(anchor="w")
     except Exception as e:
        showerror("Error", f"Error al obtener consejo de IA: {e}")

     boton_volver = tb.Button(
        self.contenedor, text="Volver al inicio", bootstyle="danger", command=self.ventana_inicio
    )
     boton_volver.pack(pady=10)
