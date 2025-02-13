import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from funciones import (
    obtener_info_procesador,
    obtener_info_ram,
    obtener_info_disco,
    
)

def crear_base_de_datos():
    conn = sqlite3.connect('rendimiento.db')
    cursor = conn.cursor()

    # Crear tabla para almacenar información del procesador
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procesador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
             
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

 

    conn.commit()
    conn.close()

def almacenar_datos(info_procesador, info_ram, info_disco):
    conn = sqlite3.connect('rendimiento.db')
    cursor = conn.cursor()

    # Insertar datos del procesador
    cursor.execute('''
        INSERT INTO procesador (nombre, uso_cpu, fecha)
        VALUES (?, ?, ?)
    ''', (
        info_procesador["Nombre"],
         
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

  

    conn.commit()
    conn.close()


def preparar_datos_historicos():
    conn = sqlite3.connect('rendimiento.db')

    # Recuperar datos de las tablas
    df_procesador = pd.read_sql_query("SELECT * FROM procesador", conn)
    df_ram = pd.read_sql_query("SELECT * FROM ram", conn)
    df_disco = pd.read_sql_query("SELECT * FROM disco", conn)
    
    conn.close()

    # Convertir todos los nombres de columnas a minúsculas
    df_procesador.columns = [col.lower() for col in df_procesador.columns]
    df_ram.columns = [col.lower() for col in df_ram.columns]
    df_disco.columns = [col.lower() for col in df_disco.columns]
    

    # Renombrar columnas específicas para que coincidan con lo esperado
    if "uso de ram (%)" in df_ram.columns and "uso_ram" not in df_ram.columns:
        df_ram.rename(columns={"uso de ram (%)": "uso_ram"}, inplace=True)
    if "uso del cpu (%)" in df_procesador.columns and "uso_cpu" not in df_procesador.columns:
        df_procesador.rename(columns={"uso del cpu (%)": "uso_cpu"}, inplace=True)

    # Convertir la columna "fecha" a datetime y ordenar por fecha
    for df in [df_procesador, df_ram, df_disco]:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df.sort_values("fecha", inplace=True)

    return df_procesador, df_ram, df_disco

def crear_grafico_arima(serie_temporal, predicciones, titulo, frame):
    """
    Grafica los datos históricos y las predicciones futuras.
    
    :param serie_temporal: Serie temporal histórica.
    :param predicciones: Predicciones futuras.
    :param titulo: Título del gráfico.
    :param frame: Frame donde se mostrará el gráfico.
    :return: Texto con los datos y predicciones.
    """
    fig, ax = plt.subplots(figsize=(4, 2))

    # --- Graficar datos históricos ---
    # Usar números de días en lugar de fechas para el eje X
    dias_historicos = range(1, len(serie_temporal) + 1)
    ax.plot(dias_historicos, serie_temporal.values, label="Datos históricos", marker="o")

    # --- Graficar predicciones futuras ---
    # Los días futuros comienzan desde el último día histórico + 1
    dias_futuros = range(len(serie_temporal) + 1, len(serie_temporal) + len(predicciones) + 1)
    ax.plot(dias_futuros, predicciones, label="Predicciones futuras", marker="x", linestyle="--")

    # --- Configurar el gráfico ---
    ax.set_xlabel("Días")  # Cambiar "Fecha" por "Días"
    ax.set_ylabel(titulo)
    ax.set_title(titulo)
    ax.legend()

    # --- Mostrar el gráfico en la interfaz ---
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    # --- Preparar texto con los datos y predicciones ---
    output_text = "Datos:\n"
    for dia, valor in zip(dias_historicos, serie_temporal.values):
        output_text += f"Porcentaje de rendimiento {dia}: {valor:.2f}%\n"  # Cambiado "Día" por "Porcentaje de rendimiento"
    output_text += "\nPredicciones futuras:\n"
    for dia, pred in zip(dias_futuros, predicciones):
        output_text += f"Porcentaje de rendimiento {dia}: {pred:.2f}%\n"  # Cambiado "Día" por "Porcentaje de rendimiento"

    return output_text