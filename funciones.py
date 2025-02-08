import psutil
import platform
import GPUtil
import cpuinfo
from configuraciones import model, client

# Función para obtener información del procesador
def obtener_info_procesador():
    cpu_info = cpuinfo.get_cpu_info()
     

    return {
        "Nombre": cpu_info["brand_raw"],
        
        "Uso del CPU (%)": psutil.cpu_percent(interval=1),
      
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
            return {
                "Nombre": "No disponible",
                "Carga (%)": 0,
                "Memoria Usada (GB)": 0,
                "Memoria Total (GB)": 0,
                "Temperatura (°C)": 0,
            }
        
        gpu = gpus[0]
        return {
            "Nombre": gpu.name,
            "Carga (%)": gpu.load * 100,
            "Memoria Usada (GB)": round(gpu.memoryUsed, 2) if gpu.memoryUsed is not None else 0,
            "Memoria Total (GB)": round(gpu.memoryTotal, 2) if gpu.memoryTotal is not None else 0,
            "Temperatura (°C)": gpu.temperature,
        }
    except Exception as e:
        return {
            "Nombre": "No disponible",
            "Carga (%)": 0,
            "Memoria Usada (GB)": 0,
            "Memoria Total (GB)": 0,
            "Temperatura (°C)": 0,
        }
 
# Función para generar el prompt personalizado
def generar_prompt_personalizado(info_procesador, info_ram, info_disco, info_gpu):
    
    prompt = "Basado en el análisis del sistema, proporciona consejos específicos para optimizar el rendimiento, centrándote solo en las acciones a realizar. Aquí están los puntos clave:\n\n"
    
    # Procesador
    prompt += f"Procesador: Uso del CPU {info_procesador['Uso del CPU (%)']}%.\n"
    
    # RAM
    prompt += f"RAM: Usada {info_ram['RAM Usada (GB)']} GB, Uso {info_ram['Uso de RAM (%)']}%.\n"
    
    # Disco
    prompt += f"Disco: Usado {info_disco['Disco Usado (GB)']} GB, Uso {info_disco['Uso de Disco (%)']}%.\n"
    
    # GPU
    prompt += f"GPU: Carga {info_gpu['Carga (%)']}%, Memoria Usada {info_gpu['Memoria Usada (GB)']} GB, Temperatura {info_gpu['Temperatura (°C)']} °C.\n"
    
    prompt += "Proporciona acciones específicas para optimizar este sistema."
    return prompt

# Función para obtener consejo de la IA utilizando Groq
def obtener_consejo_ia(prompt):
    try:
        # Llamada al modelo de Groq con el prompt
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al generar el consejo: {e}"