import streamlit as st
import pandas as pd
from src.data.fetcher import fetch_northbound_flow
from src.ui.components import render_metric_card
from src.utils.helpers import format_money
from lightweight_charts_v5 import lightweight_charts_v5_component


def render_market_overview():
    """
    Render the Market Overview page (Northbound Fund Flow).
    """
    st.markdown("### 市场概览: 北向资金 (Northbound Flow)")

    with st.spinner("获取北向资金数据中..."):
        df = fetch_northbound_flow("北向资金")

    if df.empty:
        st.error("无法获取北向资金数据。")
        return

    df = df.loc[:, ~df.columns.duplicated()]

    # Data Processing
    # Ensure date is string YYYY-MM-DD
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"], errors="coerce").dt.strftime("%Y-%m-%d")
        df = df.dropna(subset=["日期"])

    # Latest Data
    last_row = df.iloc[-1]
    net_inflow = (
        float(last_row["当日成交净买额"])
        if pd.notna(last_row["当日成交净买额"])
        else 0.0
    )
    cum_inflow = (
        float(last_row["历史累计净买额"])
        if pd.notna(last_row["历史累计净买额"])
        else 0.0
    )

    # Leader Stock
    leader_name = last_row.get("领涨股", "-")
    leader_change = last_row.get("领涨股-涨跌幅", 0.0)

    # 1. Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card(
            "当日净流入 (Daily Net)", format_money(net_inflow), None, color_inverse=True
        )
    with col2:
        render_metric_card(
            "累计净流入 (Cumulative)",
            format_money(cum_inflow),
            None,
            color_inverse=True,
        )
    with col3:
        leader_color = "#ef5350" if leader_change > 0 else "#26a69a"
        st.markdown(
            f"""<div style="
                background: linear-gradient(135deg, #141b2d 0%, #0f172a 100%); 
                padding: 15px; 
                border-radius: 12px; 
                border: 1px solid #1e293b;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);">
<div style="color: #94a3b8; font-size: 0.9rem;">领涨股 (Leader)</div>
<div style="font-size: 1.4rem; font-weight: 700; color: #f8fafc;">{leader_name}</div>
<div style="color: {leader_color}; font-weight: bold;">{leader_change:+.2f}%</div>
</div>""",
            unsafe_allow_html=True,
        )

    # 2. Chart (Net Inflow History)
    st.markdown("#### 资金流向趋势 (Fund Flow Trend)")

    # Prepare data for lightweight charts histogram
    hist_data = []
    for _, row in df.tail(100).iterrows():  # Show last 100 days
        val = float(row["当日成交净买额"]) if pd.notna(row["当日成交净买额"]) else 0.0
        color = "#ef5350" if val > 0 else "#26a69a"
        hist_data.append({"time": str(row["日期"]), "value": val, "color": color})

    chart_options = {
        "layout": {
            "background": {"type": "solid", "color": "#0a0e27"},
            "textColor": "#f8fafc",
        },
        "grid": {
            "vertLines": {"color": "#1e293b"},
            "horzLines": {"color": "#1e293b"},
        },
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.1,
                "bottom": 0.1,
            }
        },
    }

    series = [
        {
            "type": "Histogram",
            "data": hist_data,
            "options": {
                "priceFormat": {"type": "volume"},
            },
        }
    ]

    charts_config = [{"chart": chart_options, "series": series}]

    lightweight_charts_v5_component(
        name="market_chart", charts=charts_config, height=400
    )

    st.dataframe(df.tail(10))
