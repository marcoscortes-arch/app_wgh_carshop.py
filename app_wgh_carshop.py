import streamlit as st
import urllib.parse
import os

# Base de datos configurada con LISTA de imágenes por producto
PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX (2014-2018)": [
            {
                "producto": "Mascarilla D-Max (2014-2018)", 
                "anos": "2014-2018", 
                "precio": 135.0, 
                "obs": "Modelos disponibles: Con Luces, Exhibición y QuCLuces", 
                "imagenes": [
                    "fotos/chevrolet_dmax_Mascarilla20142018CLuces.jpeg",
                    "fotos/chevrolet_dmax_Mascarilla20142018ExCLuces.jpeg",
                    "fotos/chevrolet_dmax_Mascarilla20142018QuCLuces.jpeg"
                ]
            }
        ]
    }
}

st.set_page_config(page_title="Cotizador W.G.H CarShop", layout="wide")
st.title("📦 Cotizador y Gestor de Ofertas")

# 1. Menús de Selección
col1, col2, col3 = st.columns(3)

with col1:
    marca_sel = st.selectbox("1. Marca", list(PRECIOS_CATALOGO.keys()))

with col2:
    modelos_disponibles = list(PRECIOS_CATALOGO[marca_sel].keys())
    modelo_sel = st.selectbox("2. Modelo", modelos_disponibles)

with col3:
    productos_disponibles = [item["producto"] for item in PRECIOS_CATALOGO[marca_sel][modelo_sel]]
    producto_sel = st.selectbox("3. Repuesto", productos_disponibles)

# Obtener datos del producto seleccionado
detalles = PRECIOS_CATALOGO[marca_sel][modelo_sel]
info = next(item for item in detalles if item["producto"] == producto_sel)

st.markdown("---")

col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader(f"🏷️ Ficha: {marca_sel} {modelo_sel}")
    st.write(f"**Repuesto:** {info['producto']}")
    st.write(f"**Años compatibles:** {info['anos']}")
    if info['obs']:
        st.info(f"**Observación:** {info['obs']}")
    
    precio_final = st.number_input(
        "💵 Precio Final ($ USD):", 
        min_value=0.0, 
        value=float(info['precio']), 
        step=5.0
    )

    # VISUALIZADOR DE MÚLTIPLES IMÁGENES EN STREAMLIT
    st.markdown("### 🖼️ Galería de Fotografías")
    lista_imagenes = info.get("imagenes", [])
    
    if lista_imagenes:
        # Pestañas organizadas para visualizar cada variante o ángulo
        tabs = st.tabs([f"Foto {i+1}" for i in range(len(lista_imagenes))])
        for idx, tab in enumerate(tabs):
            with tab:
                ruta_img = lista_imagenes[idx]
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_column_width=True)
                else:
                    st.warning(f"⚠️ Imagen no encontrada: `{ruta_img}`")
    else:
        st.warning("No hay imágenes asignadas para este repuesto.")

with col_der:
    st.subheader("📲 Opciones de Envío por WhatsApp")
    
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")

    mensaje_texto = (
        f"📌 *FICHA DE OFERTA - W.G.H CAR SHOP*\n\n"
        f"🚘 *Vehículo:* {marca_sel} {modelo_sel}\n"
        f"⚙️ *Repuesto:* {info['producto']}\n"
        f"📅 *Años:* {info['anos']}\n"
        f"💵 *Precio Oferta:* ${precio_final:.2f}\n"
    )
    if info['obs']:
        mensaje_texto += f"📝 *Nota:* {info['obs']}\n"
        
    mensaje_texto += "\n✨ *Producto garantizado. Escríbenos para confirmar tu pedido.*"

    mensaje_encoded = urllib.parse.quote(mensaje_texto)
    url_wa_texto = f"https://wa.me/{telefono.strip()}?text={mensaje_encoded}" if telefono.strip() else f"https://wa.me/?text={mensaje_encoded}"

    # Único botón para enviar WhatsApp
    st.markdown(
        f"""
        <a href="{url_wa_texto}" target="_blank">
            <button style="
                background-color: #25D366;
                color: white;
                border: none;
                padding: 14px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            ">
                📲 Enviar Ficha por WhatsApp
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
