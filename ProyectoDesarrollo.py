import tkinter as tk
from tkinter import messagebox
import psutil
import platform
from datetime import timedelta
import clr  # Necesario para usar OpenHardwareMonitor
import os
#Necesarias para el api de Gemini
import requests
from dotenv import load_dotenv
from PIL import Image, ImageTk
import google.generativeai as genai

# Ruta al DLL de OpenHardwareMonitor
dll_path = r"C:\Users\ramse\Downloads\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"No se encontró el archivo DLL en la ruta: {dll_path}")

clr.AddReference(dll_path)
from OpenHardwareMonitor import Hardware


# Cargar las variables desde el archivo .env
load_dotenv()

# Obtener la API Key desde las variables de entorno
api_key = os.getenv("API_KEY")

# Configurar la API Key 
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Función para obtener información del procesador
def obtener_info_procesador():
    cpu_freq = psutil.cpu_freq()
    return {
        "Nombre": platform.processor(),
        "Frecuencia Base (GHz)": round(cpu_freq.min / 1000, 2) if cpu_freq else "No disponible",
        "Frecuencia Máxima (GHz)": round(cpu_freq.max / 1000, 2) if cpu_freq else "No disponible",
        "Frecuencia Actual (GHz)": round(cpu_freq.current / 1000, 2) if cpu_freq else "No disponible",
        "Núcleos Físicos": psutil.cpu_count(logical=False),
        "Núcleos Lógicos": psutil.cpu_count(logical=True),
    }

# Función para obtener información de la RAM

def obtener_info_ram():
    ram_info = psutil.virtual_memory()
    return {
        "RAM Total (GB)": round(ram_info.total / (1024 ** 3), 2),
        "RAM Usada (GB)": round(ram_info.used / (1024 ** 3), 2),
        "RAM Libre (GB)": round(ram_info.available / (1024 ** 3), 2),
        "Uso de RAM (%)": ram_info.percent,
    }

def obtener_infoqram():
    try:
        import wmi
        c = wmi.WMI()
        ram_info = []
        for mem in c.Win32_PhysicalMemory():
            tipo_ram_codigo = str(mem.MemoryType)
            tipo_ram = {
                "20": "DDR", "21": "DDR2", "22": "DDR2 FB-DIMM",
                "24": "DDR3", "26": "DDR4"
            }.get(tipo_ram_codigo, "Desconocido")
            ram_info.append({
                "Tipo": tipo_ram,
                "Velocidad (MHz)": mem.Speed,
                "Capacidad (GB)": round(int(mem.Capacity) / (1024 ** 3), 2)
            })
        return ram_info
    except Exception as e:
        return [{"Error": f"No se pudo obtener información de la RAM: {e}"}]

def obtener_info_disco():
    disco_info = psutil.disk_usage('/')
    return {
        "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
        "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
        "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
        "Uso de Disco (%)": disco_info.percent,
    }


# Función para obtener las temperaturas del hardware
def obtener_temperaturas_hardware():
    try:
        computer = Hardware.Computer()
        computer.CPUEnabled = True
        computer.Open()
        temperaturas = {}
        for hardware in computer.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature:
                    temperaturas[sensor.Name] = sensor.Value
        return temperaturas
    except Exception as e:
        return {"Error": f"No se pudo obtener las temperaturas: {e}"}

# Función para obtener información general del sistema
def obtener_info_sistema():
    ram_info = psutil.virtual_memory()
    disco_info = psutil.disk_usage('/')
    return {
        "Sistema Operativo": platform.system() + " " + platform.release(),
        "Arquitectura": platform.architecture()[0],
        "RAM Total (GB)": round(ram_info.total / (1024 ** 3), 2),
        "RAM Usada (GB)": round(ram_info.used / (1024 ** 3), 2),
        "RAM Libre (GB)": round(ram_info.available / (1024 ** 3), 2),
        "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
        "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
        "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
        "Disco Usado (%)": round(disco_info.percent, 2),
        "Tiempo de Uso del Sistema": str(timedelta(seconds=psutil.boot_time())),
    }

