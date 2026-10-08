import pandas as pd
import plotly.express as px
import streamlit as st

from reels_analyst.analytics.service import kpis, performance_by, top_reels
from reels_analyst.core.config import DATABASE_PATH

st.set_page_config(page_title="Reels Analyst", page_icon="📈", layout="wide")
st.title("📈 Reels Analyst")
st.caption("A lightweight performance cockpit for Instagram Reels exports")

if not DATABASE_PATH.exists():
    st.info(
        "No warehouse yet. Run `make demo` or ingest your export, "
        "then run `reels-analyst transform`."
    )
    st.stop()

try:
    summary = kpis()
except Exception:
    st.info("No analytical views yet. Run `reels-analyst transform` after ingestion.")
    st.stop()

metrics = [
    ("Reels", summary["reels"], ""),
    ("Reach", f"{summary['reach']:,}", ""),
    ("Engagement rate", f"{summary['engagement_rate']:.1%}", "of reach"),
    (
        "New follows",
        f"{summary['follows']:,}",
        f"{summary['follow_conversion_rate']:.2%} conversion",
    ),
]
for column, (label, value, delta) in zip(st.columns(4), metrics):
    column.metric(label, value, delta)

st.subheader("What is working")
breakdown = st.selectbox(
    "Compare performance by", ["topic", "publish_hour", "duration_bucket", "published_week"]
)
performance = pd.DataFrame(performance_by(breakdown))
if not performance.empty:
    chart = px.bar(
        performance.sort_values("engagement_rate"),
        x="dimension",
        y="engagement_rate",
        color="follow_conversion_rate",
        color_continuous_scale="Tealgrn",
        hover_data=["reels", "reach"],
        labels={"dimension": breakdown, "engagement_rate": "Engagement rate"},
    )
    chart.update_yaxes(tickformat=".1%")
    st.plotly_chart(chart, use_container_width=True)

st.subheader("Top Reels by engagement rate")
leaders = pd.DataFrame(top_reels(10))
if not leaders.empty:
    st.dataframe(
        leaders[
            [
                "published_date",
                "topic",
                "duration_seconds",
                "reach",
                "plays",
                "engagement_rate",
                "follow_conversion_rate",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "engagement_rate": st.column_config.NumberColumn("Engagement rate", format="%.1%%"),
            "follow_conversion_rate": st.column_config.NumberColumn(
                "Follow conversion", format="%.2%%"
            ),
        },
    )
