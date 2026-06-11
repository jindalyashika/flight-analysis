import streamlit as st
import psycopg2
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="✈️ Flight Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* ── Background ── */
.stApp {
    background: linear-gradient(150deg, #f5f3ff 0%, #ede9fe 40%, #e0e7ff 75%, #f0f9ff 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    width: 240px !important;
    min-width: 240px !important;
    background: rgba(255,255,255,0.60) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    border-right: 1px solid rgba(139,92,246,0.15) !important;
    box-shadow: 4px 0 30px rgba(109,40,217,0.08) !important;
}
[data-testid="stSidebar"] * { color: #3b0764 !important; }
[data-testid="stSidebar"] .stSelectbox label {
    color: #7c3aed !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.8px !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(139,92,246,0.25) !important;
    border-radius: 12px !important;
    color: #3b0764 !important;
}

/* ── Collapse arrow ── */
[data-testid="stSidebarCollapseButton"] {
    position: fixed !important;
    top: 50% !important;
    left: 240px !important;
    transform: translateY(-50%) !important;
    z-index: 9999 !important;
}
[data-testid="stSidebarCollapseButton"] button {
    width: 28px !important;
    height: 56px !important;
    background: rgba(167,139,250,0.25) !important;
    border: 1px solid rgba(139,92,246,0.35) !important;
    border-left: none !important;
    border-radius: 0 14px 14px 0 !important;
    color: #5b21b6 !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 4px 0 16px rgba(109,40,217,0.15) !important;
    transition: background 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    background: rgba(167,139,250,0.45) !important;
}
[data-testid="stSidebarCollapseButton"] button svg {
    width: 14px !important;
    height: 14px !important;
    stroke: #5b21b6 !important;
}

/* ── Main container ── */
[data-testid="stMainBlockContainer"] {
    padding: 1.5rem 2.5rem 2.5rem 2.5rem !important;
    max-width: 1300px !important;
    margin: 0 auto !important;
}

/* ── Glass card ── */
.glass {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(139,92,246,0.18);
    border-radius: 24px;
    padding: 28px 28px 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 8px 32px rgba(109,40,217,0.08), inset 0 1px 0 rgba(255,255,255,0.8);
}

/* ── KPI Grid ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 22px;
}
.kpi-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(139,92,246,0.20);
    border-radius: 20px;
    padding: 22px 14px 18px 14px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(109,40,217,0.08), inset 0 1px 0 rgba(255,255,255,0.9);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #a78bfa, #818cf8, #c4b5fd);
    border-radius: 20px 20px 0 0;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 36px rgba(109,40,217,0.14), inset 0 1px 0 rgba(255,255,255,1);
}
.kpi-icon  { font-size: 1.8rem; display: block; margin-bottom: 10px; }
.kpi-value { font-size: 1.5rem; font-weight: 800; color: #3b0764; line-height: 1.1; }
.kpi-label { font-size: 0.65rem; color: #7c3aed; text-transform: uppercase; letter-spacing: 2px; margin-top: 7px; font-weight: 700; }

/* ── Section titles ── */
.section-title { font-size: 1.05rem; font-weight: 700; color: #3b0764; margin-bottom: 2px; }
.section-sub   { font-size: 0.76rem; color: #7c3aed; margin-bottom: 16px; }

/* ── Insight pills ── */
.pill {
    display: inline-block;
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 50px;
    padding: 6px 15px;
    font-size: 0.78rem;
    color: #4c1d95;
    font-weight: 600;
    margin: 4px 3px;
}

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 24px 0 32px 0;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    color: #2e1065;
    letter-spacing: -1.5px;
    margin-bottom: 8px;
    line-height: 1.1;
}
.hero-accent {
    background: linear-gradient(90deg, #7c3aed, #4f46e5, #0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #7c3aed;
    font-size: 0.8rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-weight: 600;
}

/* ── Divider ── */
hr { border-color: rgba(139,92,246,0.12) !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 16px !important; overflow: hidden !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: rgba(167,139,250,0.08); }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.25); border-radius: 10px; }

/* ── Plotly modebar ── */
.js-plotly-plot .plotly .modebar {
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Chart layout helper — light theme ──
def base_layout(h=360, extra_margin=None):
    m = extra_margin or dict(t=20, b=20, l=20, r=20)
    return dict(
        paper_bgcolor="rgba(0,0,0,0.0)",
        plot_bgcolor="rgba(0,0,0,0.0)",
        font=dict(color="#4c1d95", family="Inter"),
        height=h,
        margin=m,
        xaxis=dict(
            gridcolor="rgba(139,92,246,0.10)",
            color="#7c3aed",
            linecolor="rgba(139,92,246,0.15)",
            showgrid=True,
            zerolinecolor="rgba(139,92,246,0.10)"
        ),
        yaxis=dict(
            gridcolor="rgba(139,92,246,0.10)",
            color="#7c3aed",
            linecolor="rgba(139,92,246,0.15)",
            showgrid=True,
            zerolinecolor="rgba(139,92,246,0.10)"
        ),
        showlegend=False,
    )


# Lavender palette — deep enough to read on white cards
LAV_COLORS = ["#7c3aed", "#6366f1", "#0ea5e9", "#8b5cf6", "#06b6d4", "#a78bfa", "#818cf8"]


@st.cache_data
def get_data(query):
    creds = st.secrets["postgres"]
    conn = psycopg2.connect(
        host=creds["host"],
        database=creds["database"],
        user=creds["user"],
        password=creds["password"],
        port=creds["port"]
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
        <div style='
            padding: 20px 4px 20px 4px;
            border-bottom: 1px solid rgba(139,92,246,0.15);
            margin-bottom: 20px;
            text-align: center;
        '>
            <div style='
                width:52px; height:52px; border-radius:50%;
                background: linear-gradient(135deg,#ede9fe,#ddd6fe);
                border: 1.5px solid rgba(139,92,246,0.3);
                display:inline-flex; align-items:center; justify-content:center;
                font-size:1.5rem; margin-bottom:10px;
            '>✈️</div>
            <p style='font-size:0.95rem;font-weight:800;margin:0 0 4px 0;color:#3b0764;letter-spacing:0.3px;'>Flight Analytics</p>
            <p style='font-size:0.62rem;color:#7c3aed;margin:0;letter-spacing:3px;text-transform:uppercase;font-weight:600;'>Indian Aviation</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p style='color:#a78bfa;font-size:0.62rem;letter-spacing:2.5px;
                  text-transform:uppercase;font-weight:700;margin-bottom:14px;padding-left:2px;'>
            🎛&nbsp; Filters
        </p>
    """, unsafe_allow_html=True)

    airlines = get_data("SELECT DISTINCT airline_name FROM dim_airline ORDER BY airline_name")
    selected_airline = st.selectbox("✈️ Airline", ["All"] + airlines["airline_name"].drop_duplicates().tolist())

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    selected_class = st.selectbox("💺 Class", ["All", "Economy", "Business"])

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    cities = get_data("SELECT DISTINCT city_name FROM dim_city ORDER BY city_name")
    selected_city = st.selectbox("🏙 Source City", ["All"] + cities["city_name"].drop_duplicates().tolist())

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='border-top:1px solid rgba(139,92,246,0.12);padding-top:14px;text-align:center;'>
            <p style='color:#c4b5fd;font-size:0.65rem;letter-spacing:1.5px;margin:0;'>
                Built by<br>
                <span style='color:#7c3aed;font-weight:700;letter-spacing:0.5px;'>Yashika Jindal 🚀</span>
            </p>
        </div>
    """, unsafe_allow_html=True)


# ── Hero ──
st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">✈️ <span class="hero-accent">Flight Price</span> Analytics</div>
        <div class="hero-sub">Indian Aviation &nbsp;•&nbsp; 49K+ Flights &nbsp;•&nbsp; Real Insights</div>
    </div>
""", unsafe_allow_html=True)


# ── KPI Cards ──
total  = get_data("SELECT COUNT(*) as cnt FROM fact_flights")
avg_p  = get_data("SELECT ROUND(AVG(price),0) as avg FROM fact_flights")
cheap  = get_data("SELECT MIN(price) as mn FROM fact_flights")
costl  = get_data("SELECT MAX(price) as mx FROM fact_flights")
routes = get_data("SELECT COUNT(DISTINCT source_city_id::text || '-' || destination_city_id::text) as cnt FROM fact_flights")

kpis = [
    ("🛫", f"{total['cnt'][0]:,}",        "Total Flights"),
    ("💰", f"₹{int(avg_p['avg'][0]):,}",  "Avg Price"),
    ("🤑", f"₹{cheap['mn'][0]:,}",        "Cheapest"),
    ("💸", f"₹{int(costl['mx'][0]):,}",   "Costliest"),
    ("🗺️", f"{routes['cnt'][0]}",         "Total Routes"),
]

kpi_html = '<div class="kpi-grid">'
for icon, value, label in kpis:
    kpi_html += f'''
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)


# ── Chart 1 — Airline-wise Average Price ──
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<p class="section-title">💜 Airline-wise Average Price</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Which airline gives the best deal?</p>', unsafe_allow_html=True)

airline_df = get_data("""
    SELECT a.airline_name, ROUND(AVG(f.price),0) AS avg_price, COUNT(*) AS total_flights
    FROM fact_flights f JOIN dim_airline a ON f.airline_id = a.airline_id
    GROUP BY a.airline_name ORDER BY avg_price ASC
""")

fig1 = go.Figure(go.Bar(
    x=airline_df["airline_name"],
    y=airline_df["avg_price"],
    marker=dict(
        color=LAV_COLORS[:len(airline_df)],
        opacity=0.88,
        line=dict(color="rgba(255,255,255,0.6)", width=1.5)
    ),
    text=[f"₹{int(p):,}" for p in airline_df["avg_price"]],
    textposition="outside",
    textfont=dict(color="#4c1d95", size=11, family="Inter"),
    hovertemplate="<b>%{x}</b><br>Avg Price: ₹%{y:,}<extra></extra>"
))
l1 = base_layout(360)
l1["bargap"] = 0.38
fig1.update_layout(**l1)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
    <div>
        <span class="pill">🥇 AirAsia = Best Budget Pick</span>
        <span class="pill">💸 Vistara = Most Premium</span>
        <span class="pill">📊 6x Price Gap</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Charts 2 + 3 ──
col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">🕐 Best Time to Fly</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">When should you book for cheaper flights?</p>', unsafe_allow_html=True)

    time_df = get_data("""
        SELECT t.time_label, ROUND(AVG(f.price),0) AS avg_price, COUNT(*) AS total_flights
        FROM fact_flights f JOIN dim_time t ON f.time_id = t.time_id
        GROUP BY t.time_label ORDER BY avg_price ASC
    """)

    fig2 = go.Figure(go.Bar(
        x=time_df["time_label"],
        y=time_df["avg_price"],
        marker=dict(
            color=["#7c3aed", "#6366f1", "#0ea5e9", "#8b5cf6"],
            opacity=0.88,
            line=dict(color="rgba(255,255,255,0.6)", width=1.5)
        ),
        text=[f"₹{int(p):,}" for p in time_df["avg_price"]],
        textposition="outside",
        textfont=dict(color="#4c1d95", size=11),
        hovertemplate="<b>%{x}</b><br>₹%{y:,}<extra></extra>"
    ))
    l2 = base_layout(300)
    l2["bargap"] = 0.42
    fig2.update_layout(**l2)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<span class="pill">🌙 Night flights = 37% cheaper than Evening!</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">💺 Economy vs Business</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">How much extra does comfort cost?</p>', unsafe_allow_html=True)

    class_df = get_data("""
        SELECT c.class_name, ROUND(AVG(f.price),0) AS avg_price
        FROM fact_flights f JOIN dim_class c ON f.class_id = c.class_id
        GROUP BY c.class_name
    """)

    fig3 = go.Figure(go.Pie(
        labels=class_df["class_name"],
        values=class_df["avg_price"],
        hole=0.62,
        marker=dict(
            colors=["#a78bfa", "#6366f1"],
            line=dict(color="rgba(255,255,255,0.8)", width=3)
        ),
        textfont=dict(color="#3b0764", size=13),
        hovertemplate="<b>%{label}</b><br>Avg: ₹%{value:,}<extra></extra>"
    ))
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0.0)",
        plot_bgcolor="rgba(0,0,0,0.0)",
        font=dict(color="#4c1d95", family="Inter"),
        height=300,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            font=dict(color="#4c1d95", size=12),
            bgcolor="rgba(255,255,255,0.6)",
            bordercolor="rgba(139,92,246,0.2)",
            borderwidth=1
        ),
        annotations=[dict(
            text="<b>6x</b><br>costlier",
            x=0.5, y=0.5,
            font=dict(size=17, color="#3b0764"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<span class="pill">💸 Business = 6x Economy price</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Chart 4 — Top 10 Busiest Routes ──
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🗺️ Top 10 Busiest Routes</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Most popular flight routes in India — color = avg price</p>', unsafe_allow_html=True)

route_df = get_data("""
    SELECT s.city_name || ' → ' || d.city_name AS route,
           COUNT(*) AS total_flights, ROUND(AVG(f.price),0) AS avg_price
    FROM fact_flights f
    JOIN dim_city s ON f.source_city_id = s.city_id
    JOIN dim_city d ON f.destination_city_id = d.city_id
    GROUP BY s.city_name, d.city_name
    ORDER BY total_flights DESC LIMIT 10
""")

fig4 = go.Figure(go.Bar(
    y=route_df["route"],
    x=route_df["total_flights"],
    orientation="h",
    marker=dict(
        color=route_df["avg_price"],
        colorscale=[[0, "#c4b5fd"], [0.5, "#818cf8"], [1, "#4c1d95"]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Avg ₹", font=dict(color="#4c1d95", size=11)),
            tickfont=dict(color="#7c3aed", size=10),
            bgcolor="rgba(255,255,255,0.5)",
            bordercolor="rgba(139,92,246,0.2)",
            borderwidth=1
        ),
        opacity=0.88,
        line=dict(color="rgba(255,255,255,0.5)", width=1)
    ),
    text=route_df["total_flights"],
    textposition="outside",
    textfont=dict(color="#4c1d95", size=11),
    hovertemplate="<b>%{y}</b><br>Flights: %{x}<extra></extra>"
))
fig4.update_layout(
    paper_bgcolor="rgba(0,0,0,0.0)",
    plot_bgcolor="rgba(0,0,0,0.0)",
    font=dict(color="#4c1d95", family="Inter"),
    height=420,
    margin=dict(t=20, b=20, l=160, r=80),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(139,92,246,0.10)",
        color="#7c3aed",
        linecolor="rgba(139,92,246,0.12)"
    ),
    yaxis=dict(
        gridcolor="rgba(139,92,246,0.10)",
        color="#3b0764",
        autorange="reversed"
    ),
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
    <div>
        <span class="pill">🏆 Delhi ↔ Mumbai = Busiest Route</span>
        <span class="pill">🏙️ Delhi = Aviation Hub</span>
        <span class="pill">💡 Darker = Costlier</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Live Flight Explorer ──
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🔍 Live Flight Explorer</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Use sidebar filters to explore flights live</p>', unsafe_allow_html=True)

query = """
    SELECT a.airline_name AS "Airline", c.class_name AS "Class",
           s.city_name AS "From", d.city_name AS "To",
           f.stop AS "Stops", f.duration_minutes AS "Duration (min)",
           t.time_label AS "Departure", f.price AS "Price ₹"
    FROM fact_flights f
    JOIN dim_airline a ON f.airline_id = a.airline_id
    JOIN dim_class c ON f.class_id = c.class_id
    JOIN dim_city s ON f.source_city_id = s.city_id
    JOIN dim_city d ON f.destination_city_id = d.city_id
    JOIN dim_time t ON f.time_id = t.time_id
    WHERE 1=1
"""
if selected_airline != "All":
    query += f" AND a.airline_name = '{selected_airline}'"
if selected_class != "All":
    query += f" AND c.class_name = '{selected_class}'"
if selected_city != "All":
    query += f" AND s.city_name = '{selected_city}'"
query += " ORDER BY f.price ASC LIMIT 100"

filtered_df = get_data(query)
st.markdown(f"<p style='color:#7c3aed;font-size:0.78rem;font-weight:500;'>Showing {len(filtered_df)} results</p>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align:center;color:#c4b5fd;font-size:0.7rem;letter-spacing:2.5px;font-weight:500;'>
        ✈️ FLIGHT PRICE ANALYTICS &nbsp;•&nbsp; PYSPARK + POSTGRESQL + STAR SCHEMA + STREAMLIT &nbsp;•&nbsp; YASHIKA JINDAL
    </p>
""", unsafe_allow_html=True)