"""
Proyecto Final - Ciencia de Datos con Python y Streamlit
Análisis de Violencia de Género e Intrafamiliar - Alcaldía de Bucaramanga

Aplicando: Manipulación, Limpieza, Transformación y Visualización de Datos
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="Violencia de Género e Intrafamiliar - Bucaramanga",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def cargar_datos():
    """Carga el CSV con manejo de encoding para caracteres especiales."""
    base = Path(__file__).parent
    csv_files = list(base.glob("*.csv"))
    if not csv_files:
        csv_files = list(Path(".").glob("*.csv"))  
    if not csv_files:
        st.error("No se encontró ningún archivo CSV en el directorio.")
        return None
    ruta = csv_files[0]
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return pd.read_csv(ruta, encoding=enc, on_bad_lines="skip")
        except UnicodeDecodeError:
            continue
    return pd.read_csv(ruta, encoding="utf-8", on_bad_lines="skip", errors="ignore")


st.markdown("""
<style>
    /* Tema profesional - tonos sobrios para datos sensibles */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f26 100%);
    }
    
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        color: #e8eaed !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #38bdf8 !important;
    }
    
    .footer-note {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown(
        '<p style="text-align:center;font-size:2.75rem;line-height:1;margin:0 0 0.35rem 0;">📊</p>',
        unsafe_allow_html=True,
    )
    st.title("Proyecto Final")
    st.markdown("**Ciencia de Datos con Python**")
    st.markdown("---")
    
    seccion = st.radio(
        "Navegación",
        ["🏠 Inicio", "📂 Explorar Datos", "🧹 Limpieza & Transformación", 
         "📈 Análisis Estadístico", "📉 Visualizaciones"]
    )
    st.markdown("---")
    st.caption("Datos: Alcaldía de Bucaramanga - SIVIGILA")


df_raw = cargar_datos()
if df_raw is None:
    st.stop()


COL_VICTIMA = "sexo_" 
COL_VIOLENCIA = "def_naturaleza"  
COL_EDAD = "Grupo edad"
COL_CICLO = "Ciclo de vida"
COL_COMUNA = "Comuna"
COL_BARRIO = "Barrio"
COL_MES = "MES"
COL_ANO = "año"
COL_PARENTEZCO = "parentezco_vict"  
COL_SEGURIDAD = "Tipo de Seguridad Social"
COL_AREA = "area_"  


def preparar_df_visual(df_in: pd.DataFrame) -> pd.DataFrame:
    """Limpieza mínima para la sección de gráficos."""
    df = df_in.copy()
    for c in [COL_VIOLENCIA, COL_VICTIMA, COL_EDAD, COL_COMUNA, COL_CICLO, COL_AREA, COL_BARRIO]:
        if c in df.columns:
            df[c] = df[c].fillna("Sin información")
    return df


def filtrar_para_graficos(df: pd.DataFrame, comunas, anos, areas, tipos_viol, sexos) -> pd.DataFrame:
    """Aplica filtros de la barra interactiva (operadores como en clase)."""
    out = df
    if comunas:
        out = out[out[COL_COMUNA].isin(comunas)]
    if anos:
        y_num = pd.to_numeric(out[COL_ANO], errors="coerce")
        out = out[y_num.isin(anos)]
    if areas and COL_AREA in out.columns:
        out = out[out[COL_AREA].isin(areas)]
    if tipos_viol:
        out = out[out[COL_VIOLENCIA].isin(tipos_viol)]
    if sexos:
        out = out[out[COL_VICTIMA].isin(sexos)]
    return out


PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToAdd": ["select2d", "lasso2d", "resetScale2d"],
    "toImageButtonOptions": {"format": "png", "filename": "grafico_dashboard"},
}


if seccion == "🏠 Inicio":
    st.title("Análisis de Violencia de Género e Intrafamiliar")
    st.subheader("Bucaramanga - Datos SIVIGILA")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Registros", f"{len(df_raw):,}")
    with col2:
        st.metric("📅 Años de Datos", f"{df_raw[COL_ANO].nunique()}")
    with col3:
        st.metric("📊 Columnas", len(df_raw.columns))
    with col4:
        nulos = df_raw.isnull().sum().sum()
        st.metric("⚠️ Valores Nulos", f"{nulos:,}")
    
    st.markdown("---")
    st.markdown("""
    Este dashboard aplica las técnicas vistas en clase:
    - **Filtrado**: Operadores de comparación y lógicos
    - **Sondeo**: `unique()`, `nunique()`, `value_counts()`
    - **Ordenamiento**: `sort_values()`
    - **Limpieza**: Manejo de NaN con `fillna()`, `dropna()`
    - **Conversión de tipos**: `astype()`
    - **Agrupación**: `groupby()` con `agg()`
    """)