# Función para generar el prompt
def generar_prompt_personalizado():
    info_procesador = obtener_info_procesador()
    info_ram = obtener_info_ram()
    info_disco = obtener_info_disco()
    info_sistema = obtener_info_sistema()
    info_temperaturas = obtener_temperaturas_hardware()
    info_tipo_ram = obtener_infoqram()

    prompt = "He escaneado un sistema con las siguientes características:\n\n"
    prompt += (
        f"- **Procesador**: {info_procesador['Nombre']}\n"
        f"  - Frecuencia Base: {info_procesador['Frecuencia Base (GHz)']} GHz\n"
        f"  - Frecuencia Máxima: {info_procesador['Frecuencia Máxima (GHz)']} GHz\n"
        f"  - Frecuencia Actual: {info_procesador['Frecuencia Actual (GHz)']} GHz\n"
        f"  - Núcleos Físicos: {info_procesador['Núcleos Físicos']}\n"
        f"  - Núcleos Lógicos: {info_procesador['Núcleos Lógicos']}\n\n"
    )
    prompt += (
        "- **Memoria RAM**:\n"
        f"  - RAM Total: {info_ram['RAM Total (GB)']} GB\n"
        f"  - RAM Usada: {info_ram['RAM Usada (GB)']} GB\n"
        f"  - RAM Libre: {info_ram['RAM Libre (GB)']} GB\n"
        f"  - Uso de RAM: {info_ram['Uso de RAM (%)']}%\n"
    )
    if info_tipo_ram and not isinstance(info_tipo_ram[0], dict) and "Error" not in info_tipo_ram[0]:
        for idx, ram in enumerate(info_tipo_ram):
            prompt += f"  - Módulo {idx + 1}: Tipo {ram['Tipo']}, Velocidad {ram['Velocidad (MHz)']} MHz, Capacidad {ram['Capacidad (GB)']} GB\n"
    elif "Error" in info_tipo_ram[0]:
        prompt += f"  - {info_tipo_ram[0]['Error']}\n"
    prompt += (
        "- **Almacenamiento**:\n"
        f"  - Disco Total: {info_disco['Disco Total (GB)']} GB\n"
        f"  - Disco Usado: {info_disco['Disco Usado (GB)']} GB\n"
        f"  - Disco Libre: {info_disco['Disco Libre (GB)']} GB\n"
        f"  - Uso del Disco: {info_disco['Uso de Disco (%)']}%\n\n"
    )
    if info_temperaturas and "Error" not in info_temperaturas:
        prompt += "- **Temperaturas**:\n"
        for sensor, temp in info_temperaturas.items():
            prompt += f"  - {sensor}: {temp} °C\n"
        prompt += "\n"
    else:
        prompt += f"- **Temperaturas**: {info_temperaturas.get('Error', 'No disponible')}\n\n"
    prompt += (
        "- **Información General del Sistema**:\n"
        f"  - Sistema Operativo: {info_sistema['Sistema Operativo']}\n"
        f"  - Arquitectura: {info_sistema['Arquitectura']}\n"
        f"  - Tiempo de Uso del Sistema: {info_sistema['Tiempo de Uso del Sistema']}\n"
    )
    prompt += "\nPor favor, bríndame un consejo personalizado para optimizar este sistema.\n"
    return prompt
