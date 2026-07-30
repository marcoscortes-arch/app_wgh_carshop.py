import streamlit as st
import os

# 1. Base de datos con los precios base extraídos de tu PDF
PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX": [
            {"producto": "Kit Cromado", "anos": "2003-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Apliques Negros de Faros y Guías", "anos": "2009-2013", "precio_base": 90.0, "obs": ""},
            {"producto": "Cubrelluvias", "anos": "2003-2025", "precio_base": 95.0, "obs": ""},
            {"producto": "Lamevidrios", "anos": "2014-2025", "precio_base": 85.0, "obs": "Diciembre"},
            {"producto": "Bandejas", "anos": "2014-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2014-2018", "precio_base": 55.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2009-2025", "precio_base": 135.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2019-2025", "precio_base": 165.0, "obs": ""},
            {"producto": "Estribos", "anos": "2014-2025", "precio_base": 175.0, "obs": "Diciembre"},
        ],
        "AVEO (EMOTION / FAMILY / ACTIVO)": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 25.0, "obs": ""}
        ]
    },
    "TOYOTA": {
        "HILUX": [
            {"producto": "Kit Cromados", "anos": "2003-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2003-2025", "precio_base": 165.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2003-2025", "precio_base": 125.0, "obs": ""}
        ]
    }
}

# Banco de fotos/enlaces del catálogo de WhatsApp (pueden ser rutas locales "img/dmax1.jpg" o URLs)
IMAGENES_CATALOGO = {
    "CHEVROLET_D-MAX_Mascarillas Con Luz": [
        "https://via.placeholder.com/600x400.png?text=D-MAX+Mascarilla+Con+Luz+Vista+1",
        "https://via.placeholder.com/600x400.png?text=D-MAX+Mascarilla+Con+Luz+Vista+2"
    ],
    "CHEVROLET_D-MAX_Kit Cromado": [
        "https://via.placeholder.com/600x400.png?text=D-MAX+Kit+Cromado"
    ]
}

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Cotizador & Buscador Visual", layout="wide")
st.title("📦 Cotizador y Buscador de Imágenes")

# Pestañas de Selección Secuencial
col1, col2, col3 = st.columns(3)

with col1:
    marca_sel = st.selectbox("1. Marca", list(PRECIOS_CATALOGO.keys()))

with col2:
    modelos_disponibles = list(PRECIOS_CATALOGO[marca_sel].keys())
    modelo_sel = st.selectbox("2. Modelo", modelos_disponibles)

with col3:
    productos_disponibles = [item["producto"] for item in PRECIOS_CATALOGO[marca_sel][modelo_sel]]
    producto_sel = st.selectbox("3. Repuesto", productos_disponibles)

# Obtener los datos del ítem seleccionado
detalles_lista = PRECIOS_CATALOGO[marca_sel][modelo_sel]
producto_info = next(item for item in detalles_lista if item["producto"] == producto_sel)
precio_base = producto_info["precio_base"]

st.markdown("---")

# Layout de 2 columnas principales: Ajuste de Precio a la izquierda / Búsqueda y Muestra de Imagen a la derecha
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader(f"🏷️ Detalle: {marca_sel} {modelo_sel}")
    st.write(f"**Producto:** {producto_sel}")
    st.write(f"**Años:** {producto_info['anos']}")
    if producto_info['obs']:
        st.info(f"**Observación:** {producto_info['obs']}")

    st.markdown("### 💰 Modificador de Precio")
    tipo_incremento = st.radio("Aplicar Incremento por:", ["Porcentaje (%)", "Monto Fijo ($)"], horizontal=True)
    
    if tipo_incremento == "Porcentaje (%)":
        porcentaje_inc = st.number_input("Porcentaje extra (%)", min_value=0.0, max_value=200.0, value=10.0, step=5.0)
        monto_inc = precio_base * (porcentaje_inc / 100.0)
    else:
        monto_inc = st.number_input("Monto extra ($)", min_value=0.0, value=15.0, step=5.0)

    precio_final = precio_base + monto_inc

    st.metric("Precio Base", f"${precio_base:.2f}")
    st.metric("Precio Final al Cliente", f"${precio_final:.2f}", delta=f"+${monto_inc:.2f}")

with col_der:
    st.subheader("🖼️ Galería y Búsqueda Visual del Producto")
    
    # Clave de búsqueda automática
    clave_busqueda = f"{marca_sel}_{modelo_sel}_{producto_sel}"
    
    # Streamlit busca la imagen asociada
    fotos_encontradas = IMAGENES_CATALOGO.get(clave_busqueda, [])
    
    if fotos_encontradas:
        st.success(f"Se encontraron {len(fotos_encontradas)} imagen(es) para este repuesto:")
        
        # Muestra visual en cuadrícula o pestañas de la imagen
        tabs = st.tabs([f"Foto {i+1}" for i in range(len(fotos_encontradas))])
        
        for i, url in enumerate(fotos_encontradas):
            with tabs[i]:
                # Streamlit muestra directamente la imagen buscada
                st.image(url, caption=f"{marca_sel} {modelo_sel} - {producto_sel}", use_container_width=True)
                
                # Botón de acción para guardar o descargar
                st.download_button(
                    label=f"📥 Guardar Foto {i+1} en el celular",
                    data=b"", # Reemplazar por binario si usas archivos locales
                    file_name=f"{clave_busqueda}_{i+1}.jpg",
                    mime="image/jpeg",
                    key=f"dl_{i}"
                )
    else:
        st.warning("⚠️ No se encontraron imágenes locales para esta combinación.")
        st.write("Puedes compartir directamente desde el Catálogo de WhatsApp Business usando el nombre exacto del producto.")
