import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import urllib.parse
import io
import os

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="W.G.H CarShop - Generador de Ofertas",
    page_icon="🚘",
    layout="wide"
)

# ---------------------------------------------------------
# 2. FUNCIÓN DE GENERACIÓN DEL AFICHE (1080x1080)
# ---------------------------------------------------------
def generar_banner_cuadrado(marca, modelo, producto, precio, anos, lista_rutas):
    ANCHO, ALTO = 1080, 1080
    lienzo = Image.new("RGB", (ANCHO, ALTO), color=(15, 15, 15))
    draw = ImageDraw.Draw(lienzo)

    # Cabecera Elegante
    ALTO_CABECERA = 260
    draw.rectangle([(0, 0), (ANCHO, ALTO_CABECERA)], fill=(22, 22, 22))
    draw.rectangle([(0, ALTO_CABECERA - 6), (ANCHO, ALTO_CABECERA)], fill=(217, 4, 41))

    # Fuentes ajustadas y grandes
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 60)
        font_sub = ImageFont.truetype("arial.ttf", 42)
        font_repuesto = ImageFont.truetype("arial.ttf", 36)
        font_precio_label = ImageFont.truetype("arial.ttf", 32)
        font_precio = ImageFont.truetype("arial.ttf", 64)
    except IOError:
        font_titulo = font_sub = font_repuesto = font_precio_label = font_precio = ImageFont.load_default()

    # Textos principales (Izquierda)
    draw.text((40, 25), "W.G.H CAR SHOP", fill=(217, 4, 41), font=font_titulo)
    draw.text((40, 95), f"{marca} {modelo}", fill=(255, 255, 255), font=font_sub)
    draw.text((40, 160), f"REPUESTO: {str(producto).upper()} ({anos})", fill=(200, 200, 200), font=font_repuesto)
    
    # Caja de Precio (Derecha)
    ANCHO_CAJA, ALTO_CAJA = 420, 180
    x_box_i, y_box_i = ANCHO - ANCHO_CAJA - 40, 35
    x_box_f, y_box_f = ANCHO - 40, y_box_i + ALTO_CAJA

    draw.rectangle([(x_box_i, y_box_i), (x_box_f, y_box_f)], fill=(10, 10, 10), outline=(217, 4, 41), width=4)
    draw.text((x_box_i + 30, y_box_i + 20), "PRECIO OFERTA", fill=(200, 200, 200), font=font_precio_label)
    draw.text((x_box_i + 30, y_box_i + 75), f"${precio:.2f}", fill=(255, 255, 255), font=font_precio)

    # Procesar Fotografías
    imgs_validas = [r for r in lista_rutas if os.path.exists(r)]
    num_imgs = len(imgs_validas)
    y_inicio = ALTO_CABECERA + 20
    alto_disponible = ALTO - y_inicio - 20
    ancho_disponible = ANCHO - 40

    if num_imgs == 1:
        img = Image.open(imgs_validas[0]).convert("RGB")
        img.thumbnail((ancho_disponible, alto_disponible))
        x = (ANCHO - img.width) // 2
        lienzo.paste(img, (x, y_inicio))
    elif num_imgs == 2:
        w_box = (ancho_disponible // 2) - 10
        for i, ruta in enumerate(imgs_validas[:2]):
            img = Image.open(ruta).convert("RGB")
            img.thumbnail((w_box, alto_disponible))
            lienzo.paste(img, (20 + i * (w_box + 20), y_inicio))
    elif num_imgs >= 3:
        w_izq = (ancho_disponible // 2) - 10
        h_der = (alto_disponible // 2) - 10

        img1 = Image.open(imgs_validas[0]).convert("RGB")
        img1.thumbnail((w_izq, alto_disponible))
        lienzo.paste(img1, (20, y_inicio))

        img2 = Image.open(imgs_validas[1]).convert("RGB")
        img2.thumbnail((w_izq, h_der))
        lienzo.paste(img2, (20 + w_izq + 20, y_inicio))

        img3 = Image.open(imgs_validas[2]).convert("RGB")
        img3.thumbnail((w_izq, h_der))
        lienzo.paste(img3, (20 + w_izq + 20, y_inicio + h_der + 20))

    buffer = io.BytesIO()
    lienzo.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    return buffer

# ---------------------------------------------------------
# 3. INTERFAZ EN COLUMNAS (ESTRUCTURA ÚNICA Y SIN DUPLICADOS)
# ---------------------------------------------------------
st.title("🚘 W.G.H CarShop - Generador de Ofertas")

col_izq, col_der = st.columns([1, 1])

# --- COLUMNA IZQUIERDA: PARÁMETROS ---
with col_izq:
    st.subheader("📋 Datos del Vehículo y Repuesto")
    
    # Asegúrate de mantener tus variables o diccionarios base aquí:
    marca_sel = st.selectbox("Seleccione Marca:", ["CHEVROLET"], key="sel_marca")
    modelo_sel = st.selectbox("Seleccione Modelo:", ["D-MAX"], key="sel_modelo")
    
    # Datos del producto
    info = {
        'producto': 'Mascarilla D-Max con LED',
        'anos': '2014-2018',
        'precio': 175.00
    }
    
    precio_final = st.number_input("Precio Final ($):", value=info['precio'], key="input_precio")
    
    # Lista de imágenes locales para el banner
    lista_imagenes = ["dmax_1.jpg", "dmax_2.jpg"]  # Reemplaza con tus rutas reales

# --- COLUMNA DERECHA: RESULTADO Y CIERRE DE VENTA ---
with col_der:
    st.subheader("🖼️ Afiche Publicitario (1080x1080)")
    
    # 1. Generar banner
    buffer_banner = generar_banner_cuadrado(
        marca_sel, modelo_sel, info['producto'], precio_final, info['anos'], lista_imagenes
    )

    # 2. Mostrar imagen
    st.image(buffer_banner, caption="Afiche listo para WhatsApp", use_container_width=True)

    # 3. Botón descargar
    st.download_button(
        label="📥 Descargar Afiche (JPEG)",
        data=buffer_banner,
        file_name=f"Oferta_{marca_sel}_{modelo_sel}.jpg",
        mime="image/jpeg",
        use_container_width=True,
        key="btn_descarga_banner"
    )

    st.markdown("---")
    
    # 4. Sección de Cierre de Venta
    st.subheader("💬 Cierre de Venta (Pago Contra Entrega)")
    st.info("🚛 **Servientrega:** Envíos seguros con pago al recibir el producto.")
    
    mensaje_cierre = f"""¡Saludos! Le comparto los detalles para concretar su pedido de *{marca_sel} {modelo_sel}* ({info['producto']}):

Nuestro sistema de trabajo es **pago contra entrega** con la seguridad de **Servientrega**. Una vez que el paquete llegue a su domicilio o agencia, usted realiza el pago directo al recibirlo.

Para emitir la guía de remisión, por favor ayúdenos con los siguientes datos:
1. Nombre y Apellido:
2. Número de Cédula:
3. Dirección exacta o Agencia Servientrega preferida:
4. Teléfono de contacto:

¡Apenas nos confirme los datos, preparamos y despachamos su paquete! 🚘"""

    st.text_area("Texto listo para copiar:", value=mensaje_cierre, height=200, key="txt_area_cierre")

    # 5. Teléfono (ÚNICO INPUT)
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="", key="input_telefono_unico_v1")
    
    # 6. Botón de WhatsApp (ÚNICO BOTÓN)
    mensaje_encoded = urllib.parse.quote(mensaje_cierre)
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
                margin-top: 10px;
            ">
                📲 Enviar Cierre de Venta por WhatsApp
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
