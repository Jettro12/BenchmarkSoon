import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    obtener_info_gpu,
)

def crear_base_de_datos():
    conn = sqlite3.connect('rendimiento.db')
    cursor = conn.cursor()

    # Crear tabla para almacenar información del procesador
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procesador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fabricante TEXT,
            arquitectura TEXT,
            frecuencia_base REAL,
            frecuencia_maxima REAL,
            frecuencia_actual REAL,
            nucleos_fisicos INTEGER,
            nucleos_logicos INTEGER,
            uso_cpu REAL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Crear tabla para almacenar información de la RAM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ram_total REAL,
            ram_usada REAL,
            ram_libre REAL,
            uso_ram REAL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Crear tabla para almacenar información del disco
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disco_total REAL,
            disco_usado REAL,
            disco_libre REAL,
            uso_disco REAL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
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
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    conn.close()

def almacenar_datos(info_procesador, info_ram, info_disco, info_gpu):
    conn = sqlite3.connect('rendimiento.db')
    cursor = conn.cursor()

    # Insertar datos del procesador
    cursor.execute('''
        INSERT INTO procesador (nombre, fabricante, arquitectura, frecuencia_base, frecuencia_maxima, frecuencia_actual, nucleos_fisicos, nucleos_logicos, uso_cpu, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        info_procesador["Nombre"],
        info_procesador["Fabricante"],
        info_procesador["Arquitectura"],
        info_procesador["Frecuencia Base (GHz)"],
        info_procesador["Frecuencia Máxima (GHz)"],
        info_procesador["Frecuencia Actual (GHz)"],
        info_procesador["Núcleos Físicos"],
        info_procesador["Núcleos Lógicos"],
        info_procesador["Uso del CPU (%)"],
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

    # Insertar datos de la GPU (si están disponibles)
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

def preparar_datos_historicos():
    conn = sqlite3.connect('rendimiento.db')

    # Recuperar datos de las tablas
    df_procesador = pd.read_sql_query("SELECT * FROM procesador", conn)
    df_ram = pd.read_sql_query("SELECT * FROM ram", conn)
    df_disco = pd.read_sql_query("SELECT * FROM disco", conn)
    df_gpu = pd.read_sql_query("SELECT * FROM gpu", conn)

    conn.close()

    # Convertir todos los nombres de columnas a minúsculas
    df_procesador.columns = [col.lower() for col in df_procesador.columns]
    df_ram.columns = [col.lower() for col in df_ram.columns]
    df_disco.columns = [col.lower() for col in df_disco.columns]
    df_gpu.columns = [col.lower() for col in df_gpu.columns]

    # Renombrar columnas específicas (si existen) para que coincidan con lo esperado
    if "uso de ram (%)" in df_ram.columns and "uso_ram" not in df_ram.columns:
        df_ram.rename(columns={"uso de ram (%)": "uso_ram"}, inplace=True)
    if "uso del cpu (%)" in df_procesador.columns and "uso_cpu" not in df_procesador.columns:
        df_procesador.rename(columns={"uso del cpu (%)": "uso_cpu"}, inplace=True)

    # Convertir la columna "fecha" a datetime y agregar la columna "dias" a df_procesador, df_ram y df_disco
    for df in [df_procesador, df_ram, df_disco]:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        # Si hay registros, calcular 'dias' como diferencia en días respecto a la fecha mínima
        if not df["fecha"].isnull().all():
            df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days
        else:
            df["dias"] = 0

    return df_procesador, df_ram, df_disco, df_gpu

def crear_grafico_barras(modelo, df, x_col, y_col, titulo, frame):
    try:
        # Crear un diccionario que mapea el nombre en minúsculas al nombre original
        col_map = {col.lower(): col for col in df.columns}
        
        # Adaptar x_col
        if x_col.lower() in col_map:
            x_col_actual = col_map[x_col.lower()]
        else:
            raise ValueError(f"La columna '{x_col}' no existe en el DataFrame.")
        
        # Adaptar y_col
        if y_col.lower() in col_map:
            y_col_actual = col_map[y_col.lower()]
        else:
            raise ValueError(f"La columna '{y_col}' no existe en el DataFrame.")
        
        # Asegurarse de que la variable de tiempo 'dias' exista en el DataFrame.
        # Si no existe, se calculará a partir de la columna 'fecha'.
        if "dias" not in [col.lower() for col in df.columns]:
            if "fecha" in [col.lower() for col in df.columns]:
                fecha_col = [col for col in df.columns if col.lower() == "fecha"][0]
                # Calcular 'dias' como la diferencia en días entre cada fecha y la mínima
                df["dias"] = (df[fecha_col] - df[fecha_col].min()).dt.days
            else:
                raise ValueError("No se puede calcular 'dias'; la columna 'fecha' no existe.")
        
        # Forzar que se use la variable 'dias' como eje X para consistencia
        x_col_actual = "dias"
        
        # Crear el gráfico de barras utilizando la columna 'dias' y la variable objetivo
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(df[x_col_actual], df[y_col_actual], color='blue', alpha=0.7)
        ax.set_xlabel(x_col_actual)
        ax.set_ylabel(y_col_actual)
        ax.set_title(titulo)
        
        # Anotar cada barra con su valor
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8)
        
        # Mostrar el gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Agregar la barra de herramientas
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Preparar una cadena de texto para mostrar los datos reales
        output_text = "Datos:\n"
        for index, row in df.iterrows():
            output_text += f"{row[x_col_actual]}: {row[y_col_actual]}\n"
        
        # Generar predicciones futuras usando la columna 'dias'
        max_dias = df[x_col_actual].max()
        # Pronosticar 6 días en el futuro (ajusta según tus necesidades)
        future_days = np.arange(max_dias + 1, max_dias + 7)
        # Crear un DataFrame para la predicción usando la misma columna de tiempo 'dias'
        df_pred = pd.DataFrame(future_days, columns=[x_col_actual])
        predicciones_futuras = modelo.predict(df_pred)
        ax.plot(future_days, predicciones_futuras, color='red', marker='o', label="Predicciones futuras")
        ax.legend()
        output_text += "\nPredicciones futuras:\n"
        for t, p in zip(future_days, predicciones_futuras):
            output_text += f"Día {t}: {p:.2f}\n"
        
        # Agregar un recuadro de texto en la esquina superior izquierda del gráfico con los datos y predicciones
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, output_text, transform=ax.transAxes, fontsize=8,
                verticalalignment='top', bbox=props)
        
        return output_text

    except Exception as e:
        return f"Error en crear_grafico_barras: {e}"
