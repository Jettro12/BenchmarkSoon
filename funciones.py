import psutil
import platform
from configuraciones import Hardware, model

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

def generar_prompt_personalizado(info_procesador, info_ram, info_disco):
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
    return prompt

def obtener_consejo_ia(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar el consejo: {e}"