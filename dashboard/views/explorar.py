"""Exploración del DataFrame."""

import pandas as pd
import streamlit as st

from dashboard.constants import (
    COL_CICLO,
    COL_COMUNA,
    COL_EDAD,
    COL_PARENTEZCO,
    COL_SEGURIDAD,
    COL_VICTIMA,
    COL_VIOLENCIA,
)


def render(df_raw: pd.DataFrame) -> None:
    st.title("Exploración del DataFrame")

    tab1, tab2, tab3 = st.tabs(["Vista general", "Estructura", "Frecuencias"])

    with tab1:
        st.subheader("Primeras filas (head)")
        st.dataframe(df_raw.head(20), use_container_width=True)

    with tab2:
        st.subheader("Info del DataFrame")
        buffer = [
            f"**Filas:** {df_raw.shape[0]} | **Columnas:** {df_raw.shape[1]}",
            f"\n**Tipos de datos:**\n{df_raw.dtypes.to_string()}",
        ]
        st.text("\n".join(buffer))
        st.subheader("Estadísticas descriptivas (describe)")
        st.dataframe(df_raw.describe(include="all").T, use_container_width=True)

    with tab3:
        st.subheader("value_counts() - Frecuencias por categoría")
        col_sel = st.selectbox(
            "Selecciona columna",
            [
                COL_VIOLENCIA,
                COL_VICTIMA,
                COL_EDAD,
                COL_CICLO,
                COL_COMUNA,
                COL_PARENTEZCO,
                COL_SEGURIDAD,
            ],
        )
        counts = df_raw[col_sel].value_counts()
        st.dataframe(counts, use_container_width=True)
        st.caption(f"Total categorías únicas: {df_raw[col_sel].nunique()}")
