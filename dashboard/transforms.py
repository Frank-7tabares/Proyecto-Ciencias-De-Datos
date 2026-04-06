"""Transformaciones reutilizables sobre DataFrames."""

import pandas as pd

from dashboard.constants import (
    COL_ANO,
    COL_AREA,
    COL_BARRIO,
    COL_CICLO,
    COL_COMUNA,
    COL_EDAD,
    COL_VICTIMA,
    COL_VIOLENCIA,
)


def preparar_df_visual(df_in: pd.DataFrame) -> pd.DataFrame:
    """Limpieza mínima para la sección de gráficos."""
    df = df_in.copy()
    for c in [COL_VIOLENCIA, COL_VICTIMA, COL_EDAD, COL_COMUNA, COL_CICLO, COL_AREA, COL_BARRIO]:
        if c in df.columns:
            df[c] = df[c].fillna("Sin información")
    return df


def filtrar_para_graficos(
    df: pd.DataFrame,
    comunas: list,
    anos: list,
    areas: list,
    tipos_viol: list,
    sexos: list,
) -> pd.DataFrame:
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
