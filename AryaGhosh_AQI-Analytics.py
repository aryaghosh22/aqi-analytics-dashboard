import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings

warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AQI Analytics Dashboard",
    page_icon="🌿",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        html, body, [class*="css"] { font-family: "Segoe UI", system-ui, sans-serif; }

        .dash-header {
            background: linear-gradient(135deg, #1a3c5e 0%, #2d6a9f 100%);
            border-radius: 12px;
            padding: 28px 36px;
            margin-bottom: 28px;
            color: #ffffff;
        }
        .dash-header h1 { margin: 0 0 4px 0; font-size: 2rem; font-weight: 700; }
        .dash-header p  { margin: 0; font-size: 0.95rem; opacity: 0.80; }

        .metric-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px 22px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
        .metric-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: .06em;
            color: #57606a;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 1.55rem;
            font-weight: 700;
            color: #1a3c5e;
            word-break: break-word;
        }
        .metric-sub {
            font-size: 0.82rem;
            color: #57606a;
            margin-top: 4px;
        }

        .section-heading {
            font-size: 2.05rem;
            font-weight: 600;
            color: var(--text-color);
            border-left: 4px solid #2d6a9f;
            padding-left: 10px;
            margin: 32px 0 16px 0;
        }

        .dash-footer {
            text-align: center;
            font-size: 0.78rem;
            color: var(--text-color);
            margin-top: 48px;
            padding-top: 16px;
            border-top: 1px solid #e5e7eb;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load & Clean Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "AQI data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Normalise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Coerce numeric columns
    numeric_cols = ["pollutant_min", "pollutant_max", "pollutant_avg"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Drop rows where ALL numeric pollutant columns are NaN
    df.dropna(subset=numeric_cols, how="all", inplace=True)

    # Fill remaining NaN numerics with column median
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Strip whitespace from string columns
    for col in ["country", "state", "city", "station", "pollutant_id"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️  **AQI data.csv** not found. Place the file in the same directory as app.py and refresh.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dash-header">
        <h1>🌿 AQI Analytics Dashboard</h1>
        <p>Real-time snapshot of pollutant levels across Indian states &amp; cities</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")
    all_states = sorted(df["state"].unique())
    selected_states = st.multiselect("Filter by State", all_states, default=all_states)

    all_pollutants = sorted(df["pollutant_id"].unique())
    selected_pollutants = st.multiselect("Filter by Pollutant", all_pollutants, default=all_pollutants)

    st.markdown("---")
    st.markdown(f"**Total records:** {len(df):,}")
    st.markdown(f"**States covered:** {df['state'].nunique()}")
    st.markdown(f"**Cities covered:** {df['city'].nunique()}")

# Apply filters
mask = df["state"].isin(selected_states) & df["pollutant_id"].isin(selected_pollutants)
fdf = df[mask]

if fdf.empty:
    st.warning("No data matches the selected filters. Please broaden your selection.")
    st.stop()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Key Performance Indicators</div>', unsafe_allow_html=True)

most_polluted_state     = fdf.groupby("state")["pollutant_avg"].mean().idxmax()
most_polluted_state_val = fdf.groupby("state")["pollutant_avg"].mean().max()

max_spike_row  = fdf.loc[fdf["pollutant_max"].idxmax()]
max_spike_city = max_spike_row["city"]
max_spike_val  = max_spike_row["pollutant_max"]

top_pollutant     = fdf.groupby("pollutant_id")["pollutant_avg"].mean().idxmax()
top_pollutant_avg = fdf.groupby("pollutant_id")["pollutant_avg"].mean().max()

overall_avg = fdf["pollutant_avg"].mean()

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "Most Polluted State",      most_polluted_state,          f"Avg: {most_polluted_state_val:.1f} µg/m³"),
    (c2, "Highest Pollutant Spike",  max_spike_city,               f"Max: {max_spike_val:.1f} µg/m³"),
    (c3, "Most Prominent Pollutant", top_pollutant,                f"Avg: {top_pollutant_avg:.1f} µg/m³"),
    (c4, "Overall Avg Pollutant",    f"{overall_avg:.2f} µg/m³",  "All selected stations"),
]
for col, label, value, sub in cards:
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Visual Analytics</div>', unsafe_allow_html=True)

ch1, ch2 = st.columns(2)

PALETTE_5  = ["#1a3c5e", "#2d6a9f", "#4a90c4", "#7bb3d8", "#b0d0e8"]

# ── Chart 1: Top 5 most polluted states (horizontal bar) ─────────────────────
with ch1:
    st.markdown("**Top 5 Most Polluted States** *(avg pollutant level)*")

    top5_states = (
        fdf.groupby("state")["pollutant_avg"]
        .mean()
        .nlargest(5)
        .sort_values()
    )

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    bars = ax1.barh(
        top5_states.index, top5_states.values,
        color=PALETTE_5, edgecolor="none", height=0.55,
    )
    ax1.bar_label(bars, fmt="%.1f", padding=4, fontsize=9, color="#1f2328")
    ax1.set_xlabel("Average Pollutant Level (µg/m³)", fontsize=9, color="#57606a")
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax1.tick_params(axis="both", labelsize=9, colors="#1f2328")
    ax1.spines[["top", "right", "bottom"]].set_visible(False)
    ax1.spines["left"].set_color("#e5e7eb")
    ax1.set_facecolor("#ffffff")
    fig1.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

# ── Chart 2: Average concentration by pollutant type (vertical bar) ──────────
with ch2:
    st.markdown("**Average Concentration by Pollutant** *(µg/m³)*")

    pollutant_avg = (
        fdf.groupby("pollutant_id")["pollutant_avg"]
        .mean()
        .sort_values(ascending=False)
    )

    # Build a colour list — darkest bar for the highest pollutant
    n = len(pollutant_avg)
    bar_colors = [
        PALETTE_5[min(i, len(PALETTE_5) - 1)] for i in range(n)
    ]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    bars2 = ax2.bar(
        pollutant_avg.index, pollutant_avg.values,
        color=bar_colors, edgecolor="none", width=0.55,
    )
    ax2.bar_label(bars2, fmt="%.1f", padding=3, fontsize=8, color="#1f2328")
    ax2.set_ylabel("Avg Concentration (µg/m³)", fontsize=9, color="#57606a")
    ax2.set_xlabel("Pollutant", fontsize=9, color="#57606a")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax2.tick_params(axis="both", labelsize=9, colors="#1f2328")
    ax2.tick_params(axis="x", rotation=30)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.spines["bottom"].set_color("#e5e7eb")
    ax2.set_facecolor("#ffffff")
    fig2.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# ── Severe Pollution Risks Table ──────────────────────────────────────────────
SPIKE_THRESHOLD = 400

st.markdown('<div class="section-heading">⚠️ Severe Pollution Risks</div>', unsafe_allow_html=True)

hotspots = (
    fdf[fdf["pollutant_max"] >= SPIKE_THRESHOLD]
    [["state", "city", "station", "pollutant_id", "pollutant_min", "pollutant_max", "pollutant_avg"]]
    .sort_values("pollutant_max", ascending=False)
    .reset_index(drop=True)
)

if hotspots.empty:
    st.info("No stations currently exceed the 400 µg/m³ threshold in the selected filters.")
else:
    st.caption(
        f"Showing **{len(hotspots):,}** station-reading(s) where `pollutant_max` ≥ {SPIKE_THRESHOLD} µg/m³ — "
        "these locations require immediate attention."
    )
    st.dataframe(
        hotspots.style.format({
            "pollutant_min": "{:.1f}",
            "pollutant_max": "{:.1f}",
            "pollutant_avg": "{:.1f}",
        }),
        use_container_width=True,
    )

# ── Actionable Insights ───────────────────────────────────────────────────────
st.markdown('<div class="section-heading">📋 Actionable Insights</div>', unsafe_allow_html=True)

# Dynamically identify the top 2 pollutants by average concentration
top2_pollutants = (
    fdf.groupby("pollutant_id")["pollutant_avg"]
    .mean()
    .nlargest(2)
    .index
    .tolist()
)
top2_str = " and ".join(top2_pollutants)

spike_city_count = hotspots["city"].nunique() if not hotspots.empty else 0

if not hotspots.empty:
    st.error(
        f"🚨 **Action Required:** {spike_city_count} city/cities are recording `pollutant_max` values above "
        f"{SPIKE_THRESHOLD} µg/m³. Implement emergency smog-reduction protocols in affected areas immediately. "
        f"National emissions-reduction policies should prioritise **{top2_str}** sources, which currently show "
        f"the highest average concentrations across all monitoring stations."
    )
else:
    st.warning(
        f"⚠️ **Advisory:** No stations currently exceed {SPIKE_THRESHOLD} µg/m³ under the active filters. "
        f"Continue monitoring **{top2_str}** levels closely — these pollutants carry the highest average "
        f"concentrations and pose the greatest long-term health risk."
    )

# ── Raw Data Preview ──────────────────────────────────────────────────────────
with st.expander("📋 Raw Data Preview (first 100 rows)"):
    st.dataframe(fdf.head(100), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="dash-footer">India AQI Dashboard · Built with Streamlit &amp; Pandas</div>',
    unsafe_allow_html=True,
)
