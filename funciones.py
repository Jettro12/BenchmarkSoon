import psutil
import platform
from configuraciones import model
import GPUtil
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def obtener_info_procesador():
    try:
        cpu_freq = psutil.cpu_freq()
        return {
            "Nombre": platform.processor(),
            "Frecuencia Base (GHz)": round(cpu_freq.min / 1000, 2) if cpu_freq else "No disponible",
            "Frecuencia Máxima (GHz)": round(cpu_freq.max / 1000, 2) if cpu_freq else "No disponible",
            "Frecuencia Actual (GHz)": round(cpu_freq.current / 1000, 2) if cpu_freq else "No disponible",
            "Núcleos Físicos": psutil.cpu_count(logical=False),
            "Núcleos Lógicos": psutil.cpu_count(logical=True),
        }
    except Exception as e:
        return {"Error": f"Error al obtener informacion del procesador: {str(e)}"}

def obtener_info_ram():
    try:
        ram_info = psutil.virtual_memory()
        return {
            "RAM Total (GB)": round(ram_info.total / (1024 ** 3), 2),
            "RAM Usada (GB)": round(ram_info.used / (1024 ** 3), 2),
            "RAM Libre (GB)": round(ram_info.available / (1024 ** 3), 2),
            "Uso de RAM (%)": ram_info.percent,
        }
    except Exception as e:
        return {"Error": f"Error al obtener informacion de la RAM: {str(e)}"}

def obtener_info_disco():
    try:
        disco_info = psutil.disk_usage('/')
        return {
            "Disco Total (GB)": round(disco_info.total / (1024 ** 3), 2),
            "Disco Usado (GB)": round(disco_info.used / (1024 ** 3), 2),
            "Disco Libre (GB)": round(disco_info.free / (1024 ** 3), 2),
            "Uso de Disco (%)": disco_info.percent,
        }
    except Exception as e:
        return {"Error": f"Error al obtener informacion del disco: {str(e)}"}

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

def generar_prompt_personalizado(info_procesador, info_ram, info_disco, info_gpu):
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
    
    # Información de la GPU
    if "No disponible" in info_gpu.values():
        prompt += "- **GPU**: No se detecto GPU en este sistema.\n\n"
    else:
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
    
