"""Carga del dataset desde CSV."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@st.cache_data
def cargar_datos() -> Optional[pd.DataFrame]:
    """Carga el CSV con manejo de encoding para caracteres especiales."""
    base = _project_root()
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
