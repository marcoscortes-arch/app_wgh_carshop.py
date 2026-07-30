import pandas as pd
import streamlit as st

# Configuración de la interfaz
st.set_page_config(
    page_title="W.G.H. Car Shop - Catálogo Vendedores",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Catálogo Digital de Repuestos")
st.subheader("Buscador y filtros para vendedores")

# URL de tu plantilla de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1IaHxrsTMgm3SRjpdLOnpx8hpwV0MhL97/export?format=csv"


@st.cache_data(ttl=60)  # Se actualiza automáticamente cada 60 segundos
def cargar_inventario():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        # Asegurar que todas las celdas sean tratadas adecuadamente
        return df.fillna("")
    except Exception as e:
        st.error(f"Error al conectar con la plantilla de Google Sheets: {e}")
        return pd.DataFrame()


df = cargar_inventario()

if not df.empty:
    # ---------------------------------------------------------
    # FILTROS DESPLEGABLES (Marca, Modelo, Año, Categoría)
    # ---------------------------------------------------------
    st.markdown("### 🔍 Filtros de Búsqueda")

    col_f1, col_f2 = st.columns(2)
    col_f3, col_f4 = st.columns(2)

    # Detección inteligente de columnas en tu Google Sheet
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

    # Buscador de texto libre adicional
    busqueda = st.text_input(
        "🔎 Buscar por descripción o código (opcional):", ""
    )

    # Aplicar filtros
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
    # MOSTRAR RESULTADOS
    # ---------------------------------------------------------
    for idx, row in df_filtrado.iterrows():
        # Captura de campos
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
        categoria = str(row.get("Categoría", row.get("CATEGORIA", "")))

        st.markdown(f"### 📦 {producto}")

        col_detalles, col_fotos = st.columns([1, 1])

        with col_detalles:
            # Info detallada del repuesto
            info_text = f"* 🏷️ **Código / SKU:** `{sku}`\n"
            if marca or modelo or anio:
                info_text += (
                    f"* 🚗 **Vehículo:** {marca} {modelo} ({anio})\n".strip()
                    + "\n"
                )
            if categoria:
                info_text += f"* 📁 **Categoría:** {categoria}\n"
            info_text += f"* 💵 **Precio Oferta:** ${precio_raw}\n"
            info_text += f"* 🚚 **Envío:** $10.00 (Servientrega)\n"
            info_text += f"* 💳 **Pago:** Contra entrega al recibir"

            st.info(info_text)

            mensaje = f"¡Hola! Disponemos de *{producto}* en oferta por *${precio_raw}* + envío. Pago contra entrega por Servientrega. ¿Desea coordinar el pedido?"
            st.text_area(
                "📋 Copiar texto para el cliente:",
                value=mensaje,
                height=90,
                key=f"txt_{idx}",
            )

        with col_fotos:
            st.markdown("**📷 Vista previa de fotos:**")

            cols_img = [
                c
                for c in df.columns
                if any(x in c.lower() for x in ["imagen", "foto", "url", "link"])
            ]
            hay_fotos = False

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

                    st.image(url_img, use_container_width=True)
                    hay_fotos = True

            if not hay_fotos:
                st.caption("📷 Sin imagen configurada.")

        st.divider()
else:
    st.warning(
        "No se pudieron obtener datos. Verifica los permisos de la plantilla en Google Sheets."
    )