elif seccion == "📂 Explorar Datos":
    st.title("Exploración del DataFrame")
    
    tab1, tab2, tab3 = st.tabs(["Vista general", "Estructura", "Frecuencias"])
    
    with tab1:
        st.subheader("Primeras filas (head)")
        st.dataframe(df_raw.head(20), use_container_width=True)
    
    with tab2:
        st.subheader("Info del DataFrame")
        buffer = []
        buffer.append(f"**Filas:** {df_raw.shape[0]} | **Columnas:** {df_raw.shape[1]}")
        buffer.append(f"\n**Tipos de datos:**\n{df_raw.dtypes.to_string()}")
        st.text("\n".join(buffer))
        st.subheader("Estadísticas descriptivas (describe)")
        st.dataframe(df_raw.describe(include="all").T, use_container_width=True)
    
    with tab3:
        st.subheader("value_counts() - Frecuencias por categoría")
        col_sel = st.selectbox("Selecciona columna", 
            [COL_VIOLENCIA, COL_VICTIMA, COL_EDAD, COL_CICLO, COL_COMUNA, COL_PARENTEZCO, COL_SEGURIDAD])
        counts = df_raw[col_sel].value_counts()
        st.dataframe(counts, use_container_width=True)
        st.caption(f"Total categorías únicas: {df_raw[col_sel].nunique()}")


elif seccion == "🧹 Limpieza & Transformación":
    st.title("Limpieza y Transformación de Datos")
    
    df = df_raw.copy()
    
    st.subheader("1. Detección de nulos")
    nulos_tabla = df.isnull().sum()
    nulos_tabla = nulos_tabla[nulos_tabla > 0].sort_values(ascending=False)
    if len(nulos_tabla) > 0:
        st.dataframe(nulos_tabla.to_frame("Cantidad nulos"), use_container_width=True)
    else:
        st.success("No hay valores nulos en el dataset.")
    
    st.subheader("2. Estrategias de limpieza")
    strat = st.radio("Estrategia para columnas clave con nulos:", 
        ["Rellenar con 'Sin información' (categóricas)", 
         "Eliminar filas con nulos en columnas clave"])
    
    columnas_clave = [COL_VIOLENCIA, COL_VICTIMA, COL_EDAD, COL_MES]
    
    if strat.startswith("Rellenar"):
        for c in columnas_clave:
            if c in df.columns and df[c].isnull().any():
                df[c] = df[c].fillna("Sin información")
        st.success("Valores nulos rellenados con 'Sin información'")
    else:
        df = df.dropna(subset=columnas_clave, how="any")
        st.success(f"Filas eliminadas. Registros restantes: {len(df):,}")
    
    st.subheader("3. Filtrado inteligente (ejemplo de clase)")
    st.markdown("Filtrar por **tipo de violencia** y **sexo de la víctima**:")
    tipos = df[COL_VIOLENCIA].dropna().unique().tolist()
    sexos = df[COL_VICTIMA].dropna().unique().tolist()
    
    filtro_tipo = st.multiselect("Tipo de violencia", tipos, default=tipos[:3])
    filtro_sexo = st.multiselect("Sexo víctima", sexos)
    
    df_filtrado = df[
        (df[COL_VIOLENCIA].isin(filtro_tipo)) &
        (df[COL_VICTIMA].isin(filtro_sexo) if filtro_sexo else True)
    ]
    st.metric("Registros filtrados", len(df_filtrado))
    
    st.subheader("4. Ordenamiento (sort_values)")
    df_ordenado = df_filtrado.sort_values(by=COL_ANO, ascending=False)
    st.dataframe(df_ordenado[[COL_ANO, COL_MES, COL_VIOLENCIA, COL_VICTIMA, COL_EDAD]].head(15), use_container_width=True)
    
    st.subheader("5. Agrupación con agg() - Reporte por año")
    reporte = df.groupby(COL_ANO)[COL_VIOLENCIA].agg(["count", "nunique"])
    reporte = reporte.rename(columns={"count": "Total casos", "nunique": "Tipos de violencia"})
    st.dataframe(reporte, use_container_width=True)


elif seccion == "📈 Análisis Estadístico":
    st.title("Análisis Estadístico")
    
    df = df_raw.copy()
    
    for c in [COL_VIOLENCIA, COL_VICTIMA, COL_EDAD]:
        if c in df.columns:
            df[c] = df[c].fillna("Sin información")
    
    st.subheader("Agrupación: Casos por tipo de violencia y sexo")
    reporte = df.groupby([COL_VIOLENCIA, COL_VICTIMA]).size().reset_index(name="cantidad")
    reporte = reporte.sort_values("cantidad", ascending=False)
    st.dataframe(reporte, use_container_width=True)
    
    st.subheader("Agrupación: Casos por comuna (top 15)")
    por_comuna = df.groupby(COL_COMUNA).agg({
        COL_VIOLENCIA: "count",
        COL_ANO: "nunique"
    }).rename(columns={COL_VIOLENCIA: "Total casos", COL_ANO: "Años con datos"})
    por_comuna = por_comuna.sort_values("Total casos", ascending=False).head(15)
    st.dataframe(por_comuna, use_container_width=True)
    
    st.subheader("Agrupación: Evolución temporal (por año)")
    evol = df.groupby(COL_ANO).size().reset_index(name="casos")
    st.dataframe(evol, use_container_width=True)


elif seccion == "📉 Visualizaciones":
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
            st.metric("Zona seleccionada", comunas_sel[0][:40] + ("…" if len(comunas_sel[0]) > 40 else ""))
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


st.markdown("---")
st.markdown('<p class="footer-note">Proyecto Final - Ciencia de Datos con Python y Streamlit | Fuente: SIVIGILA - Alcaldía de Bucaramanga</p>', unsafe_allow_html=True)
