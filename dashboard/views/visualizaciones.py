"""Gráficos interactivos con filtros globales."""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.constants import (
    COL_ANO,
    COL_AREA,
    COL_BARRIO,
    COL_CICLO,
    COL_COMUNA,
    COL_VICTIMA,
    COL_VIOLENCIA,
    PLOTLY_CONFIG,
)
from dashboard.transforms import filtrar_para_graficos, preparar_df_visual


def render(df_raw: pd.DataFrame) -> None:
    st.title("Visualizaciones interactivas")
    st.caption(
        "Usa los filtros de abajo: al cambiar **comuna (zona)**, **años**, **área**, **tipo de violencia** o **sexo**, "
        "todos los gráficos se actualizan con el mismo subconjunto de datos. En los gráficos puedes hacer zoom, "
        "pan y selección con la barra de herramientas de Plotly."
    )

    df_base = preparar_df_visual(df_raw)
    template = "plotly_dark"

    lista_comunas = sorted(df_base[COL_COMUNA].dropna().astype(str).unique().tolist())
    anos_numeric = pd.to_numeric(df_base[COL_ANO], errors="coerce").dropna()
    y_min = int(anos_numeric.min()) if len(anos_numeric) else 2015
    y_max = int(anos_numeric.max()) if len(anos_numeric) else 2025
    lista_areas = (
        sorted(df_base[COL_AREA].dropna().astype(str).unique().tolist())
        if COL_AREA in df_base.columns
        else []
    )
    lista_tipos = sorted(df_base[COL_VIOLENCIA].dropna().astype(str).unique().tolist())
    lista_sexos = sorted(df_base[COL_VICTIMA].dropna().astype(str).unique().tolist())

    with st.expander("Filtros globales (afectan a todos los gráficos)", expanded=True):
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            modo_zona = st.radio(
                "Zona / Comuna",
                ["Todas las comunas", "Una comuna", "Varias comunas"],
                horizontal=True,
                key="viz_modo_comuna",
            )
            comunas_sel = []
            if modo_zona == "Una comuna":
                comunas_sel = [st.selectbox("Elige la comuna", lista_comunas, key="viz_una_comuna")]
            elif modo_zona == "Varias comunas":
                comunas_sel = st.multiselect(
                    "Elige una o más comunas",
                    lista_comunas,
                    default=[],
                    key="viz_varias_comunas",
                    help="Si no marcas ninguna, se consideran todas.",
                )
        with r1c2:
            rango_anos = st.slider(
                "Rango de años",
                min_value=y_min,
                max_value=y_max,
                value=(y_min, y_max),
                key="viz_rango_anos",
            )
            anos_sel = list(range(rango_anos[0], rango_anos[1] + 1))
        with r1c3:
            areas_sel = []
            if lista_areas:
                areas_sel = st.multiselect(
                    "Área (cabecera / rural)",
                    lista_areas,
                    default=[],
                    key="viz_areas",
                    help="Vacío = todas las áreas.",
                )

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            tipos_sel = st.multiselect(
                "Tipo de violencia",
                lista_tipos,
                default=[],
                key="viz_tipos",
                help="Vacío = todos los tipos.",
            )
        with r2c2:
            sexos_sel = st.multiselect(
                "Sexo de la víctima",
                lista_sexos,
                default=[],
                key="viz_sexos",
                help="Vacío = todos.",
            )

        st.caption(
            "Para ver otra zona: elige **Una comuna** o ajusta el rango de años. "
            "En Plotly: icono de cámara = descargar imagen; zoom/pan en la barra superior del gráfico."
        )

    df = filtrar_para_graficos(df_base, comunas_sel, anos_sel, areas_sel, tipos_sel, sexos_sel)

    n_total = len(df_base)
    n_filtrado = len(df)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Registros con filtros actuales", f"{n_filtrado:,}")
    with m2:
        st.metric("Porcentaje del total", f"{100 * n_filtrado / n_total:.1f} %" if n_total else "0 %")
    with m3:
        if modo_zona == "Una comuna" and comunas_sel:
            z = comunas_sel[0]
            st.metric("Zona seleccionada", z[:40] + ("…" if len(z) > 40 else ""))
        elif comunas_sel:
            st.metric("Comunas en filtro", len(comunas_sel))
        else:
            st.metric("Zona", "Todas")

    if n_filtrado == 0:
        st.warning("No hay datos con esta combinación de filtros. Amplía años o quita filtros.")
        st.stop()

    subtitulo_ctx = ""
    if comunas_sel:
        subtitulo_ctx = f" — filtrado: {len(comunas_sel)} comuna(s)"
    if rango_anos != (y_min, y_max):
        subtitulo_ctx += f" | años {rango_anos[0]}–{rango_anos[1]}"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Casos por tipo de violencia{subtitulo_ctx}")
        datos_viol = df[COL_VIOLENCIA].value_counts().reset_index()
        datos_viol.columns = ["Tipo", "Cantidad"]
        fig1 = px.bar(
            datos_viol.head(15),
            x="Tipo",
            y="Cantidad",
            color="Cantidad",
            color_continuous_scale="Blues",
            labels={"Tipo": "Tipo de violencia", "Cantidad": "Número de casos"},
        )
        fig1.update_layout(
            template=template,
            xaxis_tickangle=-45,
            showlegend=False,
            hovermode="x unified",
        )
        fig1.update_traces(hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>")
        st.plotly_chart(fig1, use_container_width=True, config=PLOTLY_CONFIG)

    with col2:
        st.subheader("Distribución por sexo de la víctima")
        datos_sexo = df[COL_VICTIMA].value_counts().reset_index()
        datos_sexo.columns = ["Sexo", "Cantidad"]
        fig2 = px.pie(
            datos_sexo,
            values="Cantidad",
            names="Sexo",
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig2.update_traces(hovertemplate="<b>%{label}</b><br>%{value} casos (%{percent})<extra></extra>")
        fig2.update_layout(template=template)
        st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CONFIG)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Casos por ciclo de vida")
        if COL_CICLO in df.columns:
            datos_ciclo = df[COL_CICLO].value_counts().reset_index()
            datos_ciclo.columns = ["Ciclo", "Cantidad"]
            fig3 = px.bar(
                datos_ciclo,
                x="Ciclo",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale="Teal",
            )
            fig3.update_layout(template=template, xaxis_tickangle=-45, showlegend=False, hovermode="x")
            fig3.update_traces(hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>")
            st.plotly_chart(fig3, use_container_width=True, config=PLOTLY_CONFIG)

    with col4:
        una_zona = len(comunas_sel) == 1
        if una_zona and COL_BARRIO in df.columns:
            st.subheader("Barrios en la zona seleccionada (top 12)")
            datos_ubi = df[COL_BARRIO].value_counts().head(12).reset_index()
            datos_ubi.columns = ["Barrio", "Cantidad"]
            fig4 = px.bar(
                datos_ubi,
                x="Barrio",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale="Purples",
            )
            fig4.update_layout(template=template, xaxis_tickangle=-45, showlegend=False)
        else:
            st.subheader("Top comunas en el subconjunto filtrado")
            datos_ubi = df[COL_COMUNA].value_counts().head(12).reset_index()
            datos_ubi.columns = ["Comuna", "Cantidad"]
            fig4 = px.bar(
                datos_ubi,
                x="Comuna",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale="Purples",
            )
            fig4.update_layout(template=template, xaxis_tickangle=-45, showlegend=False)
        fig4.update_traces(hovertemplate="<b>%{x}</b><br>Casos: %{y}<extra></extra>")
        st.plotly_chart(fig4, use_container_width=True, config=PLOTLY_CONFIG)

    st.subheader("Evolución anual de casos (según filtros)")
    evol = df.groupby(COL_ANO).size().reset_index(name="casos")
    evol[COL_ANO] = pd.to_numeric(evol[COL_ANO], errors="coerce")
    evol = evol.dropna(subset=[COL_ANO]).sort_values(COL_ANO)
    fig5 = px.line(evol, x=COL_ANO, y="casos", markers=True)
    fig5.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate="Año: %{x}<br>Casos: %{y}<extra></extra>",
    )
    fig5.update_layout(
        template=template,
        xaxis_title="Año",
        yaxis_title="Número de casos",
        hovermode="x unified",
    )
    st.plotly_chart(fig5, use_container_width=True, config=PLOTLY_CONFIG)

    st.subheader("Mapa de calor: ciclo de vida vs tipo de violencia")
    cross = pd.crosstab(df[COL_CICLO], df[COL_VIOLENCIA])
    if cross.size == 0:
        st.info("No hay filas suficientes para el mapa de calor.")
    else:
        fig6 = px.imshow(
            cross,
            aspect="auto",
            color_continuous_scale="Blues",
            labels=dict(x="Tipo de violencia", y="Ciclo de vida", color="Casos"),
        )
        fig6.update_layout(template=template, hovermode="closest")
        fig6.update_traces(hovertemplate="%{y} / %{x}<br>Casos: %{z}<extra></extra>")
        st.plotly_chart(fig6, use_container_width=True, config=PLOTLY_CONFIG)
