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
import google.generativeai as genai

# Ruta al DLL de OpenHardwareMonitor
dll_path = r"C:\Users\ErickMau\Downloads\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
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
    def abrir_analisis():
        ventana.destroy()
        ventana_analisis()

    ventana = tk.Tk()
    ventana.title("Inicio - Benchmark del Sistema")
    ventana.geometry("400x300")

    label_titulo = tk.Label(ventana, text="Bienvenido al Benchmark del Sistema", font=("Arial", 14), pady=20)
    label_titulo.pack()

    boton_analizar = tk.Button(ventana, text="Analizar", font=("Arial", 12), command=abrir_analisis)
    boton_analizar.pack(pady=20)

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

    frame_info = tk.Frame(ventana)
    frame_info.pack(pady=10)

    label_titulo = tk.Label(frame_info, text="Resultados del Análisis", font=("Arial", 14))
    label_titulo.pack()

    info_procesador = obtener_info_procesador()
    info_ram = obtener_info_ram()
    info_disco = obtener_info_disco()

    for categoria, datos in {
        "Procesador": info_procesador,
        "RAM": info_ram,
        "Disco": info_disco,
    }.items():
        frame_categoria = tk.LabelFrame(ventana, text=categoria, padx=10, pady=10)
        frame_categoria.pack(fill="x", padx=10, pady=5)
        for clave, valor in datos.items():
            label = tk.Label(frame_categoria, text=f"{clave}: {valor}")
            label.pack(anchor="w")

    boton_consejo = tk.Button(ventana, text="Dame un consejo", command=mostrar_consejo)
    boton_consejo.pack(pady=10)

    boton_volver = tk.Button(ventana, text="Volver al inicio", command=volver_inicio)
    boton_volver.pack(pady=10)

    ventana.mainloop()

# Ventana de consejos
def ventana_consejo():
    def volver_inicio():
        ventana.destroy()
        ventana_inicio()

    ventana = tk.Tk()
    ventana.title("Consejo con IA")
    ventana.geometry("400x300")

    # Generar un consejo utilizando la API de Gemini
    consejo_generado = obtener_consejo_ia("Dame un consejo para optimizar el rendimiento del sistema:")

    label_consejo = tk.Label(ventana, text=consejo_generado, font=("Arial", 12), wraplength=380, pady=20)
    label_consejo.pack()

    boton_volver = tk.Button(ventana, text="Volver al inicio", command=volver_inicio)
    boton_volver.pack(pady=20)

    ventana.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    ventana_inicio()
