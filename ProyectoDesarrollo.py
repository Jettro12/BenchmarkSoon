import psutil
import platform
from datetime import timedelta
import clr  # Necesario para usar OpenHardwareMonitor
import os
import streamlit as st
 
 # Ruta al DLL de OpenHardwareMonitor
dll_path = r"C:\Users\casa\Downloads\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"No se encontró el archivo DLL en la ruta: {dll_path}")

# Cargar la biblioteca OpenHardwareMonitor
clr.AddReference(dll_path)
from OpenHardwareMonitor import Hardware


# Función para obtener las temperaturas usando OpenHardwareMonitor
def obtener_temperaturas_hardware():
    """
    Obtiene las temperaturas del hardware utilizando OpenHardwareMonitor.
    """
    try:
        computer = Hardware.Computer()
        computer.CPUEnabled = True  # Activa el monitoreo de la CPU
        computer.Open()

        temperaturas = {}
        for hardware in computer.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature:
                    temperaturas[sensor.Name] = sensor.Value
        return temperaturas
    except Exception as e:
        return {"Error": f"No se pudo obtener la temperatura: {e}"}


# Función para obtener la información del sistema
def obtener_info_sistema():
    """
    Recopila información del sistema como procesador, RAM, disco y tiempo de uso.
    """
    ram_info = psutil.virtual_memory()
    disco_info = psutil.disk_usage('/')
    return {
        "Procesador": platform.processor(),
        "RAM Total (GB)": round(ram_info.total / (1024 ** 3), 2),
        "RAM Usada (GB)": round(ram_info.used / (1024 ** 3), 2),
        "RAM Libre (GB)": round(ram_info.available / (1024 ** 3), 2),
        "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
        "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
        "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
        "Disco Usado (%)": round(disco_info.percent, 2),
        "Tiempo de Uso del Sistema": str(timedelta(seconds=psutil.boot_time())),
    }