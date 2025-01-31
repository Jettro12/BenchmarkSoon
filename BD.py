import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


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
    print("Datos del procesador:", datos_procesador)

    # Cargar datos de la RAM
    cursor.execute("SELECT * FROM ram")
    datos_ram = cursor.fetchall()
    print("Datos de la RAM:", datos_ram)

    # Cargar datos del disco
    cursor.execute("SELECT * FROM disco")
    datos_disco = cursor.fetchall()
    print("Datos del disco:", datos_disco)

    # Cargar datos de la GPU
    cursor.execute("SELECT * FROM gpu")
    datos_gpu = cursor.fetchall()
    print("Datos de la GPU:", datos_gpu)

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
    df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days
    X = df[["dias"]]
    y = df[columna_objetivo]
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo, df["fecha"].min()

def crear_grafico_barras(modelo, df, columna_fecha, columna_objetivo, titulo, frame):
    try:
        # Convertir las fechas a días desde la fecha mínima
        df["dias"] = (df[columna_fecha] - df[columna_fecha].min()).dt.days

        # Obtener la fecha mínima y máxima
        fecha_minima = df[columna_fecha].min()
        fecha_maxima = df[columna_fecha].max()

        # Generar fechas futuras para las predicciones (próximos 7 días)
        fechas_futuras = [fecha_maxima + timedelta(days=i) for i in range(1, 8)]
        dias_futuros = [(fecha - fecha_minima).days for fecha in fechas_futuras]

        # Realizar predicciones para las fechas futuras
        predicciones_futuras = modelo.predict(pd.DataFrame(dias_futuros, columns=["dias"]))

        # Crear el gráfico de barras
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(range(len(predicciones_futuras)), predicciones_futuras, color="skyblue")
        ax.set_title(titulo)
        ax.set_xlabel("Días futuros")
        ax.set_ylabel(titulo)
        ax.set_xticks(range(len(predicciones_futuras)))
        ax.set_xticklabels([f"Día {i+1}" for i in range(len(predicciones_futuras))], rotation=45)

        # Insertar gráfico en la ventana
        canvas_grafico = FigureCanvasTkAgg(fig, master=frame)
        canvas_grafico.draw()
        canvas_grafico.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Crear la interpretación de la predicción
        interpretacion = f"Predicciones para los próximos 7 días:\n"
        for i, (fecha, prediccion) in enumerate(zip(fechas_futuras, predicciones_futuras)):
            interpretacion += f"- {fecha.strftime('%Y-%m-%d')}: {prediccion:.2f} {titulo.split(' ')[-1]}\n"

        # Mostrar la interpretación debajo del gráfico
        cuadro_prediccion = tk.Label(frame, text=interpretacion, font=("Arial", 10), bg="lightgray", width=50, justify="left")
        cuadro_prediccion.pack(pady=5)

        return interpretacion
    except Exception as e:
        print(f"Error en crear_grafico_barras: {e}")
        return f"Error: {e}"

 