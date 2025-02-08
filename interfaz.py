import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkinter import  messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import tkinter as tk
import requests
import torch  
import tkinter.ttk as ttk
from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    obtener_info_gpu,
    generar_prompt_personalizado,
    obtener_consejo_ia,
)
from tkinter.messagebox import showerror, showinfo
from tkinter import BOTH, X, Y, END, VERTICAL, RIGHT, LEFT, BOTTOM
from configuraciones import (
    ESTILO_BOTON_PRIMARIO,
    ESTILO_BOTON_SECUNDARIO,
    ESTILO_LABEL_TITULO,
    ESTILO_LABEL_TEXTO,
    #ESTILO_TEXTO_CONSEJO,
    #ESTILO_LABEL_CATEGORIA,
    ESTILO_LABEL_PROMPTPERSONAL,
    ESTILO_LABEL_TEXTO1,
    ESTILO_FRAMES,
)
from funciones_graficos import (
    crear_grafico_cpu,
    crear_grafico_ram,
    crear_grafico_disco,
    crear_grafico_gpu,
)
from BD import (
    almacenar_datos,
    crear_grafico_arima,
    preparar_datos_historicos,
    crear_base_de_datos,
)
from modelo import (
entrenar_modelo_arima,
hacer_predicciones_arima
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import markdown
from tkhtmlview import HTMLLabel
import webbrowser

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Athen-IA")
        # Configuración inicial con ttkbootstrap
        self.style = tb.Style("morph")  # Cambia el tema aquí según tus preferencias
        
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        self.root.geometry(f"{pantalla_ancho}x{pantalla_alto}")
        # Crear las tablas si no existen
        crear_base_de_datos()
        # Configurar estilos personalizados
        self.style.configure("Primary.TButton", **ESTILO_BOTON_PRIMARIO)
        self.style.configure("Secondary.TButton", **ESTILO_BOTON_SECUNDARIO)

        # Crear un marco contenedor
        self.contenedor = tb.Frame(self.root)
        self.contenedor.pack(fill=BOTH, expand=True)

        # Mostrar la ventana de inicio
        self.ventana_inicio()

    def limpiar_contenedor(self):
        """Elimina todo el contenido del contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def _crear_botones_navegacion(self):
        """Crea y posiciona los botones de navegación comunes."""
        #Iconos
        self.icono_home = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/home.png").resize((30, 30)))
        self.icono_salir = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/salir.png").resize((20, 20)))
        self.icono_predic = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/predic.png").resize((30, 30)))
        self.icono_nosotros = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/noso.png").resize((30, 30)))
        self.icono_regresar = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/regresar.png").resize((20, 20)))
        self.icono_consejo = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/consejo.png").resize((30, 30)))

        #Frame para los botones
        frame_botones = tb.Frame(self.contenedor, width=300, height=810)
        frame_botones.place(relx=0, rely=0.45, anchor="w")

        boton_Prediccion = tb.Button(
            frame_botones,
            text="Predicciones",
            command=self.mostrar_predicciones,
            style="Primary.TButton",
            cursor="hand2",
            image=self.icono_predic,
            compound=tk.LEFT,
        )
        boton_inicio = tb.Button(
            frame_botones,
            text="Inicio",
            command=self.ventana_inicio,
            style="Primary.TButton",
            cursor="hand2",
            image=self.icono_home,
            compound=tk.LEFT,
        )
        boton_sobre_nosotros = tb.Button(
            frame_botones,
            text="Sobre Nosotros",
            style="Primary.TButton",
            cursor="hand2",
            command=self.ventana_sobre_nosotros,
            image=self.icono_nosotros,
            compound=tk.LEFT,
         )

        boton_salir = tb.Button(
            frame_botones,
            text="Salir",
            command=self.root.quit,
            style="Secondary.TButton",
            cursor="hand2",
            image=self.icono_salir,
            compound=tk.LEFT,
        )
 
        boton_inicio.place(relx=0.2, rely=0.2, anchor="w")
        boton_Prediccion.place(relx=0.2, rely=0.4, anchor="w")
        boton_sobre_nosotros.place(relx=0.2, rely=0.6, anchor="w")
        boton_salir.place(relx=0.2, rely=0.8, anchor="w")

    def ventana_inicio(self):
        """Muestra la pantalla de inicio."""
        self.actualizando_datos = False  # Controlar si la actualización está activa
        self.frames_categorias = {}  # Almacenar los frames de las categorías
        self.canvas_graficos = {}  # Almacenar los canvas de los gráficos
        self.limpiar_contenedor()

        # Fondo de imagen
        try:
            fondo = Image.open("BenchmarkSoon/Media/modelo1.png").resize((576, 768), Image.LANCZOS)
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
            tb.Messagebox.show_error(title="Error", message=f"No se pudo cargar la imagen de fondo: {e}")
            return

        # Título
        label_titulo = tb.Label(
            self.contenedor,
            text="Athen-IA",
            **ESTILO_LABEL_TITULO,
        )
        label_titulo.pack(pady=20)

        self.icono_analisis=ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/analisis.png").resize((30, 30)))

        # Botón para ir al análisis
        boton_analizar = tb.Button(
            self.contenedor,
            text="Analizar",
            style="Primary.TButton",
            cursor="hand2",
            command=self.ventana_analisis,
            image=self.icono_analisis,
            compound=tk.LEFT,
        )
        
        boton_analizar.place(relx=0.5, rely=0.8, anchor="center")
        self._crear_botones_navegacion()

    def verificar_conexion_internet(self):
        """Verifica si hay conexión a Internet."""
        try:
            # Intentar hacer una solicitud a un servidor confiable
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False
     

    def actualizar_datos(self):
     """Actualiza los datos del análisis sin borrar los botones ni el fondo."""
     if not self.actualizando_datos:
        return  # Detener la actualización si no está activa

     try:
        # Obtener nuevos datos (ya son listas de valores)
        self.info_procesador = obtener_info_procesador()
        self.info_ram = obtener_info_ram()
        self.info_disco = obtener_info_disco()
        self.info_gpu = obtener_info_gpu()

        # Verificar que los frames de las categorías existan
        if not hasattr(self, "frames_categorias"):
            print("Error: Los frames de las categorías no se han creado correctamente.")
            return

        # Actualizar gráficos y datos
        self.actualizar_grafico("Uso del CPU (%)", self.info_procesador, crear_grafico_cpu(self.info_procesador))
        self.actualizar_grafico("RAM", self.info_ram, crear_grafico_ram(self.info_ram))
        self.actualizar_grafico("Disco", self.info_disco, crear_grafico_disco(self.info_disco))

        if "No disponible" in self.info_gpu.values():
            self.actualizar_grafico("GPU", {"GPU": "No se detectó ninguna GPU en este sistema"}, crear_grafico_gpu(self.info_gpu))
        else:
            self.actualizar_grafico("GPU", self.info_gpu, crear_grafico_gpu(self.info_gpu))

        # Volver a ejecutar la función después de 2000ms (2 segundos)
        self.root.after(2000, self.actualizar_datos)

     except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar los datos: {e}")

    def actualizar_grafico(self, categoria, datos, grafico):
        """Actualiza el gráfico y los datos en el frame correspondiente."""
        frame = self.frames_categorias[categoria]

        # Limpiar solo los widgets de datos y gráficos, no el frame completo
        for widget in frame.winfo_children():
            if widget not in [self.canvas_graficos.get(categoria)]:  # Evitar destruir el canvas del gráfico
                widget.destroy()

        # Mostrar los datos en el frame
        label_datos = tk.Label(frame, text=str(datos))
        label_datos.pack()

        # Actualizar el gráfico
        if categoria in self.canvas_graficos:
            self.canvas_graficos[categoria].get_tk_widget().destroy()  # Eliminar el canvas anterior

        canvas = FigureCanvasTkAgg(grafico, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas_graficos[categoria] = canvas  # Guardar el nuevo canvas


    def ventana_analisis(self):
        """Configura la ventana de análisis con los frames y botones necesarios."""
        self.limpiar_contenedor()

        # Cargar y mostrar el fondo
        fondo = Image.open("BenchmarkSoon/Media/modelo2.png").resize((576, 768), Image.LANCZOS)
        fondo_tk = ImageTk.PhotoImage(fondo)

        ventana_ancho = self.root.winfo_width()
        ventana_alto = self.root.winfo_height()
        fondo_x = (ventana_ancho - 576) // 2
        fondo_y = (ventana_alto - 768) // 2

        label_fondo = tk.Label(self.contenedor, image=fondo_tk)
        label_fondo.image = fondo_tk
        label_fondo.place(x=fondo_x, y=fondo_y, width=576, height=768)

        # Crear los frames para cada categoría
        self.frames_categorias = {
            "Uso del CPU (%)": tk.Frame(self.contenedor, width=50, height=50),
            "RAM": tk.Frame(self.contenedor, width=50, height=50),
            "Disco": tk.Frame(self.contenedor, width=50, height=50),
            "GPU": tk.Frame(self.contenedor, width=50, height=50),
        }

        # Posicionar los frames
        self.frames_categorias["Uso del CPU (%)"].place(x=50, y=15)
        self.frames_categorias["RAM"].place(x=900, y=60)
        self.frames_categorias["Disco"].place(x=900, y=420)
        self.frames_categorias["GPU"].place(x=80, y=430)

        # Iniciar actualización de datos
        self.actualizando_datos = True
        self.actualizar_datos()

        # Botón de consejo
        self.boton_consejo = tk.Button(
            self.contenedor,
            text="Dame un consejo Atenea",
            command=self.verificar_y_redirigir,
            cursor="hand2",
        )
        self.boton_consejo.place(relx=0.5, rely=0.8, anchor="center")

        # Botón de regresar
        self.boton_regresar = tb.Button(
            self.contenedor,
            text="Regresar",
            command=self.ventana_inicio,
            style="Secondary.TButton",
            cursor="hand2",
            image=self.icono_regresar,
            compound=tk.LEFT,
        )
        self.boton_regresar.place(relx=0.1, rely=0.9, anchor="center")
        

    def verificar_y_redirigir(self):
        """Verifica la conexión a Internet y redirige o muestra un mensaje."""
        if self.verificar_conexion_internet():
            self.ventana_consejo()  # Redirigir a la siguiente ventana
        else:
            messagebox.showwarning(
                "Sin conexión a Internet",
                "No hay conexión a Internet. Inténtalo de nuevo más tarde.",
            )

    def mostrar_categoria(self, categoria, datos, grafico, posicion, ancho, alto):
        """Muestra una categoría con su frame y labels correspondientes."""
        x, y = posicion

        # Crear el frame para la categoría
        frame_categoria = tb.Labelframe(
            self.contenedor,
            text=categoria,
            padding=10,
            bootstyle="primary",
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

        # Mostrar gráfico
        canvas = FigureCanvasTkAgg(grafico, master=frame_categoria)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    def ventana_consejo(self):
        self.actualizando_datos = False
        self.limpiar_contenedor()
         
        # Frame principal para dividir la ventana en dos partes
        frame_principal = tb.Frame(self.contenedor)
        frame_principal.pack(fill=BOTH, expand=True, padx=0.8, pady=0.8)

        # Configurar el grid en el frame principal
        frame_principal.grid_rowconfigure(0, weight=1)  # Fila 0 ocupa todo el espacio vertical
        frame_principal.grid_columnconfigure(0, weight=2)  # Columna 0 (consejo) ocupa 2/3 del espacio
        frame_principal.grid_columnconfigure(1, weight=1)  # Columna 1 (chatbot) ocupa 1/3 del espacio


        # Frame para el lado izquierdo (consejo)
        frame_izquierdo = tb.Frame(frame_principal)
        frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=0.8, pady=0.8)

        # Frame para el lado derecho (chatbot)
        frame_derecho = tb.Frame(frame_principal)
        frame_derecho.grid(row=0, column=1, sticky="nsew", padx=0.8, pady=0.8)

        try:
            # Generar el prompt y obtener el consejo
            prompt = generar_prompt_personalizado(
                self.info_procesador,
                self.info_ram,
                self.info_disco,
                self.info_gpu,
            )
            consejo = obtener_consejo_ia(prompt)

            
            # Aplicar estilo al título del consejo
            label_consejo = tb.Label(
                frame_izquierdo,
                text="Consejo de Optimización:",
                **ESTILO_LABEL_TITULO,
            )
            label_consejo.pack(pady=10)

            # Convertir el consejo a HTML
            consejo_html = markdown.markdown(consejo)

            # Mostrar el consejo en formato HTML
            html_label = HTMLLabel(frame_izquierdo, html=consejo_html)
            html_label.pack(fill="both", expand=True, padx=10,pady=10)

        except Exception as e:
            showerror("Error", f"Error al obtener consejo de IA: {e}")

        # Frame para el chatbot en el lado derecho
        self.chatbot_seccion(frame_derecho)

        # Frame para los botones de volver y salir en la parte inferior
        frame_botones = tb.Frame(self.contenedor)
        frame_botones.pack(fill=BOTH, padx=10, pady=10)

        # Aplicar estilo secundario al botón "Volver al inicio"
        boton_volver = tb.Button(
            frame_botones,
            text="Volver al inicio",
            command=self.ventana_inicio,
            style="Secondary.TButton",
            cursor="hand2",
            image=self.icono_regresar,
            compound=tk.LEFT,
        )
        boton_volver.pack(side=LEFT, padx=5)

        # Aplicar estilo secundario al botón "Salir"
        boton_salir = tb.Button(
            frame_botones,
            text="Salir",
            command=self.root.quit,
            style="Secondary.TButton",
            cursor="hand2",
            image=self.icono_salir,
            compound=tk.LEFT,
        )
        boton_salir.pack(side=RIGHT, padx=5)

    def chatbot_seccion(self, frame_chatbot):
        """Agrega la sección de chatbot a la ventana."""
        frame_chat = tb.Labelframe(
            frame_chatbot,
            text="Chatbot de Optimización",
            padding=9,
            bootstyle="primary"
        )
        frame_chat.pack(fill=BOTH, expand=True, padx=3, pady=5)

        # Pregunta inicial
        label_pregunta = tb.Label(
            frame_chat,
            text="¿Necesitas algo en especial?",
            **ESTILO_LABEL_TITULO
        )
        label_pregunta.pack(pady=5)

        # Opciones predefinidas
        self.seleccion = tb.StringVar(value="Otro")
        opciones = ["Optimizar para jugar", "Optimizar para programar", "Otro"]

        for opcion in opciones:
            tb.Radiobutton(
                frame_chat,
                text=opcion,
                variable=self.seleccion,
                value=opcion
            ).pack(anchor="w")


        # Botón para obtener sugerencias
        boton_obtener = tb.Button(
            frame_chat,
            text="Obtener Sugerencias",
            command=self.obtener_sugerencias
        )
        boton_obtener.pack(pady=10)

        # Área de salida para las sugerencias
        self.texto_respuesta = HTMLLabel(frame_chat, html="")  # Usar HTMLLabel en lugar de Text
        self.texto_respuesta.pack(fill="both", expand=True, padx=5, pady=15)


        # Frame para el input del prompt personalizado (se ubicará antes del cuadro de salida)
        self.frame_prompt = tb.Frame(frame_chat)

        # Entrada para un prompt personalizado
        label_prompt = tb.Label(
            self.frame_prompt,
            text="Detalla lo que necesitas:",
            **ESTILO_LABEL_PROMPTPERSONAL
        )
        label_prompt.pack(pady=5)

        self.entry_prompt = tb.Entry(self.frame_prompt, width=50)
        self.entry_prompt.pack(pady=5)

        # Vincular cambios en la selección a la actualización de la visibilidad del input
        self.seleccion.trace_add("write", lambda *args: self.actualizar_visibilidad_prompt())

        # Aplicar visibilidad inicial
        self.actualizar_visibilidad_prompt()

    def actualizar_visibilidad_prompt(self):
        """Muestra el input antes del cuadro de salida si la opción seleccionada es 'Otro'."""
        if self.seleccion.get() == "Otro":
            self.frame_prompt.pack(before=self.texto_respuesta, pady=5)  # Ubicarlo antes de la salida de texto
        else:
            self.frame_prompt.pack_forget()  # Ocultar si no es "Otro"


    def obtener_sugerencias(self):
        opcion = self.seleccion.get()
        prompt_usuario = self.entry_prompt.get().strip()

        if opcion == "Otro":
            if prompt_usuario:
                # Generar el prompt personalizado del usuario
                prompt_combinado = generar_prompt_personalizado(
                    self.info_procesador,
                    self.info_ram,
                    self.info_disco,
                    self.info_gpu
                ) + f"\n\n{prompt_usuario}"
                self.generar_sugerencias(prompt_combinado)
            else:
                showerror("Advertencia", "Por favor, ingresa un prompt personalizado.")
        else:
            if opcion == "Optimizar para jugar":
                prompt_jugar = generar_prompt_personalizado(
                    self.info_procesador,
                    self.info_ram,
                    self.info_disco,
                    self.info_gpu
                )
                prompt_jugar += "\n\nDe acuerdo al analisis del sistema quiero suguerencias cortas, especificas y de mucho valor para optimizar la PC para jugar y que vaya con fluides."
                self.generar_sugerencias(prompt_jugar)
            elif opcion == "Optimizar para programar":
                prompt_programar = generar_prompt_personalizado(
                    self.info_procesador,
                    self.info_ram,
                    self.info_disco,
                    self.info_gpu
                )
                prompt_programar += "\n\nDe acuerdo al analisis del sistema quiero suguerencias cortas, especificas y de mucho valor para optimizar la PC para Programas y siguiere para tres tipos de lenguajes python Java C# para que obtenga lo recursos necesarios para programar ."
                self.generar_sugerencias(prompt_programar)

    def generar_sugerencias(self, prompt_usuario):
        """Genera sugerencias personalizadas basadas en el prompt del usuario."""
        sugerencias_md = obtener_consejo_ia(prompt_usuario)
        # Convertir Markdown a HTML
        sugerencias_html = markdown.markdown(sugerencias_md)
        # Mostrar las sugerencias en formato HTML
        self.texto_respuesta.set_html(sugerencias_html)

    def mostrar_predicciones(self):
     self.actualizando_datos = False
     self.limpiar_contenedor()

     try:
        # Verificar disponibilidad de la GPU
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("GPU disponible")
        else:
            device = torch.device("cpu")
            print("GPU no disponible, usando CPU")

        # Crear un Canvas y un Scrollbar
        canvas = tk.Canvas(self.contenedor)
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configurar el Canvas para que sea desplazable
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Empaquetar el Canvas y el Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cargar y preparar datos históricos
        df_procesador, df_ram, df_disco, df_gpu = preparar_datos_historicos()

        # Verificar que existan datos suficientes para las predicciones
        if df_ram.empty or df_procesador.empty or df_disco.empty:
            messagebox.showwarning("Advertencia", "No hay suficientes datos para generar predicciones.")
            self.ventana_inicio()
            return

        # Convertir fechas a datetime
        df_ram["fecha"] = pd.to_datetime(df_ram["fecha"], errors='coerce')
        df_procesador["fecha"] = pd.to_datetime(df_procesador["fecha"], errors='coerce')
        df_disco["fecha"] = pd.to_datetime(df_disco["fecha"], errors='coerce')

        # Convertir todos los nombres de columnas a minúsculas
        df_ram.columns = [col.lower() for col in df_ram.columns]
        df_procesador.columns = [col.lower() for col in df_procesador.columns]
        df_disco.columns = [col.lower() for col in df_disco.columns]

        # Verificar y renombrar columnas según corresponda
        if "uso_ram" not in df_ram.columns and "uso de ram (%)" in df_ram.columns:
            df_ram.rename(columns={"uso de ram (%)": "uso_ram"}, inplace=True)
        if "uso_cpu" not in df_procesador.columns and "uso del cpu (%)" in df_procesador.columns:
            df_procesador.rename(columns={"uso del cpu (%)": "uso_cpu"}, inplace=True)

        # Preparar series temporales para ARIMA
        serie_ram = df_ram.set_index("fecha")["uso_ram"]
        serie_procesador = df_procesador.set_index("fecha")["uso_cpu"]
        serie_disco = df_disco.set_index("fecha")["uso_disco"]

        # Entrenar modelos ARIMA
        modelo_ram = entrenar_modelo_arima(serie_ram, orden=(1, 1, 1))  # Ajusta (p, d, q) según sea necesario
        modelo_procesador = entrenar_modelo_arima(serie_procesador, orden=(1, 1, 1))
        modelo_disco = entrenar_modelo_arima(serie_disco, orden=(1, 1, 1))

        # Hacer predicciones futuras
        predicciones_ram = hacer_predicciones_arima(modelo_ram, pasos_futuros=6)
        predicciones_procesador = hacer_predicciones_arima(modelo_procesador, pasos_futuros=6)
        predicciones_disco = hacer_predicciones_arima(modelo_disco, pasos_futuros=6)

        # Crear DataFrames para las predicciones
        df_ram_pred = pd.DataFrame({
            "fecha": pd.date_range(start=serie_ram.index[-1] + pd.Timedelta(days=1), periods=6),
            "uso_ram": predicciones_ram
        })
        df_procesador_pred = pd.DataFrame({
            "fecha": pd.date_range(start=serie_procesador.index[-1] + pd.Timedelta(days=1), periods=6),
            "uso_cpu": predicciones_procesador
        })
        df_disco_pred = pd.DataFrame({
            "fecha": pd.date_range(start=serie_disco.index[-1] + pd.Timedelta(days=1), periods=6),
            "uso_disco": predicciones_disco
        })

        # Títulos y estilos
        label_titulo = ttk.Label(
            scrollable_frame,
            text="Predicciones de Rendimiento",
            **ESTILO_LABEL_TITULO,
        )
        label_titulo.pack(pady=20, fill="x", anchor="center")

        # Frame para los gráficos en 2 columnas
        frame_graficos = ttk.Frame(scrollable_frame)
        frame_graficos.pack(fill="both", expand=True, pady=10)

        # Configurar 2 columnas con espaciado
        frame_graficos.columnconfigure(0, weight=1, pad=15)
        frame_graficos.columnconfigure(1, weight=1, pad=15)

        # Lista de gráficos a generar
        graficos = [
            (serie_ram, predicciones_ram, "Uso de RAM (%)"),
            (serie_procesador, predicciones_procesador, "Uso del Procesador (%)"),
            (serie_disco, predicciones_disco, "Uso del Disco (%)")
        ]

        # Generar gráficos en grid dinámico
        for i, (serie, pred, titulo) in enumerate(graficos):
            row = i // 2  # Dos gráficos por fila
            col = i % 2

            # Frame contenedor para cada gráfico con borde
            contenedor_grafico = ttk.Frame(frame_graficos, relief='groove', borderwidth=2)
            contenedor_grafico.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Generar gráfico
            interpretacion = crear_grafico_arima(serie, pred, titulo, contenedor_grafico)

            # Crear un ScrolledText para la interpretación
            texto_interpretacion = ScrolledText(contenedor_grafico, wrap="word", height=5, width=50, state="normal")
            texto_interpretacion.insert(tk.END, f"{titulo}:\n{interpretacion}")
            texto_interpretacion.config(state="disabled")
            texto_interpretacion.pack(pady=10, fill="x", padx=10)

        # Si no hay datos de GPU, mostrar un mensaje en lugar del gráfico
        if df_gpu.empty:
            row = len(graficos) // 2  # Calcular la fila correspondiente
            col = len(graficos) % 2

            # Frame contenedor para el mensaje de GPU no disponible
            contenedor_mensaje = ttk.Frame(frame_graficos, relief='groove', borderwidth=2)
            contenedor_mensaje.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Mostrar mensaje de GPU no disponible
            label_mensaje = ttk.Label(contenedor_mensaje, text="GPU no disponible", **ESTILO_LABEL_TITULO)
            label_mensaje.pack(pady=20, fill="both", expand=True)


        self._crear_botones_navegacion()
        

        # Centrar el contenido en el scrollable_frame
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Centrar el contenido horizontalmente
        canvas_width = canvas.winfo_width()
        frame_width = scrollable_frame.winfo_width()
        if frame_width < canvas_width:
            canvas.create_window((canvas_width // 1.7, 0), window=scrollable_frame, anchor="n")

     except Exception as e:
        messagebox.showerror("Error", f"Error al generar predicciones: {e}")

    def ventana_sobre_nosotros(self):
        self.limpiar_contenedor()
        #Iconos
        self.imagen_git = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/git.png").resize((60, 60)))
        self.icono_web = ImageTk.PhotoImage(Image.open("BenchmarkSoon/Media/web.png").resize((20, 20)))

        label_titulo = tb.Label(
            self.contenedor,
            text="Sobre Nosotros",
            **ESTILO_LABEL_TITULO,
        )
        label_titulo.pack(pady=10)
        
        frame_Progra1 = tb.Labelframe(
            self.contenedor,
            text="Erick290211",
            padding=10,
            bootstyle="primary",
        )
        frame_Progra1.place(x=350, y=50, width=320, height=320)

        # Descripción de Erick
        label_descripcion1 = tb.Label(
            frame_Progra1,
            text="- Desarrollador backend\n"+
                "- Desarrollador Frontend\n"+
                "- Tester/QA\n"
                "Si deseas saber mas acerca de Erick, te dejamos su GitHub, dale click en el logo.",
            **ESTILO_LABEL_TEXTO1,
        )
        label_descripcion1.pack(pady=10)

        label_redes1 = tb.Label(
            frame_Progra1,
            text="GitHub",
            font=("Arial", 14),
            anchor="center",
            foreground="black",
        )
        label_redes1.pack()
        
        boton_github1 = tk.Label(
            frame_Progra1,
            image=self.imagen_git,
            cursor="hand2",
        )
        boton_github1.pack(pady=10)
        boton_github1.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Erick290911"))

        frame_Progra2 = tb.Labelframe(
            self.contenedor,
            text="Jettro12",
            padding=10,
            bootstyle="primary",
        )
        frame_Progra2.place(x=1000, y=50, width=320, height=320)

        # Descripción de Jair
        label_descripcion2 = tb.Label(
            frame_Progra2,
            text="- Desarrollador backend\n"+
                "- Desarrollador Frontend\n"+
                "- Arquitecto de Software\n"+
                "Si deseas saber mas acerca de Jair, te dejamos su GitHub, dale click en el logo.",
            **ESTILO_LABEL_TEXTO1,
        )
        label_descripcion2.pack(pady=10)

        label_redes2 = tb.Label(
            frame_Progra2,
            text="GitHub",
            font=("Arial", 14),
            anchor="center",
            foreground="black",
        )
        label_redes2.pack()
        
        boton_github2 = tk.Label(
            frame_Progra2,
            image=self.imagen_git,
            cursor="hand2",
        )
        boton_github2.pack(pady=10)
        boton_github2.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Jettro12"))

        frame_Progra3 = tb.Labelframe(
            self.contenedor,
            text="CupidoRam",
            padding=10,
            bootstyle="primary",
        )
        frame_Progra3.place(x=680, y=400, width=320, height=320)

        # Descripción de Ramses
        label_descripcion3 = tb.Label(
            frame_Progra3,
            text="- Desarrollador backend\n"+
                "- Desarrollador Frontend\n"+
                "- Diseñador UX/UI\n"+
                "Si deseas saber mas acerca de Ramses, te dejamos su GitHub, dale click en el logo.",
            **ESTILO_LABEL_TEXTO1,
        )
        label_descripcion3.pack(pady=10)

        label_redes3 = tb.Label(
            frame_Progra3,
            text="GitHub",
            font=("Arial", 14),
            anchor="center",
            foreground="black",
        )
        label_redes3.pack()

        boton_github3 = tk.Label(
            frame_Progra3,
            image=self.imagen_git,
            cursor="hand2",
        )
        boton_github3.pack(pady=10)
        boton_github3.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/RamCupido"))

        boton_repos = tb.Button(
            self.contenedor,
            text="Ir al Repositorio",
            style="Primary.TButton",
            cursor="hand2",
            command=self.repositorio,
            image=self.icono_web,
            compound=tk.LEFT,
        )
        boton_repos.place(relx=0.9, rely=0.8, anchor="center")
        self._crear_botones_navegacion()

    def repositorio (self):
        webbrowser.open('https://github.com/Jettro12/BenchmarkSoon')