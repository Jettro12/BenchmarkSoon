import matplotlib.pyplot as plt
import numpy as np

# Variables globales para almacenar historiales
historial_cpu = []
historial_ram = []
historial_disco = []
historial_gpu = []

def crear_grafico_cpu(datos, ax):
    """
    Actualiza un gráfico de barras del uso del CPU.
    """
    global historial_cpu

    if "Uso del CPU (%)" not in datos:
        raise ValueError("La clave 'Uso del CPU (%)' no está presente en los datos.")

    # Agregar el valor actual al historial
    uso_actual = datos["Uso del CPU (%)"]
    historial_cpu.append(uso_actual)

    # Limitar el historial a los últimos 20 registros
    if len(historial_cpu) > 20:
        historial_cpu.pop(0)

    # Limpiar el eje y dibujar el nuevo gráfico
    ax.clear()
    x = np.arange(len(historial_cpu))
    y = historial_cpu
    colores = ['green' if val < 50 else 'orange' if val < 80 else 'red' for val in y]
    ax.bar(x, y, color=colores, edgecolor='black')

    # Configurar el fondo transparente
    ax.set_facecolor('none')  # Fondo del eje transparente
    ax.figure.patch.set_alpha(0)  # Fondo de la figura transparente

    # Estilo del gráfico
    ax.set_title("Uso del CPU", color='black')  # Color del título
    ax.set_xlabel("Tiempo", color='black')  # Color del eje X
    #ax.set_ylabel("Uso (%)", color='black')  # Color del eje Y
    ax.tick_params(axis='x', colors='black')  # Color de las etiquetas del eje X
    ax.tick_params(axis='y', colors='black')  # Color de las etiquetas del eje Y
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7, color='black')  # Color de la cuadrícula

    # Mostrar el nombre y los datos encima del gráfico
    nombre = datos.get("Nombre", "CPU")
    ax.text(
        0.5, 1.1,  # Posición (x, y) relativa al gráfico
        f"{nombre}\nUso: {uso_actual}%",  # Texto a mostrar
        transform=ax.transAxes,  # Usar coordenadas relativas
        fontsize=10, color='none', ha='center', va='bottom'  # Estilo del texto
    )

def crear_grafico_ram(datos, ax):
    """
    Actualiza un gráfico de área del uso de RAM.
    """
    global historial_ram

    if "Uso de RAM (%)" not in datos:
        raise ValueError("La clave 'Uso de RAM (%)' no está presente en los datos.")

    uso_actual = datos["Uso de RAM (%)"]
    historial_ram.append(uso_actual)
    if len(historial_ram) > 20:
        historial_ram.pop(0)

    ax.clear()
    x = np.arange(len(historial_ram))
    y = np.array(historial_ram)
    ax.fill_between(x, y, color='blue', alpha=0.4)
    ax.plot(x, y, color='blue', linewidth=2)

    # Configurar el fondo transparente
    ax.set_facecolor('none')  # Fondo del eje transparente
    ax.figure.patch.set_alpha(0)  # Fondo de la figura transparente

    # Estilo del gráfico
    ax.set_title("Uso de la RAM", color='black')
    ax.set_xlabel("Tiempo", color='black')
    ax.set_ylabel("Uso (%)", color='black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.set_ylim(0, 100)
    ax.grid(True, color='black', linestyle='--', alpha=0.7)

    # Mostrar el nombre y los datos encima del gráfico
    nombre = "RAM"
    ax.text(
        0.5, 1.1,  # Posición (x, y) relativa al gráfico
        f"{nombre}\nUso: {uso_actual}%",  # Texto a mostrar
        transform=ax.transAxes,  # Usar coordenadas relativas
        fontsize=10, color='none', ha='center', va='bottom'  # Estilo del texto
    )

def crear_grafico_disco(datos, ax):
    """
    Actualiza un gráfico de dispersión del uso del disco.
    """
    global historial_disco

    if "Uso de Disco (%)" not in datos:
        raise ValueError("La clave 'Uso de Disco (%)' no está presente en los datos.")

    uso_actual = datos["Uso de Disco (%)"]
    historial_disco.append(uso_actual)
    if len(historial_disco) > 20:
        historial_disco.pop(0)

    ax.clear()
    x = np.arange(len(historial_disco))
    y = historial_disco
    ax.scatter(x, y, color='orange', edgecolor='black', s=50)

    # Configurar el fondo transparente
    ax.set_facecolor('none')  # Fondo del eje transparente
    ax.figure.patch.set_alpha(0)  # Fondo de la figura transparente

    # Estilo del gráfico
    ax.set_title("Uso del Disco", color='black')
    ax.set_xlabel("Tiempo", color='black')
    ax.set_ylabel("Uso (%)", color='black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.set_ylim(0, 100)
    ax.grid(True, color='black', linestyle='--', alpha=0.7)

    # Mostrar el nombre y los datos encima del gráfico
    nombre = "Disco"
    ax.text(
        0.5, 1.1,  # Posición (x, y) relativa al gráfico
        f"{nombre}\nUso: {uso_actual}%",  # Texto a mostrar
        transform=ax.transAxes,  # Usar coordenadas relativas
        fontsize=10, color='none', ha='center', va='bottom'  # Estilo del texto
    )

def crear_grafico_gpu(datos, ax):
    """
    Actualiza un gráfico de líneas del uso de la GPU.
    """
    global historial_gpu

    uso_actual = datos.get("Carga (%)", 0)
    historial_gpu.append(uso_actual)
    if len(historial_gpu) > 20:
        historial_gpu.pop(0)

    ax.clear()
    x = np.arange(len(historial_gpu))
    y = historial_gpu
    ax.plot(x, y, color='purple', linewidth=2)
    ax.fill_between(x, y, color='purple', alpha=0.3)

    # Configurar el fondo transparente
    ax.set_facecolor('none')  # Fondo del eje transparente
    ax.figure.patch.set_alpha(0)  # Fondo de la figura transparente

    # Estilo del gráfico
    ax.set_title("Uso de la GPU", color='black')
    ax.set_xlabel("Tiempo", color='black')
    ax.set_ylabel("Uso (%)", color='black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.set_ylim(0, 100)
    ax.grid(True, color='black', linestyle='--', alpha=0.7)

    # Mostrar el nombre y los datos encima del gráfico
    nombre = datos.get("Nombre", "GPU")
    ax.text(
        0.5, 1.1,  # Posición (x, y) relativa al gráfico
        f"{nombre}\nUso: {uso_actual}%",  # Texto a mostrar
        transform=ax.transAxes,  # Usar coordenadas relativas
        fontsize=10, color='none', ha='center', va='bottom'  # Estilo del texto
    )