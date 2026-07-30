import pandas as pd
import streamlit as st

# Configuración de la interfaz
st.set_page_config(
    page_title="W.G.H. Car Shop - Catálogo Vendedores",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Catálogo Digital de Repuestos")
st.subheader("Buscador de productos e imágenes para vendedores")

# URL de tu plantilla de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1IaHxrsTMgm3SRjpdLOnpx8hpwV0MhL97/export?format=csv"


@st.cache_data(ttl=60)  # Se actualiza automáticamente cada 60 segundos
def cargar_inventario():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al conectar con la plantilla de Google Sheets: {e}")
        return pd.DataFrame()


df = cargar_inventario()

if not df.empty:
    busqueda = st.text_input(
        "🔍 Buscar por repuesto, código o modelo (Ej. D-Max, Mascarilla):", ""
    )

    if busqueda.strip():
        mask = (
            df.astype(str)
            .apply(
                lambda row: row.str.contains(busqueda, case=False, na=False)
            )
            .any(axis=1)
        )
        df_filtrado = df[mask]
    else:
        df_filtrado = df

    st.markdown("---")
    st.caption(f"Mostrando {len(df_filtrado)} resultado(s)")

    for idx, row in df_filtrado.iterrows():
        # Detección flexible de columnas
        producto = row.get(
            "Producto / Descripción",
            row.get(
                "Producto", row.get("Descripción", "Repuesto Automotriz")
            ),
        )
        precio = row.get("Precio ($)", row.get("Precio", "0.00"))
        sku = row.get("SKU / Código", row.get("Código", "N/A"))

        st.markdown(f"### 📦 {producto}")

        col_detalles, col_fotos = st.columns([1, 1])

        with col_detalles:
            st.info(f"""
            * 🏷️ **Código / SKU:** `{sku}`
            * 💵 **Precio Oferta:** ${precio}
            * 🚚 **Envío:** $10.00 (Servientrega)
            * 💳 **Pago:** Contra entrega al recibir
            """)

            mensaje = f"¡Hola! Disponemos de *{producto}* en oferta por *${precio}* + envío. Pago contra entrega por Servientrega. ¿Desea coordinar el pedido?"
            st.text_area(
                "📋 Copiar texto para el cliente:",
                value=mensaje,
                height=90,
                key=f"txt_{idx}",
            )

        with col_fotos:
            st.markdown("**📷 Vista previa de fotos:**")

            # Buscar cualquier columna que contenga links de imágenes
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
                    # Formatear URLs de Google Drive para visualización directa
                    if "drive.google.com" in url_img:
                        if "/file/d/" in url_img:
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
