import urllib.parse
import pandas as pd
import requests
import streamlit as st

# Configuración de la app
st.set_page_config(
    page_title="W.G.H. Car Shop - Catálogo Vendedores",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 W.G.H. Car Shop - Catálogo Digital")
st.subheader("Buscador de repuestos y recursos para WhatsApp Business")

# URL de tu plantilla de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1IaHxrsTMgm3SRjpdLOnpx8hpwV0MhL97/export?format=csv"


@st.cache_data(ttl=60)
def cargar_inventario():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception:
        return pd.DataFrame()


df = cargar_inventario()

if not df.empty:
    # ---------------------------------------------------------
    # FILTROS EN CASCADA / BÚSQUEDA INTELLIGENTE
    # ---------------------------------------------------------
    st.markdown("### 🔍 Filtros de Búsqueda")

    col_f1, col_f2 = st.columns(2)
    col_f3, col_f4 = st.columns(2)

    def obtener_opciones(col_names):
        for col in col_names:
            if col in df.columns:
                vals = [
                    str(x).strip()
                    for x in df[col].unique()
                    if str(x).strip() != ""
                ]
                return col, ["Todos"] + sorted(vals)
        return None, ["Todos"]

    col_marca, opciones_marca = obtener_opciones(
        ["Marca", "MARCA", "marca_vehiculo"]
    )
    col_modelo, opciones_modelo = obtener_opciones(
        ["Modelo", "MODELO", "modelo_vehiculo"]
    )
    col_anio, opciones_anio = obtener_opciones(["Año", "AÑO", "Anio", "anio"])
    col_categoria, opciones_categoria = obtener_opciones(
        ["Categoría", "CATEGORIA", "Categoria", "categoria"]
    )

    with col_f1:
        sel_marca = st.selectbox("🚘 Marca:", opciones_marca)
    with col_f2:
        sel_modelo = st.selectbox("🏎️ Modelo:", opciones_modelo)
    with col_f3:
        sel_anio = st.selectbox("📅 Año:", opciones_anio)
    with col_f4:
        sel_categoria = st.selectbox("🏷️ Categoría:", opciones_categoria)

    busqueda = st.text_input(
        "🔎 Buscar por descripción o código (opcional):", ""
    )

    # Filtrar datos
    df_filtrado = df.copy()

    if col_marca and sel_marca != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_marca].astype(str).str.strip() == sel_marca
        ]
    if col_modelo and sel_modelo != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_modelo].astype(str).str.strip() == sel_modelo
        ]
    if col_anio and sel_anio != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_anio].astype(str).str.strip() == sel_anio
        ]
    if col_categoria and sel_categoria != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_categoria].astype(str).str.strip() == sel_categoria
        ]

    if busqueda.strip():
        mask = (
            df_filtrado.astype(str)
            .apply(
                lambda row: row.str.contains(busqueda, case=False, na=False)
            )
            .any(axis=1)
        )
        df_filtrado = df_filtrado[mask]

    st.markdown("---")
    st.caption(f"Mostrando {len(df_filtrado)} resultado(s)")

    # ---------------------------------------------------------
    # PRODUCTOS Y BOTONES DE RECURSOS
    # ---------------------------------------------------------
    for idx, row in df_filtrado.iterrows():
        producto = str(
            row.get(
                "Producto / Descripción",
                row.get(
                    "Descripción", row.get("Producto", "Repuesto Automotriz")
                ),
            )
        )
        precio_raw = str(
            row.get("Precio ($)", row.get("Precio", "0.00"))
        ).replace("$", "")
        sku = str(row.get("SKU / Código", row.get("Código", "N/A")))
        marca = str(row.get("Marca", row.get("MARCA", "")))
        modelo = str(row.get("Modelo", row.get("MODELO", "")))
        anio = str(row.get("Año", row.get("AÑO", "")))

        # Extraer URLs de fotos
        cols_img = [
            c
            for c in df.columns
            if any(x in c.lower() for x in ["imagen", "foto", "url", "link"])
        ]
        links_fotos = []

        for col in cols_img:
            url_img = str(row.get(col, "")).strip()
            if (
                url_img
                and url_img.lower() != "nan"
                and url_img.startswith("http")
            ):
                if "drive.google.com" in url_img and "/file/d/" in url_img:
                    file_id = (
                        url_img.split("/file/d/")[1]
                        .split("/")[0]
                        .split("?")[0]
                    )
                    url_img = f"https://lh3.googleusercontent.com/d/{file_id}"
                links_fotos.append(url_img)

        st.markdown(f"### 📦 {producto}")

        col_detalles, col_fotos = st.columns([1, 1])

        with col_detalles:
            st.info(f"""
            * 🏷️ **Código / SKU:** `{sku}`
            * 🚗 **Vehículo:** {marca} {modelo} ({anio})
            * 💵 **Precio Oferta:** ${precio_raw}
            * 🚚 **Envío:** $10.00 (Servientrega)
            * 💳 **Pago:** Contra entrega
            """)

            # Mensaje para el cliente
            mensaje_cliente = (
                f"¡Hola! Disponemos de *{producto}*\n"
                f"🏷️ *Oferta:* ${precio_raw} + $10.00 de envío\n"
                f"📦 *Pago:* Contra entrega por Servientrega.\n"
                f"¿Desea confirmar su pedido?"
            )

            st.text_area(
                "📋 Texto para copiar rápido:",
                value=mensaje_cliente,
                height=110,
                key=f"txt_{idx}",
            )

            # Botón directo para enviar texto a WhatsApp
            msg_encoded = urllib.parse.quote(mensaje_cliente)
            link_wa = f"https://api.whatsapp.com/send?text={msg_encoded}"
            st.link_button(
                "📲 1. Enviar Texto a WhatsApp",
                link_wa,
                use_container_width=True,
            )

        with col_fotos:
            st.markdown("**📷 Descarga rápida de fotos:**")

            if links_fotos:
                for num, img_url in enumerate(links_fotos, 1):
                    st.image(img_url, use_container_width=True)

                    # Descarga directa de la imagen para adjuntar nativamente
                    try:
                        res = requests.get(img_url, timeout=5)
                        if res.status_code == 200:
                            st.download_button(
                                label=f"📥 Descargar Foto {num} al Teléfono",
                                data=res.content,
                                file_name=f"{sku}_foto_{num}.jpg",
                                mime="image/jpeg",
                                key=f"dl_{idx}_{num}",
                                use_container_width=True,
                            )
                    except Exception:
                        pass
            else:
                st.caption("📷 Sin imágenes configuradas.")

        st.divider()
else:
    st.warning(
        "No se pudieron obtener datos. Verifica los permisos de la plantilla en Google Sheets."
    )