# Función para obtener consejo de la IA utilizando Gemini
def obtener_consejo_ia(prompt):
    try:
        # Llamada al modelo de Gemini con el prompt
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar el consejo: {e}"



 
# Ventana principal (Inicio)
def ventana_inicio():
    from PIL import Image, ImageTk  # Asegúrate de que solo importas lo necesario

    def abrir_analisis():
        ventana.destroy()
        ventana_analisis()

    ventana = tk.Tk()
    ventana.title("Inicio - Benchmark del Sistema")
    ventana.geometry("450x600")  # Establecer el tamaño de la ventana a 450x600
    ventana.config(bg="#1E1E2F")

    # Cargar y redimensionar la imagen de fondo
    try:
        fondo = Image.open("BenchmarkSoon\Media\Atenea.jpg")  # Cambia esto por la ruta de tu imagen de fondo
        fondo = fondo.resize((450, 600), Image.LANCZOS)  # Redimensionar usando LANCZOS
        fondo_tk = ImageTk.PhotoImage(fondo)  # Convertir a formato compatible con Tkinter
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
        return

    # Etiqueta para la imagen de fondo
    label_fondo = tk.Label(ventana, image=fondo_tk)
    label_fondo.image = fondo_tk  # Evitar que la imagen sea recolectada por el garbage collector
    label_fondo.place(relwidth=1, relheight=1)  # Ajustar la imagen al tamaño de la ventana
   
    # Etiqueta del título
    label_titulo = tk.Label(
        ventana, 
        text="Bienvenido al Benchmark del Sistema", 
        font=("Verdana", 20, "bold"), 
        pady=0.1, 
        fg="#FFD700",
        bg="#1E1E2F"
    )
    label_titulo.place(relx=0.5, rely=0.2, anchor="center")

    try:
        imagen_boton = Image.open("BenchmarkSoon\Media\Boton1.webp")  # Cambia esto por la ruta de tu imagen de fondo
        imagen_boton = imagen_boton.resize((150, 50), Image.LANCZOS)  # Redimensionar usando LANCZOS
        imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)  # Convertir a formato compatible con Tkinter
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
        return
    
    # Botón Analizar
    boton_analizar = tk.Button(
        ventana,
        image=imagen_boton_tk,
        bg="#1E1E2F",
        borderwidth=0,
        highlightthickness=0,
        command=abrir_analisis
    )
    # Posicionarlo en la parte inferior, un poco debajo de la mitad
    boton_analizar.place(relx=0.5, rely=0.90, anchor="center")

    ventana.mainloop()





# Ventana de análisis
def ventana_analisis():
    def mostrar_consejo():
        ventana.destroy()
        ventana_consejo()

    def volver_inicio():
        ventana.destroy()
        ventana_inicio()

    ventana = tk.Tk()
    ventana.title("Análisis del Sistema")
    ventana.geometry("600x400")
    ventana.configure(bg="#1E1E2F")

    # Crear un Canvas con una barra de desplazamiento vertical
    canvas = tk.Canvas(ventana)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un Frame para contener los widgets dentro del canvas
    frame_info = tk.Frame(canvas)

    # Configurar la barra de desplazamiento
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame_info, anchor="nw")

    # Agregar los elementos dentro del frame_info
    label_titulo = tk.Label(frame_info, text="Resultados del Análisis", font=("Verdana", 20, "bold"), fg="#FFD700", bg="#1E1E2F")
    label_titulo.pack(pady=20)

    info_procesador = obtener_info_procesador()
    info_ram = obtener_info_ram()
    info_disco = obtener_info_disco()

    for categoria, datos in {
        "Procesador": info_procesador,
        "RAM": info_ram,
        "Disco": info_disco,
    }.items():
        frame_categoria = tk.LabelFrame(frame_info, text=categoria, padx=10, pady=10, bg="#2E2E3E")
        frame_categoria.pack(fill="both", padx=20, pady=20, expand=True)
        for clave, valor in datos.items():
            label = tk.Label(frame_categoria, text=f"{clave}: {valor}", font=("Verdana", 14), fg="white", bg="#2E2E3E")
            label.pack(anchor="w", pady=5)

    boton_consejo = tk.Button(frame_info, text="Dame un consejo", font=("Verdana", 14), bg="#4CAF50", fg="white",
                              activebackground="#45A049", activeforeground="white", command=mostrar_consejo)
    boton_consejo.pack(pady=10)

    boton_volver = tk.Button(frame_info, text="Volver al inicio", font=("verdana", 14), bg="#F44336", fg="white",
                             activebackground="#D32F2F", activeforeground="white", command=volver_inicio)
    boton_volver.pack(pady=10)

    # Actualizar el tamaño del frame_info para ajustarse al contenido
    frame_info.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    ventana.mainloop()

