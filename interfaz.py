# --- Clase de la Interfaz Gráfica ---
import ttkbootstrap as tb
from PIL import Image, ImageTk
from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    generar_prompt_personalizado,
    obtener_consejo_ia,
)
from tkinter.messagebox import showerror
from tkinter import BOTH, X, Y, END, VERTICAL, RIGHT, LEFT, BOTTOM

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark del Sistema")
        self.style = tb.Style("vapor")
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        self.root.geometry(f"{pantalla_ancho}x{pantalla_alto}")

        self.contenedor = tb.Frame(self.root)
        self.contenedor.pack(fill=BOTH, expand=True)

        self.ventana_inicio()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def ventana_inicio(self):
        self.limpiar_contenedor()

        try:
            fondo = Image.open("Media/modelo1.jpg").resize((576, 768), Image.LANCZOS)
            fondo_tk = ImageTk.PhotoImage(fondo)

            self.root.update()
            ventana_ancho = self.root.winfo_width()
            ventana_alto = self.root.winfo_height()
            fondo_x = (ventana_ancho - 576) // 2
            fondo_y = (ventana_alto - 768) // 2

            label_fondo = tb.Label(self.contenedor, image=fondo_tk)
            label_fondo.image = fondo_tk
            label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)

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
            self.info_procesador = obtener_info_procesador()
            self.info_ram = obtener_info_ram()
            self.info_disco = obtener_info_disco()

            fondo = Image.open("Media/modelo2.jpg").resize((576, 768), Image.LANCZOS)
            fondo_tk = ImageTk.PhotoImage(fondo)

            ventana_ancho = self.root.winfo_width()
            ventana_alto = self.root.winfo_height()
            fondo_x = (ventana_ancho - 576) // 2
            fondo_y = (ventana_alto - 768) // 2

            label_fondo = tb.Label(self.contenedor, image=fondo_tk)
            label_fondo.image = fondo_tk
            label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)

            posiciones = {
                "Procesador": (320, 79),
                "RAM": (750, 199),
                "Disco": (660, 565),
            }

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

            boton_consejo = tb.Button(
                self.contenedor, text="Dame un consejo Atenea", bootstyle="danger", command=self.ventana_consejo
            )
            boton_consejo.place(x=500, y=700)

        except Exception as e:
            showerror("Error", f"No se pudo completar el análisis: {e}")

    def ventana_consejo(self):
        self.limpiar_contenedor()

        frame_principal = tb.Frame(self.contenedor)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para el consejo
        frame_consejo = tb.Frame(frame_principal)
        frame_consejo.pack(fill=BOTH, expand=True, padx=10, pady=10)

        try:
            prompt = generar_prompt_personalizado(self.info_procesador, self.info_ram, self.info_disco)
            consejo = obtener_consejo_ia(prompt)

            # Crear un Canvas para el scroll
            canvas = tb.Canvas(frame_consejo)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # Barra de desplazamiento
            scrollbar = tb.Scrollbar(frame_consejo, orient=VERTICAL, command=canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            # Frame interno para el contenido
            frame_interno = tb.Frame(canvas)
            canvas.create_window((0, 0), window=frame_interno, anchor="nw")

            label_consejo = tb.Label(frame_interno, text="Consejo de Optimización:", font=("Arial", 14))
            label_consejo.pack(pady=10)

            texto_consejo = tb.Text(frame_interno, wrap="word", height=15, width=80, state="normal")
            texto_consejo.insert(END, consejo)
            texto_consejo.config(state="disabled")
            texto_consejo.pack(pady=10)

        except Exception as e:
            showerror("Error", f"Error al obtener consejo de IA: {e}")

        # Frame para el chatbot
        frame_chatbot = tb.Frame(frame_principal)
        frame_chatbot.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.chatbot_seccion(frame_chatbot)

        # Frame para los botones de volver y salir
        frame_botones = tb.Frame(self.contenedor)
        frame_botones.pack(fill=X, padx=10, pady=10)

        boton_volver = tb.Button(
            frame_botones, text="Volver al inicio", bootstyle="danger", command=self.ventana_inicio
        )
        boton_volver.pack(side=LEFT, padx=5)

        boton_salir = tb.Button(
            frame_botones, text="Salir", bootstyle="danger", command=self.root.quit
        )
        boton_salir.pack(side=RIGHT, padx=5)

    def chatbot_seccion(self, frame_chatbot):
        """Agrega la sección de chatbot a la ventana."""
        frame_chat = tb.Labelframe(frame_chatbot, text="Chatbot de Optimización", padding=10, bootstyle="secondary")
        frame_chat.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Pregunta inicial
        label_pregunta = tb.Label(frame_chat, text="¿Necesitas algo en especial?", font=("Arial", 14))
        label_pregunta.pack(pady=5)

        # Opciones predefinidas
        self.seleccion = tb.StringVar(value="Otro")
        opciones = ["Optimizar para jugar", "Optimizar para programar", "Otro"]
        for opcion in opciones:
            tb.Radiobutton(
                frame_chat, text=opcion, variable=self.seleccion, value=opcion
            ).pack(anchor="w")

        # Entrada para un prompt personalizado
        label_prompt = tb.Label(frame_chat, text="O escribe un prompt personalizado:", font=("Arial", 12))
        label_prompt.pack(pady=5)

        self.entry_prompt = tb.Entry(frame_chat, width=50)
        self.entry_prompt.pack(pady=5)

        # Botón para obtener sugerencias
        boton_obtener = tb.Button(
            frame_chat, text="Obtener Sugerencias", command=self.obtener_sugerencias
        )
        boton_obtener.pack(pady=10)

        # Área de salida para las sugerencias
        self.texto_respuesta = tb.Text(frame_chat, wrap="word", height=10, width=80, state="disabled")
        self.texto_respuesta.pack(pady=10)

    def obtener_sugerencias(self):
        """Obtiene sugerencias basadas en la opción seleccionada."""
        opcion = self.seleccion.get()
        prompt_usuario = self.entry_prompt.get().strip()

        if opcion == "Otro":
            if prompt_usuario:
                # Combinar el prompt inicial con el prompt del usuario
                prompt_combinado = f"{generar_prompt_personalizado(self.info_procesador, self.info_ram, self.info_disco)}\n\n{prompt_usuario}"
                self.generar_sugerencias(prompt_combinado)  # Llamar a la función para generar sugerencias
            else:
                showerror("Advertencia", "Por favor, ingresa un prompt personalizado.")
        else:
            # Aquí puedes agregar la lógica para mostrar sugerencias específicas
            sugerencias = f"Sugerencias para {opcion}: Mejora tu configuración para {opcion.lower()}."
            self.texto_respuesta.config(state="normal")
            self.texto_respuesta.delete(1.0, END)
            self.texto_respuesta.insert(END, sugerencias)
            self.texto_respuesta.config(state="disabled")

    def generar_sugerencias(self, prompt_usuario):
        """Genera sugerencias personalizadas basadas en el prompt del usuario."""
        sugerencias = obtener_consejo_ia(prompt_usuario)  # Usar el prompt combinado
        self.texto_respuesta.config(state="normal")
        self.texto_respuesta.delete(1.0, END)
        self.texto_respuesta.insert(END, sugerencias)
        self.texto_respuesta.config(state="disabled")