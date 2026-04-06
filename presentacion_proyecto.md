---
marp: true
theme: default
paginate: true
header: 'Proyecto final · Ciencia de datos con Python'
footer: 'Violencia de género e intrafamiliar · Bucaramanga (SIVIGILA)'
style: |
  section { font-size: 26px; }
  h1 { color: #1e3a5f; font-size: 1.35em; }
  h2 { color: #0f766e; font-size: 1.05em; }
  table { font-size: 0.85em; }
---

<!-- _class: lead -->
# Dashboard interactivo
## Violencia de género e intrafamiliar
### Alcaldía de Bucaramanga · datos SIVIGILA

**Ciencia de datos con Python, Pandas y Streamlit**

---

## 1. Equipo y roles

| Integrante | Rol principal | Participación |
|------------|---------------|----------------|
| *(Frank Edwin Tabares Gil)* | Datos / Pandas | Limpieza, filtros, `groupby`, `agg` |
| *(Daniel Esteban Lozano)* | Interfaz Streamlit | Navegación, secciones, estilos |
| *(Juan Diego Gomez Higuita)* | Despliegue y pruebas | GitHub, Streamlit Cloud, validación |
| *(Kevin David Galeano Tabares)* | Despliegue y pruebas | GitHub, Streamlit Cloud, validación |

*Todos participaron en revisiones, pruebas y documentación.*

---

## 2. Propósito del proyecto

Construir una **aplicación web** que permita:

- Explorar un **dataset real** de vigilancia en salud pública (SIVIGILA)
- Aplicar **manipulación, limpieza y transformación** con **Pandas**
- Visualizar resultados con **gráficos interactivos** (Plotly)
- Acceder al análisis **desde el navegador** y en la **nube**

---

## 3. Objetivos generales

1. **Cargar** el CSV con manejo de encoding y rutas robustas
2. **Explorar** el DataFrame (`head`, `describe`, `value_counts`)
3. **Limpiar** nulos (`fillna` / `dropna`) en columnas clave
4. **Transformar:** filtros, `sort_values`, `groupby` + `agg`
5. **Visualizar** con filtros globales por **comuna, año, área, tipo, sexo**
6. **Desplegar** en **Streamlit Community Cloud** vía GitHub

---

## 4. Fuente de datos

- **Tema:** Violencia de género e intrafamiliar — **Bucaramanga**
- **Origen:** Alcaldía / **SIVIGILA** (vigilancia en salud pública)
- **Formato:** CSV · miles de registros

**Variables de análisis:** tipo de violencia (`def_naturaleza`), sexo de la víctima, grupo de edad, ciclo de vida, comuna, barrio, año, mes, etc.

---

## 5. Demo — estructura de la app

**Menú lateral — cinco módulos:**

1. **Inicio** — métricas (registros, años, nulos)
2. **Explorar datos** — tablas y frecuencias
3. **Limpieza y transformación** — nulos, filtros, orden, reporte por año
4. **Análisis estadístico** — tablas resumen
5. **Visualizaciones** — gráficos con **filtros que actualizan toda la vista**

*Demo en vivo: una comuna + rango de años + gráficos interactivos (zoom, hover).*

---

## 6. Pandas — conceptos de clase

| Tema | Uso en el proyecto |
|------|---------------------|
| **Filtrado** | `isin`, `&`, condiciones por columna |
| **Sondeo** | `unique`, `nunique`, `value_counts` |
| **Orden** | `sort_values` (ej. por año descendente) |
| **Limpieza** | `fillna("Sin información")`, `dropna(subset=…)` |
| **Agrupación** | `groupby` + `agg` (`count`, `nunique`) |

---

## 7. Arquitectura del código

```
app.py
├── cargar_datos()          → pd.read_csv + @st.cache_data
├── preparar_df_visual()
├── filtrar_para_graficos()
├── Secciones (st.sidebar → radio)
└── Plotly: bar, pie, line, imshow
```

- Entrada: `streamlit run app.py`
- Dependencias: `requirements.txt` · entorno: `venv`

---

## 8. Entorno y despliegue

- **venv** — entorno virtual aislado
- **pip install -r requirements.txt** — Pandas, Streamlit, Plotly
- **Git + GitHub** — control de versiones y respaldo del CSV
- **Streamlit Community Cloud** — URL pública `*.streamlit.app`

---

## 9. Tecnologías y justificación

| Tecnología | Propósito |
|------------|-----------|
| **Python** | Lenguaje del análisis |
| **Pandas** | Tablas, limpieza, agregaciones |
| **Streamlit** | App web rápida sin stack front complejo |
| **Plotly** | Gráficos interactivos |
| **Git / GitHub** | Historial y despliegue |

*Elección académica estándar: integración directa datos → UI → nube.*

---

## 10. Conclusiones

- Se cubrió el flujo **datos → limpieza → análisis → visualización → nube**
- Los **filtros por zona y tiempo** orientan el análisis territorial y temporal
- **`fillna` vs `dropna`** muestra cómo la estrategia de nulos altera el tamaño y la interpretación del dataset

---

## 11. Logros · dificultades · aprendizajes

**Logros:** aplicación funcional, despliegue web, práctica integral de Pandas  

**Dificultades:** nulos en variables clave, encoding del CSV, coherencia de filtros y gráficos  

**Aprendizajes:** calidad y documentación de datos son base de conclusiones válidas  

---

<!-- _class: lead -->
## Gracias



