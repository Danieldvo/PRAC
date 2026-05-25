# 🏠 Inversión Airbnb Madrid — Visualización Interactiva

![Streamlit App](https://mercado-inmobiliario-dvo.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

Aplicación interactiva desarrollada como proyecto de visualización para el **Máster en Data Science (UOC)** — PRAC.

Analiza 8.296 alojamientos activos en Madrid para responder a una pregunta clave: **¿merece la pena invertir en Airbnb en Madrid, y dónde?**

---

## 📖 Descripción

Esta herramienta permite explorar el mercado de alquiler vacacional en Madrid cruzando datos de **Inside Airbnb**, **Idealista** y **OpenStreetMap** para calcular la rentabilidad potencial de una inversión inmobiliaria en función del distrito, tipología y número de habitaciones.

### Páginas de la aplicación

| Página | Descripción |
|--------|-------------|
| 📖 Introducción | Contexto del análisis, métricas globales, preguntas clave y metodología |
| 🏠 Resumen del mercado | KPIs dinámicos, margen bruto por distrito, distribución por tipo |
| 🗺️ ¿Dónde invertir? | Mapa de calor interactivo + scatter rentabilidad vs. atractivo turístico |
| 💰 ¿Cuánto ganaré? | Heatmaps de ingreso anual y margen bruto por tipología y habitaciones |
| 🎯 Conclusiones | Top 3 distritos dinámico, hallazgos clave y perfil óptimo de inversión |

---

## 📊 Datos

| Fuente | Descripción |
|--------|-------------|
| [Inside Airbnb](http://insideairbnb.com/) | Listings activos en Madrid (2025): precios, disponibilidad, valoraciones |
|  [Idealista API](https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/venta/madrid-comunidad/madrid-provincia/madrid/) | Precio medio por m² por barrio (para estimar coste de adquisición) |
| OpenStreetMap (POI) | 44 puntos de interés turístico de Madrid |

### Métrica principal calculada

```
Margen bruto (%) = Ingreso anual estimado / Coste de adquisición × 100
```

Donde:
- **Ingreso anual** = precio/noche × días de ocupación estimada
- **Coste de adquisición** = precio/m² × m² estimados del inmueble

---

## 🚀 Ejecución local

### Requisitos

- Python 3.10+
- Git

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/airbnb-madrid-inversion.git
cd airbnb-madrid-inversion

# 2. Instalar dependencias
python -m pip install -r requirements.txt

# 3. Lanzar la aplicación
python -m streamlit run app.py
```

En Windows también puedes hacer doble clic en `run.bat`.

---

## 🌐 Despliegue en Streamlit Cloud

La app está desplegada en [Streamlit Community Cloud](https://streamlit.io/cloud) (gratuito).

Para desplegarla en tu propia cuenta:

1. Haz fork de este repositorio en GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Selecciona el repositorio, rama `main` y fichero principal `app.py`
4. Haz clic en **Deploy**

---

## 📦 Estructura del proyecto

```
streamlit_app/
├── app.py                    # Aplicación principal (5 páginas)
├── requirements.txt          # Dependencias Python
├── run.bat                   # Script de ejecución en Windows
├── LICENSE                   # Licencia MIT
├── README.md                 # Este archivo
├── notebooks/
│   ├── 01_ImportacionDatos.ipynb    # Carga y limpieza de datos brutos de Airbnb e Idealista
│   ├── 02_CreacionVariables.ipynb   # Ingeniería de variables: margen bruto, atractivo turístico, discretización
│   └── 03_Analisis.ipynb            # Análisis exploratorio, estadísticas descriptivas y validación
└── data/
    ├── tablon_analitico.csv  # Dataset principal (8.296 filas × 27 cols)
    └── poi_madrid.csv        # Puntos de interés turístico (44 POIs)
```

---

## 🛠️ Tecnologías utilizadas

| Librería | Uso |
|----------|-----|
| [Streamlit](https://streamlit.io/) | Framework de la aplicación web |
| [Plotly](https://plotly.com/python/) | Gráficos interactivos (barras, scatter, heatmap, violín, donut) |
| [Folium](https://python-visualization.github.io/folium/) | Mapa interactivo con capa de calor y POIs |
| [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) | Integración Folium ↔ Streamlit |
| [pandas](https://pandas.pydata.org/) | Manipulación y análisis de datos |
| [numpy](https://numpy.org/) | Cálculos numéricos |

---

## 🤖 Uso de IA

Este proyecto fue desarrollado con asistencia de **Claude (Anthropic)** para la generación de código Streamlit/Plotly/Folium y la redacción de textos narrativos.

El análisis de datos, las métricas de negocio, las conclusiones y la selección del dataset son trabajo original del autor.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT** — consulta el fichero [LICENSE](LICENSE) para más detalles.

---

## ✉️ Contacto

**Daniel Vargas Olivencia** · Máster en Data Science, UOC  
danidvo@gmail.com
