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
# 2. CATÁLOGO BASE DE DATOS
# ---------------------------------------------------------
DATOS_PRODUCTOS = {
    "CHEVROLET": {
        "DMAX": [
            {"producto": "Kit Cromado", "anos": "2003-2025", "precio": 125.00},
            {"producto": "Apliques Negros de Faros y Guías", "anos": "2009-2013", "precio": 90.00},
            {"producto": "Cubrelluvias", "anos": "2003-2025", "precio": 95.00},
            {"producto": "Lamevidrios", "anos": "2014-2025", "precio": 85.00},
            {"producto": "Bandejas", "anos": "2014-2025", "precio": 55.00},
            {"producto": "Cromado de Neblineros", "anos": "2014-2018", "precio": 55.00},
            {"producto": "Cromado de Compuerta", "anos": "2003-2025", "precio": 75.00},
            {"producto": "Cobertor Cromado Retrovisor con Luz", "anos": "2003-2025", "precio": 85.00},
            {"producto": "Respiradero de Capot Cromado", "anos": "2014-2025", "precio": 60.00},
            {"producto": "Apliques Decorativos de Tablero", "anos": "2003-2007", "precio": 95.00},
            {"producto": "Mascarillas sin Luz", "anos": "2009-2025", "precio": 135.00},
            {"producto": "Mascarillas con Luz", "anos": "2019-2025", "precio": 165.00},
            {"producto": "Estribos", "anos": "2014-2025", "precio": 175.00},
            {"producto": "Rudones", "anos": "2014-2025", "precio": 130.00}
        ],
        "AVEO (Emotion Family Activo)": [
            {"producto": "Kit Cromado", "anos": "Varios", "precio": 125.00},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 25.00}
        ],
        "SAIL": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio": 125.00},
            {"producto": "Cromado de Neblinero", "anos": "2008-2016", "precio": 55.00},
            {"producto": "Contorno de Ventanas", "anos": "2017-2023", "precio": 110.00}
        ]
    },
    "TOYOTA": {
        "HILUX": [
            {"producto": "Kit Cromados", "anos": "2003-2025", "precio": 125.00},
            {"producto": "Cromado de Retrovisor con Luz", "anos": "2003-2015", "precio": 85.00},
            {"producto": "Lamevidrios", "anos": "2003-2025", "precio": 75.00},
            {"producto": "Mascarillas con Luz", "anos": "2003-2025", "precio": 165.00},
            {"producto": "Mascarillas sin Luz", "anos": "2003-2025", "precio": 125.00},
            {"producto": "Tapa de Balde Corrediza", "anos": "2017-2025", "precio": 850.00},
            {"producto": "Rudones", "anos": "2003-2025", "precio": 130.00}
        ],
        "FORTUNER": [
            {"producto": "Kit Cromados", "anos": "2008-2025", "precio": 125.00},
            {"producto": "Bisel de Compuerta con Luz", "anos": "2012-2025", "precio": 145.00},
            {"producto": "Mascarillas con Luz", "anos": "2008-2025", "precio": 165.00}
        ]
    },
    "HYUNDAI": {
        "TUCSON CLASICO": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.00},
            {"producto": "Mascarilla Cromada", "anos": "Varios", "precio": 110.00},
            {"producto": "Estribos", "anos": "Varios", "precio": 165.00}
        ],
        "TUCSON ix 35": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.00},
            {"producto": "Estribos", "anos": "Varios", "precio": 175.00},
            {"producto": "Mascarillas", "anos": "Varios", "precio": 155.00}
        ]
    },
    "FORD": {
        "RANGER": [
            {"producto": "Kit Cromado", "anos": "2012-2025", "precio": 125.00},
            {"producto": "Tapa de Balde Corrediza", "anos": "2012-2025", "precio": 850.00},
            {"producto": "Bodykit Raptor Guardachoques", "anos": "2017-2025", "precio": 1250.00},
            {"producto": "Mascarilla Raptor con Luz", "anos": "2012-2015", "precio": 260.00}
        ],
        "F-150": [
            {"producto": "Cubrelluvias Cromadas", "anos": "2009-2021", "precio": 180.00},
            {"producto": "Mascarillas", "anos": "2018-2024", "precio": 320.00},
            {"producto": "Tapa de Balde Corrediza", "anos": "2009-2025", "precio": 850.00}
        ]
    }
}

