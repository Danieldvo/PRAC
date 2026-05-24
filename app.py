"""
Inversión Inmobiliaria Madrid · Análisis Airbnb
PRAC2 – Visualización de Datos · Máster Data Science
3 páginas: Resumen · ¿Dónde? · ¿Cuánto?
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Madrid Airbnb · Inversión Inmobiliaria",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY   = "#1A3A5C"
SECONDARY = "#2E6DA4"
ACCENT    = "#E87722"
TEXT      = "#2C2C2C"

ROOM_COLORS = {
    "Entire home/apt": PRIMARY,
    "Private room":    SECONDARY,
    "Shared room":     ACCENT,
}

st.markdown(f"""
<style>
[data-testid="stSidebar"] {{
    background-color: {PRIMARY};
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {{
    color: rgba(255,255,255,0.85) !important;
}}
[data-testid="stSidebar"] .stRadio > label {{
    color: rgba(255,255,255,0.6) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.kpi-card {{
    background: white;
    border-radius: 12px;
    padding: 18px 16px 14px;
    border-top: 4px solid {ACCENT};
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    text-align: center;
}}
.kpi-val {{
    font-size: 28px;
    font-weight: 700;
    color: {PRIMARY};
    line-height: 1.1;
}}
.kpi-lbl {{
    font-size: 11px;
    color: #888;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}}
.sec {{
    font-size: 12px;
    font-weight: 600;
    color: {PRIMARY};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 2px solid {ACCENT};
    padding-bottom: 4px;
    margin: 16px 0 10px;
}}
.page-title {{
    font-size: 22px;
    font-weight: 800;
    color: {PRIMARY};
    margin-bottom: 2px;
}}
.page-sub {{
    font-size: 13px;
    color: #888;
    margin-bottom: 18px;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATOS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Cargando datos…")
def load_data():
    base = Path(__file__).parent / "data"
    conn = sqlite3.connect(str(base / "mercado_inmobiliario.db"))
    df   = pd.read_sql("SELECT * FROM tablon_analitico", conn)
    conn.close()
    poi  = pd.read_csv(base / "poi_madrid.csv")

    df = df.dropna(subset=["margen_bruto", "precio_noche", "ingreso_anual",
                            "latitude", "longitude", "neighbourhood", "distrito"])
    # Eliminar filas con neighbourhood o distrito vacíos/inválidos
    df = df[df["neighbourhood"].str.strip().ne("")]
    df = df[df["distrito"].str.strip().ne("")]
    for col in ["margen_bruto", "precio_noche", "ingreso_anual", "coste_adquisicion"]:
        df[col] = df[col].clip(upper=df[col].quantile(0.99))

    hab_map = {"0_hab": "0 hab.", "1_hab": "1 hab.", "2_hab": "2 hab.",
               "3_hab": "3 hab.", "4+_hab": "4+ hab."}
    df["hab_label"] = df["bedrooms_disc"].map(hab_map)
    return df, poi


df_full, poi = load_data()

PLOTLY_CFG = {"displayModeBar": False}

AXIS_STYLE = dict(
    tickfont=dict(size=11, color="#222222", family="Arial, sans-serif"),
    title_font=dict(size=12, color="#222222", family="Arial, sans-serif"),
    showgrid=True, gridcolor="#E8E8E8",
    linecolor="#CCCCCC", linewidth=1,
)

def fig_defaults(fig, height=320):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", color="#222222", size=11),
        height=height,
        margin=dict(l=10, r=10, t=6, b=36),
        # ← Esto elimina el "undefined" que aparecía como título vacío
        title=dict(text="", font=dict(color=PRIMARY, size=13)),
        legend=dict(
            font=dict(size=11, color="#222222"),
            title_font=dict(size=11, color="#333333"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#DDDDDD",
            borderwidth=0.5,
        ),
        coloraxis_colorbar=dict(
            title_font=dict(size=11, color="#222222"),
            tickfont=dict(size=10, color="#222222"),
            thickness=14,
        ),
    )
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

def kpi(label, value):
    return (f"<div class='kpi-card'>"
            f"<div class='kpi-val'>{value}</div>"
            f"<div class='kpi-lbl'>{label}</div></div>")

def sec(t):
    st.markdown(f"<div class='sec'>{t}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:4px 0 12px'>"
        "<span style='font-size:32px'>🏠</span><br>"
        "<span style='font-size:16px;font-weight:700;color:white'>Madrid Airbnb</span><br>"
        "<span style='font-size:11px;color:rgba(255,255,255,0.6)'>Análisis de Inversión</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:0 0 10px'>",
                unsafe_allow_html=True)

    page = st.radio("Navegación", [
        "🏠  Resumen",
        "🗺️  ¿Dónde invertir?",
        "💰  ¿Cuánto ganaré?",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:10px 0'>",
                unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px'>Filtros globales</p>",
                unsafe_allow_html=True)

    distritos_all = sorted(df_full["distrito"].unique())
    sel_dist = st.multiselect("Distrito", distritos_all, default=distritos_all,
                              placeholder="Todos…")

    rooms_all = sorted(df_full["room_type"].unique())
    sel_rooms = st.multiselect("Tipo", rooms_all, default=rooms_all,
                               placeholder="Todos…")

    hab_all = ["0 hab.", "1 hab.", "2 hab.", "3 hab.", "4+ hab."]
    sel_hab = st.multiselect("Habitaciones", hab_all, default=hab_all,
                             placeholder="Todas…")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:10px 0'>",
                unsafe_allow_html=True)
    st.caption("Datos: Inside Airbnb · Idealista · POI Madrid")


# Filtrado
df = df_full.copy()
if sel_dist:  df = df[df["distrito"].isin(sel_dist)]
if sel_rooms: df = df[df["room_type"].isin(sel_rooms)]
if sel_hab:   df = df[df["hab_label"].isin(sel_hab)]

if df.empty:
    st.warning("Sin datos con los filtros actuales. Amplía la selección.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 · RESUMEN
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Resumen":
    st.markdown("<div class='page-title'>🏠 Resumen del mercado</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='page-sub'>{len(df):,} inmuebles · "
        f"{df['distrito'].nunique()} distritos · "
        f"{df['neighbourhood'].nunique()} barrios</div>",
        unsafe_allow_html=True,
    )

    # ── KPIs ──────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi("Margen bruto medio",
                    f"{df['margen_bruto'].mean():.1f}%"), unsafe_allow_html=True)
    c2.markdown(kpi("Precio / noche medio",
                    f"€{df['precio_noche'].mean():.0f}"), unsafe_allow_html=True)
    c3.markdown(kpi("Ingreso anual medio",
                    f"€{df['ingreso_anual'].mean()/1000:.1f}K"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráfico 1: Top 8 barrios por margen bruto ─────────────────────────────
    col_a, col_b = st.columns([1.4, 0.6])

    with col_a:
        sec("Top 8 barrios · margen bruto medio")
        top8 = (df.groupby("neighbourhood")["margen_bruto"]
                .mean().nlargest(8).sort_values().reset_index())
        fig1 = px.bar(
            top8, x="margen_bruto", y="neighbourhood", orientation="h",
            color="margen_bruto", color_continuous_scale="Blues",
            text="margen_bruto",
            labels={"margen_bruto": "Margen bruto (%)", "neighbourhood": ""},
        )
        fig1.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            textfont=dict(color=PRIMARY, size=12, family="Arial Black"),
        )
        fig1.update_layout(coloraxis_showscale=False)
        fig_defaults(fig1, height=310)
        st.plotly_chart(fig1, use_container_width=True, config=PLOTLY_CFG)

    # ── Gráfico 2: Donut por tipo de alojamiento ──────────────────────────────
    with col_b:
        sec("Distribución por tipo")
        pie = df["room_type"].value_counts().reset_index()
        pie.columns = ["room_type", "count"]
        fig2 = px.pie(
            pie, values="count", names="room_type",
            color="room_type", color_discrete_map=ROOM_COLORS,
            hole=0.45,
        )
        fig2.update_traces(
            textinfo="percent+label",
            textfont=dict(size=11, color="#222222"),
            pull=[0.04, 0, 0],
        )
        fig2.update_layout(
            showlegend=False,
            plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text=""),
            height=310, margin=dict(l=10, r=10, t=6, b=10),
            font=dict(family="Arial, sans-serif", color="#222222", size=11),
        )
        st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CFG)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 · ¿DÓNDE INVERTIR?
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️  ¿Dónde invertir?":
    st.markdown("<div class='page-title'>🗺️ ¿Dónde invertir?</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Distribución geográfica y ranking de distritos</div>",
                unsafe_allow_html=True)

    # ── Controles ─────────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([1.2, 1, 0.8])
    with ctrl1:
        metrica_map = st.selectbox("Métrica en el mapa", [
            "Margen bruto (%)",
            "Precio / noche (€)",
            "Ocupación (días/año)",
            "Ingreso anual (€)",
        ])
    with ctrl2:
        vista = st.radio("Vista", ["🔥 Mapa de calor", "⭕ Círculos por barrio"],
                         horizontal=True)
    with ctrl3:
        show_poi = st.checkbox("Mostrar POIs", value=True)

    col_map = {
        "Margen bruto (%)":     "margen_bruto",
        "Precio / noche (€)":   "precio_noche",
        "Ocupación (días/año)": "estimated_occupancy_l365d",
        "Ingreso anual (€)":    "ingreso_anual",
    }[metrica_map]

    # Agregado por barrio
    barrio = (df.groupby("neighbourhood").agg(
        lat=("latitude", "mean"), lon=("longitude", "mean"),
        valor=(col_map, "mean"), count=("precio_noche", "count"),
        distrito=("distrito", "first"),
    ).reset_index())

    # ── Mapa Folium ────────────────────────────────────────────────────────────
    m = folium.Map(location=[40.416, -3.703], zoom_start=11,
                   tiles="CartoDB positron", control_scale=True)

    if "calor" in vista:
        heat = [[r.latitude, r.longitude, r[col_map]]
                for _, r in df.iterrows() if pd.notna(r[col_map])]
        HeatMap(heat, min_opacity=0.3, radius=14, blur=18,
                gradient={0.2: SECONDARY, 0.6: ACCENT, 1.0: "#C0392B"}).add_to(m)
    else:
        import branca.colormap as cm
        vmin = barrio["valor"].quantile(0.05)
        vmax = barrio["valor"].quantile(0.95)
        cmap = cm.LinearColormap([SECONDARY, ACCENT], vmin=vmin, vmax=vmax,
                                  caption=metrica_map)
        cmap.add_to(m)
        for _, r in barrio.iterrows():
            color = cmap(float(np.clip(r["valor"], vmin, vmax)))
            radio = 5 + (r["count"] / barrio["count"].max()) * 18
            folium.CircleMarker(
                location=[r["lat"], r["lon"]], radius=radio,
                color="white", weight=1,
                fill=True, fill_color=color, fill_opacity=0.78,
                tooltip=folium.Tooltip(
                    f"<b>{r['neighbourhood']}</b><br>"
                    f"{r['distrito']}<br>"
                    f"{metrica_map}: <b>{r['valor']:.1f}</b><br>"
                    f"Inmuebles: {int(r['count'])}"
                ),
            ).add_to(m)

    if show_poi:
        poi_layer = folium.FeatureGroup(name="POIs")
        for _, r in poi.iterrows():
            folium.Marker(
                location=[r["lat"], r["lon"]],
                tooltip=f"<b>{r['name']}</b><br>{r['category']}",
                icon=folium.Icon(color="darkblue", icon="info-sign", prefix="glyphicon"),
            ).add_to(poi_layer)
        poi_layer.add_to(m)
        folium.LayerControl().add_to(m)

    st_folium(m, use_container_width=True, height=430, returned_objects=[])

    # ── Gráfico 3: Ranking de distritos (métrica seleccionable) ───────────────
    sec("Ranking de distritos · " + metrica_map.lower())
    dist_rank = (df.groupby("distrito")[col_map]
                 .mean().sort_values(ascending=True).reset_index())
    fig3 = px.bar(
        dist_rank, x=col_map, y="distrito", orientation="h",
        color=col_map, color_continuous_scale="Blues",
        text=col_map,
        labels={col_map: metrica_map, "distrito": ""},
    )
    suffix = "%" if "bruto" in metrica_map else ""
    prefix = "€" if "€" in metrica_map else ""
    fig3.update_traces(
        texttemplate=f"{prefix}%{{text:.1f}}{suffix}",
        textposition="outside",
        textfont=dict(color=PRIMARY, size=11, family="Arial Black"),
    )
    fig3.update_layout(coloraxis_showscale=False)
    fig_defaults(fig3, height=380)
    st.plotly_chart(fig3, use_container_width=True, config=PLOTLY_CFG)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 · ¿CUÁNTO GANARÉ?
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰  ¿Cuánto ganaré?":
    st.markdown("<div class='page-title'>💰 ¿Cuánto ganaré?</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>Rentabilidad según tipología, ubicación y coste de adquisición</div>",
        unsafe_allow_html=True,
    )

    # ── Gráfico 4 + 5: Heatmap y Scatter en columnas ─────────────────────────
    col_a, col_b = st.columns([1, 1.35])

    with col_a:
        sec("Margen bruto medio · tipo × habitaciones")
        hm = (df.groupby(["room_type", "hab_label"])["margen_bruto"]
              .mean().reset_index())
        pivot = hm.pivot(index="room_type", columns="hab_label",
                         values="margen_bruto")
        col_order = [c for c in ["0 hab.", "1 hab.", "2 hab.", "3 hab.", "4+ hab."]
                     if c in pivot.columns]
        pivot = pivot[col_order]

        fig4 = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale="Blues",
            text=np.round(pivot.values, 1),
            texttemplate="%{text:.1f}%",
            textfont=dict(size=13, color="#111111"),
            colorbar=dict(
                title=dict(text="Margen %", font=dict(size=11, color="#222222")),
                tickfont=dict(size=10, color="#222222"),
                thickness=12, len=0.8,
            ),
        ))
        fig4.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text=""),
            height=260, margin=dict(l=10, r=10, t=6, b=36),
            font=dict(family="Arial, sans-serif", color="#222222", size=11),
        )
        fig4.update_xaxes(
            title_text="Habitaciones",
            **AXIS_STYLE,
        )
        fig4.update_yaxes(**AXIS_STYLE)
        st.plotly_chart(fig4, use_container_width=True, config=PLOTLY_CFG)

    # ── Gráfico 5: Scatter ocupación vs atractivo turístico ───────────────────
    with col_b:
        sec("Ocupación vs. atractivo turístico (por barrio)")
        barrio_occ = (df.groupby("neighbourhood").agg(
            ocupacion=("estimated_occupancy_l365d", "mean"),
            atractivo=("atractivo_turistico", "mean"),
            count=("precio_noche", "count"),
            distrito=("distrito", "first"),
        ).reset_index())

        fig5 = px.scatter(
            barrio_occ, x="atractivo", y="ocupacion",
            size="count", color="distrito",
            hover_name="neighbourhood",
            hover_data={"count": True, "atractivo": ":.1f", "ocupacion": ":.0f"},
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                "atractivo": "Índice de atractivo turístico",
                "ocupacion": "Ocupación media (días/año)",
                "count": "Inmuebles", "distrito": "Distrito",
            },
            opacity=0.85,
        )
        # Línea de tendencia
        z = np.polyfit(barrio_occ["atractivo"], barrio_occ["ocupacion"], 1)
        x_t = np.linspace(barrio_occ["atractivo"].min(),
                          barrio_occ["atractivo"].max(), 80)
        fig5.add_trace(go.Scatter(
            x=x_t, y=np.polyval(z, x_t), mode="lines",
            name="Tendencia", showlegend=False,
            line=dict(color=ACCENT, width=2, dash="dash"),
        ))
        fig5.update_layout(
            legend=dict(
                title="Distrito",
                font=dict(size=9),
                itemsizing="constant",
                tracegroupgap=2,
                x=1.01, y=1,
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#DDDDDD",
                borderwidth=0.5,
            )
        )
        fig_defaults(fig5, height=260)
        st.plotly_chart(fig5, use_container_width=True, config=PLOTLY_CFG)

    # ── Gráfico 6: Scatter coste vs ingreso (coloreado por margen) ────────────
    sec("Coste de adquisición vs. ingreso anual esperado · coloreado por margen bruto")
    sample = df.sample(min(2500, len(df)), random_state=42)
    fig6 = px.scatter(
        sample,
        x="coste_adquisicion", y="ingreso_anual",
        color="margen_bruto", color_continuous_scale="RdYlGn",
        size="margen_bruto", size_max=14,
        opacity=0.55,
        hover_data=["neighbourhood", "room_type", "distrito", "bedrooms_disc"],
        labels={
            "coste_adquisicion": "Coste de adquisición (€)",
            "ingreso_anual": "Ingreso anual estimado (€)",
            "margen_bruto": "Margen bruto (%)",
        },
    )
    fig6.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text="Margen %", font=dict(size=12, color="#222222")),
            tickfont=dict(size=11, color="#222222"),
            thickness=14, len=0.7,
        )
    )
    fig_defaults(fig6, height=340)
    st.plotly_chart(fig6, use_container_width=True, config=PLOTLY_CFG)
