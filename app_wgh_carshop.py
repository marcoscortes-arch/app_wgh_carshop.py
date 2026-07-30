import io
import threading
import urllib.parse
from PIL import Image
import pandas as pd
import requests
import streamlit as st


# ---------------------------------------------------------
# FUNCIONES DE OPTIMIZACIÓN Y ENVÍO DE IMÁGENES
# ---------------------------------------------------------
def convertir_link_drive(url):
    """Convierte cualquier URL de Google Drive (compartida o directa)

    en un enlace de imagen utilizable por Streamlit y WhatsApp.
    """
    url = str(url).strip()

    if not url or url == "nan":
        return ""

    if "drive.google.com" not in url:
        return url

    file_id = ""
    if "/file/d/" in url:
        file_id = url.split("/file/d/")[1].split("/")[0].split("?")[0]
    elif "id=" in url:
        file_id = url.split("id=")[1].split("&")[0]

    if file_id:
        return f"https://lh3.googleusercontent.com/d/{file_id}"

    return url


def descargar_y_comprimir_imagen(url_imagen, max_px=1080, calidad=75):
    """Descarga la imagen desde la red/Drive y la comprime en memoria."""
    try:
        response = requests.get(url_imagen, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Redimensionar proporcionalmente
            img.thumbnail((max_px, max_px))

            # Guardar en buffer comprimido
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=calidad, optimize=True)
            buffer.seek(0)
            return buffer
    except Exception as e:
        print(f"Error procesando la imagen {url_imagen}: {e}")
    return None


def enviar_foto_whatsapp_segundo_plano(
    url_imagen, telefono_cliente, mensaje_texto, api_url, token
):
    """Descarga, comprime y envía la foto a la API de WhatsApp en segundo plano."""
    buffer_img = descargar_y_comprimir_imagen(url_imagen)

    if not buffer_img:
        print("No se pudo obtener o comprimir la imagen.")
        return

    try:
        # Preparar payload / archivos según la API de WhatsApp que utilices
        files = {"file": ("producto.jpg", buffer_img, "image/jpeg")}
        data = {"phone": telefono_cliente, "caption": mensaje_texto}
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        # Petición HTTP en segundo plano
        response = requests.post(
            api_url, data=data, files=files, headers=headers, timeout=30
        )
        if response.status_code in [200, 201]:
            print(f"✅ Foto enviada con éxito a {telefono_cliente}")
        else:
            print(f"⚠️ Error API WhatsApp: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error enviando WhatsApp en segundo plano: {e}")


# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="W.G.H. Car Shop - Buscador de Accesorios",
    layout="wide",
    page_icon="🚗",
)

