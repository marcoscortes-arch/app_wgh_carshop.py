import streamlit as st
import urllib.parse
import os
from PIL import Image, ImageDraw, ImageFont
import io

PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX (2014-2018)": [
            {
                "producto": "Mascarilla D-Max (2014-2018)", 
                "anos": "2014-2018", 
                "precio": 175.0, 
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

def crear_ficha_consolidada(marca, modelo, producto, precio, anos, lista_rutas):
    """Crea una sola imagen uniendo las fotos y los datos de la cotización"""
    # Crear lienzo base (ancho 800px, alto dinámico)
    ancho_lienzo = 800
    alto_cabecera = 220
    alto_foto = 450
    
    # Filtrar solo imágenes existentes
    imgs_validas = [r for r in lista_rutas if os.path.exists(r)]
    num_imgs = len(imgs_validas) if len(imgs_validas) > 0 else 1
    
    alto_total = alto_cabecera + (alto_foto * num_imgs)
    lienzo = Image.new("RGB", (ancho_lienzo, alto_total), color=(20, 20, 20))
    draw = ImageDraw.Draw(lienzo)
    
    # Dibujar Cabecera
    draw.rectangle([(0, 0), (ancho_lienzo, alto_cabecera)], fill=(15, 15, 15))
    draw.rectangle([(0, alto_cabecera - 5), (ancho_lienzo, alto_cabecera)], fill=(217, 4, 41)) # Línea roja
    
    # Textos de la oferta
    draw.text((30, 20), "W.G.H CAR SHOP - FICHA DE OFERTA", fill=(255, 255, 255))
    draw.text((30, 60), f"Vehículo: {marca} {modelo}", fill=(220, 220, 220))
    draw.text((30, 95), f"Repuesto: {producto}", fill=(220, 220, 220))
    draw.text((30, 130), f"Años: {anos}", fill=(220, 220, 220))
    draw.text((30, 165), f"PRECIO ESPECIAL: ${precio:.2f} USD", fill=(37, 211, 102))

    # Pegar las imágenes una debajo de otra
    y_offset = alto_cabecera + 10
    for ruta in imgs_validas:
        img = Image.open(ruta).convert("RGB")
        # Escalar imagen manteniendo proporción
        img.thumbnail((ancho_lienzo - 40, alto_foto - 20))
        x_offset = (ancho_lienzo - img.width) // 2
        lienzo.paste(img, (x_offset, y_offset))
        y_offset += alto_foto

    # Guardar en buffer de memoria optimizado (JPEG liviano)
    buffer = io.BytesIO()
    lienzo.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Cotizador W.G.H CarShop", layout="wide")
st.title("📦 Cotizador y Gestor de Ofertas")

col1, col2, col3 = st.columns(3)
with col1:
    marca_sel = st.selectbox("1. Marca", list(PRECIOS_CATALOGO.keys()))
with col2:
    modelos_disponibles = list(PRECIOS_CATALOGO[marca_sel].keys())
    modelo_sel = st.selectbox("2. Modelo", modelos_disponibles)
with col3:
    productos_disponibles = [item["producto"] for item in PRECIOS_CATALOGO[marca_sel][modelo_sel]]
    producto_sel = st.selectbox("3. Repuesto", productos_disponibles)

detalles = PRECIOS_CATALOGO[marca_sel][modelo_sel]
info = next(item for item in detalles if item["producto"] == producto_sel)

st.markdown("---")

col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader(f"🏷️ Ficha: {marca_sel} {modelo_sel}")
    st.write(f"**Repuesto:** {info['producto']}")
    st.write(f"**Años compatibles:** {info['anos']}")
    
    precio_final = st.number_input(
        "💵 Precio Final ($ USD):", 
        min_value=0.0, 
        value=float(info['precio']), 
        step=5.0
    )

    st.markdown("### 🖼️ Galería de Fotografías")
    lista_imagenes = info.get("imagenes", [])
    if lista_imagenes:
        tabs = st.tabs([f"Foto {i+1}" for i in range(len(lista_imagenes))])
        for idx, tab in enumerate(tabs):
            with tab:
                ruta_img = lista_imagenes[idx]
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_column_width=True)

with col_der:
    st.subheader("🖼️ Generar Imagen de Oferta Única")
    st.info("Genera un banner liviano consolidado listo para enviar a tus clientes.")
    
    # Generar la imagen consolidada
    buffer_imagen = crear_ficha_consolidada(
        marca_sel, modelo_sel, info['producto'], precio_final, info['anos'], lista_imagenes
    )

    # Mostrar la previsualización de la imagen única generada
    st.image(buffer_imagen, caption="Ficha Consolidada Lista para WhatsApp", use_column_width=True)

    # Botón de Descarga
    st.download_button(
        label="📥 Descargar Imagen de Oferta (para enviar por WhatsApp)",
        data=buffer_imagen,
        file_name=f"Oferta_{marca_sel}_{modelo_sel}.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

    st.markdown("---")
    
    # Mensaje corto de acompañamiento
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")
    mensaje_texto = f"📌 Hola! Te adjunto la ficha de oferta de *{marca_sel} {modelo_sel}* (${precio_final:.2f} USD). ¡Revisa la imagen adjunta!"
    mensaje_encoded = urllib.parse.quote(mensaje_texto)
    url_wa_texto = f"https://wa.me/{telefono.strip()}?text={mensaje_encoded}" if telefono.strip() else f"https://wa.me/?text={mensaje_encoded}"

    st.markdown(
        f"""
        <a href="{url_wa_texto}" target="_blank">
            <button style="
                background-color: #25D366;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
            ">
                📲 Abrir WhatsApp y Adjuntar Imagen
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
