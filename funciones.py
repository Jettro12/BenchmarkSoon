import os
import psutil
import platform
import clr
from tkinter import Tk
from tkinter.messagebox import showerror
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from dotenv import load_dotenv
import google.generativeai as genai

# --- Configuración y Carga de Dependencias ---
# Ruta al DLL de OpenHardwareMonitor
DLL_PATH = r"C:\Users\ErickMau\Downloads\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
if not os.path.exists(DLL_PATH):
    raise FileNotFoundError(f"No se encontró el archivo DLL en la ruta: {DLL_PATH}")
clr.AddReference(DLL_PATH)
from OpenHardwareMonitor import Hardware

# Cargar configuración desde .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("La clave API_KEY no está configurada en el archivo .env.")

genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel("gemini-2.0-flash-exp")

GB = 1024 ** 3  # Conversión de bytes a GB

# --- Funciones de Información del Sistema ---
def obtener_info_procesador():
    try:
        return {
            "Procesador": platform.processor(),
            "Núcleos Físicos": psutil.cpu_count(logical=False),
            "Núcleos Lógicos": psutil.cpu_count(logical=True),
        }
    except Exception as e:
        return {"Error al obtener el procesador": str(e)}

def obtener_info_ram():
    try:
        ram = psutil.virtual_memory()
        return {
            "RAM Total": f"{ram.total / GB:.2f} GB",
            "RAM Disponible": f"{ram.available / GB:.2f} GB",
        }
    except Exception as e:
        return {"Error al obtener la RAM": str(e)}

def obtener_info_disco():
    try:
        disco = psutil.disk_usage('/')
        return {
            "Espacio Total": f"{disco.total / GB:.2f} GB",
            "Espacio Usado": f"{disco.used / GB:.2f} GB",
            "Espacio Libre": f"{disco.free / GB:.2f} GB",
        }
    except Exception as e:
        return {"Error al obtener el disco": str(e)}

def generar_prompt_personalizado():
    return (
        "Basado en el análisis del sistema, se han detectado las siguientes configuraciones: "
        "procesador, memoria RAM y espacio en disco. Sugiere optimizaciones para mejorar el rendimiento."
    )

def obtener_consejo_ia(prompt):
    try:
        respuesta = MODEL.start_chat(prompt=prompt)
        return respuesta.generations[0].text.strip()
    except Exception as e:
        return f"Error al obtener consejo de IA: {e}"