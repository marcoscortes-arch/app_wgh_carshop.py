import streamlit as st
import os

PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX": [
            {"producto": "Kit Cromado", "anos": "2003-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Apliques Negros de Faros y Guías", "anos": "2009-2013", "precio_base": 90.0, "obs": ""},
            {"producto": "Cubrelluvias", "anos": "2003-2025", "precio_base": 95.0, "obs": ""},
            {"producto": "Lamevidrios", "anos": "2014-2025", "precio_base": 85.0, "obs": "Diciembre"},
            {"producto": "Bandejas", "anos": "2014-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2014-2018", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado de Compuerta", "anos": "2003-2025", "precio_base": 75.0, "obs": ""},
            {"producto": "Cobertor Cromado Retrovisor con Luz", "anos": "2003-2025", "precio_base": 85.0, "obs": ""},
            {"producto": "Respiradero de Capot Cromado", "anos": "2014-2025", "precio_base": 60.0, "obs": "Diciembre"},
            {"producto": "Apliques Decorativos de Tablero", "anos": "2003-2007", "precio_base": 95.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2009-2025", "precio_base": 135.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2019-2025", "precio_base": 165.0, "obs": ""},
            {"producto": "Estribos", "anos": "2014-2025", "precio_base": 175.0, "obs": "Diciembre"},
            {"producto": "Rudones", "anos": "2014-2025", "precio_base": 130.0, "obs": ""}
        ],
        "AVEO (EMOTION / FAMILY / ACTIVO)": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 25.0, "obs": ""}
        ],
        "OPTRA": [
            {"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2005-2007", "precio_base": 165.0, "obs": ""}
        ],
        "SUZUKI SZ / NEC": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Respiraderos de Capot", "anos": "Todos", "precio_base": 35.0, "obs": ""},
            {"producto": "Tapa Combustible", "anos": "Todos", "precio_base": 25.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "Todos", "precio_base": 115.0, "obs": ""}
        ],
        "SPARK": [
            {"producto": "Cubrelluvias", "anos": "2008-2014", "precio_base": 95.0, "obs": ""}
        ],
        "SPARK GT": [
            {"producto": "Kit Cromado", "anos": "2008-2014", "precio_base": 125.0, "obs": ""}
        ],
        "GRAND VITARA": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio_base": 125.0, "obs": ""}
        ],
        "SAIL": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio_base": 125.0, "obs": ""},
            {"producto": "Cromado de Neblinero", "anos": "2008-2016", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado Tapa Combustible", "anos": "2008-2016", "precio_base": 25.0, "obs": ""},
            {"producto": "Bisel de Baúl", "anos": "2017-2023", "precio_base": 55.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2017-2023", "precio_base": 125.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2017-2023", "precio_base": 110.0, "obs": ""}
        ],
        "CAPTIVA": [
            {"producto": "Kit Cromado", "anos": "2006-2010", "precio_base": 125.0, "obs": ""}
        ]
    },
    "TOYOTA": {
        "HILUX": [
            {"producto": "Kit Cromados", "anos": "2003-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Cromado Retrovisor con Luz", "anos": "2003-2015", "precio_base": 85.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2003-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2003-2025", "precio_base": 25.0, "obs": ""},
            {"producto": "Lamevidrios", "anos": "2003-2025", "precio_base": 75.0, "obs": "Diciembre"},
            {"producto": "Cobertor Cromado Neblineros", "anos": "2003-2015", "precio_base": 55.0, "obs": ""},
            {"producto": "Cobertor Cromado Compuerta", "anos": "2012-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Luz de Compuerta", "anos": "2003-2011", "precio_base": 45.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2003-2025", "precio_base": 165.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2003-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2017-2025", "precio_base": 850.0, "obs": ""},
            {"producto": "Portavasos", "anos": "2003-2015", "precio_base": 110.0, "obs": "Diciembre"},
            {"producto": "Rudones", "anos": "2003-2025", "precio_base": 130.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2017-2025", "precio_base": 240.0, "obs": ""}
        ],
        "FORTUNER": [
            {"producto": "Kit Cromados", "anos": "2008-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2008-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2008-2025", "precio_base": 25.0, "obs": ""},
            {"producto": "Bisel Compuerta con Luz", "anos": "2012-2025", "precio_base": 145.0, "obs": ""},
            {"producto": "Letras Capot Cromadas / Negras", "anos": "2008-2025", "precio_base": 45.0, "obs": ""},
            {"producto": "LED Parachoques", "anos": "2017-2025", "precio_base": 85.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2025", "precio_base": 130.0, "obs": ""},
            {"producto": "Apliques Neblinero Grande", "anos": "2016-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Apliques Neblinero Pequeño", "anos": "2016-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Apliques Neblinero Parachoques", "anos": "2016-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Mascarillas Sin Luz", "anos": "2008-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Mascarillas Con Luz", "anos": "2008-2025", "precio_base": 165.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2016-2025", "precio_base": 135.0, "obs": ""}
        ],
        "COROLLA": [
            {"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2007-2010", "precio_base": 165.0, "obs": ""}
        ],
        "RAV4": [
            {"producto": "Kit Cromado +14 Piezas", "anos": "2005-2012", "precio_base": 155.0, "obs": ""}
        ]
    },
    "KIA": {
        "SPORTAGE ACTIVE": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 20.0, "obs": ""},
            {"producto": "Cobertores de Guardachoques", "anos": "Todos", "precio_base": 220.0, "obs": ""},
            {"producto": "Cobertor Cromado Neblineros", "anos": "Todos", "precio_base": 115.0, "obs": ""},
            {"producto": "Kit de Plumas", "anos": "Todos", "precio_base": 75.0, "obs": ""},
            {"producto": "Neblineros", "anos": "Todos", "precio_base": 155.0, "obs": ""},
            {"producto": "Bisel de Capot", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Parantes de Compuerta", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio_base": 165.0, "obs": ""}
        ],
        "SPORTAGE R": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 20.0, "obs": ""},
            {"producto": "Cobertores de Guardachoques", "anos": "Todos", "precio_base": 220.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "Todos", "precio_base": 110.0, "obs": ""},
            {"producto": "Cromado de Plumas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado Pluma Posterior", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio_base": 165.0, "obs": ""},
            {"producto": "Aplique Compuerta", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Cubre Lluvias", "anos": "Todos", "precio_base": 95.0, "obs": ""}
        ],
        "CERATO FORTE": [
            {"producto": "Kit Cromado", "anos": "2012-2016", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2016", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2012-2016", "precio_base": 25.0, "obs": ""}
        ],
        "RIO EXCITE": [
            {"producto": "Kit Cromado", "anos": "2007-2014", "precio_base": 125.0, "obs": ""}
        ],
        "SORENTO": [
            {"producto": "Kit Cromado", "anos": "2009-2014", "precio_base": 125.0, "obs": ""}
        ]
    },
    "HYUNDAI": {
        "TUCSON CLASICO": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Cobertor Retrovisor con Guía", "anos": "Todos", "precio_base": 85.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "Todos", "precio_base": 110.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 25.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "Todos", "precio_base": 220.0, "obs": ""},
            {"producto": "Kit de Plumas y Rejilla", "anos": "Todos", "precio_base": 115.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio_base": 165.0, "obs": ""}
        ],
        "TUCSON IX35": [
            {"producto": "Kit Cromados", "anos": "Todos", "precio_base": 125.0, "obs": ""},
            {"producto": "Cubrelluvias", "anos": "Todos", "precio_base": 95.0, "obs": ""},
            {"producto": "Bandejas", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "Todos", "precio_base": 25.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "Todos", "precio_base": 220.0, "obs": ""},
            {"producto": "Estribos", "anos": "Todos", "precio_base": 175.0, "obs": ""},
            {"producto": "Bisel Capot y Compuerta", "anos": "Todos", "precio_base": 90.0, "obs": ""},
            {"producto": "Cromado de Pluma", "anos": "Todos", "precio_base": 55.0, "obs": ""},
            {"producto": "Mascarillas", "anos": "Todos", "precio_base": 155.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "Todos", "precio_base": 110.0, "obs": ""}
        ],
        "ACCENT": [
            {"producto": "Kit Cromado", "anos": "2007-2023", "precio_base": 125.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2007-2023", "precio_base": 25.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2023", "precio_base": 55.0, "obs": ""},
            {"producto": "Contorno de Ventanas", "anos": "2012-2023", "precio_base": 110.0, "obs": ""},
            {"producto": "Bisel de Baúl", "anos": "2012-2023", "precio_base": 55.0, "obs": ""}
        ],
        "CRETA": [
            {"producto": "Kit Cromado +14 Piezas", "anos": "2014-2018", "precio_base": 155.0, "obs": ""}
        ],
        "TUCSON TL": [
            {"producto": "Kit Cromado +14 Piezas", "anos": "Hasta 2023", "precio_base": 155.0, "obs": ""},
            {"producto": "Mascarilla Cromada", "anos": "2023", "precio_base": 155.0, "obs": ""}
        ],
        "FURGONETA H1": [
            {"producto": "Cromado Faros y Guías", "anos": "2005-2011", "precio_base": 90.0, "obs": ""},
            {"producto": "Cobertor con Luz Retrovisores", "anos": "2005-2011", "precio_base": 85.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2011-2018", "precio_base": 155.0, "obs": ""}
        ],
        "GETZ": [
            {"producto": "Kit Cromado", "anos": "Todos", "precio_base": 125.0, "obs": ""}
        ],
        "SANTA FE": [
            {"producto": "Kit Cromado", "anos": "2006-2018", "precio_base": 125.0, "obs": ""},
            {"producto": "Estribos", "anos": "2007-2012", "precio_base": 165.0, "obs": ""},
            {"producto": "Cobertores Guardachoques", "anos": "2007-2012", "precio_base": 220.0, "obs": ""}
        ]
    },
    "NISSAN": {
        "TIIDA HATCHBACK": [
            {"producto": "Kit Cromado +14 Piezas con Luz", "anos": "2014", "precio_base": 165.0, "obs": ""}
        ],
        "QASHQAI": [
            {"producto": "Kit Cromado +14 Piezas", "anos": "2006-2010", "precio_base": 155.0, "obs": ""}
        ],
        "FRONTIER": [
            {"producto": "Kit Cromado sin Retrovisores", "anos": "2016-2021", "precio_base": 125.0, "obs": ""}
        ]
    },
    "MITSUBISHI": {
        "L200": [
            {"producto": "Kit Cromado 19 Piezas", "anos": "2006-2014", "precio_base": 250.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2015-2018", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2015-2018", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2015-2018", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2015-2018", "precio_base": 25.0, "obs": ""},
            {"producto": "Tapa de Balde", "anos": "2016-2024", "precio_base": 550.0, "obs": ""},
            {"producto": "Cromado Manija Compuerta", "anos": "2015-2018", "precio_base": 55.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2023", "precio_base": 130.0, "obs": ""}
        ]
    },
    "MAZDA": {
        "BT-50": [
            {"producto": "Kit Cromado", "anos": "2008-2023", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2008-2023", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2008-2015", "precio_base": 25.0, "obs": ""},
            {"producto": "Cromado Manija Compuerta", "anos": "2008-2015", "precio_base": 55.0, "obs": ""},
            {"producto": "Cromado de Neblineros", "anos": "2016-2023", "precio_base": 55.0, "obs": ""},
            {"producto": "Respiraderos Cromados", "anos": "2016-2023", "precio_base": 35.0, "obs": ""},
            {"producto": "Mascarilla", "anos": "2016-2023", "precio_base": 165.0, "obs": ""},
            {"producto": "Rudones", "anos": "2016-2023", "precio_base": 130.0, "obs": ""}
        ]
    },
    "FORD": {
        "RANGER": [
            {"producto": "Kit Cromado", "anos": "2012-2025", "precio_base": 125.0, "obs": ""},
            {"producto": "Bandejas", "anos": "2012-2025", "precio_base": 55.0, "obs": ""},
            {"producto": "Tapa de Combustible", "anos": "2012-2025", "precio_base": 25.0, "obs": ""},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2012-2025", "precio_base": 650.0, "obs": ""},
            {"producto": "Rudones", "anos": "2012-2026", "precio_base": 130.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2012-2025", "precio_base": 850.0, "obs": ""},
            {"producto": "Faros LED", "anos": "2017-2025", "precio_base": 750.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2017-2025", "precio_base": 240.0, "obs": ""},
            {"producto": "Bodykit Raptor Cárter Metálico", "anos": "2017-2025", "precio_base": 850.0, "obs": ""},
            {"producto": "Bodykit Raptor Guardachoques Metálico", "anos": "2017-2025", "precio_base": 1250.0, "obs": ""},
            {"producto": "Bodykit Raptor LED Guardachoques", "anos": "2017-2025", "precio_base": 750.0, "obs": ""},
            {"producto": "Bodykit T9", "anos": "2026", "precio_base": 1250.0, "obs": ""},
            {"producto": "Mascarilla Raptor Sin Luz", "anos": "2012-2015", "precio_base": 145.0, "obs": ""},
            {"producto": "Mascarilla Raptor Con Luz", "anos": "2012-2015", "precio_base": 260.0, "obs": ""},
            {"producto": "Mascarilla Raptor Gasolina", "anos": "2017-2025", "precio_base": 220.0, "obs": ""},
            {"producto": "Mascarilla Raptor Diesel", "anos": "2017-2025", "precio_base": 220.0, "obs": ""},
            {"producto": "Mascarilla Raptor T9", "anos": "2025", "precio_base": 220.0, "obs": ""},
            {"producto": "Estribos Raptor", "anos": "2017-2026", "precio_base": 340.0, "obs": ""}
        ],
        "ECOSPORT": [
            {"producto": "Kit Cromado", "anos": "2013-2015", "precio_base": 125.0, "obs": ""}
        ],
        "ESCAPE": [
            {"producto": "Kit Cromado", "anos": "2013-2015", "precio_base": 125.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "2007-2012", "precio_base": 220.0, "obs": ""}
        ],
        "F-150": [
            {"producto": "Cobertores Cromados Guías", "anos": "2009-2021", "precio_base": 115.0, "obs": ""},
            {"producto": "Cobertores Cromados Retrovisores", "anos": "2009-2021", "precio_base": 115.0, "obs": ""},
            {"producto": "Cubrelluvias Cromadas", "anos": "2009-2021", "precio_base": 180.0, "obs": ""},
            {"producto": "Cubrelluvias Color Negro", "anos": "2009-2014", "precio_base": 160.0, "obs": ""},
            {"producto": "Aplique Cromado Compuerta", "anos": "2009-2014", "precio_base": 350.0, "obs": ""},
            {"producto": "Cromado Manijas", "anos": "2009-2021", "precio_base": 85.0, "obs": ""},
            {"producto": "Bandejas Cromadas", "anos": "2009-2021", "precio_base": 75.0, "obs": ""},
            {"producto": "Mascarillas", "anos": "1978-2017", "precio_base": 220.0, "obs": "1998-2003 NO"},
            {"producto": "Mascarillas", "anos": "2018-2024", "precio_base": 320.0, "obs": ""},
            {"producto": "Guardachoque", "anos": "2009-2021", "precio_base": 650.0, "obs": ""},
            {"producto": "Faldones / Fenders Raptor", "anos": "2009-2021", "precio_base": 295.0, "obs": ""},
            {"producto": "Faldones / Fenders de Pernos", "anos": "2009-2021", "precio_base": 265.0, "obs": ""},
            {"producto": "Aplique Negro Compuerta", "anos": "2015-2025", "precio_base": 195.0, "obs": ""},
            {"producto": "Parachoque Negro", "anos": "2009-2021", "precio_base": 350.0, "obs": ""},
            {"producto": "Parachoque Cromado", "anos": "2009-2021", "precio_base": 350.0, "obs": ""},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2009-2025", "precio_base": 650.0, "obs": ""},
            {"producto": "Tapa de Balde Corrediza", "anos": "2009-2025", "precio_base": 850.0, "obs": ""},
            {"producto": "Faros LED", "anos": "2009-2015", "precio_base": 650.0, "obs": ""},
            {"producto": "Guías LED", "anos": "2009-2014", "precio_base": 390.0, "obs": ""}
        ],
        "EXPLORER": [
            {"producto": "Kit Cromado", "anos": "2007-2011", "precio_base": 125.0, "obs": ""},
            {"producto": "Kit Cromado", "anos": "2012-2015", "precio_base": 195.0, "obs": ""},
            {"producto": "Tapa Combustible Cromada", "anos": "2012-2015", "precio_base": 25.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "1995-2017", "precio_base": 220.0, "obs": "2002-2006 DIC"},
            {"producto": "Letras de Capot", "anos": "1995-2026", "precio_base": 40.0, "obs": ""}
        ],
        "EXPLORER SPORTRACK": [
            {"producto": "Kit Cromado", "anos": "2007-2011", "precio_base": 125.0, "obs": ""},
            {"producto": "Mascarilla Raptor", "anos": "2007-2011", "precio_base": 220.0, "obs": ""}
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
