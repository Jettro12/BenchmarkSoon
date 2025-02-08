import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Variables globales para almacenar historiales
historial_cpu = []
historial_ram = []
historial_disco = []
historial_gpu = []

def crear_grafico_cpu(datos):
    """
    Crea un gráfico de barras del uso del CPU acumulando un historial.
    Se espera que 'datos' tenga la clave "Uso del CPU (%)", con un valor float.
    """
    global historial_cpu

    if "Uso del CPU (%)" not in datos:
        raise ValueError("La clave 'Uso del CPU (%)' no está presente en los datos.")
    
    # Agregar el valor actual al historial
    uso_actual = datos["Uso del CPU (%)"]
    historial_cpu.append(uso_actual)
    
    # Limitar el historial a los últimos 20 registros
    if len(historial_cpu) > 20:
        historial_cpu[:] = historial_cpu[-20:]
    
    x = np.arange(len(historial_cpu))  # Tiempo o índices de medición
    y = historial_cpu

    # Colores: verde para uso < 50, naranja para 50-80, rojo para >80
    colores = ['green' if val < 50 else 'orange' if val < 80 else 'red' for val in y]

    fig, ax = plt.subplots(figsize=(2.5, 2))
    ax.bar(x, y, color=colores, edgecolor='black')  # Gráfico de barras
    ax.set_title("Uso del CPU")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Uso (%)")
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

def crear_grafico_ram(datos):
    """
    Crea un gráfico de área del uso de RAM acumulando un historial.
    Se espera que 'datos' tenga la clave "Uso de RAM (%)".
    """
    global historial_ram

    if "Uso de RAM (%)" not in datos:
        raise ValueError("La clave 'Uso de RAM (%)' no está presente en los datos.")
    
    uso_actual = datos["Uso de RAM (%)"]
    historial_ram.append(uso_actual)
    if len(historial_ram) > 20:
        historial_ram[:] = historial_ram[-20:]
    
    x = np.arange(len(historial_ram))
    y = np.array(historial_ram)

    fig, ax = plt.subplots(figsize=(2.5, 2))
    ax.fill_between(x, y, color='blue', alpha=0.4)  # Gráfico de área
    ax.plot(x, y, color='blue', linewidth=2)
    ax.set_title("Uso de la RAM")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Uso (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)
    return fig

def crear_grafico_disco(datos):
    """
    Crea un gráfico de dispersión del uso del disco acumulando un historial.
    Se espera que 'datos' tenga la clave "Uso de Disco (%)".
    """
    global historial_disco

    if "Uso de Disco (%)" not in datos:
        raise ValueError("La clave 'Uso de Disco (%)' no está presente en los datos.")
    
    uso_actual = datos["Uso de Disco (%)"]
    historial_disco.append(uso_actual)
    if len(historial_disco) > 20:
        historial_disco[:] = historial_disco[-20:]
    
    x = np.arange(len(historial_disco))
    y = historial_disco

    fig, ax = plt.subplots(figsize=(2.5, 2))
    ax.scatter(x, y, color='orange', edgecolor='black', s=50)  # Gráfico de dispersión
    ax.set_title("Uso del Disco")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Uso (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)
    return fig

def crear_grafico_gpu(datos):
    """
    Crea un gráfico de líneas del uso de la GPU acumulando un historial.
    Si la GPU no está disponible, se usará 0.
    Se espera que 'datos' tenga la clave "Carga (%)" si está disponible.
    """
    global historial_gpu

    # Usamos "Carga (%)" si está presente; de lo contrario, asumimos 0.
    uso_actual = datos.get("Carga (%)", 0)
    historial_gpu.append(uso_actual)
    if len(historial_gpu) > 20:
        historial_gpu[:] = historial_gpu[-20:]
    
    x = np.arange(len(historial_gpu))
    y = historial_gpu

    fig, ax = plt.subplots(figsize=(2.5, 2))
    ax.plot(x, y, color='purple', linewidth=2)  # Gráfico de líneas
    ax.fill_between(x, y, color='purple', alpha=0.3)  # Relleno de área
    ax.set_title("Uso de la GPU")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Uso (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)
    return fig