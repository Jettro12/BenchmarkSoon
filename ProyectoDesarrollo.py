import tkinter as tk
from tkinter import messagebox
import psutil
import platform
from datetime import timedelta
import clr  # Necesario para usar OpenHardwareMonitor
import os

# Ruta al DLL de OpenHardwareMonitor
dll_path = r"C:\Users\casa\Downloads\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"No se encontró el archivo DLL en la ruta: {dll_path}")

clr.AddReference(dll_path)
from OpenHardwareMonitor import Hardware

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

# Crear la interfaz en una sola ventana
def mostrar_interfaz():
    ventana = tk.Tk()
    ventana.title("Monitor de Hardware")
    ventana.geometry("800x600")

    # Sección de Información del Sistema
    frame_sistema = tk.LabelFrame(ventana, text="Información del Sistema", padx=10, pady=10)
    frame_sistema.pack(fill="x", padx=10, pady=5)
    info_sistema = obtener_info_sistema()
    for clave, valor in info_sistema.items():
        label = tk.Label(frame_sistema, text=f"{clave}: {valor}", anchor="w", padx=10)
        label.pack(fill="x", pady=2)

    # Sección de Información del Procesador
    frame_procesador = tk.LabelFrame(ventana, text="Información del Procesador", padx=10, pady=10)
    frame_procesador.pack(fill="x", padx=10, pady=5)
    info_procesador = obtener_info_procesador()
    for clave, valor in info_procesador.items():
        label = tk.Label(frame_procesador, text=f"{clave}: {valor}", anchor="w", padx=10)
        label.pack(fill="x", pady=2)

    # Sección de Información de RAM
    frame_ram = tk.LabelFrame(ventana, text="Información de RAM", padx=10, pady=10)
    frame_ram.pack(fill="x", padx=10, pady=5)
    ram_info = obtener_info_ram()
    for ram in ram_info:
        if "Error" in ram:
            label_error = tk.Label(frame_ram, text=ram["Error"], fg="red")
            label_error.pack()
        else:
            label = tk.Label(
                frame_ram,
                text=f"Tipo: {ram['Tipo']}, Velocidad: {ram['Velocidad (MHz)']} MHz, Capacidad: {ram['Capacidad (GB)']} GB",
                anchor="w",
                padx=10
            )
            label.pack(fill="x", pady=2)

    # Sección de Temperaturas
    frame_temperaturas = tk.LabelFrame(ventana, text="Temperaturas del Hardware", padx=10, pady=10)
    frame_temperaturas.pack(fill="x", padx=10, pady=5)
    temperaturas = obtener_temperaturas_hardware()
    if "Error" in temperaturas:
        label_error = tk.Label(frame_temperaturas, text=temperaturas["Error"], fg="red")
        label_error.pack()
    else:
        for componente, temp in temperaturas.items():
            if temp is not None:
                label = tk.Label(frame_temperaturas, text=f"{componente}: {temp:.2f} °C", anchor="w", padx=10)
            else:
                label = tk.Label(frame_temperaturas, text=f"{componente}: No disponible", anchor="w", padx=10)
            label.pack(fill="x", pady=2)

    ventana.mainloop()

# Ejecutar el programa
if __name__ == "__main__":
    mostrar_interfaz()
