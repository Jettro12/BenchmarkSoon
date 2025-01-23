import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    generar_prompt_personalizado,
    obtener_consejo_ia,
)

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark del Sistema")

        # Configuración inicial con ttkbootstrap
        self.style = tb.Style("superhero")  # Cambia el tema aquí según tus preferencias
        self.root.geometry("1200x800")

        # Crear un marco contenedor
        self.contenedor = tb.Frame(self.root)
        self.contenedor.pack(fill=BOTH, expand=True)

        # Mostrar la ventana de inicio
        self.ventana_inicio()

    def limpiar_contenedor(self):
        """Elimina todo el contenido del contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def ventana_inicio(self):
        """Muestra la pantalla de inicio."""
        self.limpiar_contenedor()

        # Fondo de imagen
        try:
            fondo = Image.open("Media/Atenea.jpg")
            fondo = fondo.resize((800, 600), Image.LANCZOS)
            fondo_tk = ImageTk.PhotoImage(fondo)
        except Exception as e:
            tb.Messagebox.show_error(title="Error", message=f"No se pudo cargar la imagen de fondo: {e}")
            return

        label_fondo = tb.Label(self.contenedor, image=fondo_tk)
        label_fondo.image = fondo_tk
        label_fondo.place(relwidth=1, relheight=1)

        # Título
        label_titulo = tb.Label(
            self.contenedor,
            text="Bienvenido al Benchmark del Sistema",
            font=("Helvetica", 26, "bold"),
            bootstyle="primary",
        )
        label_titulo.pack(pady=20)

        # Botón para ir al análisis
        boton_analizar = tb.Button(
            self.contenedor,
            text="Analizar",
            bootstyle="success",
            command=self.ventana_analisis,
        )
        boton_analizar.place(relx=0.5, rely=0.8, anchor="center")

    def ventana_analisis(self):
        """Muestra la pantalla de análisis del sistema."""
        self.limpiar_contenedor()

        # Crear un frame con scroll
        frame_scroll = tb.Frame(self.contenedor)
        frame_scroll.pack(fill=BOTH, expand=True)

        canvas = tb.Canvas(frame_scroll)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = tb.Scrollbar(frame_scroll, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_contenido = tb.Frame(canvas)
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")

        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Secciones de análisis y consejo
        frame_analisis = tb.Frame(frame_contenido)
        frame_analisis.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        frame_consejo = tb.Frame(frame_contenido)
        frame_consejo.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Título
        label_titulo = tb.Label(frame_analisis, text="Resultados del Análisis", font=("Arial", 16), bootstyle="info")
        label_titulo.pack(pady=10)

        # Obtener información del sistema
        self.info_procesador = obtener_info_procesador()
        self.info_ram = obtener_info_ram()
        self.info_disco = obtener_info_disco()

        for categoria, datos in {
            "Procesador": self.info_procesador,
            "RAM": self.info_ram,
            "Disco": self.info_disco,
        }.items():
            frame_categoria = tb.Labelframe(frame_analisis, text=categoria, padding=10, bootstyle="secondary")
            frame_categoria.pack(fill=X, padx=10, pady=5)
            for clave, valor in datos.items():
                label = tb.Label(frame_categoria, text=f"{clave}: {valor}")
                label.pack(anchor="w")

        # Generar el prompt basado en el análisis
        self.prompt_inicial = generar_prompt_personalizado()

        # Área para mostrar el consejo
        label_consejo = tb.Label(frame_consejo, text="Consejo de Optimización:", font=("Arial", 14))
        label_consejo.pack(pady=10)

        self.texto_consejo = tb.Text(frame_consejo, wrap="word", height=15, width=40)
        self.texto_consejo.pack(pady=10)

        boton_consejo = tb.Button(
            frame_consejo, text="Generar Consejo", bootstyle="primary", command=self.generar_consejo
        )
        boton_consejo.pack(pady=10)

        # Chatbot
        self.chatbot_seccion(frame_consejo)

        boton_volver = tb.Button(
            self.contenedor, text="Volver al inicio", bootstyle="danger", command=self.ventana_inicio
        )
        boton_volver.pack(pady=10)

    def chatbot_seccion(self, frame_consejo):
        """Agrega la sección de chatbot a la ventana."""
        frame_chatbot = tb.Labelframe(frame_consejo, text="Chatbot de Optimización", padding=10)
        frame_chatbot.pack(fill=X, padx=10, pady=20)

        label_pregunta = tb.Label(frame_chatbot, text="¿Necesitas algo en especial?", font=("Arial", 14))
        label_pregunta.pack(pady=5)

        self.seleccion = tb.StringVar(value="Otro")
        opciones = ["Optimizar para jugar", "Optimizar para programar", "Otro"]
        for opcion in opciones:
            tb.Radiobutton(
                frame_chatbot, text=opcion, variable=self.seleccion, value=opcion, bootstyle="success"
            ).pack(anchor="w")

        label_prompt = tb.Label(frame_chatbot, text="O escribe un prompt personalizado:", font=("Arial", 12))
        label_prompt.pack(pady=5)

        self.entry_prompt = tb.Entry(frame_chatbot, width=50)
        self.entry_prompt.pack(pady=5)

        boton_obtener = tb.Button(
            frame_chatbot, text="Obtener Sugerencias", bootstyle="info", command=self.obtener_sugerencias
        )
        boton_obtener.pack(pady=10)

        self.texto_respuesta = tb.Text(frame_chatbot, wrap="word", height=10, width=80, state="disabled")
        self.texto_respuesta.pack(pady=10)

    def obtener_sugerencias(self):
        opcion = self.seleccion.get()
        prompt_usuario = self.entry_prompt.get().strip()

        if opcion == "Otro":
            if prompt_usuario:
                prompt_combinado = f"{self.prompt_inicial}\n\n{prompt_usuario}"
                self.generar_sugerencias(prompt_combinado)
            else:
                tb.Messagebox.show_warning(title="Advertencia", message="Por favor, ingresa un prompt personalizado.")
        else:
            sugerencias = f"Sugerencias para {opcion}: Mejora tu configuración para {opcion.lower()}."
            self.texto_respuesta.config(state="normal")
            self.texto_respuesta.delete(1.0, "end")
            self.texto_respuesta.insert("end", sugerencias)
            self.texto_respuesta.config(state="disabled")

    def generar_consejo(self):
        consejo = obtener_consejo_ia(self.prompt_inicial)
        self.texto_consejo.delete(1.0, "end")
        self.texto_consejo.insert("end", consejo)

    def generar_sugerencias(self, prompt_usuario):
        sugerencias = obtener_consejo_ia(prompt_usuario)
        self.texto_respuesta.config(state="normal")
        self.texto_respuesta.delete(1.0, "end")
        self.texto_respuesta.insert("end", sugerencias)
        self.texto_respuesta.config(state="disabled")

if __name__ == "__main__":
    root = tb.Window()
    app = VentanaPrincipal(root)
    root.mainloop()