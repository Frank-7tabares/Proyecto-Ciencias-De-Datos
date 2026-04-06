"""Pantalla de inicio: propósito, objetivos y métricas."""

import pandas as pd
import streamlit as st

from dashboard.constants import COL_ANO


def render(df_raw: pd.DataFrame) -> None:
    st.title("Análisis de Violencia de Género e Intrafamiliar")
    st.subheader("Bucaramanga · Datos SIVIGILA")

    st.markdown("### Propósito del proyecto")
    st.markdown(
        """
Desarrollar una **aplicación analítica modular** que integre **ciencia de datos** y **visualización web** sobre
registros reales de vigilancia en salud pública, separando **carga de datos**, **reglas de negocio / transformación**
y **presentación** en archivos distintos para facilitar el mantenimiento, las pruebas y el trabajo en equipo.
        """
    )

    st.markdown("### Objetivos generales")
    st.markdown(
        """
1. **Arquitectura:** organizar el código en paquetes (`dashboard`: constantes, datos, transformaciones, vistas).
2. **Ingesta:** leer el CSV con encoding robusto y rutas independientes del directorio de trabajo.
3. **Exploración:** describir el dataset (dimensiones, tipos, frecuencias).
4. **Calidad de datos:** aplicar estrategias documentadas de manejo de nulos (`fillna` / `dropna`).
5. **Transformación:** filtrar, ordenar y agrupar con Pandas según criterios de análisis.
6. **Comunicación:** ofrecer gráficos interactivos con filtros coherentes entre sí.
7. **Despliegue:** publicar la app vía repositorio Git y Streamlit Community Cloud.
        """
    )

    st.markdown("---")
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
    st.markdown(
        """
**Técnicas de curso aplicadas en el código**

- **Filtrado:** operadores de comparación y lógicos  
- **Sondeo:** `unique()`, `nunique()`, `value_counts()`  
- **Ordenamiento:** `sort_values()`  
- **Limpieza:** `fillna()`, `dropna()`  
- **Tipos:** `astype()` donde aplica  
- **Agrupación:** `groupby()` con `agg()`
        """
    )
