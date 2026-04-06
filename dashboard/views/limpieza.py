"""Limpieza y transformación de datos."""

import pandas as pd
import streamlit as st

from dashboard.constants import COL_ANO, COL_EDAD, COL_MES, COL_VICTIMA, COL_VIOLENCIA


def render(df_raw: pd.DataFrame) -> None:
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
    strat = st.radio(
        "Estrategia para columnas clave con nulos:",
        [
            "Rellenar con 'Sin información' (categóricas)",
            "Eliminar filas con nulos en columnas clave",
        ],
    )

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
        (df[COL_VIOLENCIA].isin(filtro_tipo))
        & (df[COL_VICTIMA].isin(filtro_sexo) if filtro_sexo else True)
    ]
    st.metric("Registros filtrados", len(df_filtrado))

    st.subheader("4. Ordenamiento (sort_values)")
    df_ordenado = df_filtrado.sort_values(by=COL_ANO, ascending=False)
    st.dataframe(
        df_ordenado[[COL_ANO, COL_MES, COL_VIOLENCIA, COL_VICTIMA, COL_EDAD]].head(15),
        use_container_width=True,
    )

    st.subheader("5. Agrupación con agg() - Reporte por año")
    reporte = df.groupby(COL_ANO)[COL_VIOLENCIA].agg(["count", "nunique"])
    reporte = reporte.rename(
        columns={"count": "Total casos", "nunique": "Tipos distintos (nunique)"}
    )
    st.dataframe(reporte, use_container_width=True)
    st.caption(
        "La columna 'Tipos distintos' cuenta cuántas categorías diferentes de violencia hubo por año, no el nombre de un tipo."
    )
