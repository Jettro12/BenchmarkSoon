import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def crear_grafico_cpu(info):
    # Obtener el porcentaje de uso del CPU
    uso_cpu = info.get("Uso del CPU (%)", 0)  # Usar la clave correcta

    # Configuración para el gráfico radial
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})

    # Convertir el porcentaje de uso en un ángulo (en radianes)
    angulo = np.deg2rad(uso_cpu * 360 / 100)

    # Dibujar el gráfico radial (un "semi-círculo" que representa el uso)
    ax.bar(0, uso_cpu, width=angulo, color='cyan', bottom=0.0)

    # Personalización del gráfico
    ax.set_title(f'Uso del CPU: {uso_cpu}%', fontsize=14, color='white', y=1.1)
    ax.set_xticks([])  # Eliminar los valores en el eje X
    ax.set_yticks([0, 25, 50, 75, 100])  # Mostrar los valores del eje Y
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'], fontsize=12, color='white')

    # Ajustar fondo y bordes
    ax.set_facecolor('blue')
    fig.patch.set_alpha(0.0)

    # Agregar un círculo central para mayor estética
    ax.set_yticks([0, 100])
    ax.set_ylim(0, 100)
    ax.grid(False)  # Desactivar las líneas de la cuadrícula

    return fig
def crear_grafico_ram(info):
    fig, ax = plt.subplots(figsize=(3, 1.8))  # Tamaño de la figura
    sizes = [info["RAM Usada (GB)"], info["RAM Libre (GB)"]]
    labels = ["Usada", "Libre"]
    colors = sns.color_palette("muted")
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'width': 0.4},
        textprops={'color': 'white'}  # Color de las etiquetas
    )
    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')
    ax.set_title("Uso de RAM (Dona)", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco

    # Eliminar el fondo blanco
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    return fig

def crear_grafico_disco(info):
    fig, ax = plt.subplots(figsize=(3, 1.8))  # Tamaño de la figura
    sizes = [info["Disco Usado (GB)"], info["Disco Libre (GB)"]]
    labels = ["Usado", "Libre"]
    colors = sns.color_palette("muted")
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'width': 0.4},
        textprops={'color': 'white'}  # Color de las etiquetas
    )
    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')
    ax.set_title("Espacio en Disco (Dona)", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco

    # Eliminar el fondo blanco
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    return fig

def crear_grafico_gpu(info):
    labels = ["Memoria Usada (GB)", "Memoria Libre (GB)"]
    values = [info["Memoria Usada (GB)"], info["Memoria Total (GB)"] - info["Memoria Usada (GB)"]]
    angles = np.linspace(0, 2.5 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(3, 1.8), subplot_kw=dict(polar=True))  # Tamaño de la figura
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7, color='white')  # Tamaño de la fuente ajustado y color blanco
    ax.set_title("Uso de GPU", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco

    # Eliminar el fondo blanco
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    return fig

