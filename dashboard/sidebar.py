"""Barra lateral: navegación entre secciones."""

import streamlit as st

SECCIONES = [
    "🏠 Inicio",
    "📂 Explorar Datos",
    "🧹 Limpieza & Transformación",
    "📈 Análisis Estadístico",
    "📉 Visualizaciones",
]


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            '<p style="text-align:center;font-size:2.75rem;line-height:1;margin:0 0 0.35rem 0;">📊</p>',
            unsafe_allow_html=True,
        )
        st.title("Proyecto Final")
        st.markdown("**Ciencia de Datos con Python**")
        st.markdown("---")
        seccion = st.radio("Navegación", SECCIONES)
        st.markdown("---")
        st.caption("Datos: Alcaldía de Bucaramanga - SIVIGILA")
    return seccion
