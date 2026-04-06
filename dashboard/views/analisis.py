"""Análisis estadístico tabular."""

import pandas as pd
import streamlit as st

from dashboard.constants import COL_ANO, COL_COMUNA, COL_EDAD, COL_VICTIMA, COL_VIOLENCIA


def render(df_raw: pd.DataFrame) -> None:
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
    por_comuna = (
        df.groupby(COL_COMUNA)
        .agg({COL_VIOLENCIA: "count", COL_ANO: "nunique"})
        .rename(columns={COL_VIOLENCIA: "Total casos", COL_ANO: "Años con datos"})
    )
    por_comuna = por_comuna.sort_values("Total casos", ascending=False).head(15)
    st.dataframe(por_comuna, use_container_width=True)

    st.subheader("Agrupación: Evolución temporal (por año)")
    evol = df.groupby(COL_ANO).size().reset_index(name="casos")
    st.dataframe(evol, use_container_width=True)