# Ventana de consejos
def ventana_consejo():
    def volver_inicio():
        ventana.destroy()
        ventana_inicio()

    ventana = tk.Tk()
    ventana.title("Consejo con IA")
    ventana.geometry("400x300")

    # Crear un Canvas con una barra de desplazamiento vertical
    canvas = tk.Canvas(ventana)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un Frame para contener los widgets dentro del canvas
    frame_consejo = tk.Frame(canvas)

    # Configurar la barra de desplazamiento
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame_consejo, anchor="nw")
    
    info_procesador = obtener_info_procesador()
    info_ram = obtener_info_ram()
    info_disco = obtener_info_disco()
    info_sistema = obtener_info_sistema()
    info_temperaturas = obtener_temperaturas_hardware()
    info_tipo_ram = obtener_infoqram()
    consejo_generado = obtener_consejo_ia(
    """He escaneado un sistema con las siguientes características:

    - **Procesador**: {Nombre}
      - Frecuencia Base: {Frecuencia_Base} GHz
      - Frecuencia Máxima: {Frecuencia_Maxima} GHz
      - Frecuencia Actual: {Frecuencia_Actual} GHz
      - Núcleos Físicos: {Nucleos_Fisicos}
      - Núcleos Lógicos: {Nucleos_Logicos}

    - **Memoria RAM**:
      - RAM Total: {RAM_Total} GB
      - RAM Usada: {RAM_Usada} GB
      - RAM Libre: {RAM_Libre} GB
      - Uso de RAM: {Uso_RAM}%

    - **Almacenamiento**:
      - Disco Total: {Disco_Total} GB
      - Disco Usado: {Disco_Usado} GB
      - Disco Libre: {Disco_Libre} GB
      - Uso del Disco: {Uso_Disco}%

    - **Información General del Sistema**:
      - Sistema Operativo: {Sistema_Operativo}
      - Arquitectura: {Arquitectura}
      - Tiempo de Uso del Sistema: {Tiempo_Uso}

    Por favor, bríndame un consejo personalizado para optimizar este sistema.
    """.format(
        Nombre=info_procesador["Nombre"],
        Frecuencia_Base=info_procesador["Frecuencia Base (GHz)"],
        Frecuencia_Maxima=info_procesador["Frecuencia Máxima (GHz)"],
        Frecuencia_Actual=info_procesador["Frecuencia Actual (GHz)"],
        Nucleos_Fisicos=info_procesador["Núcleos Físicos"],
        Nucleos_Logicos=info_procesador["Núcleos Lógicos"],
        RAM_Total=info_ram["RAM Total (GB)"],
        RAM_Usada=info_ram["RAM Usada (GB)"],
        RAM_Libre=info_ram["RAM Libre (GB)"],
        Uso_RAM=info_ram["Uso de RAM (%)"],
        Disco_Total=info_disco["Disco Total (GB)"],
        Disco_Usado=info_disco["Disco Usado (GB)"],
        Disco_Libre=info_disco["Disco Libre (GB)"],
        Uso_Disco=info_disco["Uso de Disco (%)"],
        Sistema_Operativo=info_sistema["Sistema Operativo"],
        Arquitectura=info_sistema["Arquitectura"],
        Tiempo_Uso=info_sistema["Tiempo de Uso del Sistema"]
    )
    )



    label_consejo = tk.Label(frame_consejo, text=consejo_generado, font=("Verdana", 14), wraplength=380, pady=20)
    label_consejo.pack()

    boton_volver = tk.Button(frame_consejo, text="Volver al inicio", font=("verdana", 14), bg="#F44336", fg="white",
                             activebackground="#D32F2F", activeforeground="white", command=volver_inicio)
    boton_volver.pack(pady=20)

    # Actualizar el tamaño del frame_consejo para ajustarse al contenido
    frame_consejo.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    ventana.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    ventana_inicio()
