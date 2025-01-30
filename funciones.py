import psutil
import platform
import GPUtil
from configuraciones import model

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

# Función para obtener información del disco
def obtener_info_disco():
    disco_info = psutil.disk_usage('/')
    return {
        "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
        "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
        "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
        "Uso de Disco (%)": disco_info.percent,
    }

#Obtener info del gpu
def obtener_info_gpu():
    try:    
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
    except Exception as e:
        return {"GPU": "No disponible"}
 
# Función para generar el prompt personalizado
def generar_prompt_personalizado(info_procesador, info_ram, info_disco, info_gpu):
    
    prompt = "Basado en el análisis del sistema, proporciona consejos específicos para optimizar el rendimiento, centrándote solo en las acciones a realizar. Aquí están los puntos clave:\n\n"
    
    # Procesador
    prompt += f"Procesador: Frecuencia Actual {info_procesador['Frecuencia Actual (GHz)']} GHz..\n"
    
    # RAM
    prompt += f"RAM: Usada {info_ram['RAM Usada (GB)']} GB, Uso {info_ram['Uso de RAM (%)']}%.\n"
    
    # Disco
    prompt += f"Disco: Usado {info_disco['Disco Usado (GB)']} GB, Uso {info_disco['Uso de Disco (%)']}%.\n"
    
    # GPU
    prompt += f"GPU: Carga {info_gpu['Carga (%)']}%, Memoria Usada {info_gpu['Memoria Usada (GB)']} GB, Temperatura {info_gpu['Temperatura (°C)']} °C.\n"
    
    prompt += "Proporciona acciones específicas para optimizar este sistema."
    return prompt

# Función para obtener consejo de la IA utilizando Gemini
def obtener_consejo_ia(prompt):
    try:
        # Llamada al modelo de Gemini con el prompt
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar el consejo: {e}"