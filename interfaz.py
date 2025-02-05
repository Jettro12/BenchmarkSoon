import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import tkinter as tk
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
    ESTILO_TEXTO_CONSEJO,
    ESTILO_LABEL_CATEGORIA,
    ESTILO_LABEL_PROMPTPERSONAL
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

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Athen-IA")
        # Configuración inicial con ttkbootstrap
        self.style = tb.Style("vapor")  # Cambia el tema aquí según tus preferencias
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

    def ventana_inicio(self):
        """Muestra la pantalla de inicio."""
        self.limpiar_contenedor()

        # Fondo de imagen
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
            tb.Messagebox.show_error(title="Error", message=f"No se pudo cargar la imagen de fondo: {e}")
            return

        # Título
        label_titulo = tb.Label(
            self.contenedor,
            text="Athen-IA",
            **ESTILO_LABEL_TITULO,
        )
        label_titulo.pack(pady=20)

        # Botón para ir al análisis
        boton_analizar = tb.Button(
            self.contenedor,
            text="Analizar",
            style="Primary.TButton",
            command=self.ventana_analisis,
        )
        boton_Prediccion = tb.Button(
            self.contenedor,
            text="Predicciones",
            command=self.mostrar_predicciones,
            style="Primary.TButton",  # Aplicar estilo primario
        )
         
        boton_analizar.place(relx=0.5, rely=0.8, anchor="center")
        boton_Prediccion.place(relx=0.5, rely=0.9, anchor="center")

    def ventana_analisis(self):
        """Muestra la pantalla de análisis del sistema."""
        self.limpiar_contenedor()

        try:
            # Obtener información del sistema
            self.info_procesador = obtener_info_procesador()
            self.info_ram = obtener_info_ram()
            self.info_disco = obtener_info_disco()
            self.info_gpu = obtener_info_gpu()
            
            # Almacenar los datos en la base de datos al presionar "Analizar"
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

            # Mostrar gráficos y datos
            fig1 = crear_grafico_cpu(self.info_procesador)
            self.mostrar_categoria(
                categoria="Frecuencias CPU",
                datos=self.info_procesador,
                grafico=fig1,
                posicion=(30, 15),
                ancho=470,
                alto=370,
            )

            # Configuración para el frame de la RAM
            fig3 = crear_grafico_ram(self.info_ram)
            self.mostrar_categoria(
                categoria="RAM",
                datos=self.info_ram,
                grafico=fig3,
                posicion=(1100, 15),
                ancho=200,
                alto=280,
            )

            # Configuración para el frame del Disco
            fig4 = crear_grafico_disco(self.info_disco)
            self.mostrar_categoria(
                categoria="Disco",
                datos=self.info_disco,
                grafico=fig4,
                posicion=(1100, 405),
                ancho=210,
                alto=280,
            )

            # Configuración para el frame de la GPU
            fig5 = crear_grafico_gpu(self.info_gpu)
            if "No disponible" in self.info_gpu.values():
                self.mostrar_categoria(
                    categoria="GPU",
                    datos={"GPU": "No se detecto ninguna GPU en este sistema"},
                    grafico=fig5,
                    posicion=(30, 405),
                    ancho=470,
                    alto=280,
                )
            else:
                self.mostrar_categoria(
                    categoria="GPU",
                    datos=self.info_gpu,
                    grafico=fig5,
                    posicion=(30, 405),
                    ancho=470,
                    alto=280,
                )

            # Aplicar estilo al botón de análisis
            boton_consejo = tb.Button(
                self.contenedor,
                text="Dame un consejo Atenea",
                command=self.ventana_consejo,
                style="Primary.TButton",
            )
            boton_consejo.place(relx=0.5, rely=0.8, anchor="center")
        except Exception as e:
            showerror("Error", f"No se pudo completar el análisis: {e}")

    def mostrar_categoria(self, categoria, datos, grafico, posicion, ancho, alto):
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

        # Mostrar gráfico
        canvas = FigureCanvasTkAgg(grafico, master=frame_categoria)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    def ventana_consejo(self):
        self.limpiar_contenedor()

        # Frame principal para dividir la ventana en dos partes
        frame_principal = tb.Frame(self.contenedor)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para el lado izquierdo (consejo)
        frame_izquierdo = tb.Frame(frame_principal)
        frame_izquierdo.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para el lado derecho (chatbot)
        frame_derecho = tb.Frame(frame_principal)
        frame_derecho.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        try:
            # Generar el prompt y obtener el consejo
            prompt = generar_prompt_personalizado(
                self.info_procesador,
                self.info_ram,
                self.info_disco,
                self.info_gpu,
            )
            consejo = obtener_consejo_ia(prompt)

            # Crear un Canvas para el scroll en el lado izquierdo
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

            # Aplicar estilo al título del consejo
            label_consejo = tb.Label(
                frame_consejo,
                text="Consejo de Optimización:",
                **ESTILO_LABEL_TITULO,
            )
            label_consejo.pack(pady=10)

            # Aplicar estilo al texto del consejo
            texto_consejo = tb.Label(
                frame_consejo,
                text=consejo,
                **ESTILO_TEXTO_CONSEJO,
            )
            texto_consejo.pack(pady=10)

        except Exception as e:
            showerror("Error", f"Error al obtener consejo de IA: {e}")

        # Frame para el chatbot en el lado derecho
        self.chatbot_seccion(frame_derecho)

        # Frame para los botones de volver y salir en la parte inferior
        frame_botones = tb.Frame(self.contenedor)
        frame_botones.pack(fill=X, padx=10, pady=10)

        # Aplicar estilo secundario al botón "Volver al inicio"
        boton_volver = tb.Button(
            frame_botones,
            text="Volver al inicio",
            command=self.ventana_inicio,
            style="Secondary.TButton",
        )
        boton_volver.pack(side=LEFT, padx=5)

        # Aplicar estilo secundario al botón "Salir"
        boton_salir = tb.Button(
            frame_botones,
            text="Salir",
            command=self.root.quit,
            style="Secondary.TButton",
        )
        boton_salir.pack(side=RIGHT, padx=5)

    def chatbot_seccion(self, frame_chatbot):
        """Agrega la sección de chatbot a la ventana."""
        frame_chat = tb.Labelframe(
            frame_chatbot,
            text="Chatbot de Optimización",
            padding=10,
            bootstyle="secondary"
        )
        frame_chat.pack(fill=BOTH, expand=True, padx=10, pady=10)

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

        # Entrada para un prompt personalizado
        label_prompt = tb.Label(
            frame_chat,
            text="O escribe un prompt personalizado:",
            **ESTILO_LABEL_PROMPTPERSONAL
        )
        label_prompt.pack(pady=5)

        self.entry_prompt = tb.Entry(frame_chat, width=50)
        self.entry_prompt.pack(pady=5)

        # Botón para obtener sugerencias
        boton_obtener = tb.Button(
            frame_chat,
            text="Obtener Sugerencias",
            command=self.obtener_sugerencias
        )
        boton_obtener.pack(pady=10)

        # Área de salida para las sugerencias
        self.texto_respuesta = tb.Text(frame_chat, wrap="word", height=10, width=80, state="disabled")
        self.texto_respuesta.pack(pady=10)

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
        sugerencias = obtener_consejo_ia(prompt_usuario)
        self.texto_respuesta.config(state="normal")
        self.texto_respuesta.delete(1.0, END)
        self.texto_respuesta.insert(END, sugerencias)
        self.texto_respuesta.config(state="disabled")

    def mostrar_predicciones(self):
        self.limpiar_contenedor()

        try:
            # Crear un Canvas y un Scrollbar
            canvas = tk.Canvas(self.contenedor)
            scrollbar = tb.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
            scrollable_frame = tb.Frame(canvas)

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
            label_titulo = tb.Label(
                scrollable_frame,
                text="Predicciones de Rendimiento",
                **ESTILO_LABEL_TITULO,
            )
            label_titulo.pack(pady=20, fill="x", anchor="center")

            # Frame para los gráficos en 2 columnas
            frame_graficos = tb.Frame(scrollable_frame)
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

            interpretacion_completa = "--- Predicciones de Rendimiento ---\n\n"

            # Generar gráficos en grid dinámico
            for i, (serie, pred, titulo) in enumerate(graficos):
                row = i // 2  # Dos gráficos por fila
                col = i % 2

                # Frame contenedor para cada gráfico con borde
                contenedor_grafico = tb.Frame(frame_graficos, relief='groove', borderwidth=2)
                contenedor_grafico.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Generar gráfico
                interpretacion = crear_grafico_arima(serie, pred, titulo, contenedor_grafico)
                interpretacion_completa += f"{titulo}:\n{interpretacion}\n\n"

            # Área de texto desplazable para interpretación
            texto_interpretacion = ScrolledText(scrollable_frame, wrap="word", height=10, width=90, state="normal")
            texto_interpretacion.insert(tk.END, interpretacion_completa)
            texto_interpretacion.config(state="disabled")
            texto_interpretacion.pack(pady=10, fill="x", padx=10)

            # Botón para regresar al análisis
            boton_venanalizar = tb.Button(
                self.contenedor,
                text="Volver al Inicio",
                command=self.ventana_inicio,
                style="Primary.TButton",
            )
            boton_venanalizar.place(relx=0.0, rely=0.9, anchor="w")

            # Centrar el contenido en el scrollable_frame
            scrollable_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            # Centrar el contenido horizontalmente
            canvas_width = canvas.winfo_width()
            frame_width = scrollable_frame.winfo_width()
            if frame_width < canvas_width:
                canvas.create_window((canvas_width // 2, 0), window=scrollable_frame, anchor="n")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar predicciones: {e}")
