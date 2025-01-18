import clr
import os
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

# Configuración de la API Key
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")