"""Nombres de columnas del CSV y configuración de gráficos."""

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

PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToAdd": ["select2d", "lasso2d", "resetScale2d"],
    "toImageButtonOptions": {"format": "png", "filename": "grafico_dashboard"},
}