def crear_base_de_datos():
 conn = sqlite3.connect('rendimiento.db')
 cursor = conn.cursor()

    # Crear tabla para almacenar información del procesador
 cursor.execute('''
        CREATE TABLE IF NOT EXISTS procesador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            frecuencia_base REAL,
            frecuencia_maxima REAL,
            frecuencia_actual REAL,
            nucleos_fisicos INTEGER,
            nucleos_logicos INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Crear tabla para almacenar información de la RAM
 cursor.execute('''
        CREATE TABLE IF NOT EXISTS ram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ram_total REAL,
            ram_usada REAL,
            ram_libre REAL,
            uso_ram REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Crear tabla para almacenar información del disco
 cursor.execute('''
        CREATE TABLE IF NOT EXISTS disco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disco_total REAL,
            disco_usado REAL,
            disco_libre REAL,
            uso_disco REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Crear tabla para almacenar información de la GPU
 cursor.execute('''
        CREATE TABLE IF NOT EXISTS gpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            carga REAL,
            memoria_usada REAL,
            memoria_total REAL,
            temperatura REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

 conn.commit()
 conn.close()



def almacenar_datos(info_procesador, info_ram, info_disco, info_gpu):
    conn = sqlite3.connect('rendimiento.db')
    cursor = conn.cursor()

    # Insertar datos del procesador
    cursor.execute('''
        INSERT INTO procesador (nombre, frecuencia_base, frecuencia_maxima, frecuencia_actual, nucleos_fisicos, nucleos_logicos, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        info_procesador["Nombre"],
        info_procesador["Frecuencia Base (GHz)"],
        info_procesador["Frecuencia Máxima (GHz)"],
        info_procesador["Frecuencia Actual (GHz)"],
        info_procesador["Núcleos Físicos"],
        info_procesador["Núcleos Lógicos"],
        datetime.now()
    ))

    # Insertar datos de la RAM
    cursor.execute('''
        INSERT INTO ram (ram_total, ram_usada, ram_libre, uso_ram, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        info_ram["RAM Total (GB)"],
        info_ram["RAM Usada (GB)"],
        info_ram["RAM Libre (GB)"],
        info_ram["Uso de RAM (%)"],
        datetime.now()
    ))

    # Insertar datos del disco
    cursor.execute('''
        INSERT INTO disco (disco_total, disco_usado, disco_libre, uso_disco, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        info_disco["Disco Total (GB)"],
        info_disco["Disco Usado (GB)"],
        info_disco["Disco Libre (GB)"],
        info_disco["Uso de Disco (%)"],
        datetime.now()
    ))

    # Insertar datos de la GPU (si está disponible)
    if "No disponible" not in info_gpu.values():
        cursor.execute('''
            INSERT INTO gpu (nombre, carga, memoria_usada, memoria_total, temperatura, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            info_gpu["Nombre"],
            info_gpu["Carga (%)"],
            info_gpu["Memoria Usada (GB)"],
            info_gpu["Memoria Total (GB)"],
            info_gpu["Temperatura (°C)"],
            datetime.now()
        ))

    conn.commit()
    conn.close()

def cargar_datos_historicos():
 conn = sqlite3.connect('rendimiento.db')
 cursor = conn.cursor()

    # Cargar datos del procesador
 cursor.execute("SELECT * FROM procesador")
 datos_procesador = cursor.fetchall()

    # Cargar datos de la RAM
 cursor.execute("SELECT * FROM ram")
 datos_ram = cursor.fetchall()

    # Cargar datos del disco
 cursor.execute("SELECT * FROM disco")
 datos_disco = cursor.fetchall()

    # Cargar datos de la GPU
 cursor.execute("SELECT * FROM gpu")
 datos_gpu = cursor.fetchall()

 conn.close()

 return datos_procesador, datos_ram, datos_disco, datos_gpu

def preparar_datos_historicos():
 datos_procesador, datos_ram, datos_disco, datos_gpu = cargar_datos_historicos()

    # Convertir datos de RAM en un DataFrame
 columnas_ram = ["id", "ram_total", "ram_usada", "ram_libre", "uso_ram", "fecha"]
 df_ram = pd.DataFrame(datos_ram, columns=columnas_ram)
 df_ram["fecha"] = pd.to_datetime(df_ram["fecha"])  # Convertir a tipo datetime
 df_ram = df_ram.sort_values(by="fecha")  # Ordenar por fecha

  # Convertir datos de CPU en un DataFrame (opcional, si quieres predecir CPU)
 columnas_procesador = ["id", "nombre", "frecuencia_base", "frecuencia_maxima", "frecuencia_actual", "nucleos_fisicos", "nucleos_logicos", "fecha"]
 df_procesador = pd.DataFrame(datos_procesador, columns=columnas_procesador)
 df_procesador["fecha"] = pd.to_datetime(df_procesador["fecha"])
 df_procesador = df_procesador.sort_values(by="fecha")

    # Convertir datos de disco en un DataFrame (opcional, si quieres predecir disco)
 columnas_disco = ["id", "disco_total", "disco_usado", "disco_libre", "uso_disco", "fecha"]
 df_disco = pd.DataFrame(datos_disco, columns=columnas_disco)
 df_disco["fecha"] = pd.to_datetime(df_disco["fecha"])
 df_disco = df_disco.sort_values(by="fecha")

    # Convertir datos de GPU en un DataFrame (opcional, si quieres predecir GPU)
 columnas_gpu = ["id", "nombre", "carga", "memoria_usada", "memoria_total", "temperatura", "fecha"]
 df_gpu = pd.DataFrame(datos_gpu, columns=columnas_gpu)
 df_gpu["fecha"] = pd.to_datetime(df_gpu["fecha"])
 df_gpu = df_gpu.sort_values(by="fecha")

 return df_ram, df_procesador, df_disco, df_gpu

def entrenar_modelo(df, columna_objetivo):
    # Convertir fechas a valores numéricos (días desde la primera fecha)
    df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days

    # Definir características (X) y variable objetivo (y)
    X = df[["dias"]]
    y = df[columna_objetivo]

    # Entrenar un modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X, y)

    return modelo, df["fecha"].min()

def predecir_y_graficar(modelo, fecha_minima, columna_objetivo, nombre_objetivo):
    # Crear fechas futuras (por ejemplo, los próximos 7 días)
 fechas_futuras = [fecha_minima + timedelta(days=i) for i in range(1, 8)]
 dias_futuros = [(fecha - fecha_minima).days for fecha in fechas_futuras]

    # Hacer predicciones
 predicciones = modelo.predict(pd.DataFrame(dias_futuros, columns=["dias"]))

    # Graficar los resultados
 plt.figure(figsize=(10, 6))
 plt.plot(fechas_futuras, predicciones, marker='o', linestyle='-', color='b', label=f"Predicción de {nombre_objetivo}")
 plt.title(f"Predicción de {nombre_objetivo} en los próximos 7 días")
 plt.xlabel("Fecha")
 plt.ylabel(nombre_objetivo)
 plt.grid(True)
 plt.legend()
 plt.tight_layout()

    # Mostrar la gráfica
 plt.show()

    # Interpretación de los resultados
 interpretacion = (
        f"Interpretación:\n"
        f"El gráfico muestra la predicción de {nombre_objetivo} en los próximos 7 días.\n"
        f"Se espera que {nombre_objetivo} aumente/disminuya a {predicciones[-1]:.2f}%.\n"
        "Considera monitorear el rendimiento y optimizar el sistema si es necesario."
    )
 return interpretacion