import streamlit as st
import urllib.parse
import os
from PIL import Image, ImageDraw, ImageFont
import io

# ==========================================
# 1. BASE DE DATOS EXTRAÍDA DEL PDF OFICIAL
# ==========================================
PRECIOS_CATALOGO = {
    "CHEVROLET": {
        "D-MAX": [
            {"producto": "Kit Cromado", "anos": "2003-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Apliques Negros de Faros y Guías", "anos": "2009-2013", "precio": 90.0, "obs": "", "imagenes": []},
            {"producto": "Cubrelluvias", "anos": "2003-2025", "precio": 95.0, "obs": "", "imagenes": []},
            {"producto": "Lamevidrios", "anos": "2014-2025", "precio": 85.0, "obs": "Diciembre", "imagenes": []},
            {"producto": "Bandejas", "anos": "2014-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Neblineros", "anos": "2014-2018", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Compuerta", "anos": "2003-2025", "precio": 75.0, "obs": "", "imagenes": []},
            {"producto": "Cobertor Cromado Retrovisor con Luz", "anos": "2003-2025", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Respiradero de Capot Cromado", "anos": "2014-2025", "precio": 60.0, "obs": "Diciembre", "imagenes": []},
            {"producto": "Apliques Decorativos de Tablero", "anos": "2003-2007", "precio": 95.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas sin Luz", "anos": "2009-2025", "precio": 135.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas con Luz", "anos": "2019-2025", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla D-Max con LED", "anos": "2014-2018", "precio": 175.0, "obs": "Incluye Kit de Luces LED", "imagenes": [
                "fotos/chevrolet_dmax_Mascarilla20142018CLuces.jpeg",
                "fotos/chevrolet_dmax_Mascarilla20142018ExCLuces.jpeg",
                "fotos/chevrolet_dmax_Mascarilla20142018QuCLuces.jpeg"
            ]},
            {"producto": "Estribos", "anos": "2014-2025", "precio": 175.0, "obs": "Diciembre", "imagenes": []},
            {"producto": "Rudones", "anos": "2014-2025", "precio": 130.0, "obs": "", "imagenes": []}
        ],
        "AVEO (EMOTION / FAMILY / ACTIVO)": [
            {"producto": "Kit Cromado", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 25.0, "obs": "", "imagenes": []}
        ],
        "OPTRA": [
            {"producto": "Kit Cromado más de 14 piezas con Luz", "anos": "2005-2007", "precio": 165.0, "obs": "", "imagenes": []}
        ],
        "SUZUKI SZ / VITARA SZ": [
            {"producto": "Kit Cromado", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Respiraderos de Capot", "anos": "Varios", "precio": 35.0, "obs": "", "imagenes": []},
            {"producto": "Tapa Combustible", "anos": "Varios", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Cromada", "anos": "Varios", "precio": 115.0, "obs": "", "imagenes": []}
        ],
        "SPARK / SPARK GT": [
            {"producto": "Cubrelluvias Spark", "anos": "2008-2014", "precio": 95.0, "obs": "", "imagenes": []},
            {"producto": "Kit Cromado Spark GT", "anos": "2008-2014", "precio": 125.0, "obs": "", "imagenes": []}
        ],
        "GRAND VITARA": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio": 125.0, "obs": "", "imagenes": []}
        ],
        "SAIL": [
            {"producto": "Kit Cromado", "anos": "2008-2016", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Neblinero", "anos": "2008-2016", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cromado Tapa de Combustible", "anos": "2008-2016", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Bisel de Baúl", "anos": "2017-2023", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Kit Cromado Nuevo", "anos": "2017-2023", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Contorno de Ventanas", "anos": "2017-2023", "precio": 110.0, "obs": "", "imagenes": []}
        ],
        "CAPTIVA": [
            {"producto": "Kit Cromado", "anos": "2006-2010", "precio": 125.0, "obs": "", "imagenes": []}
        ]
    },
    "TOYOTA": {
        "HILUX": [
            {"producto": "Kit Cromados", "anos": "2003-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Cromado Retrovisor con Luz", "anos": "2003-2015", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2003-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2003-2025", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Lamevidrios", "anos": "2003-2025", "precio": 75.0, "obs": "Diciembre", "imagenes": []},
            {"producto": "Cobertor Cromado Neblineros", "anos": "2003-2015", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cobertor Cromado de Compuerta", "anos": "2012-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Luz de Compuerta", "anos": "2003-2011", "precio": 45.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas con Luz", "anos": "2003-2025", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas sin Luz", "anos": "2003-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde Corrediza", "anos": "2017-2025", "precio": 850.0, "obs": "", "imagenes": []},
            {"producto": "Portavasos", "anos": "2003-2015", "precio": 110.0, "obs": "Diciembre", "imagenes": []},
            {"producto": "Rudones", "anos": "2003-2025", "precio": 130.0, "obs": "", "imagenes": []},
            {"producto": "Guías LED", "anos": "2017-2025", "precio": 240.0, "obs": "", "imagenes": []}
        ],
        "FORTUNER": [
            {"producto": "Kit Cromados", "anos": "2008-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2008-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2008-2025", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Bisel de Compuerta con Luz", "anos": "2012-2025", "precio": 145.0, "obs": "", "imagenes": []},
            {"producto": "Letras de Capot Cromadas / Negras", "anos": "2008-2025", "precio": 45.0, "obs": "", "imagenes": []},
            {"producto": "LED de Parachoques", "anos": "2017-2025", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Rudones", "anos": "2016-2025", "precio": 130.0, "obs": "", "imagenes": []},
            {"producto": "Apliques de Neblinero Grande / Pequeño", "anos": "2016-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas sin Luz", "anos": "2008-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas con Luz", "anos": "2008-2025", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Contorno de Ventanas", "anos": "2016-2025", "precio": 135.0, "obs": "", "imagenes": []}
        ],
        "COROLLA": [
            {"producto": "Kit Cromado +14 piezas con Luz", "anos": "2007-2010", "precio": 165.0, "obs": "", "imagenes": []}
        ],
        "RAV4": [
            {"producto": "Kit Cromado +14 piezas", "anos": "2005-2012", "precio": 155.0, "obs": "", "imagenes": []}
        ]
    },
    "KIA": {
        "SPORTAGE ACTIVE": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 20.0, "obs": "", "imagenes": []},
            {"producto": "Cobertores de Guardachoques", "anos": "Varios", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Cobertor Cromado Neblineros", "anos": "Varios", "precio": 115.0, "obs": "", "imagenes": []},
            {"producto": "Kit de Plumas", "anos": "Varios", "precio": 75.0, "obs": "", "imagenes": []},
            {"producto": "Neblineros", "anos": "Varios", "precio": 155.0, "obs": "", "imagenes": []},
            {"producto": "Bisel de Capot", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Parantes de Compuerta", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Estribos", "anos": "Varios", "precio": 165.0, "obs": "", "imagenes": []}
        ],
        "SPORTAGE R": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 20.0, "obs": "", "imagenes": []},
            {"producto": "Cobertores de Guardachoques", "anos": "Varios", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Contorno de Ventanas", "anos": "Varios", "precio": 110.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Plumas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Estribos", "anos": "Varios", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Cubrelluvias", "anos": "Varios", "precio": 95.0, "obs": "", "imagenes": []}
        ],
        "CERATO FORTE": [
            {"producto": "Kit Cromado", "anos": "2012-2016", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2012-2016", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2012-2016", "precio": 25.0, "obs": "", "imagenes": []}
        ],
        "RIO EXCITE": [
            {"producto": "Kit Cromado", "anos": "2007-2014", "precio": 125.0, "obs": "", "imagenes": []}
        ],
        "SORENTO": [
            {"producto": "Kit Cromado", "anos": "2009-2014", "precio": 125.0, "obs": "", "imagenes": []}
        ]
    },
    "HYUNDAI": {
        "TUCSON CLASICO": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cobertor Retrovisor con Guía", "anos": "Varios", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Cromada", "anos": "Varios", "precio": 110.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Cobertores de Guardachoques", "anos": "Varios", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Kit de Plumas y Rejilla", "anos": "Varios", "precio": 115.0, "obs": "", "imagenes": []},
            {"producto": "Estribos", "anos": "Varios", "precio": 165.0, "obs": "", "imagenes": []}
        ],
        "TUCSON ix35": [
            {"producto": "Kit Cromados", "anos": "Varios", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Cubrelluvias", "anos": "Varios", "precio": 95.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "Varios", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "Varios", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Cobertores de Guardachoques", "anos": "Varios", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Estribos", "anos": "Varios", "precio": 175.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas", "anos": "Varios", "precio": 155.0, "obs": "", "imagenes": []},
            {"producto": "Contorno de Ventanas", "anos": "Varios", "precio": 110.0, "obs": "", "imagenes": []}
        ],
        "ACCENT": [
            {"producto": "Kit Cromado", "anos": "2007-2023", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2007-2023", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2012-2023", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Contorno de Ventanas", "anos": "2012-2023", "precio": 110.0, "obs": "", "imagenes": []},
            {"producto": "Bisel de Baúl", "anos": "2012-2023", "precio": 55.0, "obs": "", "imagenes": []}
        ],
        "CRETA": [
            {"producto": "Kit Cromado +14 piezas", "anos": "2014-2018", "precio": 155.0, "obs": "", "imagenes": []}
        ],
        "TUCSON TL": [
            {"producto": "Kit Cromado +14 piezas", "anos": "hasta 2023", "precio": 155.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Cromada", "anos": "2023", "precio": 155.0, "obs": "", "imagenes": []}
        ],
        "FURGONETA H1": [
            {"producto": "Cromado de Faros y Guías", "anos": "2005-2011", "precio": 90.0, "obs": "", "imagenes": []},
            {"producto": "Cobertor Cromado con Luz Retrovisores", "anos": "2005-2011", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Kit Cromado", "anos": "2011-2018", "precio": 155.0, "obs": "", "imagenes": []}
        ],
        "SANTA FE": [
            {"producto": "Kit Cromado", "anos": "2006-2018", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Estribos", "anos": "2007-2012", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Cobertores de Guardachoque", "anos": "2007-2012", "precio": 220.0, "obs": "", "imagenes": []}
        ]
    },
    "NISSAN": {
        "TIIDA HATCHBACK": [
            {"producto": "Kit Cromado +14 piezas con Luz", "anos": "2014", "precio": 165.0, "obs": "", "imagenes": []}
        ],
        "QASHQAI": [
            {"producto": "Kit Cromado +14 piezas", "anos": "2006-2010", "precio": 155.0, "obs": "", "imagenes": []}
        ],
        "FRONTIER": [
            {"producto": "Kit Cromado sin Retrovisores", "anos": "2016-2021", "precio": 125.0, "obs": "", "imagenes": []}
        ]
    },
    "MITSUBISHI": {
        "L200": [
            {"producto": "Kit Cromado 19 Piezas", "anos": "2006-2014", "precio": 250.0, "obs": "", "imagenes": []},
            {"producto": "Kit Cromado", "anos": "2015-2018", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2015-2018", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Neblineros", "anos": "2015-2018", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2015-2018", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde", "anos": "2016-2024", "precio": 550.0, "obs": "", "imagenes": []},
            {"producto": "Cromado Manija de Compuerta", "anos": "2015-2018", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Rudones", "anos": "2016-2023", "precio": 130.0, "obs": "", "imagenes": []}
        ]
    },
    "MAZDA": {
        "BT-50": [
            {"producto": "Kit Cromado", "anos": "2008-2023", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2008-2023", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2008-2015", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Cromado Manija de Compuerta", "anos": "2008-2015", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Neblineros", "anos": "2016-2023", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Respiraderos Cromados", "anos": "2016-2023", "precio": 35.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla", "anos": "2016-2023", "precio": 165.0, "obs": "", "imagenes": []},
            {"producto": "Rudones", "anos": "2016-2023", "precio": 130.0, "obs": "", "imagenes": []}
        ]
    },
    "FORD": {
        "RANGER": [
            {"producto": "Kit Cromado", "anos": "2012-2025", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas", "anos": "2012-2025", "precio": 55.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible", "anos": "2012-2025", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2012-2025", "precio": 650.0, "obs": "", "imagenes": []},
            {"producto": "Rudones", "anos": "2012-2026", "precio": 130.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde Corrediza", "anos": "2012-2025", "precio": 850.0, "obs": "", "imagenes": []},
            {"producto": "Faros LED", "anos": "2017-2025", "precio": 750.0, "obs": "", "imagenes": []},
            {"producto": "Guías LED", "anos": "2017-2025", "precio": 240.0, "obs": "", "imagenes": []},
            {"producto": "Bodykit Raptor Cárter Metálico", "anos": "2017-2025", "precio": 850.0, "obs": "", "imagenes": []},
            {"producto": "Bodykit Raptor Guardachoque Metálico", "anos": "2017-2025", "precio": 1250.0, "obs": "", "imagenes": []},
            {"producto": "Bodykit Raptor con LED", "anos": "2017-2025", "precio": 750.0, "obs": "", "imagenes": []},
            {"producto": "Bodykit T9", "anos": "2026", "precio": 1250.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor sin Luz", "anos": "2012-2015", "precio": 145.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor con Luz", "anos": "2012-2015", "precio": 260.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor Gasolina / Diesel", "anos": "2017-2025", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor T9", "anos": "2025", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Estribos Raptor", "anos": "2017-2026", "precio": 340.0, "obs": "", "imagenes": []}
        ],
        "F-150": [
            {"producto": "Cobertores Cromados de Guías / Retrovisores", "anos": "2009-2021", "precio": 115.0, "obs": "", "imagenes": []},
            {"producto": "Cubrelluvias Cromadas", "anos": "2009-2021", "precio": 180.0, "obs": "", "imagenes": []},
            {"producto": "Cubrelluvias Color Negro", "anos": "2009-2014", "precio": 160.0, "obs": "", "imagenes": []},
            {"producto": "Aplique Cromado de Compuerta", "anos": "2009-2014", "precio": 350.0, "obs": "", "imagenes": []},
            {"producto": "Cromado de Manijas", "anos": "2009-2021", "precio": 85.0, "obs": "", "imagenes": []},
            {"producto": "Bandejas Cromadas", "anos": "2009-2021", "precio": 75.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas (1978-2017)", "anos": "1978-2017", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Mascarillas (2018-2024)", "anos": "2018-2024", "precio": 320.0, "obs": "", "imagenes": []},
            {"producto": "Guardachoque", "anos": "2009-2021", "precio": 650.0, "obs": "", "imagenes": []},
            {"producto": "Faldones / Fenders Raptor", "anos": "2009-2021", "precio": 295.0, "obs": "", "imagenes": []},
            {"producto": "Faldones / Fenders de Pernos", "anos": "2009-2021", "precio": 265.0, "obs": "", "imagenes": []},
            {"producto": "Aplique Negro de Compuerta", "anos": "2015-2025", "precio": 195.0, "obs": "", "imagenes": []},
            {"producto": "Parachoque Negro / Cromado", "anos": "2009-2021", "precio": 350.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde Estilo Americano", "anos": "2009-2025", "precio": 650.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Balde Corrediza", "anos": "2009-2025", "precio": 850.0, "obs": "", "imagenes": []},
            {"producto": "Faros LED", "anos": "2009-2015", "precio": 650.0, "obs": "", "imagenes": []},
            {"producto": "Guías LED", "anos": "2009-2014", "precio": 390.0, "obs": "", "imagenes": []}
        ],
        "EXPLORER": [
            {"producto": "Kit Cromado (2007-2011)", "anos": "2007-2011", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Kit Cromado (2012-2015)", "anos": "2012-2015", "precio": 195.0, "obs": "", "imagenes": []},
            {"producto": "Tapa de Combustible Cromada", "anos": "2012-2015", "precio": 25.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor", "anos": "1995-2017", "precio": 220.0, "obs": "", "imagenes": []},
            {"producto": "Letras de Capot", "anos": "1995-2026", "precio": 40.0, "obs": "", "imagenes": []}
        ],
        "EXPLORER SPORT TRAC": [
            {"producto": "Kit Cromado", "anos": "2007-2011", "precio": 125.0, "obs": "", "imagenes": []},
            {"producto": "Mascarilla Raptor", "anos": "2007-2011", "precio": 220.0, "obs": "", "imagenes": []}
        ]
    }
}

# ==========================================
# 2. GENERADOR DE AFICHE NÍTIDO (1080x1080)
# ==========================================
def generar_banner_cuadrado(marca, modelo, producto, precio, anos, lista_rutas):
    ANCHO, ALTO = 1080, 1080
    lienzo = Image.new("RGB", (ANCHO, ALTO), color=(15, 15, 15))
    draw = ImageDraw.Draw(lienzo)

    # Cabecera Elegante W.G.H (Ampliada un poco de alto para albergar fuentes grandes)
    ALTO_CABECERA = 260
    draw.rectangle([(0, 0), (ANCHO, ALTO_CABECERA)], fill=(22, 22, 22))
    draw.rectangle([(0, ALTO_CABECERA - 6), (ANCHO, ALTO_CABECERA)], fill=(217, 4, 41))

    # Fuentes mucho más grandes para garantizar legibilidad en móviles
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
    draw.text((40, 160), f"REPUESTO: {producto.upper()} ({anos})", fill=(200, 200, 200), font=font_repuesto)
    
    # Caja de Precio Rediseñada (Derecha)
    ANCHO_CAJA = 420
    ALTO_CAJA = 180
    x_box_i = ANCHO - ANCHO_CAJA - 40
    y_box_i = 35
    x_box_f = ANCHO - 40
    y_box_f = y_box_i + ALTO_CAJA

    # Dibujar caja de precio con borde grueso
    draw.rectangle([(x_box_i, y_box_i), (x_box_f, y_box_f)], fill=(10, 10, 10), outline=(217, 4, 41), width=4)
    draw.text((x_box_i + 30, y_box_i + 20), "PRECIO OFERTA", fill=(200, 200, 200), font=font_precio_label)
    draw.text((x_box_i + 30, y_box_i + 75), f"${precio:.2f}", fill=(255, 255, 255), font=font_precio)

    # Distribución de Fotografías (Ajustado al nuevo alto de cabecera)
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
            x = 20 + i * (w_box + 20)
            lienzo.paste(img, (x, y_inicio))

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
# ==========================================
# 3. INTERFAZ INTERACTIVA STREAMLIT
# ==========================================
st.set_page_config(page_title="Ofertas - W.G.H CarShop", layout="wide")
st.title("📦 Cotizador y Ofertas W.G.H CarShop")

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
    if info['obs']:
        st.info(f"💡 **Nota:** {info['obs']}")
    
    precio_final = st.number_input(
        "💵 Precio Final ($ USD):", 
        min_value=0.0, 
        value=float(info['precio']), 
        step=5.0
    )

    st.markdown("### 🖼️ Galería de Fotos")
    lista_imagenes = info.get("imagenes", [])
    if lista_imagenes:
        tabs = st.tabs([f"Foto {i+1}" for i in range(len(lista_imagenes))])
        for idx, tab in enumerate(tabs):
            with tab:
                ruta_img = lista_imagenes[idx]
                if os.path.exists(ruta_img):
                    st.image(ruta_img, use_column_width=True)
    else:
        st.caption("*(Puedes agregar fotos locales en el repositorio para este repuesto)*")

with col_der:
    st.subheader("🖼️ Afiche Publicitario Generado (1080x1080)")
    
    buffer_banner = generar_banner_cuadrado(
        marca_sel, modelo_sel, info['producto'], precio_final, info['anos'], lista_imagenes
    )

    # 1. Muestra del afiche
    st.image(buffer_banner, caption="Vista previa de afiche para WhatsApp", use_column_width=True)

    # 2. Descarga del afiche
    st.download_button(
        label="📥 Descargar Afiche de Oferta (JPEG)",
        data=buffer_banner,
        file_name=f"Oferta_{marca_sel}_{modelo_sel}.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

    st.markdown("---")
    
    # 3. Bloque de Cierre de Venta (Justo abajo del afiche)
    st.subheader("🤝 Cierre de Venta (Pago Contra Entrega)")
    st.info("🚛 **Servientrega:** Envíos seguros con pago al recibir el producto.")
    
    mensaje_cierre = f"""¡Saludos! Le comparto los detalles para concretar su pedido de *{marca_sel} {modelo_sel}* ({info['producto']}):

Nuestro sistema de trabajo es **pago contra entrega** con la seguridad de **Servientrega**. Una vez que el paquete llegue a su domicilio o agencia, usted realiza el pago directo al recibirlo.

Para emitir la guía de remisión, por favor ayúdenos con los siguientes datos:
1. Nombre y Apellido:
2. Número de Cédula:
3. Dirección exacta o Agencia Servientrega preferida:
4. Teléfono de contacto:

¡Apenas nos confirme los datos, preparamos e despachamos su paquete! 🚘"""

    st.text_area("Texto de cierre (listo para copiar):", value=mensaje_cierre, height=210)

    # 4. Input y Botón de envío directo por WhatsApp
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")
    
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
    st.markdown("---")
    
    telefono = st.text_input("Número del cliente (opcional, ej: 593991234567)", value="")
    mensaje_texto = f"📌 *W.G.H CAR SHOP* | Le comparto la ficha de oferta para *{marca_sel} {modelo_sel}* (${precio_final:.2f} USD). ¡Revisa el afiche adjunto!"
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
                📲 Abrir WhatsApp y Enviar Oferta Inicial
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # Mensaje de Cierre para Contra Entrega (Servientrega)
    st.markdown("### 💬 Cierre de Venta (Envío Contra Entrega)")
    mensaje_cierre = f"""¡Saludos! Le comparto: nuestro sistema de trabajo es **pago contra entrega** con la seguridad de Servientrega. 

Una vez que el paquete llegue a su domicilio o agencia, usted realiza el pago al recibirlo. 

Para proceder con la guía de remisión, envíenos los siguientes datos:
1. Nombre y Apellido
2. Número de Cédula
3. Dirección precisa o Agencia de Servientrega preferida
4. Teléfono

¡Apenas nos confirme los datos, preparamos su paquete! 🚘"""

    st.text_area("Texto listo para copiar y enviar al cliente:", value=mensaje_cierre, height=200)
