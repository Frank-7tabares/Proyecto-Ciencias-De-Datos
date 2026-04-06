"""
Proyecto Final - Ciencia de Datos con Python y Streamlit
Punto de entrada: configura la app, carga datos y delega cada pantalla al paquete `dashboard`.
"""

import streamlit as st

from dashboard.data import cargar_datos
from dashboard.sidebar import render_sidebar
from dashboard.styles import inject_custom_css, render_footer
from dashboard.views import analisis, explorar, inicio, limpieza, visualizaciones

st.set_page_config(
    page_title="Violencia de Género e Intrafamiliar - Bucaramanga",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
seccion = render_sidebar()

df_raw = cargar_datos()
if df_raw is None:
    st.stop()

if seccion == "🏠 Inicio":
    inicio.render(df_raw)
elif seccion == "📂 Explorar Datos":
    explorar.render(df_raw)
elif seccion == "🧹 Limpieza & Transformación":
    limpieza.render(df_raw)
elif seccion == "📈 Análisis Estadístico":
    analisis.render(df_raw)
elif seccion == "📉 Visualizaciones":
    visualizaciones.render(df_raw)

render_footer()
