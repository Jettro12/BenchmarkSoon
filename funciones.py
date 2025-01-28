import psutil
import platform
from configuraciones import model
import GPUtil
import pynvml

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

def obtener_info_ram():
    ram_info = psutil.virtual_memory()
    return {
        "RAM Total (GB)": round(ram_info.total / (1024 ** 3), 2),
        "RAM Usada (GB)": round(ram_info.used / (1024 ** 3), 2),
        "RAM Libre (GB)": round(ram_info.available / (1024 ** 3), 2),
        "Uso de RAM (%)": ram_info.percent,
    }

def obtener_info_disco():
    disco_info = psutil.disk_usage('/')
    return {
        "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
        "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
        "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
        "Uso de Disco (%)": disco_info.percent,
    }

def obtener_temperaturas():
    temperaturas = {"CPU": "No disponible", "GPU": "No disponible"}

    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Primera GPU
        temperatura_gpu = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        temperaturas["GPU"] = f"{temperatura_gpu} °C"
    except pynvml.NVMLError:
        pass
    finally:
        pynvml.nvmlShutdown()

    return temperaturas

def obtener_info_gpu():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return {"GPU": "No disponible"}
    
    gpu = gpus[0]
    return {
        "Nombre": gpu.name,
        "Carga (%)": gpu.load * 100,
        "Memoria Usada (GB)": round(gpu.memoryUsed, 2),
        "Memoria Total (GB)": round(gpu.memoryTotal, 2),
        "Temperatura (°C)": gpu.temperature,
    }

def generar_prompt_personalizado(info_procesador, info_ram, info_disco, info_gpu, temperaturas):
    prompt = "He escaneado un sistema con las siguientes características:\n\n"
    prompt += (
        f"- **Procesador**: {info_procesador['Nombre']}\n"
        f"  - Frecuencia Base: {info_procesador['Frecuencia Base (GHz)']} GHz\n"
        f"  - Frecuencia Máxima: {info_procesador['Frecuencia Máxima (GHz)']} GHz\n"
        f"  - Frecuencia Actual: {info_procesador['Frecuencia Actual (GHz)']} GHz\n"
        f"  - Núcleos Físicos: {info_procesador['Núcleos Físicos']}\n"
        f"  - Núcleos Lógicos: {info_procesador['Núcleos Lógicos']}\n\n"
        f"  - Temperatura: {temperaturas['CPU']}\n\n"
    )
    prompt += (
        "- **Memoria RAM**:\n"
        f"  - RAM Total: {info_ram['RAM Total (GB)']} GB\n"
        f"  - RAM Usada: {info_ram['RAM Usada (GB)']} GB\n"
        f"  - RAM Libre: {info_ram['RAM Libre (GB)']} GB\n"
        f"  - Uso de RAM: {info_ram['Uso de RAM (%)']}%\n\n"
    )
    prompt += (
        "- **Almacenamiento**:\n"
        f"  - Disco Total: {info_disco['Disco Total (GB)']} GB\n"
        f"  - Disco Usado: {info_disco['Disco Usado (GB)']} GB\n"
        f"  - Disco Libre: {info_disco['Disco Libre (GB)']} GB\n"
        f"  - Uso del Disco: {info_disco['Uso de Disco (%)']}%\n"
    )
    prompt += "\nPor favor, bríndame un consejo personalizado para optimizar este sistema.\n"
    
    # Información de la GPU
    prompt += (
        "- **GPU**:\n"
        f"  - Nombre: {info_gpu['Nombre']}\n"
        f"  - Carga: {info_gpu['Carga (%)']}%\n"
        f"  - Memoria Usada: {info_gpu['Memoria Usada (GB)']} GB\n"
        f"  - Memoria Total: {info_gpu['Memoria Total (GB)']} GB\n"
        f"  - Temperatura: {info_gpu['Temperatura (°C)']} °C\n\n"
    )
    
    return prompt

def obtener_consejo_ia(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar el consejo: {e}"