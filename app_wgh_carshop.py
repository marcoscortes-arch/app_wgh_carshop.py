import streamlit as st
import urllib.parse

# 1. Base de datos con los precios base exactos del PDF
PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX": [
            {"producto": "Kit Cromado", "anos": "2003-2025", "precio": 125.0, "obs": ""},
            {"producto": "Apliques Negros de Faros y Guías", "anos": "2009-2013", "precio": 90.0, "obs": ""},
            {"producto": "Cubrelluvias", "anos": "2003-2025", "precio": 95.0, "obs": ""},
            {"producto": "Lamevidrios", "anos": "2014-2025", "precio": 85.0, "obs": "Diciembre"},
            {"producto": "Bandejas", "anos": "2014-2025", "precio": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2014-2018", "precio": 55.0, "obs": ""},
            {"producto": "Cromado de Compuerta", "anos": "2003-2025", "precio": 75.0, "obs": ""},
            {"producto": "Cobertor Cromado Retrovisor con Luz", "anos": "2003-2025", "precio": 85.0, "obs": ""},
            {"producto": "Respiradero de Capot Cromado", "anos": "2014-2025", "precio": 60.0, "obs": "Diciembre"},
            {"producto": "Apliques Decorativos de Tablero", "anos": "2003-2007", "precio": 95.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2009-2025", "precio": 135.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2019-2025", "precio": 165.0, "obs": ""},
            {"producto": "Estribos", "anos": "2014-2025", "precio": 175.0, "obs": "Diciembre"},
            {"producto": "Rudones", "anos": "2014-2025", "precio": 130.0, "obs": ""}
        ],
        "AVEO (EMOTION / FAMILY / ACTIVO)": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio": 25.0, "obs": ""}
        ],
        "OPTRA": [{"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2005-2007", "precio": 165.0, "obs": ""}],
        "SUZUKI SZ / NEC": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Respiraderos de Capot", "anos": "Todos", "precio": 35.0, "obs": ""},
            {"producto": "Tapa Combustible", "anos": "Todos", "precio": 25.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "Todos", "precio": 115.0, "obs": ""}
        ],
        "SPARK": [{"producto": "Cubrelluvias", "anos": "2008-2014", "precio": 95.0, "obs": ""}],
        "SPARK GT": [{"producto": "Kit Cromado", "anos": "2008-2014", "precio": 125.0, "obs": ""}],
        "GRAND VITARA": [{"producto": "Kit Cromado", "anos": "2008-2016", "precio": 125.0, "obs": ""}],
        "SAIL": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio": 125.0, "obs": ""},
            {"producto": "Cromado de Neblinero", "anos": "2008-2016", "precio": 55.0, "obs": ""},
            {"producto": "Cromado Tapa Combustible", "anos": "2008-2016", "precio": 25.0, "obs": ""},
            {"producto": "Bisel de Baúl", "anos": "2017-2023", "precio": 55.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2017-2023", "precio": 125.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2017-2023", "precio": 110.0, "obs": ""}
        ],
        "CAPTIVA": [{"producto": "Kit Cromado", "anos": "2006-2010", "precio": 125.0, "obs": ""}]
    },
    "TOYOTA": {
        "HILUX": [
            {"producto": "Kit Cromados", "anos": "2003-2025", "precio": 125.0, "obs": ""},
            {"producto": "Cromado Retrovisor con Luz", "anos": "2003-2015", "precio": 85.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2003-2025", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2003-2025", "precio": 25.0, "obs": ""},
            {"producto": "Lamevidrios", "anos": "2003-2025", "precio": 75.0, "obs": "Diciembre"},
            {"producto": "Cobertor Cromado Neblineros", "anos": "2003-2015", "precio": 55.0, "obs": ""},
            {"producto": "Cobertor Cromado Compuerta", "anos": "2012-2025", "precio": 55.0, "obs": ""},
            {"producto": "Luz de Compuerta", "anos": "2003-2011", "precio": 45.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2003-2025", "precio": 165.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2003-2025", "precio": 125.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2017-2025", "precio": 850.0, "obs": ""},
            {"producto": "Portavasos", "anos": "2003-2015", "precio": 110.0, "obs": "Diciembre"},
            {"producto": "Rudones", "anos": "2003-2025", "precio": 130.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2017-2025", "precio": 240.0, "obs": ""}
        ],
        "FORTUNER": [
            {"producto": "Kit Cromados", "anos": "2008-2025", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2008-2025", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2008-2025", "precio": 25.0, "obs": ""},
            {"producto": "Bisel Compuerta con Luz", "anos": "2012-2025", "precio": 145.0, "obs": ""},
            {"producto": "Letras Capot Cromadas / Negras", "anos": "2008-2025", "precio": 45.0, "obs": ""},
            {"producto": "LED Parachoques", "anos": "2017-2025", "precio": 85.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2025", "precio": 130.0, "obs": ""},
            {"producto": "Apliques Neblinero Grande", "anos": "2016-2025", "precio": 55.0, "obs": ""},
            {"producto": "Apliques Neblinero Pequeño", "anos": "2016-2025", "precio": 55.0, "obs": ""},
            {"producto": "Apliques Neblinero Parachoques", "anos": "2016-2025", "precio": 55.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2008-2025", "precio": 125.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2008-2025", "precio": 165.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2016-2025", "precio": 135.0, "obs": ""}
        ],
        "COROLLA": [{"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2007-2010", "precio": 165.0, "obs": ""}],
        "RAV4": [{"producto": "Kit Cromado +14 Piezas", "anos": "2005-2012", "precio": 155.0, "obs": ""}]
    },
    "KIA": {
        "SPORTAGE ACTIVE": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio": 20.0, "obs": ""},
            {"producto": "Cobertores de Guardachoques", "anos": "Todos", "precio": 220.0, "obs": ""},
            {"producto": "Cobertor Cromado Neblineros", "anos": "Todos", "precio": 115.0, "obs": ""},
            {"producto": "Kit de Plumas", "anos": "Todos", "precio": 75.0, "obs": ""},
            {"producto": "Neblineros", "anos": "Todos", "precio": 155.0, "obs": ""},
            {"producto": "Bisel de Capot", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Parantes de Compuerta", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio": 165.0, "obs": ""}
        ],
        "SPORTAGE R": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio": 20.0, "obs": ""},
            {"producto": "Cobertores de Guardachoques", "anos": "Todos", "precio": 220.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "Todos", "precio": 110.0, "obs": ""},
            {"producto": "Cromado de Plumas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Cromado Pluma Posterior", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio": 165.0, "obs": ""},
            {"producto": "Aplique Compuerta", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Cubre Lluvias", "anos": "Todos", "precio": 95.0, "obs": ""}
        ],
        "CERATO FORTE": [
            {"producto": "Kit Cromado", "anos": "2012-2016", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2016", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2012-2016", "precio": 25.0, "obs": ""}
        ],
        "RIO EXCITE": [{"producto": "Kit Cromado", "anos": "2007-2014", "precio": 125.0, "obs": ""}],
        "SORENTO": [{"producto": "Kit Cromado", "anos": "2009-2014", "precio": 125.0, "obs": ""}]
    },
    "HYUNDAI": {
        "TUCSON CLASICO": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Cobertor Retrovisor con Guía", "anos": "Todos", "precio": 85.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "Todos", "precio": 110.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio": 25.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "Todos", "precio": 220.0, "obs": ""},
            {"producto": "Kit de Plumas y Rejilla", "anos": "Todos", "precio": 115.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio": 165.0, "obs": ""}
        ],
        "TUCSON IX35": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio": 125.0, "obs": ""},
            {"producto": "Cubrelluvias", "anos": "Todos", "precio": 95.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio": 25.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "Todos", "precio": 220.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio": 175.0, "obs": ""},
            {"producto": "Bisel Capot y Compuerta", "anos": "Todos", "precio": 90.0, "obs": ""},
            {"producto": "Cromado de Pluma", "anos": "Todos", "precio": 55.0, "obs": ""},
            {"producto": "Mascarillas", "anos": "Todos", "precio": 155.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "Todos", "precio": 110.0, "obs": ""}
        ],
        "ACCENT": [
            {"producto": "Kit Cromado", "anos": "2007-2023", "precio": 125.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2007-2023", "precio": 25.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2023", "precio": 55.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2012-2023", "precio": 110.0, "obs": ""},
            {"producto": "Bisel de Baúl", "anos": "2012-2023", "precio": 55.0, "obs": ""}
        ],
        "CRETA": [{"producto": "Kit Cromado +14 Piezas", "anos": "2014-2018", "precio": 155.0, "obs": ""}],
        "TUCSON TL": [
            {"producto": "Kit Cromado +14 Piezas", "anos": "Hasta 2023", "precio": 155.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "2023", "precio": 155.0, "obs": ""}
        ],
        "FURGONETA H1": [
            {"producto": "Cromado Faros y Guías", "anos": "2005-2011", "precio": 90.0, "obs": ""},
            {"producto": "Cobertor con Luz Retrovisores", "anos": "2005-2011", "precio": 85.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2011-2018", "precio": 155.0, "obs": ""}
        ],
        "GETZ": [{"producto": "Kit Cromado", "anos": "Todos", "precio": 125.0, "obs": ""}],
        "SANTA FE": [
            {"producto": "Kit Cromado", "anos": "2006-2018", "precio": 125.0, "obs": ""},
            {"producto": "Estribos", "anos": "2007-2012", "precio": 165.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "2007-2012", "precio": 220.0, "obs": ""}
        ]
    },
    "NISSAN": {
        "TIIDA HATCHBACK": [{"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2014", "precio": 165.0, "obs": ""}],
        "QASHQAI": [{"producto": "Kit Cromado +14 Piezas", "anos": "2006-2010", "precio": 155.0, "obs": ""}],
        "FRONTIER": [{"producto": "Kit Cromado sin Retrovisores", "anos": "2016-2021", "precio": 125.0, "obs": ""}]
    },
    "MITSUBISHI": {
        "L200": [
            {"producto": "Kit Cromado 19 Piezas", "anos": "2006-2014", "precio": 250.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2015-2018", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2015-2018", "precio": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2015-2018", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2015-2018", "precio": 25.0, "obs": ""},
            {"producto": "Tapa de Balde", "anos": "2016-2024", "precio": 550.0, "obs": ""},
            {"producto": "Cromado Manija Compuerta", "anos": "2015-2018", "precio": 55.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2023", "precio": 130.0, "obs": ""}
        ]
    },
    "MAZDA": {
        "BT-50": [
            {"producto": "Kit Cromado", "anos": "2008-2023", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2008-2023", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2008-2015", "precio": 25.0, "obs": ""},
            {"producto": "Cromado Manija Compuerta", "anos": "2008-2015", "precio": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2016-2023", "precio": 55.0, "obs": ""},
            {"producto": "Respiraderos Cromados", "anos": "2016-2023", "precio": 35.0, "obs": ""},
            {"producto": "Mascarilla", "anos": "2016-2023", "precio": 165.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2023", "precio": 130.0, "obs": ""}
        ]
    },
    "FORD": {
        "RANGER": [
            {"producto": "Kit Cromado", "anos": "2012-2025", "precio": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2025", "precio": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2012-2025", "precio": 25.0, "obs": ""},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2012-2025", "precio": 650.0, "obs": ""},
            {"producto": "Rudones", "anos": "2012-2026", "precio": 130.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2012-2025", "precio": 850.0, "obs": ""},
            {"producto": "Faros LED", "anos": "2017-2025", "precio": 750.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2017-2025", "precio": 240.0, "obs": ""},
            {"producto": "Bodykit Raptor Cárter Metálico", "anos": "2017-2025", "precio": 850.0, "obs": ""},
            {"producto": "Bodykit Raptor Guardachoques Metálico", "anos": "2017-2025", "precio": 1250.0, "obs": ""},
            {"producto": "Bodykit Raptor LED Guardachoques", "anos": "2017-2025", "precio": 750.0, "obs": ""},
            {"producto": "Bodykit T9", "anos": "2026", "precio": 1250.0, "obs": ""},
            {"producto": "Mascarilla Raptor Sin Luz", "anos": "2012-2015", "precio": 145.0, "obs": ""},
            {"producto": "Mascarilla Raptor Con Luz", "anos": "2012-2015", "precio": 260.0, "obs": ""},
            {"producto": "Mascarilla Raptor Gasolina", "anos": "2017-2025", "precio": 220.0, "obs": ""},
            {"producto": "Mascarilla Raptor Diesel", "anos": "2017-2025", "precio": 220.0, "obs": ""},
            {"producto": "Mascarilla Raptor T9", "anos": "2025", "precio": 220.0, "obs": ""},
            {"producto": "Estribos Raptor", "anos": "2017-2026", "precio": 340.0, "obs": ""}
        ],
        "ECOSPORT": [{"producto": "Kit Cromado", "anos": "2013-2015", "precio": 125.0, "obs": ""}],
        "ESCAPE": [
            {"producto": "Kit Cromado", "anos": "2013-2015", "precio": 125.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "2007-2012", "precio": 220.0, "obs": ""}
        ],
        "F-150": [
            {"producto": "Cobertores Cromados Guías", "anos": "2009-2021", "precio": 115.0, "obs": ""},
            {"producto": "Cobertores Cromados Retrovisores", "anos": "2009-2021", "precio": 115.0, "obs": ""},
            {"producto": "Cubrelluvias Cromadas", "anos": "2009-2021", "precio": 180.0, "obs": ""},
            {"producto": "Cubrelluvias Color Negro", "anos": "2009-2014", "precio": 160.0, "obs": ""},
            {"producto": "Aplique Cromado Compuerta", "anos": "2009-2014", "precio": 350.0, "obs": ""},
            {"producto": "Cromado Manijas", "anos": "2009-2021", "precio": 85.0, "obs": ""},
            {"producto": "Bandejas Cromadas", "anos": "2009-2021", "precio": 75.0, "obs": ""},
            {"producto": "Mascarillas", "anos": "1978-2017", "precio": 220.0, "obs": "1998-2003 NO"},
            {"producto": "Mascarillas", "anos": "2018-2024", "precio": 320.0, "obs": ""},
            {"producto": "Guardachoque", "anos": "2009-2021", "precio": 650.0, "obs": ""},
            {"producto": "Faldones / Fenders Raptor", "anos": "2009-2021", "precio": 295.0, "obs": ""},
            {"producto": "Faldones / Fenders de Pernos", "anos": "2009-2021", "precio": 265.0, "obs": ""},
            {"producto": "Aplique Negro Compuerta", "anos": "2015-2025", "precio": 195.0, "obs": ""},
            {"producto": "Parachoque Negro", "anos": "2009-2021", "precio": 350.0, "obs": ""},
            {"producto": "Parachoque Cromado", "anos": "2009-2021", "precio": 350.0, "obs": ""},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2009-2025", "precio": 650.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2009-2025", "precio": 850.0, "obs": ""},
            {"producto": "Faros LED", "anos": "2009-2015", "precio": 650.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2009-2014", "precio": 390.0, "obs": ""}
        ],
        "EXPLORER": [
            {"producto": "Kit Cromado", "anos": "2007-2011", "precio": 125.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2012-2015", "precio": 195.0, "obs": ""},
            {"producto": "Tapa Combustible Cromada", "anos": "2012-2015", "precio": 25.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "1995-2017", "precio": 220.0, "obs": "2002-2006 DIC"},
            {"producto": "Letras de Capot", "anos": "1995-2026", "precio": 40.0, "obs": ""}
        ],
        "EXPLORER SPORTRACK": [
            {"producto": "Kit Cromado", "anos": "2007-2011", "precio": 125.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "2007-2011", "precio": 220.0, "obs": ""}
        ]
    }
}

# Link directo a tu Catálogo de WhatsApp Business
URL_CATALOGO_GENERAL = "https://wa.me/c/593987278753"

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Cotizador & WhatsApp Business", layout="wide")
st.title("📦 Cotizador y Gestor de Ofertas")

# 1. Pestañas / Menús de Selección
col1, col2, col3 = st.columns(3)

with col1:
    marca_sel = st.selectbox("1. Marca", list(PRECIOS_CATALOGO.keys()))

with col2:
    modelos_disponibles = list(PRECIOS_CATALOGO[marca_sel].keys())
    modelo_sel = st.selectbox("2. Modelo", modelos_disponibles)

with col3:
    productos_disponibles = [item["producto"] for item in PRECIOS_CATALOGO[marca_sel][modelo_sel]]
    producto_sel = st.selectbox("3. Repuesto", productos_disponibles)

# Obtener los datos del producto
detalles = PRECIOS_CATALOGO[marca_sel][modelo_sel]
info = next(item for item in detalles if item["producto"] == producto_sel)

st.markdown("---")

col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader(f"🏷️ Ficha de Oferta: {marca_sel} {modelo_sel}")
    st.write(f"**Repuesto:** {info['producto']}")
    st.write(f"**Años compatibles:** {info['anos']}")
    if info['obs']:
        st.info(f"**Observación:** {info['obs']}")
    
    st.metric("Precio Oferta", f"${info['precio']:.2f}")

with col_der:
    st.subheader("📲 Opciones de Envío por WhatsApp")
    
    # Campo opcional para teléfono
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")

    # Generación de la Ficha Técnica de Texto
    mensaje_texto = (
        f"📌 *FICHA DE OFERTA*\n\n"
        f"🚘 *Vehículo:* {marca_sel} {modelo_sel}\n"
        f"⚙️ *Repuesto:* {info['producto']}\n"
        f"📅 *Años:* {info['anos']}\n"
        f"💵 *Precio Oferta:* ${info['precio']:.2f}\n"
    )
    if info['obs']:
        mensaje_texto += f"📝 *Nota:* {info['obs']}\n"
    mensaje_texto += "\n✨ *Producto garantizado. Escríbenos para confirmar tu pedido.*"

    mensaje_encoded = urllib.parse.quote(mensaje_texto)
    url_wa_texto = f"https://wa.me/{telefono.strip()}?text={mensaje_encoded}" if telefono.strip() else f"https://wa.me/?text={mensaje_encoded}"

    # Botón 1: Enviar Ficha Técnica en Texto
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
                margin-bottom: 12px;
            ">
                📲 Enviar Ficha de Texto por WhatsApp
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # Botón 2: Abrir Catálogo Nativo con Fotos
    st.markdown(
        f"""
        <a href="{URL_CATALOGO_GENERAL}" target="_blank">
            <button style="
                background-color: #075E54;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
            ">
                🛍️ Abrir Catálogo de WhatsApp Business
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )amente desde tu Catálogo de WhatsApp Business.")
