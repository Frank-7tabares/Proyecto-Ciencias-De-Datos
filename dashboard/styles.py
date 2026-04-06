"""Estilos globales de la interfaz."""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    .main { background: linear-gradient(180deg, #0f1419 0%, #1a1f26 100%); }
    h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #e8eaed !important; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #38bdf8 !important; }
    .footer-note { text-align: center; padding: 2rem; color: #64748b; font-size: 0.85rem; }
</style>
"""


def inject_custom_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown("---")
    st.markdown(
        '<p class="footer-note">Proyecto Final - Ciencia de Datos con Python y Streamlit | '
        "Fuente: SIVIGILA - Alcaldía de Bucaramanga</p>",
        unsafe_allow_html=True,
    )
