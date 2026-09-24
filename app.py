import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

st.set_page_config(
    page_title="Bolsa de Valores Quito BI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Bolsa de Valores Quito BI")
st.write("Análisis financiero interactivo de empresas")
st.caption("Elaborado por: Carlos Carrillo")

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------

st.sidebar.title("⚙️ Parámetros")

archivo = st.sidebar.file_uploader(
    "Cargue su archivo CSV",
    type=["csv"]
)

# ---------------------------------------------------------
# LECTURA DEL ARCHIVO
# ---------------------------------------------------------

if archivo is not None:

    tabla = pd.read_csv(archivo)

    # Eliminar columna de índice innecesaria
    if "Unnamed: 0" in tabla.columns:
        tabla = tabla.drop(columns=["Unnamed: 0"])

    # Convertir fecha
    tabla["Period Ending"] = pd.to_datetime(
        tabla["Period Ending"],
        errors="coerce"
    )

    # ---------------------------------------------------------
    # FILTROS
    # ---------------------------------------------------------

    empresas = sorted(
        tabla["Ticker Symbol"]
        .dropna()
        .unique()
    )

    empresa = st.sidebar.selectbox(
        "Seleccione una empresa",
        empresas
    )

    # Filtrar empresa
    df_empresa = tabla[
        tabla["Ticker Symbol"] == empresa
    ].copy()

    df_empresa = df_empresa.sort_values("Period Ending")

    # ---------------------------------------------------------
    # INFORMACIÓN GENERAL
    # ---------------------------------------------------------

    st.subheader(f"📌 Empresa seleccionada: {empresa}")

    st.write(
        f"""
        Registros disponibles: **{len(df_empresa)}**  
        Periodo inicial: **{df_empresa['Period Ending'].min().date()}**  
        Periodo final: **{df_empresa['Period Ending'].max().date()}**
        """
    )

    # Último periodo disponible
    ultimo = df_empresa.iloc[-1]

    # ---------------------------------------------------------
    # KPI PRINCIPALES
    # ---------------------------------------------------------

    st.subheader("📈 Indicadores financieros")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Ingresos Totales",
        f"${ultimo['Total Revenue']:,.0f}"
    )

    col2.metric(
        "Utilidad Neta",
        f"${ultimo['Net Income']:,.0f}"
    )

    col3.metric(
        "ROE",
        f"{ultimo['After Tax ROE']:.2f}%"
    )

    col4.metric(
        "Margen Neto",
        f"{ultimo['Profit Margin']:.2f}%"
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Activos Totales",
        f"${ultimo['Total Assets']:,.0f}"
    )

    col6.metric(
        "Pasivos Totales",
        f"${ultimo['Total Liabilities']:,.0f}"
    )

    col7.metric(
        "Patrimonio",
        f"${ultimo['Total Equity']:,.0f}"
    )

    if pd.notna(ultimo["Earnings Per Share"]):
        eps = f"${ultimo['Earnings Per Share']:.2f}"
    else:
        eps = "N/D"

    col8.metric(
        "EPS",
        eps
    )

    st.divider()

    # ---------------------------------------------------------
    # PESTAÑAS
    # ---------------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Resultados",
            "💰 Rentabilidad",
            "🏦 Situación Financiera",
            "💧 Liquidez",
            "📋 Datos"
        ]
    )

    # =========================================================
    # TAB 1 - RESULTADOS
    # =========================================================

    with tab1:

        st.subheader("Evolución de ingresos y utilidad")

        columnas_resultados = [
            "Period Ending",
            "Total Revenue",
            "Gross Profit",
            "Operating Income",
            "Net Income"
        ]

        df_resultados = df_empresa[
            columnas_resultados
        ].melt(
            id_vars="Period Ending",
            var_name="Indicador",
            value_name="Valor"
        )

        fig = px.line(
            df_resultados,
            x="Period Ending",
            y="Valor",
            color="Indicador",
            markers=True,
            title="Evolución de resultados financieros"
        )

        fig.update_layout(
            xaxis_title="Periodo",
            yaxis_title="USD"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Barras ingresos vs utilidad
        fig2 = px.bar(
            df_empresa,
            x="Period Ending",
            y=[
                "Total Revenue",
                "Net Income"
            ],
            barmode="group",
            title="Ingresos vs. Utilidad Neta"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =========================================================
    # TAB 2 - RENTABILIDAD
    # =========================================================

    with tab2:

        st.subheader("Indicadores de rentabilidad")

        df_rentabilidad = df_empresa[
            [
                "Period Ending",
                "Gross Margin",
                "Operating Margin",
                "Pre-Tax Margin",
                "Profit Margin"
            ]
        ].melt(
            id_vars="Period Ending",
            var_name="Indicador",
            value_name="Porcentaje"
        )

        fig3 = px.line(
            df_rentabilidad,
            x="Period Ending",
            y="Porcentaje",
            color="Indicador",
            markers=True,
            title="Evolución de márgenes"
        )

        fig3.update_layout(
            xaxis_title="Periodo",
            yaxis_title="Porcentaje"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # ROE
        fig4 = px.bar(
            df_empresa,
            x="Period Ending",
            y="After Tax ROE",
            title="Rentabilidad sobre el patrimonio (ROE)"
        )

        fig4.update_layout(
            xaxis_title="Periodo",
            yaxis_title="ROE (%)"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    # =========================================================
    # TAB 3 - SITUACIÓN FINANCIERA
    # =========================================================

    with tab3:

        st.subheader("Estructura financiera")

        df_balance = df_empresa[
            [
                "Period Ending",
                "Total Assets",
                "Total Liabilities",
                "Total Equity"
            ]
        ].melt(
            id_vars="Period Ending",
            var_name="Cuenta",
            value_name="Valor"
        )

        fig5 = px.bar(
            df_balance,
            x="Period Ending",
            y="Valor",
            color="Cuenta",
            barmode="group",
            title="Activos, Pasivos y Patrimonio"
        )

        fig5.update_layout(
            xaxis_title="Periodo",
            yaxis_title="USD"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

        # Deuda
        fig6 = px.line(
            df_empresa,
            x="Period Ending",
            y="Long-Term Debt",
            markers=True,
            title="Evolución de la deuda de largo plazo"
        )

        fig6.update_layout(
            xaxis_title="Periodo",
            yaxis_title="USD"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

    # =========================================================
    # TAB 4 - LIQUIDEZ
    # =========================================================

    with tab4:

        st.subheader("Indicadores de liquidez")

        df_liquidez = df_empresa[
            [
                "Period Ending",
                "Current Ratio",
                "Quick Ratio",
                "Cash Ratio"
            ]
        ].melt(
            id_vars="Period Ending",
            var_name="Indicador",
            value_name="Valor"
        )

        fig7 = px.line(
            df_liquidez,
            x="Period Ending",
            y="Valor",
            color="Indicador",
            markers=True,
            title="Evolución de indicadores de liquidez"
        )

        fig7.update_layout(
            xaxis_title="Periodo",
            yaxis_title="Ratio"
        )

        st.plotly_chart(
            fig7,
            use_container_width=True
        )

        # Activo corriente vs pasivo corriente
        fig8 = px.bar(
            df_empresa,
            x="Period Ending",
            y=[
                "Total Current Assets",
                "Total Current Liabilities"
            ],
            barmode="group",
            title="Activos Corrientes vs. Pasivos Corrientes"
        )

        st.plotly_chart(
            fig8,
            use_container_width=True
        )

    # =========================================================
    # TAB 5 - DATOS
    # =========================================================

    with tab5:

        st.subheader("Base de datos")

        st.dataframe(
            df_empresa,
            use_container_width=True
        )

        # Descargar información filtrada
        csv = df_empresa.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Descargar datos de la empresa",
            data=csv,
            file_name=f"{empresa}_datos_financieros.csv",
            mime="text/csv"
        )

# ---------------------------------------------------------
# MENSAJE INICIAL
# ---------------------------------------------------------

else:

    st.info(
        "👈 Cargue el archivo `fundamentals.csv` desde el panel lateral para visualizar el dashboard."
    )
