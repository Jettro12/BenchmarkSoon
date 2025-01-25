import tkinter as tk
from tkinter import messagebox
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
        self.root.geometry("576x768")

        # Crear un marco contenedor
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        # Mostrar la ventana de inicio al iniciar
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
            fondo = Image.open("Media/modelo1.jpg")
            fondo = fondo.resize((576, 768), Image.LANCZOS)
            fondo_tk = ImageTk.PhotoImage(fondo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
            return

        label_fondo = tk.Label(self.contenedor, image=fondo_tk)
        label_fondo.image = fondo_tk
        label_fondo.place(relwidth=1, relheight=1)

        # Título
        label_titulo = tk.Label(
            self.contenedor, text="Atenea", font=("Ginchiest", 30), bg="Gray"
        )
        label_titulo.pack(pady=10)

        # Botón para ir al análisis
        boton_analizar = tk.Button(
            self.contenedor, text="Analizar", font=("Arial", 12), command=self.ventana_analisis
        )
        boton_analizar.place(relx=0.5, rely=0.8, anchor="center")

    def ventana_analisis(self):
        """Muestra la pantalla de análisis del sistema."""
        self.limpiar_contenedor()

        # Crear el Canvas para scroll
        canvas = tk.Canvas(self.contenedor)
        canvas.pack(side="left", fill="both", expand=True)

        # Crear la barra de desplazamiento
        scrollbar = tk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del canvas para organizar los widgets
        frame_contenido = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")

        # Vincular el scroll del canvas
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Crear un marco para el análisis y otro para generar consejo
        frame_analisis = tk.Frame(frame_contenido)
        frame_analisis.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_consejo = tk.Frame(frame_contenido)
        frame_consejo.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Título
        label_titulo = tk.Label(frame_analisis, text="Resultados del Análisis", font=("Arial", 16))
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
            frame_categoria = tk.LabelFrame(frame_analisis, text=categoria, padx=10, pady=10)
            frame_categoria.pack(fill="x", padx=10, pady=5)
            for clave, valor in datos.items():
                label = tk.Label(frame_categoria, text=f"{clave}: {valor}")
                label.pack(anchor="w")

        # Generar el prompt basado en el análisis
        self.prompt_inicial = generar_prompt_personalizado()

        # Área para mostrar el consejo
        label_consejo = tk.Label(frame_consejo, text="Consejo de Optimización:", font=("Arial", 14))
        label_consejo.pack(pady=10)

        self.texto_consejo = tk.Text(frame_consejo, wrap="word", height=15, width=40)
        self.texto_consejo.pack(pady=10)

        # Botón para generar el consejo basado en el análisis
        boton_consejo = tk.Button(
            frame_consejo, text="Generar Consejo", font=("Arial", 12), command=self.generar_consejo
        )
        boton_consejo.pack(pady=10)

        # Chatbot sección
        self.chatbot_seccion(frame_consejo)

        # Botón para regresar a la pantalla de inicio
        boton_volver = tk.Button(
            self.contenedor, text="Volver al inicio", font=("Arial", 12), command=self.ventana_inicio
        )
        boton_volver.pack(pady=10)

    def chatbot_seccion(self, frame_consejo):
        """Agrega la sección de chatbot a la ventana."""
        frame_chatbot = tk.LabelFrame(frame_consejo, text="Chatbot de Optimización", padx=10, pady=10)
        frame_chatbot.pack(fill="x", padx=10, pady=20)

        # Pregunta inicial
        label_pregunta = tk.Label(frame_chatbot, text="¿Necesitas algo en especial?", font=("Arial", 14))
        label_pregunta.pack(pady=5)

        # Opciones predefinidas
        self.seleccion = tk.StringVar(value="Otro")
        opciones = ["Optimizar para jugar", "Optimizar para programar", "Otro"]
        for opcion in opciones:
            tk.Radiobutton(
                frame_chatbot, text=opcion, variable=self.seleccion, value=opcion, font=("Arial", 12)
            ).pack(anchor="w")

        # Entrada para un prompt personalizado
        label_prompt = tk.Label(frame_chatbot, text="O escribe un prompt personalizado:", font=("Arial", 12))
        label_prompt.pack(pady=5)

        self.entry_prompt = tk.Entry(frame_chatbot, width=50, font=("Arial", 12))
        self.entry_prompt.pack(pady=5)

        # Botón para obtener sugerencias
        boton_obtener = tk.Button(
            frame_chatbot, text="Obtener Sugerencias", font=("Arial", 12), command=self.obtener_sugerencias
        )
        boton_obtener.pack(pady=10)

        # Área de salida para las sugerencias
        self.texto_respuesta = tk.Text(frame_chatbot, wrap="word", height=10, width=80, state="disabled")
        self.texto_respuesta.pack(pady=10)

    def obtener_sugerencias(self):
        """Obtiene sugerencias basadas en la opción seleccionada."""
        opcion = self.seleccion.get()
        prompt_usuario = self.entry_prompt.get().strip()

        if opcion == "Otro":
            if prompt_usuario:
                # Combinar el prompt inicial con el prompt del usuario
                prompt_combinado = f"{self.prompt_inicial}\n\n{prompt_usuario}"
                self.generar_sugerencias(prompt_combinado)  # Llamar a la función para generar sugerencias
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingresa un prompt personalizado.")
        else:
            # Aquí puedes agregar la lógica para mostrar sugerencias específicas
            sugerencias = f"Sugerencias para {opcion}: Mejora tu configuración para {opcion.lower()}."
            self.texto_respuesta.config(state="normal")
            self.texto_respuesta.delete(1.0, tk.END)
            self.texto_respuesta.insert(tk.END, sugerencias)
            self.texto_respuesta.config(state="disabled")

    def generar_consejo(self):
        """Genera un consejo basado en el análisis del sistema."""
        consejo = obtener_consejo_ia(self.prompt_inicial)  # Usar el prompt inicial
        self.texto_consejo.delete(1.0, tk.END)
        self.texto_consejo.insert(tk.END, consejo)

    def generar_sugerencias(self, prompt_usuario):
        """Genera sugerencias personalizadas basadas en el prompt del usuario."""
        sugerencias = obtener_consejo_ia(prompt_usuario)  # Usar el prompt combinado
        self.texto_respuesta.config(state="normal")
        self.texto_respuesta.delete(1.0, tk.END)
        self.texto_respuesta.insert(tk.END, sugerencias)
        self.texto_respuesta.config(state="disabled")

# Aquí se debe agregar el código para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()