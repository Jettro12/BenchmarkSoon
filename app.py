import streamlit as st
from ProyectoDesarrollo import obtener_info_sistema, obtener_temperaturas_hardware

def mostrar_temperaturas(temperaturas):
    """
    Muestra las temperaturas del hardware en la interfaz gráfica.
    """
    if "Error" in temperaturas:
        # Si ocurre un error al obtener temperaturas, se muestra una advertencia.
        st.warning(temperaturas["Error"])
    else:
        for componente, temp in temperaturas.items():
            if temp is not None:  # Verificar si el valor no es None
                st.metric(label=f"Temperatura {componente}", value=f"{temp:.2f} °C")
            else:
                st.metric(label=f"Temperatura {componente}", value="No disponible")


def main():
    """
    Interfaz principal de la aplicación.
    """
    # Título principal de la página
    st.title("Monitor de Hardware")
    
    # Barra lateral
    st.sidebar.title("Opciones")
    st.sidebar.write("Seleccione la información a mostrar.")

    # Botón en la barra lateral para actualizar la información
    if st.sidebar.button("Actualizar Información"):
        # Se obtienen los datos del sistema y las temperaturas
        datos_pc = obtener_info_sistema()
        temperaturas = obtener_temperaturas_hardware()

        # **Sección de Información General**
        st.subheader("Información General del Sistema")
        st.write(f"**Procesador**: {datos_pc['Procesador']}")
        st.write(f"**RAM Total**: {datos_pc['RAM Total (GB)']} GB")
        st.write(f"**RAM Usada**: {datos_pc['RAM Usada (GB)']} GB")
        st.write(f"**RAM Libre**: {datos_pc['RAM Libre (GB)']} GB")
        st.write(f"**Disco Total**: {datos_pc['Disco Total (GB)']} GB")
        st.write(f"**Disco Usado**: {datos_pc['Disco Usado (GB)']} GB ({datos_pc['Disco Usado (%)']}%)")
        st.write(f"**Disco Libre**: {datos_pc['Disco Libre (GB)']} GB")
        st.write(f"**Tiempo de Uso del Sistema**: {datos_pc['Tiempo de Uso del Sistema']}")

        # **Sección de Temperaturas**
        st.subheader("Temperaturas del Hardware")
        mostrar_temperaturas(temperaturas)
    else:
        # Mensaje inicial antes de presionar "Actualizar Información"
        st.write("Presiona el botón 'Actualizar Información' en el menú lateral para comenzar.")

# Ejecución principal de la aplicación
if __name__ == "__main__":
    main()