st.markdown(
    """
<style>
    .reportview-container .main .block-container{
        padding-top: 1rem;
    }
    .wgh-header {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #e62117; /* Rojo WGH */
        font-size: 36px;
        text-align: center;
        margin-bottom: 0px;
    }
    .wgh-sub {
        font-family: Arial, Helvetica, sans-serif;
        color: #333;
        font-size: 18px;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="wgh-header">W.G.H. Car Shop</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="wgh-sub">Buscador Rápido de Mascarillas y Accesorios</div>',
    unsafe_allow_html=True,
)

# Configuración de API WhatsApp en Sidebar
st.sidebar.title("⚙️ API WhatsApp")
api_whatsapp_url = st.sidebar.text_input(
    "URL Endpoint API WhatsApp:",
    value="https://api.tu-proveedor.com/send-image",
)
api_token = st.sidebar.text_input(
    "Token / API Key:", value="", type="password"
)

# Enlace a Google Sheet (CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDj39gzuKoA_6SgtWcVs5It-0WSzxGwb5it-9Ja012Al9pw3jpP6Ioxf8VrL66MQ/pub?output=csv"


@st.cache_data(ttl=300)
def cargar_inventario():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()

        if "Año Inicial" in df.columns:
            df["Año Inicial"] = (
                pd.to_numeric(df["Año Inicial"], errors="coerce")
                .fillna(1900)
                .astype(int)
            )
        if "Año Final" in df.columns:
            df["Año Final"] = (
                pd.to_numeric(df["Año Final"], errors="coerce")
                .fillna(2100)
                .astype(int)
            )

        return df
    except Exception as e:
        st.error(f"Error al conectar con la base de datos de Google Sheets: {e}")
        return pd.DataFrame()


df = cargar_inventario()

# Pestañas principales
tab_campana, tab_inventario = st.tabs([
    "⚡ Modo Campaña Rápida (4 Campañas)",
    "🔍 Buscador de Inventario General",
])

# ---------------------------------------------------------
# PESTAÑA 1: MODO CAMPAÑA RÁPIDA
# ---------------------------------------------------------
with tab_campana:
    st.markdown("### ⚡ Generador Instantáneo para Campañas")

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        campana_sel = st.selectbox(
            "1. Selecciona la Campaña:",
            [
                "Mascarilla D-Max (Todos los años)",
                "Mascarillas Ford (Varios modelos)",
                "Protectores de Puerta (Multimarca)",
                "Otras Mascarillas / Accesorios",
            ],
        )

        if "D-Max" in campana_sel:
            opciones_sub = [
                "D-Max 2014 - 2018",
                "D-Max 2019 - 2021",
                "D-Max 2022 - 2024",
                "D-Max Luv / Clásica",
            ]
            precio_def = 175.0
        elif "Ford" in campana_sel:
            opciones_sub = [
                "Ford Ranger 2013 - 2016",
                "Ford Ranger 2017 - 2021",
                "Ford Ranger 2022+",
                "Ford F-150 / Raptor",
            ]
            precio_def = 185.0
        elif "Protectores" in campana_sel:
            opciones_sub = [
                "Toyota Hilux",
                "Chevrolet D-Max",
                "Ford Ranger",
                "Nissan Frontier / NP300",
                "Great Wall Poer / Wingle",
            ]
            precio_def = 120.0
        else:
            opciones_sub = ["Universal / Adaptable", "Modelo Específico"]
            precio_def = 150.0

        sub_sel = st.selectbox(
            "2. Selecciona Modelo / Año / Versión:", opciones_sub
        )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            precio_prod = st.number_input(
                "Precio Oferta ($):", value=precio_def, step=5.0
            )
        with col_p2:
            costo_envio = st.number_input(
                "Costo de Envío ($):", value=10.0, step=1.0
            )

        telefono_cli = st.text_input(
            "Número de WhatsApp Cliente (Ej. 593991234567):", ""
        )
        ciudad_cli = st.text_input(
            "Ciudad del Cliente (Opcional):",
            placeholder="Ej. Cuenca, Quito, Guayaquil",
        )

        urls_encontradas = []
        if not df.empty:
            cols_img = [
                c
                for c in df.columns
                if "imagen" in c.lower()
                or "foto" in c.lower()
                or "url" in c.lower()
            ]
            palabras_clave = [
                p.strip()
                for p in sub_sel.replace("-", " ")
                .replace("/", " ")
                .split()
                if len(p.strip()) > 2
            ]

            df_coincidencias = df.copy()
            for kw in palabras_clave:
                mask = (
                    df_coincidencias.astype(str)
                    .apply(
                        lambda row: row.str.contains(kw, case=False, na=False)
                    )
                    .any(axis=1)
                )
                if mask.any():
                    df_coincidencias = df_coincidencias[mask]

            if not df_coincidencias.empty:
                fila = df_coincidencias.iloc[0]
                for col in cols_img:
                    val = str(fila.get(col, "")).strip()
                    if val and val.lower() != "nan" and "http" in val:
                        urls_encontradas.append(val)

        urls_def_text = "\n".join(urls_encontradas) if urls_encontradas else ""

        urls_input = st.text_area(
            "URLs de Imágenes del Producto (1 por línea):",
            value=urls_def_text,
            height=100,
            placeholder="https://drive.google.com/file/d/...",
        )

        incluir_saludo = st.checkbox("Incluir saludo ('Buen día')", value=True)

    with col_c2:
        st.markdown("### 📲 Mensaje Formateado Listo")

        saludo_txt = "Buen día\n\n" if incluir_saludo else ""
        ciudad_txt = (
            f" para {ciudad_cli.strip().title()}" if ciudad_cli.strip() else ""
        )

        lista_urls_raw = [
            u.strip() for u in urls_input.split("\n") if u.strip() != ""
        ]
        lista_urls_directas = []

        for u in lista_urls_raw:
            u_dir = convertir_link_drive(u)
            if u_dir:
                lista_urls_directas.append(u_dir)

        img_txt = ""
        if len(lista_urls_directas) == 1:
            img_txt = f"\n\n📷 Ver foto del producto:\n{lista_urls_directas[0]}"
        elif len(lista_urls_directas) > 1:
            img_txt = "\n\n📷 Ver fotos del producto:\n" + "\n".join(
                [f"• {u}" for u in lista_urls_directas]
            )

        msg_campana = (
            f"{saludo_txt}"
            f"Disponemos la mascarilla para *{sub_sel}*{ciudad_txt}.\n\n"
            f"En oferta *${precio_prod:.2f}* más *${costo_envio:.2f}* de envío.\n\n"
            f"¿UD nos paga al recibir su pedido por Servientrega?{img_txt}"
        )

        st.text_area("Vista previa del mensaje:", msg_campana, height=200)

        if lista_urls_directas:
            st.markdown("**Vista previa de fotos adjuntas:**")
            for idx, link_f in enumerate(lista_urls_directas, 1):
                st.image(link_f, caption=f"Foto {idx}", use_container_width=True)

        # BOTÓN 1: Envío directo con Foto Comprimida en Segundo Plano (API)
        if st.button("🚀 Enviar Foto Comprimida en Segundo Plano"):
            if not telefono_cli.strip():
                st.warning("⚠️ Ingresa el número del cliente para enviar.")
            elif not lista_urls_directas:
                st.warning("⚠️ No hay imagen seleccionada.")
            else:
                img_a_enviar = lista_urls_directas[0]
                hilo = threading.Thread(
                    target=enviar_foto_whatsapp_segundo_plano,
                    args=(
                        img_a_enviar,
                        telefono_cli.strip(),
                        msg_campana,
                        api_whatsapp_url,
                        api_token,
                    ),
                )
                hilo.start()
                st.success(
                    "⚡ ¡Iniciando envío de foto comprimida en segundo plano!"
                )

        st.divider()

        # BOTÓN 2: Enlace estándar de WhatsApp Web
        text_encoded = urllib.parse.quote(msg_campana)
        link_wa_campana = f"https://api.whatsapp.com/send?text={text_encoded}"

        st.markdown(
            f"""
            <a href="{link_wa_campana}" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #25D366;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    width: 100%;
                    cursor: pointer;
                ">
                    📲 Abrir enlace en WhatsApp Web
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# PESTAÑA 2: BUSCADOR GENERAL DE INVENTARIO
# ---------------------------------------------------------
with tab_inventario:
    if not df.empty:
        st.markdown("### 🔍 Búsqueda Directa")
        busqueda_directa = st.text_input(
            "Busca por SKU, nombre de mascarilla o palabra clave:", ""
        )

        if busqueda_directa.strip():
            mask = (
                df.astype(str)
                .apply(
                    lambda row: row.str.contains(
                        busqueda_directa, case=False, na=False
                    )
                )
                .any(axis=1)
            )
            df_filtrado = df[mask]
        else:
            st.markdown("### 🚘 Filtrar por Vehículo")
            col1, col2, col3 = st.columns(3)

            with col1:
                marcas = (
                    sorted([
                        m
                        for m in df["Marca"].dropna().unique()
                        if str(m).strip()
                    ])
                    if "Marca" in df.columns
                    else []
                )
                marca_sel = st.selectbox("1. Marca", ["Todas"] + marcas)

            df_f1 = (
                df
                if marca_sel == "Todas" or "Marca" not in df.columns
                else df[df["Marca"] == marca_sel]
            )

            with col2:
                modelos = (
                    sorted([
                        m
                        for m in df_f1["Modelo"].dropna().unique()
                        if str(m).strip()
                    ])
                    if "Modelo" in df_f1.columns
                    else []
                )
                modelo_sel = st.selectbox("2. Modelo", ["Todos"] + modelos)

            df_f2 = (
                df_f1
                if modelo_sel == "Todos" or "Modelo" not in df_f1.columns
                else df_f1[df_f1["Modelo"] == modelo_sel]
            )

            with col3:
                anio_sel = st.number_input(
                    "3. Año del Vehículo",
                    min_value=1980,
                    max_value=2030,
                    value=2016,
                )

            if "Año Inicial" in df_f2.columns and "Año Final" in df_f2.columns:
                df_filtrado = df_f2[
                    (df_f2["Año Inicial"] <= anio_sel)
                    & (df_f2["Año Final"] >= anio_sel)
                ]
            else:
                df_filtrado = df_f2

        st.divider()
        st.subheader(f"📦 Mascarillas Encontradas ({len(df_filtrado)})")

        if df_filtrado.empty:
            st.info("No se encontraron mascarillas compatibles.")
        else:
            for idx, row in df_filtrado.iterrows():
                with st.container():
                    producto_nombre = row.get(
                        "Producto / Descripción",
                        row.get("Producto", "Mascarilla"),
                    )
                    anio_in = row.get("Año Inicial", "")
                    anio_fin = row.get("Año Final", "")
                    st.markdown(
                        f"#### {producto_nombre} ({anio_in}-{anio_fin})"
                    )

                    col_img1, col_img2, col_img3 = st.columns(3)

                    url_img1 = convertir_link_drive(
                        row.get("URL Imagen 1 (Principal)", "")
                    )
                    url_img2 = convertir_link_drive(
                        row.get("URL Imagen 2 (Exhibición)", "")
                    )
                    url_img3 = convertir_link_drive(
                        row.get("URL Imagen 3 (Instalada)", "")
                    )

                    with col_img1:
                        if url_img1 and url_img1.startswith("http"):
                            st.image(
                                url_img1,
                                caption="Principal",
                                use_container_width=True,
                            )
                        else:
                            st.caption("📷 Sin Imagen 1")

                    with col_img2:
                        if url_img2 and url_img2.startswith("http"):
                            st.image(
                                url_img2,
                                caption="Exhibición",
                                use_container_width=True,
                            )
                        else:
                            st.caption("📷 Sin Imagen 2")

                    with col_img3:
                        if url_img3 and url_img3.startswith("http"):
                            st.image(
                                url_img3,
                                caption="Instalada",
                                use_container_width=True,
                            )
                        else:
                            st.caption("📷 Sin Imagen 3")

                    col_info_detalles, col_action_wa = st.columns([3, 1])

                    with col_info_detalles:
                        st.write(
                            f"🚗 **Compatibilidad:** {row.get('Marca', '')}"
                            f" {row.get('Modelo', '')}"
                        )
                        st.write(
                            f"🏷️ **SKU:** {row.get('SKU / Código', 'N/A')} | 💵"
                            " **Precio:**"
                            f" ${row.get('Precio ($)', row.get('Precio', '0.00'))}"
                        )
                        if pd.notna(row.get("Ubicación Almacén")):
                            st.caption(
                                f"📍 Ubicación: {row['Ubicación Almacén']}"
                            )

                    with col_action_wa:
                        texto_msj = (
                            "¡Hola! 👋 Le comparto las imágenes de la"
                            f" *{producto_nombre}* para tu"
                            f" {row.get('Marca', '')} {row.get('Modelo', '')}"
                            " que me consultó:\n\n💰 *Precio:*"
                            f" ${row.get('Precio ($)', row.get('Precio', '0.00'))}\n🔢"
                            f" *Código/SKU:* {row.get('SKU / Código', 'N/A')}\n\nAquí"
                            " puedes ver cómo es y cómo queda:\n"
                        )

                        if url_img1 and url_img1.startswith("http"):
                            texto_msj += f"1️⃣ *Producto:* {url_img1}\n"
                        if url_img2 and url_img2.startswith("http"):
                            texto_msj += f"2️⃣ *Exhibición:* {url_img2}\n"
                        if url_img3 and url_img3.startswith("http"):
                            texto_msj += f"3️⃣ *Instalada:* {url_img3}\n"

                        texto_msj += (
                            "\n¿Te gustaría coordinar el envío o la"
                            " instalación? Quedo atento. 🚗💨"
                        )

                        # Enlace clásico WhatsApp
                        texto_encoded = urllib.parse.quote(texto_msj)
                        link_wa = (
                            f"https://api.whatsapp.com/send?text={texto_encoded}"
                        )

                        st.markdown(
                            f"""
                            <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #e62117;
                                    color: white;
                                    border: none;
                                    padding: 10px 16px;
                                    border-radius: 8px;
                                    font-size: 14px;
                                    font-weight: bold;
                                    width: 100%;
                                    cursor: pointer;
                                ">
                                    📲 Enviar por WhatsApp
                                </button>
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.divider()