# ---------------------------------------------------------
# 3. FUNCIONES DE GENERACIÓN
# ---------------------------------------------------------
def generar_banner_cuadrado(marca, modelo, producto, precio, anos, lista_rutas):
    ANCHO, ALTO = 1080, 1080
    lienzo = Image.new("RGB", (ANCHO, ALTO), color=(15, 15, 15))
    draw = ImageDraw.Draw(lienzo)

    ALTO_CABECERA = 260
    draw.rectangle([(0, 0), (ANCHO, ALTO_CABECERA)], fill=(22, 22, 22))
    draw.rectangle([(0, ALTO_CABECERA - 6), (ANCHO, ALTO_CABECERA)], fill=(217, 4, 41))

    try:
        font_titulo = ImageFont.truetype("arial.ttf", 60)
        font_sub = ImageFont.truetype("arial.ttf", 42)
        font_repuesto = ImageFont.truetype("arial.ttf", 34)
        font_precio_label = ImageFont.truetype("arial.ttf", 30)
        font_precio = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font_titulo = font_sub = font_repuesto = font_precio_label = font_precio = ImageFont.load_default()

    draw.text((40, 25), "W.G.H CAR SHOP", fill=(217, 4, 41), font=font_titulo)
    draw.text((40, 95), f"{marca} {modelo}", fill=(255, 255, 255), font=font_sub)
    draw.text((40, 160), f"REPUESTO: {str(producto).upper()} ({anos})", fill=(200, 200, 200), font=font_repuesto)

    ANCHO_CAJA, ALTO_CAJA = 420, 180
    x_box_i, y_box_i = ANCHO - ANCHO_CAJA - 40, 35
    x_box_f, y_box_f = ANCHO - 40, y_box_i + ALTO_CAJA

    draw.rectangle([(x_box_i, y_box_i), (x_box_f, y_box_f)], fill=(10, 10, 10), outline=(217, 4, 41), width=4)
    draw.text((x_box_i + 30, y_box_i + 20), "PRECIO OFERTA", fill=(200, 200, 200), font=font_precio_label)
    draw.text((x_box_i + 30, y_box_i + 75), f"${precio:.2f}", fill=(255, 255, 255), font=font_precio)

    imgs_validas = [r for r in lista_rutas if os.path.exists(r)]
    y_inicio = ALTO_CABECERA + 20
    alto_disponible = ALTO - y_inicio - 20
    ancho_disponible = ANCHO - 40

    if imgs_validas:
        img = Image.open(imgs_validas[0]).convert("RGB")
        img.thumbnail((ancho_disponible, alto_disponible))
        x = (ANCHO - img.width) // 2
        lienzo.paste(img, (x, y_inicio))

    buffer = io.BytesIO()
    lienzo.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    return buffer

def generar_cotizacion_texto(marca, modelo, producto, precio, anos):
    return f"""========================================
     W.G.H CAR SHOP - COTIZACIÓN
========================================

Vehículo: {marca} {modelo}
Repuesto: {producto} ({anos})
Precio de Oferta: ${precio:.2f} USD

----------------------------------------
* Garantía de compatibilidad y calidad.
* Envíos a todo el país vía Servientrega.
* Pago contra entrega disponible.
========================================
"""

# ---------------------------------------------------------
# 4. ESTRUCTURA PRINCIPAL DE LA PÁGINA
# ---------------------------------------------------------
st.title("🚘 W.G.H CarShop - Generador de Ofertas")

col_izq, col_der = st.columns([1, 1])

# --- COLUMNA IZQUIERDA ---
with col_izq:
    st.subheader("📋 Selección de Producto y Vehículo")
    
    marca_sel = st.selectbox("Seleccione Marca:", list(DATOS_PRODUCTOS.keys()), key="sel_marca_db")
    modelos_disponibles = list(DATOS_PRODUCTOS[marca_sel].keys())
    modelo_sel = st.selectbox("Seleccione Modelo:", modelos_disponibles, key="sel_modelo_db")
    
    productos_lista = DATOS_PRODUCTOS[marca_sel][modelo_sel]
    nombres_prod = [f"{p['producto']} ({p['anos']})" for p in productos_lista]
    
    prod_idx = st.selectbox("Seleccione Repuesto:", range(len(nombres_prod)), format_func=lambda x: nombres_prod[x], key="sel_prod_db")
    prod_seleccionado = productos_lista[prod_idx]
    
    precio_final = st.number_input("Precio Oferta ($):", value=float(prod_seleccionado['precio']), key="input_precio_db")
    lista_imagenes = ["dmax_1.jpg"]

# --- COLUMNA DERECHA ---
with col_der:
    st.subheader("🖼️ Vista Previa y Descargas")
    
    buffer_banner = generar_banner_cuadrado(
        marca_sel, modelo_sel, prod_seleccionado['producto'], precio_final, prod_seleccionado['anos'], lista_imagenes
    )
    st.image(buffer_banner, caption="Afiche generado en tiempo real", use_container_width=True)

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        st.download_button(
            label="📥 Descargar Afiche (JPEG)",
            data=buffer_banner,
            file_name=f"Oferta_{marca_sel}_{modelo_sel}.jpg",
            mime="image/jpeg",
            use_container_width=True,
            key="btn_dl_afiche"
        )
    with c_btn2:
        txt_cotizacion = generar_cotizacion_texto(
            marca_sel, modelo_sel, prod_seleccionado['producto'], precio_final, prod_seleccionado['anos']
        )
        st.download_button(
            label="📄 Descargar Cotización (.TXT)",
            data=txt_cotizacion,
            file_name=f"Cotizacion_{marca_sel}_{modelo_sel}.txt",
            mime="text/plain",
            use_container_width=True,
            key="btn_dl_txt"
        )

    st.markdown("---")
    
    st.subheader("💬 Cierre de Venta (Pago Contra Entrega)")
    st.info("🚛 **Servientrega:** Envíos seguros con pago al recibir el producto.")
    
    mensaje_cierre = f"""¡Saludos! Le comparto los detalles para concretar su pedido de *{marca_sel} {modelo_sel}* ({prod_seleccionado['producto']}):

Nuestro sistema de trabajo es **pago contra entrega** con la seguridad de **Servientrega**. Una vez que el paquete llegue a su domicilio o agencia, usted realiza el pago directo al recibirlo.

Para emitir la guía de remisión, por favor ayúdenos con los siguientes datos:
1. Nombre y Apellido:
2. Número de Cédula:
3. Dirección exacta o Agencia Servientrega preferida:
4. Teléfono de contacto:

¡Apenas nos confirme los datos, preparamos y despachamos su paquete! 🚘"""

    st.text_area("Texto listo para enviar:", value=mensaje_cierre, height=180, key="txt_area_cierre_db")

    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="", key="input_telefono_db")
    
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
