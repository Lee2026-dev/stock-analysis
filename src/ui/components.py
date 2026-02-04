import streamlit as st
import pandas as pd
from typing import Optional
from lightweight_charts_v5 import lightweight_charts_v5_component


def render_metric_card(
    label: str, value: str, delta: Optional[str] = None, color_inverse: bool = True
):
    """
    Render a SaaS-style metric card.

    Args:
        label: Metric name
        value: Main value (string)
        delta: Change value (string, e.g. "+1.2%")
        color_inverse: If True, Red = Positive (China Standard).
    """
    delta_html = ""
    if delta:
        # Determine color
        is_positive = delta.startswith("+")
        if color_inverse:
            color = "#ef5350" if is_positive else "#26a69a"
        else:
            color = "#26a69a" if is_positive else "#ef5350"

        delta_html = f'<span style="color:{color}; font-weight:bold; margin-left:8px; font-size: 0.9rem;">{delta}</span>'

    st.markdown(
        f"""<div data-testid="stMetric" style="
            background: linear-gradient(135deg, #141b2d 0%, #0f172a 100%); 
            padding: 15px; 
            border-radius: 12px; 
            border: 1px solid #1e293b; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); 
            margin-bottom: 10px;">
<div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 4px;">{label}</div>
<div style="display: flex; align-items: baseline;">
<span style="font-size: 1.6rem; font-weight: 700; color: #f8fafc;">{value}</span>
{delta_html}
</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_chart(df: pd.DataFrame, height: int = 500):
    """
    Render a TradingView-style candlestick chart with Volume.

    Args:
        df: DataFrame with '日期', '开盘', '最高', '最低', '收盘', '成交量'
        height: Chart height in px
    """
    if df.empty:
        st.warning("暂无数据 (No Data)")
        return

    # Prepare Data
    # Ensure '日期' is string YYYY-MM-DD
    # If '日期' is index, reset it.
    chart_df = df.copy()
    if "日期" not in chart_df.columns and isinstance(chart_df.index, pd.DatetimeIndex):
        chart_df = chart_df.reset_index()
        chart_df["日期"] = chart_df["日期"].dt.strftime("%Y-%m-%d")
    elif "日期" in chart_df.columns:
        if pd.api.types.is_datetime64_any_dtype(chart_df["日期"]):
            chart_df["日期"] = chart_df["日期"].dt.strftime("%Y-%m-%d")
        else:
            chart_df["日期"] = pd.to_datetime(
                chart_df["日期"], errors="coerce"
            ).dt.strftime("%Y-%m-%d")

    chart_df = chart_df.drop_duplicates(subset=["日期"]).sort_values("日期")

    chart_df = chart_df.dropna(subset=["日期"])

    ohlc_data = []
    volume_data = []

    required_cols = ["日期", "开盘", "最高", "最低", "收盘", "成交量"]
    if not all(col in chart_df.columns for col in required_cols):
        st.error(f"Missing columns for chart. Available: {chart_df.columns.tolist()}")
        return

    for _, row in chart_df.iterrows():
        time_str = str(row["日期"])
        open_p = float(row["开盘"])
        close_p = float(row["收盘"])

        # Color for volume: Red if up, Green if down
        vol_color = "#ef5350" if close_p >= open_p else "#26a69a"

        ohlc_data.append(
            {
                "time": time_str,
                "open": open_p,
                "high": float(row["最高"]),
                "low": float(row["最低"]),
                "close": close_p,
            }
        )

        volume_data.append(
            {"time": time_str, "value": float(row["成交量"]), "color": vol_color}
        )

    # Chart Configuration
    chart_options = {
        "layout": {
            "background": {"type": "solid", "color": "#0a0e27"},
            "textColor": "#f8fafc",
        },
        "grid": {
            "vertLines": {"color": "#1e293b"},
            "horzLines": {"color": "#1e293b"},
        },
        "crosshair": {"mode": 0},
        "timeScale": {"borderColor": "#334155"},
        "rightPriceScale": {
            "mode": 0,
            "scaleMargins": {"top": 0.1, "bottom": 0.3},
        },
    }

    candlestick_series = {
        "type": "Candlestick",
        "data": ohlc_data,
        "options": {
            "upColor": "#ef5350",
            "downColor": "#26a69a",
            "borderVisible": False,
            "wickUpColor": "#ef5350",
            "wickDownColor": "#26a69a",
            "priceScaleId": "right",
        },
    }

    volume_series = {
        "type": "Histogram",
        "data": volume_data,
        "options": {
            "color": "#26a69a",
            "priceFormat": {"type": "volume"},
            "priceScaleId": "volume",
            "scaleMargins": {
                "top": 0.8,
                "bottom": 0,
            },
        },
    }

    charts_config = [
        {
            "chart": chart_options,
            "series": [candlestick_series, volume_series],
            "height": height,
        }
    ]

    lightweight_charts_v5_component(
        name="main_chart", charts=charts_config, height=height
    )
