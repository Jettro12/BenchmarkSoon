import psutil
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

# Función para generar el prompt personalizado
def generar_prompt_personalizado(info_procesador, info_ram, info_disco):
    
    prompt = """
        Basado en el análisis del sistema, proporciona consejos específicos para optimizar el rendimiento. 
        Cada consejo debe incluir:

        1. **Acciones claras y específicas** a realizar, ordenadas por su importancia.
        2. **Iconos o imágenes a color** que representen visualmente cada consejo (por ejemplo, 🚀 para optimización, 🔧 para ajustes técnicos, 📊 para análisis de datos, etc.).
        3. **Formato Markdown** para una presentación clara y atractiva, utilizando:
        - Encabezados (`##`) para cada categoría de consejos.
        - Listas numeradas o con viñetas (`-` o `1.`) para las acciones.
        - **Negritas** para resaltar puntos clave.
        - Código en línea (`` ` ``) para términos técnicos.
        - Bloques de código (``` ```) para comandos o scripts.
        - Imágenes o iconos relevantes (usando `![alt text](image_url)`).

        Ejemplo de formato:

        ## 🚀 Optimización del Sistema
        - **Acción 1:** Limpiar archivos temporales usando el comando `rm -rf /tmp/*`.
        - **Acción 2:** Deshabilitar servicios innecesarios con `systemctl disable <nombre_servicio>`.
        - **Acción 3:** Aumentar la memoria swap para mejorar el rendimiento.

        ## 🔧 Ajustes Técnicos
        - **Acción 1:** Actualizar los controladores de hardware.
        - **Acción 2:** Optimizar la configuración de la base de datos.

        ## 📊 Análisis de Datos
        - **Acción 1:** Monitorear el uso de recursos con `htop`.
        - **Acción 2:** Generar reportes de rendimiento semanales.

        Asegúrate de que cada consejo sea fácil de entender y visualmente atractivo para el usuario.Aquí están los puntos clave:
        """
    
    # Procesador
    prompt += f"Procesador: Uso del CPU {info_procesador['Uso del CPU (%)']}%.\n"
    
    # RAM
    prompt += f"RAM: Usada {info_ram['RAM Usada (GB)']} GB, Uso {info_ram['Uso de RAM (%)']}%.\n"
    
    # Disco
    prompt += f"Disco: Usado {info_disco['Disco Usado (GB)']} GB, Uso {info_disco['Uso de Disco (%)']}%.\n"
    
    prompt += "Proporciona acciones específicas para optimizar este sistema."
    return prompt

# Función para obtener consejo de la IA utilizando Groq
def obtener_consejo_ia(prompt):
    try:
        # Llamada al modelo de Groq con el prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente útil que proporciona consejos de optimización para sistemas informáticos. Devuelve la respuesta en formato Markdown."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al generar el consejo: {e}"