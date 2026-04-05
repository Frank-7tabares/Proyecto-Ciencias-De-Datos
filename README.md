# Proyecto Final - Ciencia de Datos con Python y Streamlit

**Análisis de Violencia de Género e Intrafamiliar - Alcaldía de Bucaramanga**

## Contenido del proyecto

Este proyecto aplica los conceptos vistos en clase:

- **Manipulación de DataFrames**: Filtrado, ordenamiento, selección
- **Limpieza de datos**: Manejo de nulos (`fillna`, `dropna`), conversión de tipos
- **Transformación**: Agrupación con `groupby`, `agg`, `value_counts`
- **Visualización**: Gráficos interactivos con Plotly
- **Carga de datos**: CSV con encoding UTF-8

## Requisitos

- Python 3.9 o superior
- Dependencias en `requirements.txt`

## Instalación local

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

---

## Despliegue en la nube (Streamlit Community Cloud)

### Opción A: Con GitHub

1. **Crear cuenta** en [Streamlit Community Cloud](https://share.streamlit.io/)

2. **Subir el proyecto a GitHub**
   - Crea un repositorio en GitHub
   - Sube los archivos: `app.py`, `requirements.txt` y el archivo CSV

3. **Desplegar**
   - Ve a [share.streamlit.io](https://share.streamlit.io/)
   - Clic en "New app"
   - Selecciona tu repositorio
   - **Main file path**: `app.py`
   - **App URL**: elige un nombre único
   - Clic en "Deploy"

### Opción B: Con Streamlit en Hugging Face Spaces

1. Crea una cuenta en [Hugging Face](https://huggingface.co/)
2. Crea un nuevo Space (SDK: Streamlit)
3. Sube `app.py`, `requirements.txt` y el CSV
4. El Space se desplegará automáticamente

### Estructura necesaria para despliegue

```
Proyecto-Streamlit/
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias
├── Violencia_de_Género_...csv  # Dataset
└── README.md                 # Este archivo
```

---

## Estructura de la aplicación

| Sección | Descripción |
|---------|-------------|
| **Inicio** | Métricas generales del dataset |
| **Explorar Datos** | Vista general, info, value_counts |
| **Limpieza & Transformación** | Manejo de nulos, filtrado, sort_values, groupby |
| **Análisis Estadístico** | Agregaciones por tipo de violencia, comuna, año |
| **Visualizaciones** | Gráficos de barras, torta, líneas, mapa de calor |

---

## Fuente de datos

Datos de la Alcaldía de Bucaramanga - Sistema de Vigilancia en Salud Pública (SIVIGILA) - Violencia de Género e Intrafamiliar.
