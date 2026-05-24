# ============================================================
# PRAC – Inversión Airbnb en Madrid
# Visualización interactiva con narrativa
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from pathlib import Path
import branca.colormap as cm

# ── Paleta de colores ────────────────────────────────────────
PRIMARY   = "#1A3A5C"
SECONDARY = "#2E6DA4"
ACCENT    = "#E87722"
TEXT      = "#222222"
LIGHT_BG  = "#F7F9FB"
GOLD      = "#C9A84C"
SILVER    = "#888888"
BRONZE    = "#A0522D"

# ── Configuración de página ──────────────────────────────────
st.set_page_config(
    page_title="Inversión Airbnb Madrid",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ───────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Fuentes y base */
  html, body, [data-testid="stAppViewContainer"] {{
      font-family: 'Arial', sans-serif;
      color: {TEXT};
  }}
  /* Sidebar */
  [data-testid="stSidebar"] {{
      background: {PRIMARY};
  }}
  [data-testid="stSidebar"] * {{
      color: white !important;
  }}
  /* KPI cards */
  .kpi-card {{
      background: white;
      border-radius: 10px;
      padding: 16px 18px 12px;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      border-top: 4px solid {ACCENT};
  }}
  .kpi-value {{
      font-size: 1.9rem;
      font-weight: 700;
      color: {PRIMARY};
      line-height: 1.1;
  }}
  .kpi-label {{
      font-size: 0.78rem;
      color: #666;
      margin-top: 4px;
  }}
  /* Intro hero */
  .intro-hero {{
      background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
      border-radius: 14px;
      padding: 36px 40px;
      color: white;
      margin-bottom: 24px;
  }}
  .intro-hero h1 {{
      font-size: 2.2rem;
      font-weight: 800;
      margin: 0 0 8px;
      color: white;
  }}
  .intro-hero p {{
      font-size: 1.05rem;
      color: rgba(255,255,255,0.88);
      margin: 0;
  }}
  /* Question cards */
  .question-card {{
      background: white;
      border-radius: 10px;
      padding: 18px 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      border-left: 5px solid {ACCENT};
      height: 100%;
  }}
  .question-card .q-num {{
      font-size: 2rem;
      font-weight: 800;
      color: {ACCENT};
      line-height: 1;
  }}
  .question-card h3 {{
      font-size: 1rem;
      font-weight: 700;
      color: {PRIMARY};
      margin: 6px 0 6px;
  }}
  .question-card p {{
      font-size: 0.85rem;
      color: #555;
      margin: 0;
  }}
  /* Methodology box */
  .method-box {{
      background: {LIGHT_BG};
      border-radius: 10px;
      padding: 20px 24px;
      border: 1px solid #DDE3EB;
  }}
  .method-box h4 {{
      color: {PRIMARY};
      font-size: 1rem;
      font-weight: 700;
      margin: 0 0 10px;
  }}
  .method-box p, .method-box li {{
      font-size: 0.87rem;
      color: #444;
      line-height: 1.55;
  }}
  /* Recommendation cards */
  .rec-gold {{
      background: linear-gradient(135deg, #FFF8E7 0%, #FFF0C8 100%);
      border: 2px solid {GOLD};
      border-radius: 12px;
      padding: 16px 18px;
      text-align: center;
  }}
  .rec-silver {{
      background: linear-gradient(135deg, #F5F5F5 0%, #EBEBEB 100%);
      border: 2px solid {SILVER};
      border-radius: 12px;
      padding: 16px 18px;
      text-align: center;
  }}
  .rec-bronze {{
      background: linear-gradient(135deg, #FFF3EE 0%, #FFDDD0 100%);
      border: 2px solid {BRONZE};
      border-radius: 12px;
      padding: 16px 18px;
      text-align: center;
  }}
  .rec-medal {{
      font-size: 1.6rem;
      line-height: 1;
  }}
  .rec-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: {PRIMARY};
      margin: 6px 0 4px;
  }}
  .rec-value {{
      font-size: 1.5rem;
      font-weight: 800;
      color: {ACCENT};
  }}
  .rec-sub {{
      font-size: 0.78rem;
      color: #666;
  }}
  /* Insight boxes */
  .insight-box {{
      background: white;
      border-radius: 10px;
      padding: 16px 18px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      border-left: 4px solid {SECONDARY};
      margin-bottom: 12px;
  }}
  .insight-box .i-icon {{
      font-size: 1.4rem;
      margin-right: 8px;
  }}
  .insight-box strong {{
      color: {PRIMARY};
  }}
  /* Optimal profile */
  .profile-box {{
      background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
      border-radius: 12px;
      padding: 22px 28px;
      color: white;
  }}
  .profile-box h3 {{
      color: white;
      font-size: 1.1rem;
      font-weight: 700;
      margin: 0 0 14px;
  }}
  .profile-item {{
      display: flex;
      align-items: center;
      margin-bottom: 8px;
      font-size: 0.9rem;
  }}
  .profile-item .label {{
      color: rgba(255,255,255,0.7);
      width: 160px;
      flex-shrink: 0;
  }}
  .profile-item .val {{
      color: white;
      font-weight: 700;
  }}
  /* AI disclaimer */
  .ai-disclaimer {{
      background: #FFFBF0;
      border: 1px solid #F0D080;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.78rem;
      color: #665500;
  }}
  /* Section headers */
  .section-header {{
      font-size: 1.3rem;
      font-weight: 700;
      color: {PRIMARY};
      border-bottom: 3px solid {ACCENT};
      padding-bottom: 6px;
      margin-bottom: 18px;
  }}
  /* Chart subtitles — force dark color regardless of Streamlit theme */
  .chart-label {{
      font-size: 0.97rem;
      font-weight: 700;
      color: {PRIMARY} !important;
      margin-bottom: 4px;
  }}
</style>
""", unsafe_allow_html=True)

# ── Helpers de estilo Plotly ─────────────────────────────────
AXIS_STYLE = dict(
    tickfont=dict(size=11, color=TEXT),
    title_font=dict(size=12, color=TEXT),
    showgrid=True, gridcolor="#E8E8E8",
    linecolor="#CCCCCC", linewidth=1,
)

def fig_defaults(fig, height=320):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", color=TEXT, size=11),
        height=height,
        margin=dict(l=10, r=10, t=6, b=36),
        title=dict(text=""),
        legend=dict(
            font=dict(size=11, color=TEXT),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#DDDDDD", borderwidth=0.5,
        ),
        coloraxis_colorbar=dict(
            title_font=dict(size=11, color=TEXT),
            tickfont=dict(size=10, color=TEXT), thickness=14,
        ),
    )
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

# ── Carga de datos ────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando datos…")
def load_data():
    base = Path(__file__).parent / "data"
    df   = pd.read_csv(base / "tablon_analitico.csv")
    poi  = pd.read_csv(base / "poi_madrid.csv")
    df = df.dropna(subset=["margen_bruto", "precio_noche", "ingreso_anual",
                            "latitude", "longitude", "neighbourhood", "distrito"])
    df = df[df["neighbourhood"].str.strip().ne("")]
    df = df[df["distrito"].str.strip().ne("")]
    for col in ["margen_bruto", "precio_noche", "ingreso_anual", "coste_adquisicion"]:
        df[col] = df[col].clip(upper=df[col].quantile(0.99))
    hab_map = {"0_hab": "0 hab.", "1_hab": "1 hab.", "2_hab": "2 hab.",
               "3_hab": "3 hab.", "4+_hab": "4+ hab."}
    df["hab_label"] = df["bedrooms_disc"].map(hab_map)
    return df, poi

df_full, poi_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 Inversión Airbnb Madrid")
    st.markdown("---")

    page = st.radio(
        "Navegación",
        [
            "📖  Introducción",
            "🏠  Resumen del mercado",
            "🗺️  ¿Dónde invertir?",
            "💰  ¿Cuánto ganaré?",
            "🎯  Conclusiones",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### Filtros globales")

    distritos_all = sorted(df_full["distrito"].dropna().unique())
    dist_sel = st.multiselect(
        "Distrito",
        distritos_all,
        default=distritos_all,
        key="dist_sel",
    )

    room_types = sorted(df_full["room_type"].dropna().unique())
    room_sel = st.multiselect(
        "Tipo de alojamiento",
        room_types,
        default=room_types,
        key="room_sel",
    )

    hab_options = ["0 hab.", "1 hab.", "2 hab.", "3 hab.", "4+ hab."]
    hab_sel = st.multiselect(
        "Habitaciones",
        hab_options,
        default=hab_options,
        key="hab_sel",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem; color:rgba(255,255,255,0.6);'>"
        "Fuentes: Airbnb/Inside Airbnb · Idealista API · OSM POI<br>"
        "Datos: Madrid, 2025</div>",
        unsafe_allow_html=True,
    )

# ── Aplicar filtros ───────────────────────────────────────────
df = df_full.copy()
if dist_sel:
    df = df[df["distrito"].isin(dist_sel)]
if room_sel:
    df = df[df["room_type"].isin(room_sel)]
if hab_sel:
    df = df[df["hab_label"].isin(hab_sel)]

# ── Función KPI card ──────────────────────────────────────────
def kpi(value, label):
    return f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


# ════════════════════════════════════════════════════════════
# PÁGINA 0 · INTRODUCCIÓN
# ════════════════════════════════════════════════════════════
if page == "📖  Introducción":

    st.markdown("""
    <div class="intro-hero">
        <h1>¿Merece la pena invertir en Airbnb en Madrid?</h1>
        <p>Un análisis de 8.296 alojamientos activos para ayudarte a tomar la mejor decisión de inversión inmobiliaria.</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs del dataset completo
    n_total   = len(df_full)
    precio_m  = df_full["precio_noche"].median()
    margen_m  = df_full["margen_bruto"].median()
    coste_m   = df_full["coste_adquisicion"].median() / 1000
    n_dist    = df_full["distrito"].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, lbl in zip(
        [c1, c2, c3, c4, c5],
        [f"{n_total:,}", f"€{precio_m:.0f}", f"{margen_m:.1f}%", f"€{coste_m:.0f}K", str(n_dist)],
        ["alojamientos analizados", "precio/noche mediano", "margen bruto mediano", "coste adquisición mediano", "distritos de Madrid"],
    ):
        col.markdown(kpi(val, lbl), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Preguntas clave
    st.markdown('<div class="section-header">Las 3 preguntas que responde esta aplicación</div>', unsafe_allow_html=True)

    qa, qb, qc = st.columns(3)
    qa.markdown("""
    <div class="question-card">
        <div class="q-num">01</div>
        <h3>🗺️ ¿Dónde debo invertir?</h3>
        <p>Comparamos los 21 distritos de Madrid por margen bruto, precio/m² y demanda turística para identificar las zonas más rentables.</p>
    </div>
    """, unsafe_allow_html=True)

    qb.markdown("""
    <div class="question-card">
        <div class="q-num">02</div>
        <h3>💰 ¿Cuánto dinero ganaré?</h3>
        <p>Estimamos el ingreso anual esperado según el tipo de propiedad, el número de habitaciones y la ocupación histórica del barrio.</p>
    </div>
    """, unsafe_allow_html=True)

    qc.markdown("""
    <div class="question-card">
        <div class="q-num">03</div>
        <h3>🎯 ¿Cuál es el perfil óptimo?</h3>
        <p>Identificamos la combinación de distrito + tipología + tamaño que maximiza el retorno sobre la inversión inicial.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metodología
    st.markdown('<div class="section-header">Metodología y fuentes de datos</div>', unsafe_allow_html=True)

    m1, m2 = st.columns([1, 1])
    m1.markdown("""
    <div class="method-box">
        <h4>📂 Fuentes de datos</h4>
        <ul>
            <li><b>Inside Airbnb</b> (listings activos en Madrid, 2025): precios, disponibilidad, tipo de habitación, valoraciones.</li>
            <li><b>Idealista API</b>: precio medio por m² por barrio para estimar el coste de adquisición.</li>
            <li><b>OpenStreetMap (POI)</b>: 44 puntos de interés turístico de Madrid para calcular el atractivo de cada barrio.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    m2.markdown(f"""
    <div class="method-box">
        <h4>📐 Métricas clave calculadas</h4>
        <ul>
            <li><b>Ingreso anual estimado</b> = precio/noche × ocupación estimada (días/año)</li>
            <li><b>Coste de adquisición</b> = precio/m² × m² estimados del inmueble</li>
            <li><b>Margen bruto (%)</b> = ingreso anual / coste adquisición × 100</li>
            <li><b>Atractivo turístico</b> = nº de POIs en radio de 1 km del alojamiento</li>
        </ul>
        <p>Todos los valores extremos (percentil > 99) han sido recortados para evitar distorsiones.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-disclaimer">
        🤖 <b>Nota sobre uso de IA:</b> Esta aplicación fue desarrollada con asistencia de Claude (Anthropic) para la generación de código Streamlit/Plotly/Folium y la redacción de los textos narrativos. Todo el análisis de datos, las métricas y las conclusiones son resultado del trabajo propio del autor sobre los datos originales.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PÁGINA 1 · RESUMEN DEL MERCADO
# ════════════════════════════════════════════════════════════
elif page == "🏠  Resumen del mercado":

    st.markdown('<div class="section-header">📊 Resumen del mercado de alquiler vacacional en Madrid</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados.")
        st.stop()

    # KPIs dinámicos
    n      = len(df)
    p_med  = df["precio_noche"].median()
    m_med  = df["margen_bruto"].median()
    i_med  = df["ingreso_anual"].median()

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in zip(
        [c1, c2, c3, c4],
        [f"{n:,}", f"€{p_med:.0f}", f"{m_med:.1f}%", f"€{i_med:,.0f}"],
        ["alojamientos", "precio/noche mediano", "margen bruto mediano", "ingreso anual mediano"],
    ):
        col.markdown(kpi(val, lbl), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="chart-label">Margen bruto por distrito</p>', unsafe_allow_html=True)
        dist_margen = (
            df.groupby("distrito")["margen_bruto"]
            .median()
            .reset_index()
            .sort_values("margen_bruto", ascending=True)
        )
        fig1 = go.Figure(go.Bar(
            x=dist_margen["margen_bruto"],
            y=dist_margen["distrito"],
            orientation="h",
            marker_color=SECONDARY,
            text=dist_margen["margen_bruto"].map("{:.1f}%".format),
            textposition="outside",
            textfont=dict(size=10, color=TEXT),
        ))
        fig1 = fig_defaults(fig1, height=420)
        fig1.update_xaxes(title_text="Margen bruto mediano (%)")
        fig1.update_yaxes(title_text="")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<p class="chart-label">Distribución por tipo de alojamiento</p>', unsafe_allow_html=True)
        rt_counts = df["room_type"].value_counts().reset_index()
        rt_counts.columns = ["room_type", "count"]
        fig2 = go.Figure(go.Pie(
            labels=rt_counts["room_type"],
            values=rt_counts["count"],
            hole=0.45,
            marker_colors=[SECONDARY, ACCENT, "#7FB3D3"],
            textinfo="label+percent",
            textfont=dict(size=11, color=TEXT),
        ))
        fig2 = fig_defaults(fig2, height=280)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<p class="chart-label">Precio/noche por tipo y habitaciones</p>', unsafe_allow_html=True)
        hab_order = ["0 hab.", "1 hab.", "2 hab.", "3 hab.", "4+ hab."]
        df_box = df[df["hab_label"].isin(hab_order)].copy()
        fig3 = px.violin(
            df_box, x="hab_label", y="precio_noche",
            color="room_type",
            category_orders={"hab_label": hab_order},
            color_discrete_map={
                "Entire home/apt": SECONDARY,
                "Private room": ACCENT,
                "Shared room": "#7FB3D3",
            },
            box=True, points=False,
        )
        fig3 = fig_defaults(fig3, height=260)
        fig3.update_xaxes(title_text="Habitaciones")
        fig3.update_yaxes(title_text="Precio/noche (€)")
        st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PÁGINA 2 · ¿DÓNDE INVERTIR?
# ════════════════════════════════════════════════════════════
elif page == "🗺️  ¿Dónde invertir?":

    st.markdown('<div class="section-header">🗺️ ¿Dónde invertir? — Mapa de rentabilidad y atractivo turístico</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados.")
        st.stop()

    map_col, chart_col = st.columns([1.1, 1])

    with map_col:
        st.markdown('<p class="chart-label">Mapa de calor · Margen bruto por alojamiento</p>', unsafe_allow_html=True)

        m = folium.Map(
            location=[40.416, -3.703],
            zoom_start=11,
            tiles="CartoDB positron",
        )

        # Capa de calor (margen bruto)
        heat_data = df[["latitude", "longitude", "margen_bruto"]].dropna()
        heat_data = heat_data[
            (heat_data["latitude"].between(40.2, 40.65)) &
            (heat_data["longitude"].between(-3.95, -3.45))
        ]
        HeatMap(
            heat_data[["latitude", "longitude", "margen_bruto"]].values.tolist(),
            radius=12, blur=15, max_zoom=13,
            min_opacity=0.35,
            name="Calor: Margen bruto",
        ).add_to(m)

        # POIs
        poi_group = folium.FeatureGroup(name="Puntos de Interés", show=True)
        cat_colors = {
            "Monument": "red", "Museum": "purple", "Park": "green",
            "Shopping": "orange", "Transport": "blue", "Square": "darkblue",
            "Market": "cadetblue", "Cultural": "pink", "Sports": "darkgreen",
            "Neighborhood": "gray", "Attraction": "darkred",
            "Theater": "lightred", "Exhibition": "lightblue",
        }
        for _, row in poi_df.iterrows():
            color = cat_colors.get(row.get("category", ""), "gray")
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=5,
                color=color,
                fill=True, fill_opacity=0.8,
                tooltip=f"{row['name']} ({row.get('category','')})",
            ).add_to(poi_group)
        poi_group.add_to(m)
        folium.LayerControl().add_to(m)

        st_folium(m, width=None, height=400, returned_objects=[])

    with chart_col:
        st.markdown('<p class="chart-label">Rentabilidad vs. Demanda turística por distrito</p>', unsafe_allow_html=True)

        dist_agg = df.groupby("distrito").agg(
            margen=("margen_bruto", "median"),
            atractivo=("atractivo_turistico", "median"),
            n=("margen_bruto", "count"),
        ).reset_index()

        fig4 = px.scatter(
            dist_agg,
            x="atractivo", y="margen",
            size="n", size_max=36,
            text="distrito",
            color="margen",
            color_continuous_scale=[[0, "#BDD7EE"], [0.5, SECONDARY], [1, PRIMARY]],
            labels={
                "atractivo": "Atractivo turístico mediano",
                "margen": "Margen bruto mediano (%)",
                "n": "Nº alojamientos",
            },
        )
        fig4.update_traces(
            textposition="top center",
            textfont=dict(size=9, color=TEXT),
            marker=dict(line=dict(width=0.5, color="white")),
        )
        fig4 = fig_defaults(fig4, height=370)
        fig4.update_coloraxes(showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<p class="chart-label">Top 8 distritos — Margen bruto mediano</p>', unsafe_allow_html=True)
        top8 = dist_agg.nlargest(8, "margen").sort_values("margen", ascending=True)
        fig5 = go.Figure(go.Bar(
            x=top8["margen"],
            y=top8["distrito"],
            orientation="h",
            marker=dict(
                color=top8["margen"],
                colorscale=[[0, "#BDD7EE"], [1, PRIMARY]],
                showscale=False,
            ),
            text=top8["margen"].map("{:.1f}%".format),
            textposition="outside",
            textfont=dict(size=10, color=TEXT),
        ))
        fig5 = fig_defaults(fig5, height=280)
        fig5.update_xaxes(title_text="Margen bruto mediano (%)")
        st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PÁGINA 3 · ¿CUÁNTO GANARÉ?
# ════════════════════════════════════════════════════════════
elif page == "💰  ¿Cuánto ganaré?":

    st.markdown('<div class="section-header">💰 ¿Cuánto ganaré? — Estimación de rentabilidad por tipología</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados.")
        st.stop()

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<p class="chart-label">Ingreso anual mediano por tipo y habitaciones</p>', unsafe_allow_html=True)
        hab_order = ["0 hab.", "1 hab.", "2 hab.", "3 hab.", "4+ hab."]
        heatmap_data = (
            df[df["hab_label"].isin(hab_order)]
            .groupby(["room_type", "hab_label"])["ingreso_anual"]
            .median()
            .reset_index()
            .pivot(index="room_type", columns="hab_label", values="ingreso_anual")
            .reindex(columns=hab_order)
        )
        fig6 = go.Figure(go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns.tolist(),
            y=heatmap_data.index.tolist(),
            colorscale=[[0, "#EBF3FB"], [0.5, SECONDARY], [1, PRIMARY]],
            text=np.where(
                np.isnan(heatmap_data.values),
                "",
                [[f"€{v:,.0f}" for v in row] for row in heatmap_data.values],
            ),
            texttemplate="%{text}",
            textfont=dict(size=11, color="white"),
            showscale=True,
            colorbar=dict(
                title=dict(text="€/año", font=dict(size=11, color=TEXT)),
                tickfont=dict(size=10, color=TEXT),
                thickness=14,
            ),
        ))
        fig6 = fig_defaults(fig6, height=250)
        fig6.update_xaxes(title_text="Habitaciones", **AXIS_STYLE)
        fig6.update_yaxes(title_text="Tipo de alojamiento", **AXIS_STYLE)
        st.plotly_chart(fig6, use_container_width=True)

    with col_r:
        st.markdown('<p class="chart-label">Margen bruto mediano por tipo y habitaciones</p>', unsafe_allow_html=True)
        heatmap_mb = (
            df[df["hab_label"].isin(hab_order)]
            .groupby(["room_type", "hab_label"])["margen_bruto"]
            .median()
            .reset_index()
            .pivot(index="room_type", columns="hab_label", values="margen_bruto")
            .reindex(columns=hab_order)
        )
        fig7 = go.Figure(go.Heatmap(
            z=heatmap_mb.values,
            x=heatmap_mb.columns.tolist(),
            y=heatmap_mb.index.tolist(),
            colorscale=[[0, "#FFF3E0"], [0.5, ACCENT], [1, "#B84A00"]],
            text=np.where(
                np.isnan(heatmap_mb.values),
                "",
                [[f"{v:.1f}%" for v in row] for row in heatmap_mb.values],
            ),
            texttemplate="%{text}",
            textfont=dict(size=11, color="white"),
            showscale=True,
            colorbar=dict(
                title=dict(text="Margen %", font=dict(size=11, color=TEXT)),
                tickfont=dict(size=10, color=TEXT),
                thickness=14,
            ),
        ))
        fig7 = fig_defaults(fig7, height=250)
        fig7.update_xaxes(title_text="Habitaciones", **AXIS_STYLE)
        fig7.update_yaxes(title_text="Tipo de alojamiento", **AXIS_STYLE)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('<p class="chart-label">Coste de adquisición vs. Ingreso anual esperado · coloreado por margen bruto</p>', unsafe_allow_html=True)

    smp = df.sample(min(1500, len(df)), random_state=42)
    fig8 = px.scatter(
        smp,
        x="coste_adquisicion", y="ingreso_anual",
        color="margen_bruto",
        color_continuous_scale=[[0, "#BDD7EE"], [0.5, SECONDARY], [1, PRIMARY]],
        opacity=0.55,
        labels={
            "coste_adquisicion": "Coste de adquisición (€)",
            "ingreso_anual": "Ingreso anual estimado (€)",
            "margen_bruto": "Margen%",
        },
        hover_data={"distrito": True, "room_type": True, "margen_bruto": ":.1f"},
    )
    fig8 = fig_defaults(fig8, height=340)
    fig8.update_coloraxes(
        colorbar=dict(
            title=dict(text="Margen%", font=dict(size=11, color=TEXT)),
            tickfont=dict(size=10, color=TEXT),
            thickness=14,
        )
    )
    fig8.update_xaxes(title_text="Coste de adquisición (€)", tickformat=",.0f")
    fig8.update_yaxes(title_text="Ingreso anual estimado (€)", tickformat=",.0f")
    st.plotly_chart(fig8, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PÁGINA 4 · CONCLUSIONES
# ════════════════════════════════════════════════════════════
elif page == "🎯  Conclusiones":

    st.markdown('<div class="section-header">🎯 Conclusiones y recomendaciones de inversión</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados. Ajusta los filtros del sidebar.")
        st.stop()

    # ── Calcular top 3 distritos ─────────────────────────────
    dist_rank = (
        df.groupby("distrito")["margen_bruto"]
        .median()
        .reset_index()
        .sort_values("margen_bruto", ascending=False)
        .head(3)
    )
    medal_styles  = ["rec-gold", "rec-silver", "rec-bronze"]
    medal_emojis  = ["🥇", "🥈", "🥉"]
    medal_labels  = ["Mejor opción", "2ª opción", "3ª opción"]

    st.markdown("#### 🏆 Top 3 distritos más rentables (con los filtros actuales)")
    cols = st.columns(3)
    for i, (_, row) in enumerate(dist_rank.iterrows()):
        n_in_dist = len(df[df["distrito"] == row["distrito"]])
        cols[i].markdown(f"""
        <div class="{medal_styles[i]}">
            <div class="rec-medal">{medal_emojis[i]}</div>
            <div class="rec-title">{row['distrito']}</div>
            <div class="rec-value">{row['margen_bruto']:.1f}%</div>
            <div class="rec-sub">{medal_labels[i]} · {n_in_dist} alojamientos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráfico top 5 ────────────────────────────────────────
    st.markdown("#### 📊 Comparativa de rentabilidad — Top 5 distritos")
    top5 = (
        df.groupby("distrito")["margen_bruto"]
        .median()
        .nlargest(5)
        .reset_index()
        .sort_values("margen_bruto", ascending=True)
    )
    fig_c = go.Figure(go.Bar(
        x=top5["margen_bruto"],
        y=top5["distrito"],
        orientation="h",
        marker_color=[GOLD if i == len(top5)-1 else SECONDARY for i in range(len(top5))],
        text=top5["margen_bruto"].map("{:.1f}%".format),
        textposition="outside",
        textfont=dict(size=11, color=TEXT),
    ))
    fig_c = fig_defaults(fig_c, height=230)
    fig_c.update_xaxes(title_text="Margen bruto mediano (%)")
    st.plotly_chart(fig_c, use_container_width=True)

    # ── 4 insights ───────────────────────────────────────────
    st.markdown("#### 💡 Hallazgos clave del análisis")

    # Mejor tipología
    best_type = (
        df.groupby(["room_type", "hab_label"])["margen_bruto"]
        .median()
        .idxmax()
    )
    best_mb = df.groupby(["room_type", "hab_label"])["margen_bruto"].median().max()

    # Correlación ocupación-atractivo
    corr_val = df["estimated_occupancy_l365d"].corr(df["atractivo_turistico"])

    # Ingreso mediano top distrito
    top1_name  = dist_rank.iloc[0]["distrito"]
    top1_ing   = df[df["distrito"] == top1_name]["ingreso_anual"].median()
    global_ing = df["ingreso_anual"].median()
    pct_mejor  = (top1_ing / global_ing - 1) * 100

    # Precio/noche top vs global
    top1_precio = df[df["distrito"] == top1_name]["precio_noche"].median()

    insights = [
        ("🏡", f"La tipología <strong>{best_type[0]}</strong> con <strong>{best_type[1]}</strong> ofrece el mayor margen bruto mediano: <strong>{best_mb:.1f}%</strong>. Apostar por pisos completos de 1-2 habitaciones es la estrategia más rentable."),
        ("📍", f"El distrito <strong>{top1_name}</strong> es el más rentable con los filtros actuales, con ingresos anuales medianos de <strong>€{top1_ing:,.0f}</strong> — un <strong>{pct_mejor:+.0f}%</strong> sobre la media general de €{global_ing:,.0f}."),
        ("🗺️", f"La correlación entre atractivo turístico (POIs cercanos) y ocupación es de <strong>r = {corr_val:.3f}</strong>. La proximidad a monumentos y transporte influye moderadamente en la demanda, pero no es el único factor."),
        ("💶", f"El precio/noche mediano en <strong>{top1_name}</strong> es de <strong>€{top1_precio:.0f}</strong>, frente a los €{df['precio_noche'].median():.0f} de la media global. Un precio diferencial que refleja la mayor demanda de la zona."),
    ]

    for icon, text in insights:
        st.markdown(
            f'<div class="insight-box"><span class="i-icon">{icon}</span>{text}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Perfil óptimo de inversión ────────────────────────────
    st.markdown("#### 🎯 Perfil óptimo de inversión (selección actual)")

    best_overall = (
        df.groupby(["distrito", "room_type", "hab_label"])
        .agg(margen=("margen_bruto", "median"), n=("margen_bruto", "count"))
        .query("n >= 5")
        .sort_values("margen", ascending=False)
        .head(1)
    )

    if not best_overall.empty:
        bo = best_overall.iloc[0]
        bo_dist, bo_room, bo_hab = bo.name
        bo_margen  = bo["margen"]
        bo_ingreso = df[
            (df["distrito"] == bo_dist) &
            (df["room_type"] == bo_room) &
            (df["hab_label"] == bo_hab)
        ]["ingreso_anual"].median()
        bo_coste = df[
            (df["distrito"] == bo_dist) &
            (df["room_type"] == bo_room) &
            (df["hab_label"] == bo_hab)
        ]["coste_adquisicion"].median()

        st.markdown(f"""
        <div class="profile-box">
            <h3>✅ Combinación con mayor margen bruto mediano (mín. 5 casos)</h3>
            <div class="profile-item"><span class="label">📍 Distrito</span><span class="val">{bo_dist}</span></div>
            <div class="profile-item"><span class="label">🏠 Tipo de alojamiento</span><span class="val">{bo_room}</span></div>
            <div class="profile-item"><span class="label">🛏️ Habitaciones</span><span class="val">{bo_hab}</span></div>
            <div class="profile-item"><span class="label">💰 Margen bruto mediano</span><span class="val">{bo_margen:.1f}%</span></div>
            <div class="profile-item"><span class="label">📈 Ingreso anual mediano</span><span class="val">€{bo_ingreso:,.0f}</span></div>
            <div class="profile-item"><span class="label">🏦 Coste adquisición mediano</span><span class="val">€{bo_coste:,.0f}</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Amplía los filtros para ver el perfil óptimo (se necesitan mínimo 5 casos por combinación).")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Cierre narrativo ─────────────────────────────────────
    st.markdown("""
    <div class="method-box">
        <h4>📝 Reflexión final</h4>
        <p>El mercado de alquiler vacacional en Madrid presenta oportunidades heterogéneas según el distrito. Los distritos periféricos y emergentes (como Villa de Vallecas o Barajas) ofrecen márgenes más elevados al combinar costes de adquisición moderados con una ocupación turística creciente.</p>
        <p>Sin embargo, el margen bruto es solo una de las métricas a considerar: la liquidez del mercado inmobiliario, la regulación local sobre alquiler vacacional y la diversificación del riesgo son factores igual de importantes para una inversión responsable.</p>
        <p><b>Esta herramienta no constituye asesoramiento financiero.</b> Los datos son orientativos y deben complementarse con análisis legales y de mercado actualizados.</p>
    </div>
    """, unsafe_allow_html=True)
