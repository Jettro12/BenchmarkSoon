import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def crear_grafico_cpu(info):
    fig, ax = plt.subplots(figsize=(3, 1.8))  # Aumenta el tamaño de la figura
    labels = ["Frecuencia Base", "Frecuencia Máxima", "Frecuencia Actual"]
    values = [
        info["Frecuencia Base (GHz)"],
        info["Frecuencia Máxima (GHz)"],
        info["Frecuencia Actual (GHz)"]
    ]
    sns.barplot(x=labels, y=values, hue=labels, palette="viridis", ax=ax, dodge=False, legend=False)
    
    # Ajustar el tamaño del texto de las etiquetas y títulos
    ax.set_title("Rendimiento del CPU", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco
    ax.set_ylabel("GHz", fontsize=7, color='white')  # Tamaño de la fuente ajustado y color blanco
    ax.set_xlabel("", fontsize=7, color='white')  # Color blanco para las etiquetas del eje x
    
    # Ajustar el tamaño y color de las etiquetas del eje
    ax.tick_params(axis='x', colors='white', labelsize=6)  # Tamaño ajustado y color blanco
    ax.tick_params(axis='y', colors='white', labelsize=6)  # Tamaño ajustado y color blanco

# Cambiar el color de los bordes de los ejes a blanco
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    # Eliminar el fondo blanco
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

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
    ax.set_title("Uso de RAM", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco

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
    ax.set_title("Espacio en Disco", fontsize=9, color='white')  # Tamaño de la fuente ajustado y color blanco

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

