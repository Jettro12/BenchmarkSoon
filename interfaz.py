# --- Clase de la Interfaz Gráfica ---
import ttkbootstrap as tb
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk,  messagebox
import pandas as pd

from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    generar_prompt_personalizado,
    obtener_consejo_ia,
    obtener_info_gpu,
   
)
from BD import (

    almacenar_datos,
    crear_grafico_barras,
    preparar_datos_historicos,
    entrenar_modelo,
    crear_base_de_datos,
)
from tkinter.messagebox import showerror
from tkinter import BOTH, X, Y, END, VERTICAL, RIGHT, LEFT, BOTTOM
from configuraciones import (
    ESTILO_BOTON_PRIMARIO,
    ESTILO_BOTON_SECUNDARIO,
    ESTILO_LABEL_TITULO,
    ESTILO_LABEL_TEXTO,
    ESTILO_TEXTO_CONSEJO,
    ESTILO_LABEL_CATEGORIA,
)

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark del Sistema")
        self.style = tb.Style("vapor")
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        self.root.geometry(f"{pantalla_ancho}x{pantalla_alto}")

        # Crear las tablas si no existen
        crear_base_de_datos()

        self.contenedor = tb.Frame(self.root)
        self.contenedor.pack(fill=BOTH, expand=True)

        self.ventana_inicio()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def ventana_inicio(self):
        self.limpiar_contenedor()

        try:
            fondo = Image.open("Media/modelo1.png").resize((576, 768), Image.LANCZOS)
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
            text="B/Athen-IA",
            **ESTILO_LABEL_TITULO,  # Aplicar estilo de título
        )
        label_titulo.pack(pady=20)

        boton_analizar = tb.Button(
            self.contenedor,
            text="Analizar",
            command=self.ventana_analisis,
            style="Primary.TButton",  # Aplicar estilo primario
        )
        boton_venanalizar = tb.Button(
            self.contenedor,
            text="Analisis",
            command=self.ventana_inicio,
            style="Primary.TButton",  # Aplicar estilo primario
        )
        boton_Prediccion = tb.Button(
            self.contenedor,
            text="Predicciones",
            command=self.mostrar_predicciones,
            style="Primary.TButton",  # Aplicar estilo primario
        )
        boton_analizar.place(relx=0.5, rely=0.8, anchor="center")
        boton_venanalizar.place(relx=0.0, rely=0.2, anchor="w") 
        boton_Prediccion.place(relx=0.0, rely=0.4, anchor="w") 


    def ventana_analisis(self):
        self.limpiar_contenedor()

        try:
            self.info_procesador = obtener_info_procesador()
            self.info_ram = obtener_info_ram()
            self.info_disco = obtener_info_disco()
            self.info_gpu = obtener_info_gpu()
            # Almacenar los datos en la base de datos
            almacenar_datos(self.info_procesador, self.info_ram, self.info_disco, self.info_gpu)

            fondo = Image.open("Media/modelo2.png").resize((576, 768), Image.LANCZOS)
            fondo_tk = ImageTk.PhotoImage(fondo)

            ventana_ancho = self.root.winfo_width()
            ventana_alto = self.root.winfo_height()
            fondo_x = (ventana_ancho - 576) // 2
            fondo_y = (ventana_alto - 768) // 2

            label_fondo = tb.Label(self.contenedor, image=fondo_tk)
            label_fondo.image = fondo_tk
            label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)

            # Configuración para el frame del Procesador
            self.mostrar_categoria(
                categoria="Procesador",
                datos=self.info_procesador,
                posicion=(190, 5),
                ancho=470,
                alto=170,
            )

            # Configuración para el frame de la RAM
            self.mostrar_categoria(
                categoria="RAM",
                datos=self.info_ram,
                posicion=(900, 180),
                ancho=200,
                alto=130,
            )

            # Configuración para el frame del Disco
            self.mostrar_categoria(
                categoria="Disco",
                datos=self.info_disco,
                posicion=(999, 525),
                ancho=210,
                alto=130,
            )

            # Configuración para el frame de la GPU
            if "No disponible" in self.info_gpu.values():
                self.mostrar_categoria(
                    categoria="GPU",
                    datos={"GPU": "No se detecto ninguna GPU en este sistema"},
                    posicion=(190, 525),
                    ancho=470,
                    alto=130,
                )
            else:
                self.mostrar_categoria(
                    categoria="GPU",
                    datos=self.info_gpu,
                    posicion=(190, 525),
                    ancho=470,
                    alto=150,
                )

            boton_consejo = tb.Button(
                self.contenedor,
                text="Dame un consejo Atenea",
                command=self.ventana_consejo,
                style="Primary.TButton",  # Aplicar estilo primario
            )
            boton_consejo.place(relx=0.5, rely=0.8, anchor="center")

        except Exception as e:
            showerror("Error", f"No se pudo completar el análisis: {e}")

    def mostrar_categoria(self, categoria, datos, posicion, ancho, alto):
        """Muestra una categoría con su frame y labels correspondientes."""
        x, y = posicion

        # Crear el frame para la categoría
        frame_categoria = tb.Labelframe(
            self.contenedor,
            text=categoria,
            padding=10,
            bootstyle="secondary",
        )
        frame_categoria.place(x=x, y=y, width=ancho, height=alto)

        # Mostrar los datos dentro del frame
        for clave, valor in datos.items():
            label = tb.Label(
                frame_categoria,
                text=f"{clave}: {valor}",
                **ESTILO_LABEL_TEXTO,
            )
            label.pack(anchor="w")

    def ventana_consejo(self):
        self.limpiar_contenedor()

        # Frame principal para dividir la ventana en dos partes
        frame_principal = tb.Frame(self.contenedor)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para el lado izquierdo (consejo y predicciones)
        frame_izquierdo = tb.Frame(frame_principal)
        frame_izquierdo.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para el lado derecho (chatbot)
        frame_derecho = tb.Frame(frame_principal)
        frame_derecho.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        try:
            # Generar el consejo de optimización
            prompt = generar_prompt_personalizado(
                self.info_procesador,
                self.info_ram,
                self.info_disco,
                self.info_gpu,
            )
            consejo = obtener_consejo_ia(prompt)

            # Crear un Canvas para el scroll (para el consejo)
            canvas = tb.Canvas(frame_izquierdo)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # Barra de desplazamiento
            scrollbar = tb.Scrollbar(frame_izquierdo, orient=VERTICAL, command=canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            # Frame interno para el contenido del consejo
            frame_consejo = tb.Frame(canvas)
            canvas.create_window((0, 0), window=frame_consejo, anchor="nw")

            # Mostrar el título del consejo
            label_consejo = tb.Label(
                frame_consejo,
                text="Consejo de Optimización:",
                **ESTILO_LABEL_TITULO,  # Aplicar estilo de título
            )
            label_consejo.pack(pady=10)

            # Mostrar el texto del consejo
            texto_consejo = tb.Label(
                frame_consejo,
                text=consejo,
                **ESTILO_TEXTO_CONSEJO,  # Aplicar estilo de texto de consejo
            )
            texto_consejo.pack(pady=10)

            

        except Exception as e:
            showerror("Error", f"Error al obtener consejo de IA: {e}")

        # Frame para el chatbot en el lado derecho
        self.chatbot_seccion(frame_derecho)

        # Frame para los botones de volver y salir
        frame_botones = tb.Frame(self.contenedor)
        frame_botones.pack(fill=X, padx=10, pady=10)

        # Botón "Volver al inicio"
        boton_volver = tb.Button(
            frame_botones,
            text="Volver al inicio",
            command=self.ventana_inicio,
            style="Secondary.TButton",  # Aplicar estilo secundario
        )
        boton_volver.pack(side=LEFT, padx=5)

        # Botón "Salir"
        boton_salir = tb.Button(
            frame_botones,
            text="Salir",
            command=self.root.quit,
            style="Secondary.TButton",  # Aplicar estilo secundario
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
                prompt_combinado = f"{generar_prompt_personalizado(self.info_procesador, self.info_ram, self.info_disco, self.info_gpu)}\n\n{prompt_usuario}"
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


    def mostrar_predicciones(self):
     try:
        # Crear la nueva ventana
        ventana_predicciones = tk.Toplevel(self.root)
        ventana_predicciones.title("Predicciones de Rendimiento")
        ventana_predicciones.geometry("850x600")

        # Crear un canvas para contener todo el contenido
        canvas = tk.Canvas(ventana_predicciones)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para el canvas
        scrollbar = tk.Scrollbar(ventana_predicciones, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el canvas para que use el scrollbar
        canvas.config(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del canvas
        frame_predicciones = tb.Frame(canvas)
        canvas.create_window((0, 0), window=frame_predicciones, anchor="nw")

        # Cargar y preparar datos históricos
        df_ram, df_procesador, df_disco, df_gpu = preparar_datos_historicos()

        # Verificar si hay datos
        if df_ram.empty or df_procesador.empty or df_disco.empty:
            messagebox.showwarning("Advertencia", "No hay suficientes datos para generar predicciones.")
            ventana_predicciones.destroy()
            return

        # Convertir las fechas a valores de tipo datetime
        df_ram["fecha"] = pd.to_datetime(df_ram["fecha"], errors='coerce')
        df_procesador["fecha"] = pd.to_datetime(df_procesador["fecha"], errors='coerce')
        df_disco["fecha"] = pd.to_datetime(df_disco["fecha"], errors='coerce')

        # Predicciones para los componentes
        predicciones = {
            "RAM": entrenar_modelo(df_ram, "uso_ram"),
            "Procesador": entrenar_modelo(df_procesador, "frecuencia_actual"),
            "Disco Duro": entrenar_modelo(df_disco, "uso_disco"),
        }

        # Crear un contenedor para los gráficos
        frame_graficos = tb.Frame(frame_predicciones)
        frame_graficos.pack(fill=tk.BOTH, expand=True, pady=10)

        interpretacion_completa = "--- Predicciones de Rendimiento ---\n\n"

        # Generar gráficos y mostrar las interpretaciones
        interpretacion_ram = crear_grafico_barras(predicciones["RAM"][0], df_ram, "fecha", "uso_ram", "Uso de RAM (%)", frame_graficos)
        interpretacion_completa += f"RAM:\n{interpretacion_ram}\n\n"
        
        interpretacion_procesador = crear_grafico_barras(predicciones["Procesador"][0], df_procesador, "fecha", "frecuencia_actual", "Frecuencia del Procesador (GHz)", frame_graficos)
        interpretacion_completa += f"Procesador:\n{interpretacion_procesador}\n\n"
        
        interpretacion_disco = crear_grafico_barras(predicciones["Disco Duro"][0], df_disco, "fecha", "uso_disco", "Uso del Disco (%)", frame_graficos)
        interpretacion_completa += f"Disco Duro:\n{interpretacion_disco}\n\n"

        # Área de texto desplazable para la interpretación
        texto_interpretacion = ScrolledText(frame_predicciones, wrap="word", height=10, width=90, state="normal")
        texto_interpretacion.insert(tk.END, interpretacion_completa)
        texto_interpretacion.config(state="disabled")
        texto_interpretacion.pack(pady=10)

        # Actualizar la región del canvas para ajustarse al contenido
        frame_predicciones.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Botón para cerrar la ventana
        boton_cerrar = tb.Button(frame_predicciones, text="Cerrar", bootstyle="danger", command=ventana_predicciones.destroy)
        boton_cerrar.pack(pady=10)

     except Exception as e:
        messagebox.showerror("Error", f"Error al generar predicciones: {e}")
