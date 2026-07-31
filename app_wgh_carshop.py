import streamlit as st
import urllib.parse
import os
from PIL import Image, ImageDraw, ImageFont
import io

# 1. Base de datos de repuestos
PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX (2014-2018)": [
            {
                "producto": "Mascarilla D-Max", 
                "anos": "2014-2018", 
                "precio": 175.0, 
                "obs": "Incluye Kit de Luces LED", 
                "imagenes": [
                    "fotos/chevrolet_dmax_Mascarilla20142018CLuces.jpeg",
                    "fotos/chevrolet_dmax_Mascarilla20142018ExCLuces.jpeg",
                    "fotos/chevrolet_dmax_Mascarilla20142018QuCLuces.jpeg"
                ]
            }
        ]
    }
}

def generar_banner_cuadrado(marca, modelo, producto, precio, anos, lista_rutas):
    """
    Genera una sola imagen cuadrada estilo afiche publicitario (1080x1080 px)
    con tipografía grande y distribución nítida.
    """
    ANCHO, ALTO = 1080, 1080
    lienzo = Image.new("RGB", (ANCHO, ALTO), color=(15, 15, 15))
    draw = ImageDraw.Draw(lienzo)

    # 1. Franja Superior (Cabecera Publicitaria)
    ALTO_CABECERA = 240
    draw.rectangle([(0, 0), (ANCHO, ALTO_CABECERA)], fill=(20, 20, 20))
    draw.rectangle([(0, ALTO_CABECERA - 8), (ANCHO, ALTO_CABECERA)], fill=(217, 4, 41)) # Línea roja de marca

    # Cargar tipografía por defecto o personalizada
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 36)
        font_precio = ImageFont.truetype("arial.ttf", 52)
    except IOError:
        font_titulo = font_sub = font_precio = ImageFont.load_default()

    # Textos de la Oferta
    draw.text((40, 25), "W.G.H CAR SHOP", fill=(217, 4, 41), font=font_titulo)
    draw.text((40, 85), f"{marca} {modelo} ({anos})", fill=(255, 255, 255), font=font_sub)
    draw.text((40, 135), f"REPUESTO: {producto.upper()}", fill=(200, 200, 200), font=font_sub)
    
    # Caja destacada para el Precio
    draw.rectangle([(ANCHO - 380, 30), (ANCHO - 40, 180)], fill=(37, 211, 102))
    draw.text((ANCHO - 360, 50), "OFERTA", fill=(0, 0, 0), font=font_sub)
    draw.text((ANCHO - 360, 100), f"${precio:.2f}", fill=(0, 0, 0), font=font_precio)

    # 2. Organización Mosaico de Fotografías (Grid)
    imgs_validas = [r for r in lista_rutas if os.path.exists(r)]
    num_imgs = len(imgs_validas)

    y_inicio = ALTO_CABECERA + 15
    alto_disponible = ALTO - y_inicio - 20
    ancho_disponible = ANCHO - 40

    if num_imgs == 1:
        # 1 foto centrada grande
        img = Image.open(imgs_validas[0]).convert("RGB")
        img.thumbnail((ancho_disponible, alto_disponible))
        x = (ANCHO - img.width) // 2
        lienzo.paste(img, (x, y_inicio))

    elif num_imgs == 2:
        # 2 fotos lado a lado
        w_box = (ancho_disponible // 2) - 10
        for i, ruta in enumerate(imgs_validas[:2]):
            img = Image.open(ruta).convert("RGB")
            img.thumbnail((w_box, alto_disponible))
            x = 20 + i * (w_box + 20)
            lienzo.paste(img, (x, y_inicio))

    elif num_imgs >= 3:
        # 3 fotos: 1 principal grande a la izquierda, 2 secundarias a la derecha
        w_izq = (ancho_disponible // 2) - 10
        h_der = (alto_disponible // 2) - 10

        # Foto 1 (Izquierda)
        img1 = Image.open(imgs_validas[0]).convert("RGB")
        img1.thumbnail((w_izq, alto_disponible))
        lienzo.paste(img1, (20, y_inicio))

        # Foto 2 (Derecha Arriba)
        img2 = Image.open(imgs_validas[1]).convert("RGB")
        img2.thumbnail((w_izq, h_der))
        lienzo.paste(img2, (20 + w_izq + 20, y_inicio))

        # Foto 3 (Derecha Abajo)
        img3 = Image.open(imgs_validas[2]).convert("RGB")
        img3.thumbnail((w_izq, h_der))
        lienzo.paste(img3, (20 + w_izq + 20, y_inicio + h_der + 20))

    # Guardar en memoria RAM optimizado
    buffer = io.BytesIO()
    lienzo.save(buffer, format="JPEG", quality=88)
    buffer.seek(0)
    return buffer

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Cotizador W.G.H CarShop", layout="wide")
st.title("📦 Cotizador y Creador de Ofertas")

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

    st.markdown("### 🖼️ Galería Individual")
    lista_imagenes = info.get("imagenes", [])
    if lista_imagenes:
        tabs = st.tabs([f"Foto {i+1}" for i in range(len(lista_imagenes))])
        for idx, tab in enumerate(tabs):
            with tab:
                ruta_img = lista_imagenes[idx]
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_column_width=True)

with col_der:
    st.subheader("🖼️ Afiche de Oferta Consolidado (1080x1080)")
    
    # Generar el banner cuadrado
    buffer_banner = generar_banner_cuadrado(
        marca_sel, modelo_sel, info['producto'], precio_final, info['anos'], lista_imagenes
    )

    # Previsualización
    st.image(buffer_banner, caption="Vista previa del banner publicitario para WhatsApp", use_column_width=True)

    # Botón de Descarga
    st.download_button(
        label="📥 Descargar Afiche de Oferta (JPEG)",
        data=buffer_banner,
        file_name=f"Oferta_{marca_sel}_{modelo_sel}.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

    st.markdown("---")
    
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")
    mensaje_texto = f"📌 *W.G.H CAR SHOP* | Adjunto la ficha de oferta para *{marca_sel} {modelo_sel}* (${precio_final:.2f} USD). ¡Revisa el afiche adjunto!"
    mensaje_encoded = urllib.parse.quote(mensaje_texto)
    url_wa_texto = f"https://wa.me/{telefono.strip()}?text={mensaje_encoded}" if telefono.strip() else f"https://wa.me/?text={mensaje_encoded}"

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
            ">
                📲 Abrir WhatsApp y Adjuntar Afiche
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
